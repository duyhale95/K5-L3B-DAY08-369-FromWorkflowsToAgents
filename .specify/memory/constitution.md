# LogiX-VN Lab 8 Team 369 Constitution

## Core Principles

### I. Code Owns Money, Approvals & Idempotency (NON-NEGOTIABLE)
All financial calculations, policy validity checks, per-order refund caps, and ledger writes MUST remain strictly deterministic in Python code (`lab8.tools.compute_compensation`, `lab8.compensation.quote`, and `lab8.durability.issue_refund`). `MockLLM` MAY only parse/draft non-authoritative text and MUST NEVER choose refund amounts, bypass approvals, or commit writes. Every shape (`workflow`, `single`, `orchestrator`) MUST forward the FULL quote to `durability.issue_refund(conn, claim_id, full_quote, crash_at=crash_at)` and MUST NOT subtract prior refunds itself or catch `InjectedCrash`.

### II. Protected Evaluator & Corpus Integrity (NON-NEGOTIABLE)
Protected evaluator, durability, policy, configuration, fixture, and grader-audit files (`src/lab8/metrics.py`, `src/lab8/durability.py`, `src/lab8/policy.py`, `src/config/*.yaml`, `src/data/*`, `src/grader_audit/grader_*.py`, `src/grader_audit/fixtures/*.json`) MUST NEVER be modified. Generated evidence files in `src/reports/*.json` MUST NEVER be hand-edited. `src/lab8/shapes/workflow.py` MUST NOT copy `REFERENCE_WEAKNESS` from `swarm_reference.py`.

### III. Security Boundary, Untrusted Ticket Input & Trace Contract v1 (NON-NEGOTIABLE)
Ticket text MUST always be treated as untrusted user data, never as commands or authoritative delay/policy facts; structured order rows and `is_current` policies with `effective_date <= as_of` are the sole source of truth. Every `run_claim` execution path—including early returns (`needs_info`, `escalated`, `denied`, `failed`) and crash paths—MUST emit a fresh Trace Contract v1 JSON (`{"run_id": <same RunResult.run_id>, "events": [...]}`) and construct `RunResult` via `lab8.shapes.common.finish()`. `CANARY_SECRET_*`, `parent_secret`, `raw_headers`, phone numbers, addresses, internal notes, and item names MUST NEVER appear in traces, `<run_id>*` files, `RunResult`, handoffs, or stdout.

### IV. Sequential 5-Person Ownership & Green-Main Gate
Implementation and verification proceed strictly sequentially across the 5 team members on `main` (`Người 1 → Người 2 → Người 3 → Người 4 → Người 5`). Each member MUST pull the latest `main` before starting, restrict edits to their assigned scope/files, verify that the host gate (`python -m pytest -q`) remains 100% passing alongside all tests for completed shapes and their new tests, and push cleanly to `main` without force-pushing or rewriting history.

### V. Verifiable Evidence & Individual Accountability
Every member (1 through 5) MUST leave: (1) at least one meaningful technical commit in git history on `main`, (2) at least one added or modified test in `src/tests/`, (3) one personal report at `report/team/<MSSV>_<HoTen>.md` copied from `report/team/MSSV_HoTen.md` (preserving the template file), and (4) one completed row in `TEAM.md` under `## Bảng đóng góp`. All metrics in `report/team/decision_adr.md`, `report/team/research_card.md`, `report/team/group_report.md`, and `report/team/bonus_report.md` MUST trace directly to tool-generated reports (`src/reports/*.json`, pytest outputs) with exact `commit hash` and `run_id`.

## Technical & Compliance Constraints

- **Runtime & Isolation**: Python 3.11–3.13, offline-only (`MockLLM` seeded, no live LLM API keys or network calls), cross-platform (Windows/macOS/Linux), all lab commands run from `src/`.
- **Database Lifecycle**: Every `connect(store_path)` opened by a shape MUST be closed in a `finally:` block to prevent Windows SQLite file locks.
- **Submission Gate**: Before final push by Người 5, `python -m lab8.check_submission` MUST report `0 FAIL`, `src/reports/crash.json` MUST report `20/20`, `src/reports/benchmark.json` MUST cover all 4 official shapes across 14 public claims and seeds `11,22,33,44,55`, and the chosen shape MUST satisfy all 3 must-pass conditions (`approval_bypass_count == 0`, `secret_leak_count == 0`, `crash_safety == 20/20`).
- **Bonus Track (B7)**: Team targets Bonus Topic B7 (`grader_audit` metamorphic auditing) via `src/tests/test_bonus_grader_audit.py` and `report/team/bonus_report.md` without modifying `src/grader_audit/grader_*.py` or fixtures.

## Development & Handoff Workflow

- **Branching & Sequential Handoff**: Members work directly on `main` (or merge PRs cleanly into `main`) in strict order 1 → 5. A member MUST NOT begin coding until the preceding member has pushed to `main` and updated `specs/001-logix-claim-agents/tasks.md` checkboxes `[X]`.
- **Verification Before Push**: Every push to `main` MUST be accompanied by observed passing output of `python -m lab8.smoke` and `python -m pytest -q` (and `python -m pytest -q -m student -o addopts= -k <shape>` for shape owners).
- **Secrets Hygiene**: `.env`, `traces/`, `*.sqlite`, `student_drop/`, and `src/eval/instructor/` MUST NEVER be committed.

## Governance

This Constitution supersedes ad-hoc practices for repository `K5-L3B-Day8-369-From-Workflows-to-Agents`. Amendments require team consensus, an explicit version bump following semantic versioning (`MAJOR`: principle removal/redefinition; `MINOR`: new principle or material constraint expansion; `PATCH`: clarification), and synchronization with `specs/001-logix-claim-agents/plan.md` and `tasks.md`. Every sequential handoff review MUST verify compliance with Core Principles I–V.

**Version**: 1.0.0 | **Ratified**: 2026-11-17 | **Last Amended**: 2026-11-17
