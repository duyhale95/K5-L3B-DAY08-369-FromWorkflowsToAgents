"""Shape B — one ReAct agent.

A single agent drives a bounded `lab8.runtime.run_react` loop (max 8 steps).
Each `decide` turn costs one MockLLM call and picks at most one read tool.
The agent never writes: after the loop the host re-derives the quote from the
order row it observed and is the only caller of `durability.issue_refund`.

Ticket prose is never used as evidence. Delay, damage and fee come from the
order row; the clause comes from the current policy. A customer who overstates
the delay, cites a superseded clause, or injects instructions changes nothing.

Per-order cap: `lookup_refund_history` is read for the trace, but the host
enforces the cap, so the FULL quote is passed to `issue_refund`.

Trace contract v1: every return path goes through `finish()`; a crash flushes
the trace before `InjectedCrash` propagates.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.handoff import READONLY_TOOLS
from lab8.mock_llm import complete
from lab8.runtime import Decide, ToolRejected, run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import compute_compensation, tool_cost
from lab8.trace import Trace

SHAPE = "single"
MAX_STEPS = 8


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def make_decide(
    claim_id: str,
    *,
    seed: int,
    budget: Budget,
    trace: Trace,
    memory: dict[str, Any],
) -> Decide:
    """Build the agent policy for one claim.

    `memory` is the agent scratchpad. It keeps only allowlisted facts: ids, the
    order row returned by `lookup_order`, policy ids, refund history and the
    quote. The ticket text is never stored, traced, or put in a prompt.
    """

    def think(step: str) -> None:
        # One model call per turn so cost stays comparable across shapes.
        complete(budget, seed=seed, purpose="react", prompt=f"claim_id={claim_id};step={step}")

    def call(tool: str, args: dict[str, Any]) -> dict[str, Any]:
        trace.add("react_step", {"action": "tool", "tool": tool})
        return {"tool": tool, "args": args}

    def final(status: str, *, reason: str | None = None, proposal: int = 0) -> dict[str, Any]:
        trace.add("react_step", {"action": "final", "status": status, "reason": reason})
        return {"final": {"status": status, "error_reason": reason, "proposal_amount": proposal}}

    def decide(seen: dict[str, Any]) -> dict[str, Any]:
        last_tool = seen.get("last_tool")
        result = seen.get("last_result") or {}
        think(last_tool or "start")

        if last_tool is None:
            return call("get_claim_view", {"claim_id": claim_id})

        if last_tool == "get_claim_view":
            trace.add(
                "claim_view",
                {
                    "found": bool(result.get("found")),
                    "claim_id": claim_id,
                    "has_order_id": bool(result.get("order_id")),
                },
            )
            if not result.get("found"):
                return final("failed", reason="unknown_claim")
            if not result.get("order_id"):
                # Do not guess an order id out of the ticket text.
                return final("needs_info", reason="missing_order_id")
            memory["order_id"] = result["order_id"]
            memory["principal_id"] = result["principal_id"]
            return call(
                "lookup_order",
                {"order_id": memory["order_id"], "principal_id": memory["principal_id"]},
            )

        if last_tool == "lookup_order":
            trace.add("lookup_order", safe_dump(result))
            if not result.get("visible"):
                return final("escalated", reason=result.get("reason"))
            memory["order"] = dict(result["order"])
            return call("lookup_policy", {})

        if last_tool == "lookup_policy":
            memory["policy_ids"] = [p["policy_id"] for p in result.get("policies") or []]
            trace.add("lookup_policy", {"as_of": result.get("as_of"), "policy_ids": memory["policy_ids"]})
            return call(
                "lookup_refund_history",
                {"order_id": memory["order_id"], "principal_id": memory["principal_id"]},
            )

        if last_tool == "lookup_refund_history":
            memory["refund_history"] = safe_dump(result)
            trace.add("lookup_refund_history", memory["refund_history"])
            # Quote from the order ROW, never from numbers the ticket claims.
            return call("compute_compensation", {"order": dict(memory["order"])})

        if last_tool == "compute_compensation":
            memory["quote"] = safe_dump(result)
            trace.add("quote", memory["quote"])
            amount = int(result["amount_vnd"])
            if amount <= 0:
                return final("denied", reason=result.get("reason"))
            return final("propose_refund", proposal=amount)

        return final("failed", reason="unexpected_observation")

    return decide


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))
    memory: dict[str, Any] = {}

    def done(status: str, proposal: int, reason: str | None) -> RunResult:
        return finish(
            conn,
            shape=SHAPE,
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    decide = make_decide(claim_id, seed=seed, budget=budget, trace=trace, memory=memory)
    try:
        loop = run_react(
            conn,
            budget,
            observation={"claim": {"claim_id": claim_id}},
            decide=_readonly(decide),
            max_steps=MAX_STEPS,
        )
    except ToolRejected as exc:
        trace.add("decision", {"status": "failed", "reason": "tool_rejected", "detail": str(exc)})
        return done("failed", 0, "tool_rejected")

    verdict = loop["final"]
    trace.add("react_stop", {"stopped": loop["stopped"], "max_steps": MAX_STEPS})
    status = verdict.get("status")
    reason = verdict.get("error_reason")

    if status != "propose_refund":
        if status not in ("needs_info", "escalated", "denied", "failed"):
            status, reason = "failed", "invalid_agent_verdict"
        trace.add("decision", {"status": status, "reason": reason})
        return done(status, 0, reason)

    # Host validation: recompute from the order row the tool returned. The
    # agent's number is only a proposal and must match the host's own quote.
    budget.add_tool(tool_cost())
    host_quote = compute_compensation(conn, dict(memory["order"]))
    proposal = int(host_quote["amount_vnd"])
    trace.add("host_validation", {"agent_proposal": verdict.get("proposal_amount"), "host_quote": proposal})
    if proposal <= 0 or proposal != int(verdict.get("proposal_amount") or 0):
        trace.add("decision", {"status": "failed", "reason": "quote_mismatch"})
        return done("failed", 0, "quote_mismatch")

    # Pass the FULL quote; the host checks approval and nets prior refunds on the order.
    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    effect = outcome.get("effect") or {}
    if outcome["ok"]:
        status = "resolved"
    else:
        status = "failed" if outcome.get("conflict") else "denied"
    trace.add(
        "issue_refund",
        {
            "ok": bool(outcome["ok"]),
            "status": status,
            "reason": outcome.get("reason"),
            "proposal_amount": proposal,
            "committed_amount_vnd": effect.get("amount_vnd"),
        },
    )
    return done(status, proposal, None if outcome["ok"] else outcome.get("reason"))


def _readonly(decide: Decide) -> Decide:
    """Guard in code: the agent may only name read tools, whatever it decides."""

    def guarded(seen: dict[str, Any]) -> dict[str, Any]:
        action = decide(seen)
        if "final" not in action and action.get("tool") not in READONLY_TOOLS:
            raise ToolRejected(f"single agent cannot call {action.get('tool')}")
        return action

    return guarded
