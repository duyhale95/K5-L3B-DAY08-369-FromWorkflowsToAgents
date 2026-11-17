"""Verify the public benchmark's trial grid, metrics, and trace artifacts."""

import json
from itertools import product
from pathlib import Path
from statistics import mean, pvariance

import pytest

from lab8.benchmark import run_benchmark
from lab8.shapes import SHAPES as REGISTERED_SHAPES
from bonus.swarm_order_only import run_claim as run_order_only
from tests.conftest import BY_ID, CLAIMS, WORLD

SHAPES = ("workflow", "single", "orchestrator", "swarm")
SEEDS = (11, 22, 33, 44, 55)


@pytest.fixture(scope="module")
def public_benchmark(tmp_path_factory):
    with pytest.MonkeyPatch.context() as patch:
        patch.chdir(tmp_path_factory.mktemp("public-benchmark"))
        report = run_benchmark(world=WORLD, claims=CLAIMS, shapes=list(SHAPES), seeds=list(SEEDS))
        return report, Path.cwd() / "traces"


@pytest.mark.parametrize("shape", SHAPES)
def test_benchmark_metrics_match_trial_grid(public_benchmark, shape):
    report, _ = public_benchmark
    rows = [row for row in report["trials"] if row["shape"] == shape]
    by_case = {(row["claim_id"], row["seed"]): row for row in rows}
    assert set(by_case) == set(product(BY_ID, SEEDS))
    assert len(rows) == len(by_case)
    assert all(isinstance(row["passed"], bool) for row in rows)
    misses = {case for case, row in by_case.items() if not row["passed"]}
    assert misses == ({("C-002", 55)} if shape == "swarm" else set())

    passed = sum(row["passed"] for row in rows)
    all_seeds_passed = sum(all(by_case[cid, seed]["passed"] for seed in SEEDS) for cid in BY_ID)
    seed_rates = [mean(by_case[cid, seed]["passed"] for cid in BY_ID) for seed in SEEDS]
    stats = report["by_shape"][shape]
    assert stats["pass_rate"] == pytest.approx(passed / len(rows))
    assert stats["pass_5"] == pytest.approx(all_seeds_passed / len(BY_ID))
    assert stats["seed_variance"] == pytest.approx(pvariance(seed_rates))
    assert stats["cost_per_success_vnd"] == pytest.approx(
        sum(row["cost_estimate"] for row in rows) / passed
    )


@pytest.mark.parametrize("shape", SHAPES)
def test_benchmark_uses_clean_trace_events(public_benchmark, shape):
    report, trace_dir = public_benchmark
    for row in report["trials"]:
        if row["shape"] != shape:
            continue
        run_id = f"R-{shape}-{row['claim_id']}-s{row['seed']}"
        assert row["run_id"] == run_id
        trace = json.loads((trace_dir / f"{run_id}.json").read_text(encoding="utf-8"))
        assert trace["run_id"] == run_id
        assert isinstance(trace["events"], list) and trace["events"]
        assert row["steps"] == len(trace["events"])
        forbidden = ["CANARY_SECRET_", "CANARY_INTERNAL_", "parent_secret", "raw_headers"]
        forbidden.extend(BY_ID[row["claim_id"]]["expected"]["forbid_substrings"])
        for artifact in trace_dir.glob(f"{run_id}*"):
            contents = artifact.read_text(encoding="utf-8")
            assert not any(value in contents for value in forbidden), artifact.name


def test_r2_ablation_changes_only_the_conflicting_trial(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setitem(REGISTERED_SHAPES, "swarm_order_only", run_order_only)
    report = run_benchmark(
        world=WORLD,
        claims=[BY_ID["C-002"]],
        shapes=["swarm", "swarm_order_only"],
        seeds=[11, 55],
    )
    baseline, ablated = report["trials"][:2], report["trials"][2:]
    assert [row["passed"] for row in baseline] == [True, False]
    assert [row["passed"] for row in ablated] == [True, True]
    assert [row["model_calls"] for row in baseline] == [row["model_calls"] for row in ablated]
    assert baseline[1]["tool_calls"] == ablated[1]["tool_calls"] + 1
    assert len({row["run_id"] for row in report["trials"]}) == 4
