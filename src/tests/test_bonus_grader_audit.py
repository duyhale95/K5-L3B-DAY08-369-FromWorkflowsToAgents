"""Bonus B7 — metamorphic audit of `grader_a`, `grader_b`, `grader_c`.

The audit logic lives in `src/bonus/grader_audit.py` so the same code produces
both the pytest verdicts and the generated evidence
`src/reports/bonus_grader_audit.json` (never hand-edited).

Relations under test:

1. `claim_delay_2_vs_3` (official fixture): delay 2 denies, delay 3 pays the
   shipping fee only, and the candidate summariser reports 1/2 graded passes.
2. `infra_errors_do_not_move_pass_rate` (official fixture): infrastructure
   failures must not enter the denominator as shape mistakes.
3. `duplicated_list_keeps_rates_doubles_totals` (official fixture): appending a
   copy of the trial list keeps rates and doubles counts and total cost.
4. `trial_order_does_not_move_metrics` (new relation): reversing the same
   multiset of trials must not move any aggregate.

Expected verdicts come from the audit itself: `grader_b` is the only candidate
that satisfies the official relations, `grader_a` double-counts cost, and
`grader_c` grades infra failures as policy mistakes. The new order relation also
catches a position-dependent mutant that survives all three official relations.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from bonus.grader_audit import GRADERS, RELATIONS, audit_all

EXPECTED = {
    "grader_a": {
        RELATIONS[0]: True,
        RELATIONS[1]: True,
        RELATIONS[2]: False,
        RELATIONS[3]: False,
    },
    "grader_b": {
        RELATIONS[0]: True,
        RELATIONS[1]: True,
        RELATIONS[2]: True,
        RELATIONS[3]: True,
    },
    "grader_c": {
        RELATIONS[0]: True,
        RELATIONS[1]: False,
        RELATIONS[2]: True,
        RELATIONS[3]: True,
    },
}


@pytest.fixture(scope="module")
def audit():
    return audit_all()


@pytest.mark.parametrize("name", GRADERS)
@pytest.mark.parametrize("relation_id", RELATIONS)
def test_relation_verdict_for_each_candidate(audit, name, relation_id):
    outcome = audit["graders"][name]["relations"][relation_id]
    assert outcome["passed"] is EXPECTED[name][relation_id], outcome["violations"]
    if not outcome["passed"]:
        assert outcome["violations"], "a failing relation must name the behavioural violation"


def test_exactly_one_candidate_survives_the_official_relations(audit):
    assert audit["correct_graders"] == ["grader_b"]


def test_grader_a_double_counts_cost(audit):
    duplicate = audit["graders"]["grader_a"]["relations"][RELATIONS[2]]
    joined = " | ".join(duplicate["violations"])
    assert "totals_not_doubled:total_simulated_cost_vnd" in joined
    assert "cost_per_success_vnd" in joined

    evidence = duplicate["evidence"]
    assert evidence["a"]["total_simulated_cost_vnd"] == pytest.approx(283.5)
    assert evidence["b"]["total_simulated_cost_vnd"] == pytest.approx(473.0)
    assert evidence["expected_total_simulated_cost_vnd"] == pytest.approx(567.0)
    assert evidence["a"]["cost_per_success_vnd"] == pytest.approx(31.5)
    assert evidence["b"]["cost_per_success_vnd"] == pytest.approx(26.27777777777778)


def test_grader_a_cost_totals_depend_on_first_seen_claim_row(audit):
    order = audit["graders"]["grader_a"]["relations"][RELATIONS[3]]
    joined = " | ".join(order["violations"])
    assert "metric_changed:total_simulated_cost_vnd" in joined
    assert "metric_changed:cost_per_success_vnd" in joined
    evidence = order["evidence"]
    assert evidence["a"]["total_simulated_cost_vnd"] == pytest.approx(283.5)
    assert evidence["reversed"]["total_simulated_cost_vnd"] == pytest.approx(285.0)


def test_grader_c_counts_infra_failures_as_shape_failures(audit):
    infra = audit["graders"]["grader_c"]["relations"][RELATIONS[1]]
    joined = " | ".join(infra["violations"])
    assert "graded_trials:12!=16" in joined
    assert "pass_rate" in joined
    evidence = infra["evidence"]
    assert evidence["infra_trials_added"] == 4
    assert evidence["a"]["graded_trials"] == 12
    assert evidence["b"]["graded_trials"] == 16
    assert evidence["a"]["pass_rate"] == pytest.approx(0.75)
    assert evidence["b"]["pass_rate"] == pytest.approx(0.5625)


def test_duplicate_fixture_exposes_inherited_pass5_limitation(audit):
    """All candidates inherit the same reference-ruler limit; blame not assigned."""
    for name in GRADERS:
        evidence = audit["graders"][name]["relations"][RELATIONS[2]]["evidence"]
        assert evidence["pass_5"]["a"] == pytest.approx(2 / 3)
        assert evidence["pass_5"]["b"] == pytest.approx(0.0)
        assert "metrics.summarize" in evidence["pass_5_inherited_limitation"]


def test_new_order_relation_catches_mutant_missed_by_official_three(audit):
    mutant = audit["mutant_control"]["relations"]
    for relation_id in RELATIONS[:3]:
        assert mutant[relation_id]["passed"] is True, mutant[relation_id]["violations"]

    order = mutant[RELATIONS[3]]
    assert order["passed"] is False
    assert any("total_simulated_cost_vnd" in item for item in order["violations"])
    assert order["evidence"]["a"]["total_simulated_cost_vnd"] == pytest.approx(283.5)
    assert order["evidence"]["reversed"]["total_simulated_cost_vnd"] == pytest.approx(285.0)


def test_committed_evidence_is_reproducible(audit):
    """The committed JSON must equal a fresh audit run (picoseconds untouched)."""
    path = Path(__file__).resolve().parents[1] / "reports" / "bonus_grader_audit.json"
    if not path.is_file():
        pytest.skip("reports/bonus_grader_audit.json not generated yet")
    committed = json.loads(path.read_text(encoding="utf-8"))
    assert committed == json.loads(json.dumps(audit, ensure_ascii=False))
