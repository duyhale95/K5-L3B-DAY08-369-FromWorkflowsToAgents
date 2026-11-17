# Phase 0 Research: LogiX-VN Starter Codebase & Architecture Analysis

## Decision 1: Deterministic Shape A (`workflow`) Design

- **Decision**: Implement `src/lab8/shapes/workflow.py` as a linear, deterministic Python pipeline using `connect()` with `try/finally: conn.close()`, `get_claim_view()`, `lookup_order()`, `compute_compensation()`, `durability.issue_refund(..., crash_at=crash_at)` with the full quote, optional `mock_llm.complete(..., purpose="draft")` for customer text, `Trace`, and `lab8.shapes.common.finish()`.
- **Rationale**: Code owns every business rule (`needs_info` when `order_id` empty, `escalated` when order missing or outside principal scope, `denied` when `quote == 0`, full quote forwarded to host when `quote > 0`). It avoids `swarm_reference.py`'s `REFERENCE_WEAKNESS` (seed % 5 == 0 trusting ticket delay), minimizes model/tool calls, and yields zero seed variance.
- **Alternatives considered**: Calling `MockLLM` to parse delay days or summarize claim rows — rejected because ticket prose is untrusted and violates `RULES.md` / `business_rules.md`.

## Decision 2: Bounded Shape B (`single` ReAct) Design

- **Decision**: Member 2 implements `src/lab8/shapes/single.py` using `lab8.runtime.run_react(..., max_steps=8, worker=False)` where `decide(obs)` dispatches only read tools (`get_claim_view`, `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`), logs a `MockLLM` step in `Budget`, never calls write tools inside `decide`, and invokes `durability.issue_refund` once after the loop exits cleanly.
- **Rationale**: Satisfies `src/lab8/runtime.py` contract (`write tools are host-only`) and caps exploration at 8 steps while ensuring `MockLLM` cannot alter numeric quotes or skip host authorization.
- **Alternatives considered**: Putting `issue_refund` inside `decide()` — rejected because `runtime.dispatch` raises `ToolRejected` on `WRITE_TOOLS`.

## Decision 3: Isolated Shape C (`orchestrator`) Design

- **Decision**: Member 3 implements `src/lab8/shapes/orchestrator.py` using `lab8.handoff.make_handoff(...)` with `allowed_tools=["lookup_order", "lookup_policy", "lookup_refund_history", "compute_compensation"]` (read-only), `run_readonly_investigators(...)`, and tracing `safe_dump(handoff)` rather than raw claim rows or parent context.
- **Rationale**: Enforces strict allowlist isolation (`handoff.v1`) so `parent_secret`, `raw_headers`, phone, address, internal notes, and item names never cross the worker boundary or appear in trace logs.
- **Alternatives considered**: Passing `get_claim_view` + LLM summary of `claims` row — rejected because `handoff.py` states an LLM summary is not redaction.

## Decision 4: Baseline Test & Environment Observation

- **Observed baseline (`src/.venv`, Python 3.13.3 Windows AMD64)**:
  - `python -m lab8.smoke` → `lab8.smoke pass | manifest 1.1 | MockLLM seeded | swarm C-001 refund 35000 | trace clean`
  - `python -m pytest -q` → `54 passed, 248 deselected` (includes 3 `test_grader_audit_smoke.py` cases added in starter commit `53f6368`)
  - `python -m pytest -q -m student -o addopts=` → `186 failed, 62 passed, 54 deselected` (`swarm` passes 61/62 and its 1 expected miss assertion `("C-002", 55)` passes = 62/62; the 3 stub shapes fail 62 each = 186 failed).
- **Rationale**: Confirms starter health and establishes exact baseline numbers before Member 1 writes Shape A.

## Decision 5: Bonus B7 (`grader_audit`) Scope

- **Decision**: Member 4 implements `src/tests/test_bonus_grader_audit.py` to test `grader_audit.grader_a`, `grader_b`, and `grader_c` against `metamorphic_claim_delay.json`, `metamorphic_infra.json`, `metamorphic_duplicate.json`, plus 1 newly designed metamorphic relation (e.g., scaling/permutation or zero-cost/seed-invariance check that detects bugs missed by the first three relations), and captures exact findings for Member 5 to finalize `report/team/bonus_report.md`.
- **Rationale**: Matches `docs/bonus_topics.md` B7 rubric (`+3` runnable code/tests, `+4` fair quantitative evidence without hand-typed guesses, `+3` claim/boundary/limitation analysis) without modifying `src/grader_audit/grader_*.py` or fixtures.
