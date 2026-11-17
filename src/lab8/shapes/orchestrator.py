"""Shape C — orchestrator with a sanitized handoff to read-only investigators."""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.handoff import HandoffError, make_handoff
from lab8.runtime import ToolRejected, run_readonly_investigators
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import compute_compensation, get_claim_view, tool_cost
from lab8.trace import Trace

SHAPE = "orchestrator"


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


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))

    def done(status: str, reason: str | None = None, *, proposal: int = 0) -> RunResult:
        trace.add("decision", {"status": status, "reason": reason, "proposal_amount": proposal})
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

    budget.add_tool(tool_cost())
    claim = get_claim_view(conn, claim_id)
    if not claim["found"]:
        return done("failed", "unknown_claim")
    if not claim["order_id"]:
        return done("needs_info", "missing_order_id")

    try:
        handoff = make_handoff(
            request_id=trace.run_id,
            claim_id=claim_id,
            task="investigate_order_and_policy",
            # The investigators obtain operational facts through scoped read tools.
            facts={},
            allowed_tools=["lookup_order", "lookup_policy", "lookup_refund_history"],
        )
        trace.add("handoff", safe_dump(handoff))
        findings = run_readonly_investigators(conn, budget, handoff, principal_id=claim["principal_id"])
    except (HandoffError, ToolRejected):
        return done("failed", "investigation_rejected")

    tools = findings["tools"]
    order_view = tools["lookup_order"]
    trace.add("lookup_order", {"visible": order_view["visible"], "reason": order_view["reason"]})
    if not order_view["visible"]:
        return done("escalated", order_view["reason"])

    policy = tools["lookup_policy"]
    trace.add("lookup_policy", {"as_of": policy["as_of"], "policy_count": len(policy["policies"])})
    history = tools["lookup_refund_history"]
    trace.add(
        "lookup_refund_history",
        {
            "visible": history["visible"],
            "refund_count": history.get("refund_count"),
            "refunded_vnd": history.get("refunded_vnd"),
        },
    )

    budget.add_tool(tool_cost())
    quote = compute_compensation(conn, order_view["order"])
    proposal = quote["amount_vnd"]
    trace.add("quote", safe_dump(quote))
    if proposal <= 0:
        return done("denied", quote["reason"])

    # Flush before the host write so an injected crash can propagate with a fresh trace.
    # The host applies approval checks and nets previous refunds against the full quote.
    trace.add("refund_attempt", {"proposal_amount": proposal})
    trace.write()
    outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    trace.add(
        "issue_refund",
        {
            "ok": outcome["ok"],
            "reason": outcome["reason"],
            "committed_amount_vnd": (outcome["effect"] or {}).get("amount_vnd"),
        },
    )
    if outcome["ok"]:
        return done("resolved", proposal=proposal)
    status = "failed" if outcome["conflict"] else "denied"
    return done(status, outcome["reason"], proposal=proposal)
