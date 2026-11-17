"""Shape A — deterministic workflow.

Code owns business rules, compensation calculation, policy filtering, and
idempotent host ledger commits. MockLLM is used strictly to draft a short
non-authoritative reply string after the deterministic decision is known.
"""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import compute_compensation, get_claim_view, lookup_order, tool_cost
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    """Execute a claim deterministically while upholding Trace Contract v1."""
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _draft_reply(
    budget: Budget,
    *,
    seed: int,
    status: str,
    claim_id: str,
    proposal_amount: int = 0,
) -> str:
    """Ask MockLLM only to draft non-authoritative response text."""
    return complete(
        budget,
        seed=seed,
        purpose="draft",
        prompt=f"status={status};claim_id={claim_id};proposal={proposal_amount}",
    )


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    run_id = make_run_id("workflow", claim_id, seed)
    trace = Trace(run_id)

    budget.add_tool(tool_cost())
    claim_view = get_claim_view(conn, claim_id)
    trace.add(
        "claim_view",
        {
            "found": bool(claim_view.get("found")),
            "claim_id": claim_id,
            "has_order_id": bool(claim_view.get("order_id")),
        },
    )

    if not claim_view.get("found"):
        trace.add("decision", {"status": "failed", "reason": "unknown_claim"})
        return finish(
            conn,
            shape="workflow",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="unknown_claim",
        )

    order_id = claim_view.get("order_id")
    if not order_id:
        _draft_reply(budget, seed=seed, status="needs_info", claim_id=claim_id)
        trace.add("decision", {"status": "needs_info", "reason": "missing_order_id"})
        return finish(
            conn,
            shape="workflow",
            claim_id=claim_id,
            seed=seed,
            status="needs_info",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="missing_order_id",
        )

    budget.add_tool(tool_cost())
    order_view = lookup_order(conn, order_id, claim_view["principal_id"])
    trace.add("lookup_order", safe_dump(order_view))
    if not order_view.get("visible"):
        reason = order_view.get("reason")
        _draft_reply(budget, seed=seed, status="escalated", claim_id=claim_id)
        trace.add("decision", {"status": "escalated", "reason": reason})
        return finish(
            conn,
            shape="workflow",
            claim_id=claim_id,
            seed=seed,
            status="escalated",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    # Quote strictly from structured order fields and active policy; ignore ticket prose.
    order = dict(order_view["order"])
    budget.add_tool(tool_cost())
    quote_payload = compute_compensation(conn, order)
    proposal = int(quote_payload["amount_vnd"])
    trace.add("quote", safe_dump(quote_payload))

    if proposal <= 0:
        reason = quote_payload.get("reason")
        _draft_reply(budget, seed=seed, status="denied", claim_id=claim_id)
        trace.add("decision", {"status": "denied", "proposal_amount": 0, "reason": reason})
        return finish(
            conn,
            shape="workflow",
            claim_id=claim_id,
            seed=seed,
            status="denied",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    # Pass FULL quote; host checks approval binding and subtracts prior refunds on the order.
    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    if not outcome["ok"]:
        status = "failed" if outcome.get("conflict") else "denied"
        _draft_reply(
            budget,
            seed=seed,
            status=status,
            claim_id=claim_id,
            proposal_amount=proposal,
        )
        trace.add(
            "issue_refund",
            {
                "ok": False,
                "status": status,
                "reason": outcome.get("reason"),
                "proposal_amount": proposal,
            },
        )
        return finish(
            conn,
            shape="workflow",
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=outcome.get("reason"),
        )

    _draft_reply(
        budget,
        seed=seed,
        status="resolved",
        claim_id=claim_id,
        proposal_amount=proposal,
    )
    effect = outcome.get("effect") or {}
    trace.add(
        "issue_refund",
        {
            "ok": True,
            "status": "resolved",
            "reason": outcome.get("reason"),
            "proposal_amount": proposal,
            "committed_amount_vnd": effect.get("amount_vnd"),
        },
    )
    return finish(
        conn,
        shape="workflow",
        claim_id=claim_id,
        seed=seed,
        status="resolved",
        proposal_amount=proposal,
        budget=budget,
        trace=trace,
        error_reason=None,
    )
