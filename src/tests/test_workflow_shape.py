"""Unit and contract tests for Shape A (workflow) implemented by Hà Lê Duy."""

from __future__ import annotations

import time

import pytest

from lab8.db import connect, init_store
from lab8.durability import InjectedCrash, committed_audit_count, get_refund
from lab8.metrics import artifact_blob, check_trace, trial_pass
from lab8.shapes.workflow import run_claim
from tests.conftest import BY_ID, CLAIMS, WORLD


def _fresh_store(tmp_path, name: str):
    path = tmp_path / name
    init_store(path, WORLD, CLAIMS).close()
    return path


@pytest.mark.parametrize("seed", [11, 22, 33, 44, 55])
@pytest.mark.parametrize("claim_id", ["C-002", "C-006", "C-009"])
def test_workflow_ignores_ticket_lies_old_clauses_and_injection(tmp_path, seed, claim_id):
    store = _fresh_store(tmp_path, f"wf-{claim_id}-{seed}.sqlite")
    started = time.time()
    result = run_claim(claim_id, seed=seed, store_path=str(store))
    conn = connect(store)
    try:
        passed, reason = trial_pass(
            result.as_dict(),
            BY_ID[claim_id]["expected"],
            conn,
            started_at=started,
        )
    finally:
        conn.close()
    assert passed, reason
    assert result.status == "denied"
    assert result.proposal_amount == 0


def test_workflow_early_exits_and_resolved_traces_stay_clean(tmp_path):
    store = _fresh_store(tmp_path, "wf-clean.sqlite")
    for claim_id, expected_status in [
        ("C-UNKNOWN", "failed"),
        ("C-004", "needs_info"),
        ("C-005", "escalated"),
        ("C-010", "resolved"),
    ]:
        started = time.time()
        result = run_claim(claim_id, seed=11, store_path=str(store))
        payload = result.as_dict()
        ok, trace_reason = check_trace(payload, started_at=started)
        assert ok, f"{claim_id}: {trace_reason}"
        assert result.status == expected_status
        blob = artifact_blob(payload)
        for forbidden in (
            "CANARY_SECRET_",
            "CANARY_INTERNAL_",
            "0901111222",
            "0901000107",
            "99 Duong Bi Mat",
            "12 Le Loi Q1",
            "SECRET_ITEM_VANG",
        ):
            assert forbidden not in blob


def test_workflow_enforces_per_order_cap_and_approval_claim_binding(tmp_path):
    store_borrow = _fresh_store(tmp_path, "wf-borrow.sqlite")
    conn = connect(store_borrow)
    try:
        conn.execute(
            """
            INSERT INTO claims (claim_id, principal_id, order_id, ticket, parent_secret, raw_headers_json, approval_id)
            VALUES ('C-BORROW-WF', 'P-100', 'O-808', 'late 4 days', 'CANARY_SECRET_PARENT_BORROW', '{}', 'A-001')
            """
        )
        conn.commit()
    finally:
        conn.close()

    borrowed = run_claim("C-BORROW-WF", seed=11, store_path=str(store_borrow))
    assert borrowed.status == "denied"
    assert borrowed.proposal_amount == 35000
    assert borrowed.error_reason == "approval_claim_mismatch"

    conn = connect(store_borrow)
    try:
        assert get_refund(conn, "C-BORROW-WF") is None
        audits = conn.execute(
            "SELECT details_json FROM audit_events WHERE claim_id = 'C-BORROW-WF' AND event_type = 'policy_denied'"
        ).fetchall()
        assert any("approval_claim_mismatch" in row["details_json"] for row in audits)
    finally:
        conn.close()

    for claim_id in ("C-013", "C-014"):
        store = _fresh_store(tmp_path, f"wf-{claim_id}.sqlite")
        started = time.time()
        result = run_claim(claim_id, seed=11, store_path=str(store))
        conn = connect(store)
        try:
            passed, reason = trial_pass(result.as_dict(), BY_ID[claim_id]["expected"], conn, started_at=started)
        finally:
            conn.close()
        assert passed, f"{claim_id}: {reason}"


@pytest.mark.parametrize(
    "crash_at",
    ["before_effect", "after_effect_before_checkpoint", "after_checkpoint"],
)
def test_workflow_crash_points_propagate_and_resume_idempotently(tmp_path, crash_at):
    store = _fresh_store(tmp_path, f"wf-crash-{crash_at}.sqlite")
    with pytest.raises(InjectedCrash):
        run_claim("C-012", seed=11, store_path=str(store), crash_at=crash_at)

    started = time.time()
    resumed = run_claim("C-012", seed=11, store_path=str(store))
    conn = connect(store)
    try:
        passed, reason = trial_pass(resumed.as_dict(), BY_ID["C-012"]["expected"], conn, started_at=started)
        effect = get_refund(conn, "C-012")
        audits = committed_audit_count(conn, "C-012")
    finally:
        conn.close()
    assert passed, reason
    assert effect is not None and int(effect["amount_vnd"]) == 35000
    assert audits == 1


def test_workflow_amount_conflict_returns_failed_and_keeps_committed_amount(tmp_path):
    store = _fresh_store(tmp_path, "wf-conflict.sqlite")
    first = run_claim("C-001", seed=11, store_path=str(store))
    assert first.status == "resolved"

    conn = connect(store)
    try:
        conn.execute("UPDATE orders SET shipping_fee_vnd = 10000 WHERE order_id = 'O-107'")
        conn.commit()
    finally:
        conn.close()

    started = time.time()
    second = run_claim("C-001", seed=11, store_path=str(store))
    ok, trace_reason = check_trace(second.as_dict(), started_at=started)
    assert ok, trace_reason
    assert second.status == "failed"
    assert second.error_reason == "amount_conflict"
    assert second.proposal_amount == 10000

    conn = connect(store)
    try:
        effect = get_refund(conn, "C-001")
        assert effect is not None and int(effect["amount_vnd"]) == 35000
    finally:
        conn.close()

