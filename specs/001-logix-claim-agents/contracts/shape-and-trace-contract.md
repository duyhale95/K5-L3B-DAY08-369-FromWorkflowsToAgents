# Interface Contracts: Shapes, Trace v1, Handoff v1 & Bonus B7

## 1. Shape Entrypoint Contract (`src/lab8/shapes/*.py`)

```python
def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult
```

- Must return `lab8.schemas.RunResult` via `lab8.shapes.common.finish(...)`.
- `status` MUST be one of `("resolved", "needs_info", "escalated", "denied", "failed")`.
- `run_id` MUST equal `make_run_id(shape, claim_id, seed)`.
- `proposal_amount` MUST be integer VND representing the FULL order entitlement quote (never subtracted for prior refunds).
- Exceptions other than `InjectedCrash` MUST NOT escape `run_claim` during normal execution; SQLite connection MUST close in `finally:`.

## 2. Trace Contract v1 (`docs/contracts.md`)

- `RunResult.trace_path` points to a JSON file created during the current invocation (`mtime >= started_at - 1.0`).
- JSON body MUST be an object containing `"run_id": <exact RunResult.run_id>` and `"events": [...]`.
- Any auxiliary files written by the shape MUST live in the trace directory and start with `<run_id>`.
- Forbidden substrings across `RunResult`, `trace_path`, sibling `<run_id>*` files, and stdout: `CANARY_SECRET_*`, `parent_secret`, `raw_headers`, `phone`, `address`, `internal_note`, `item_name` (and `CANARY_INTERNAL_*`).

## 3. Handoff Contract v1 (`src/lab8/handoff.py`)

- Build via `make_handoff(request_id=..., claim_id=..., task=..., facts=..., allowed_tools=...)`.
- Allowed fields: `contract_version`, `request_id`, `claim_id`, `principal_scope`, `task`, `facts`, `allowed_tools`, `max_output_tokens`.
- `allowed_tools` subset of `READONLY_TOOLS` (`get_claim_view`, `lookup_order`, `lookup_policy`, `lookup_refund_history`, `get_clause`, `compute_compensation`).
- `WRITE_TOOLS` (`issue_refund`, `append_audit`) strictly forbidden from worker/handoff payloads.

## 4. Bonus B7 Grader Audit Contract (`src/grader_audit/`)

- Candidate modules: `grader_audit.grader_a`, `grader_audit.grader_b`, `grader_audit.grader_c`, each exposing `summarize(trials: list[dict]) -> dict[str, dict]`.
- Official fixtures in `src/grader_audit/fixtures/`:
  - `metamorphic_claim_delay.json` (domain `lab8.compensation.quote` boundary: 2 vs 3 delay days)
  - `metamorphic_infra.json` (pass rate invariant under added `infra_error: true` trials)
  - `metamorphic_duplicate.json` (rates invariant & sums doubled under dataset duplication)
- Bonus B7 test module: `src/tests/test_bonus_grader_audit.py` using `@pytest.mark.parametrize` across all 3 candidates + ≥ 1 new metamorphic relation + `report/team/bonus_report.md` (`# Bonus report: B7`).
