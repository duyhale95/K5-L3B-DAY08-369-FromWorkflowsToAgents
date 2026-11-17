# Implementation Plan: LogiX-VN Multi-Architecture Claim Processing & Team 369 Sequential Delivery

**Branch**: `main` (`001-logix-claim-agents` sequential delivery) | **Date**: 2026-11-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-logix-claim-agents/spec.md`

## Summary

Implement the three missing LogiX-VN claim-processing architectures (`workflow`, `single`, `orchestrator`) alongside the reference `swarm`, enforce all three must-pass safety invariants (`approval_bypass == 0`, `secret_leak == 0`, `crash_safety == 20/20`), execute Bonus Topic **B7 (Kiểm toán grader)** via metamorphic testing against `grader_a`, `grader_b`, and `grader_c`, benchmark all four shapes on identical claims/seeds/pricing, and complete all machine-checked and narrative team reports across 5 sequential members starting with **Hà Lê Duy (2A202603851, `duyhale95`)**.

## Technical Context

**Language/Version**: Python 3.11–3.13 (verified on Python 3.13.3 on Windows AMD64)
**Primary Dependencies**: `pytest>=8.3.4,<9`, `PyYAML>=6.0.2,<7`, Python stdlib (`sqlite3`, `json`, `pathlib`, `argparse`, `unittest`/`tempfile`)
**Storage**: Per-trial isolated SQLite (`src/lab8/db.py`), schema with `meta`, `orders`, `policies`, `claims`, `approvals`, `refund_ledger`, `audit_events`, `checkpoints`
**Testing**: `pytest` (default host gate `python -m pytest -q`; student matrix `python -m pytest -q -m student -o addopts=`; bonus suite `python -m pytest -q tests/test_bonus_*.py`)
**Target Platform**: Cross-platform CLI/library (Windows PowerShell, macOS, Linux; CI matrix on `ubuntu-latest`, `windows-latest`, `macos-latest`)
**Project Type**: Single Python lab project inside `src/` with root-level governance/team reports
**Performance Goals**: Offline deterministic execution (`MockLLM` seeded); minimal token/tool cost per success (`workflow` lowest cost/steps, zero seed variance)
**Constraints**: Offline-only (zero external API keys/network calls); protected files (`metrics.py`, `durability.py`, `policy.py`, `config/*.yaml`, `data/*`, `grader_audit/grader_*.py`, `grader_audit/fixtures/*.json`) MUST NOT be edited; Windows SQLite handles MUST close in `finally:` blocks; Trace Contract v1 on every return/crash path
**Scale/Scope**: 14 public claims × 5 seeds (`11,22,33,44,55`), 20-point crash suite, 40-claim × 5-seed external hidden evaluation (`pass_rate >= 0.75` required; `>= 0.80` for Bonus B7 gate), 5 team members working sequentially

## Constitution Check

*GATE: Checked pre-design and re-checked post-design.*

1. **Principle I (Code Owns Money, Approvals & Idempotency)**: PASS — All three shapes call `lab8.tools.compute_compensation` for quotes and `lab8.durability.issue_refund(conn, claim_id, full_quote, crash_at=crash_at)` with the unsubtracted full quote; `InjectedCrash` propagates unhandled after trace flush.
2. **Principle II (Protected Evaluator & Corpus Integrity)**: PASS — Only `src/lab8/shapes/workflow.py`, `single.py`, `orchestrator.py`, new tests in `src/tests/`, generated files in `src/reports/`, `TEAM.md`, and `report/team/*.md` are edited.
3. **Principle III (Security Boundary & Trace Contract v1)**: PASS — Claims read via `get_claim_view`, orders via `lookup_order`, handoffs via `make_handoff` allowlist; traces written via `lab8.trace.Trace` + `finish()` on all return paths; zero `CANARY_SECRET_*` or PII in traces/stdout.
4. **Principle IV (Sequential 5-Person Ownership & Green-Main Gate)**: PASS — Strict 1 → 2 → 3 → 4 → 5 execution on `main` with mandatory host + shape tests before each push.
5. **Principle V (Verifiable Evidence & Accountability)**: PASS — Every member adds >= 1 commit, >= 1 test in `src/tests/`, `report/team/<MSSV>_<HoTen>.md`, and row in `TEAM.md`.

## Project Structure

### Documentation (this feature)

```text
specs/001-logix-claim-agents/
├── spec.md              # 5 sequential user stories (P1-P5) + FR/SC/Edge cases
├── checklists/
│   └── requirements.md  # Spec quality checklist
├── plan.md              # This implementation plan
├── research.md          # Phase 0 findings from repo inspection
├── data-model.md        # Entities, SQLite schema, state transitions
├── quickstart.md        # Exact verification commands & sequential handoff protocol
├── contracts/
│   └── shape-and-trace-contract.md  # RunResult, Trace v1, Handoff v1, Grader Audit contracts
└── tasks.md             # Phase 1-7 sequential 5-person task breakdown
```

### Source Code & Team Deliverables (repository root)

```text
TEAM.md                                      # Team 369 roster + sequential assignments + machine-read contribution table
report/team/
├── MSSV_HoTen.md                            # Template (KEEP UNCHANGED)
├── 2A202603851_HaLeDuy.md                   # Member 1 report (Hà Lê Duy)
├── <MSSV_2>_<HoTen_2>.md                    # Member 2 report
├── <MSSV_3>_<HoTen_3>.md                    # Member 3 report
├── <MSSV_4>_<HoTen_4>.md                    # Member 4 report
├── <MSSV_5>_<HoTen_5>.md                    # Member 5 report
├── decision_adr.md                          # Machine-checked ADR (Member 5 finalizes)
├── research_card.md                         # Machine-checked Research Card (Member 5 finalizes)
├── group_report.md                          # Main group report <= 5 pages (Member 5 finalizes)
└── bonus_report.md                          # Bonus B7 report <= 2 pages (Member 4 drafts data, Member 5 finalizes)

src/lab8/shapes/
├── workflow.py                              # Member 1 (Hà Lê Duy) — Shape A
├── single.py                                # Member 2 — Shape B
├── orchestrator.py                          # Member 3 — Shape C
└── swarm_reference.py                       # Reference Shape D (READ-ONLY)

src/tests/
├── test_workflow_shape.py                   # Member 1 tests
├── test_single_shape.py                     # Member 2 tests
├── test_orchestrator_shape.py               # Member 3 tests
├── test_must_pass_audit.py                  # Member 4 cross-shape safety/crash tests
├── test_bonus_grader_audit.py               # Member 4 Bonus B7 metamorphic tests
└── test_benchmark_invariants.py             # Member 5 benchmark/submission regression tests

src/reports/
├── crash.json                               # Generated by lab8.crash_test (Member 4/5)
├── benchmark.json                           # Generated by lab8.benchmark (Member 5)
├── bonus_grader_audit.json                  # Optional tool-generated B7 evidence script output (Member 4/5)
└── hidden_selfcheck.json                    # Optional if student_drop/ provided (Member 5)
```

**Structure Decision**: Existing skeleton-lab layout (`src/` for code/tests/reports, `report/team/` and `TEAM.md` at root) is preserved with zero structural changes to graded modules; `.specify/` and `specs/001-logix-claim-agents/` live at root cleanly outside `src/`.

## Sequential 5-Member Ownership Plan

| Thứ tự | Thành viên | Phạm vi sở hữu chính | File code / test / report phụ trách | Điều kiện bàn giao (Done Gate) |
| --- | --- | --- | --- | --- |
| **1** | **Hà Lê Duy** (`2A202603851`, `duyhale95`) | Spec Kit + Chia việc + Baseline check + **Shape A (`workflow`)** | `.specify/`, `specs/001-logix-claim-agents/*`, `TEAM.md`, `src/lab8/shapes/workflow.py`, `src/tests/test_workflow_shape.py`, `report/team/2A202603851_HaLeDuy.md` | `smoke` pass, host `pytest -q` 100% green, student `workflow` **62/62 passed**, push `main` |
| **2** | **Thành viên 2** *(điền tên/MSSV/GitHub khi nhận lượt)* | **Shape B (`single` ReAct agent)** | `src/lab8/shapes/single.py`, `src/tests/test_single_shape.py`, `TEAM.md`, `report/team/<MSSV>_<HoTen>.md`, đánh dấu `[X]` Phase 4 trong `tasks.md` | Pull `main`, host `pytest -q` green, student `workflow`+`single` **124/124 passed**, push `main` |
| **3** | **Thành viên 3** *(điền tên/MSSV/GitHub khi nhận lượt)* | **Shape C (`orchestrator` + sanitized `handoff.v1`)** | `src/lab8/shapes/orchestrator.py`, `src/tests/test_orchestrator_shape.py`, `TEAM.md`, `report/team/<MSSV>_<HoTen>.md`, đánh dấu `[X]` Phase 5 trong `tasks.md` | Pull `main`, host `pytest -q` green, student `workflow`+`single`+`orchestrator` **186/186 passed**, push `main` |
| **4** | **Thành viên 4** *(điền tên/MSSV/GitHub khi nhận lượt)* | **CP4 Must-Pass Audit + Crash 20/20 + Bonus B7 (Grader Audit)** | `src/tests/test_must_pass_audit.py`, `src/tests/test_bonus_grader_audit.py`, `src/reports/crash.json`, `TEAM.md`, `report/team/<MSSV>_<HoTen>.md`, ghi nhận kết quả B7 vào `bonus_report.md` / `tasks.md` | Pull `main`, host `pytest -q` green, `crash_test` **20/20**, `test_bonus_grader_audit.py` green, push `main` |
| **5** | **Thành viên 5** *(điền tên/MSSV/GitHub khi nhận lượt)* | **CP5 Benchmark + ADR + Research Card + Group Report + Submission Gate** | `src/tests/test_benchmark_invariants.py`, `src/reports/benchmark.json`, `report/team/decision_adr.md`, `research_card.md`, `group_report.md`, `bonus_report.md`, `TEAM.md`, `report/team/<MSSV>_<HoTen>.md` | Pull `main`, tạo `benchmark.json` + `crash.json`, `pytest` green, `check_submission` **0 FAIL**, commit hash khớp `decision_adr.md`, push `main` |

## Complexity Tracking

No Constitution violations. All three shapes use existing host helpers (`connect`, `get_claim_view`, `lookup_order`, `compute_compensation`, `issue_refund`, `run_react`, `make_handoff`, `run_readonly_investigators`, `Trace`, `finish`) without introducing external dependencies or modifying protected modules.
