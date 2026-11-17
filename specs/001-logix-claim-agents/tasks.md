---
description: "Sequential 5-person task breakdown for Lab 8 LogiX-VN (Team 369) generated via Spec Kit"
---

# Tasks: LogiX-VN Multi-Architecture Claim Processing & Team 369 Sequential Delivery

**Input**: Design documents from `specs/001-logix-claim-agents/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/shape-and-trace-contract.md`, `quickstart.md`)

**Execution Mode**: **TUẦN TỰ 5 NGƯỜI TRÊN `main` (`Người 1 → Người 2 → Người 3 → Người 4 → Người 5`)**
Mỗi thành viên chỉ bắt đầu lượt mình sau khi người đứng trước đã push commit xanh lên `main`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Có thể chạy song song trong phạm vi lượt của cùng một thành viên (khác file, không phụ thuộc nhau)
- **[Story]**: Ánh xạ User Story trong `spec.md` (`[US1]` Người 1 .. `[US5]` Người 5)
- Mọi lệnh chạy kiểm thử đều thực thi trong thư mục `src/`

---

## Phase 1: Setup (Người 1 — Hà Lê Duy, `2A202603851`, `duyhale95`)

**Purpose**: Khởi tạo Spec Kit, kiểm tra môi trường Python `src/.venv`, xác nhận baseline starter và thiết lập danh sách chia việc 5 người tuần tự.

- [ ] T001 Initialize GitHub Spec Kit (`specify init --here --integration agy --script ps`) creating `.specify/` and `.agents/skills/` at repository root
- [ ] T002 Create project governance rules in `.specify/memory/constitution.md` aligned with `RULES.md`, `RUBRIC.md`, `docs/business_rules.md`, and `docs/contracts.md`
- [ ] T003 Verify starter Python 3.11–3.13 environment in `src/.venv` (`python -m pip install -r requirements.txt`, `python -m lab8.smoke`, `python -m pytest -q`)

---

## Phase 2: Foundational Specification & Team Division (Người 1 — Hà Lê Duy, `2A202603851`, `duyhale95`)

**Purpose**: Hoàn thiện bộ tài liệu Spec Kit (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md`) và khởi tạo bảng phân công tuần tự 5 thành viên trong `TEAM.md` trước khi code Shape đầu tiên.

**⚠️ CRITICAL**: Không viết code shape trước khi Spec Kit và bảng chia việc trong `TEAM.md` sẵn sàng.

- [ ] T004 Write sequential 5-person feature specification and checklist in `specs/001-logix-claim-agents/spec.md` and `specs/001-logix-claim-agents/checklists/requirements.md`
- [ ] T005 Write technical plan, research findings, data model, contracts, and quickstart in `specs/001-logix-claim-agents/plan.md`, `specs/001-logix-claim-agents/research.md`, `specs/001-logix-claim-agents/data-model.md`, `specs/001-logix-claim-agents/contracts/shape-and-trace-contract.md`, and `specs/001-logix-claim-agents/quickstart.md`
- [ ] T006 Populate Team 369 header, sequential 5-member roster slots (Member 1 = Hà Lê Duy, slots 2–5 ready for teammates), and `## Phân công tuần tự` in `TEAM.md`

**Checkpoint**: Spec Kit + baseline host gate verified (`54 passed`); ready for Người 1's technical delivery (`[US1]`).

---

## Phase 3: User Story 1 — Shape A (`workflow`) & Phần Đầu Tiên (Priority: P1 🎯 MVP)

**Owner**: **Người 1 — Hà Lê Duy** (`MSSV: 2A202603851`, GitHub: `duyhale95`)  
**Goal**: Hoàn thành **Shape A (`workflow.py`)** chuẩn mực theo CP2 + CP3 (code sở hữu tiền, full quote vào `durability.issue_refund`, truyền `crash_at` và không bắt `InjectedCrash`, trace contract v1 sạch secret/PII), thêm test unit, viết báo cáo cá nhân và push lên `main` làm nền cho Người 2.  
**Independent Test**: `python -m pytest -q` xanh 100% và `python -m pytest -q -m student -o addopts= -k workflow` đạt `62 passed`.

### Tests for User Story 1

- [ ] T007 [P] [US1] Write unit & contract tests for Shape A covering edge policies (`SHIP-LATE-OLD`, `SHIP-LATE-FUTURE`), ticket delay override rejection, `needs_info`/`escalated` clean traces, per-order cap T13/T14, and all 3 `crash_at` points in `src/tests/test_workflow_shape.py`

### Implementation & Handoff for User Story 1

- [ ] T008 [US1] Implement deterministic claim pipeline `run_claim` in `src/lab8/shapes/workflow.py` (`connect` in `try/finally`, `get_claim_view`, `needs_info`, `lookup_order`, `escalated`, `compute_compensation`, `MockLLM` `draft` only, `durability.issue_refund` with full quote + `crash_at`, flush trace before `InjectedCrash`, return via `finish()`)
- [ ] T009 [US1] Verify host gate (`python -m pytest -q`) and Shape A student matrix (`python -m pytest -q -m student -o addopts= -k workflow` = 62 passed) from `src/`
- [ ] T010 [P] [US1] Create individual report `report/team/2A202603851_HaLeDuy.md` (copying structure from `report/team/MSSV_HoTen.md` without altering template)
- [ ] T011 [US1] Update Hà Lê Duy's contribution row in `TEAM.md` (`## Bảng đóng góp`), mark Phase 1–3 `[X]` in `specs/001-logix-claim-agents/tasks.md`, commit cleanly, and push to `main`

**Handoff Gate 1 → 2**: `main` có commit code + test của Hà Lê Duy; `python -m pytest -q` xanh và `workflow` đạt 62/62 student tests.

---

## Phase 4: User Story 2 — Shape B (`single` ReAct Agent) (Priority: P2)

**Owner**: **Người 2** *(pull `main` sau Người 1, điền Họ tên / MSSV / GitHub vào `TEAM.md`)*  
**Goal**: Implement **Shape B (`single.py`)** dùng `lab8.runtime.run_react(..., max_steps=8)` chỉ dùng read tool, không tin prose trong ticket hơn DB, tính quote bằng `compute_compensation`, gọi `durability.issue_refund` với full quote + `crash_at`, ghi Trace Contract v1 sạch secret/PII.  
**Independent Test**: `python -m pytest -q` xanh 100% và `python -m pytest -q -m student -o addopts= -k "workflow or single"` đạt `124 passed`.

### Tests for User Story 2

- [ ] T012 [P] [US2] Write unit tests for Shape B verifying `max_steps=8` enforcement, read-only tool selection in `decide`, resistance to ticket prompt-injection/inflated delay, `Budget` tracking, and `crash_at` propagation in `src/tests/test_single_shape.py`

### Implementation & Handoff for User Story 2

- [ ] T013 [US2] Implement bounded ReAct `run_claim` in `src/lab8/shapes/single.py` using `lab8.runtime.run_react`, `get_claim_view`, `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`, `MockLLM` accounting, and host `durability.issue_refund`
- [ ] T014 [US2] Verify host gate (`python -m pytest -q`), `workflow` + `single` student matrix (`124 passed`), and `test_single_shape.py` from `src/`
- [ ] T015 [P] [US2] Fill Member 2 info in `TEAM.md` (`## Thành viên` & `## Bảng đóng góp`) and create personal report `report/team/<MSSV_2>_<HoTen_2>.md`
- [ ] T016 [US2] Mark Phase 4 `[X]` in `specs/001-logix-claim-agents/tasks.md`, commit all changes cleanly, and push to `main`

**Handoff Gate 2 → 3**: `main` có `workflow` + `single` đều đạt 62/62 student tests (124/124); host gate xanh.

---

## Phase 5: User Story 3 — Shape C (`orchestrator` & Sanitized Handoff) (Priority: P3)

**Owner**: **Người 3** *(pull `main` sau Người 2, điền Họ tên / MSSV / GitHub vào `TEAM.md`)*  
**Goal**: Implement **Shape C (`orchestrator.py`)** dùng `lab8.handoff.make_handoff` + `lab8.runtime.run_readonly_investigators`, chỉ truyền allowlist facts và read-only tools (có `lookup_refund_history`), không rò rỉ `CANARY_SECRET_*` / `raw_headers` / PII vào worker hay trace, gọi `durability.issue_refund` với full quote + `crash_at`.  
**Independent Test**: `python -m pytest -q` xanh 100% và toàn bộ ma trận `python -m pytest -q -m student -o addopts=` đạt `248 passed` (`workflow`, `single`, `orchestrator` 186/186 pass; `swarm` 62/62 assertion pass).

### Tests for User Story 3

- [ ] T017 [P] [US3] Write unit tests for Shape C verifying `handoff.v1` allowlist isolation (dropping `parent_secret`, `raw_headers`, phone, address, internal_note, item_name), read-only investigator enforcement, trace cleanliness on early returns/crashes, and T13/T14 full-quote handoff in `src/tests/test_orchestrator_shape.py`

### Implementation & Handoff for User Story 3

- [ ] T018 [US3] Implement orchestrator + read-only investigator `run_claim` in `src/lab8/shapes/orchestrator.py` using `make_handoff`, `run_readonly_investigators`, `safe_dump`, `compute_compensation`, `durability.issue_refund` with `crash_at`, and `finish()`
- [ ] T019 [US3] Verify host gate (`python -m pytest -q`), full student matrix (`python -m pytest -q -m student -o addopts=` = `248 passed`), and `test_orchestrator_shape.py` from `src/`
- [ ] T020 [P] [US3] Fill Member 3 info in `TEAM.md` (`## Thành viên` & `## Bảng đóng góp`) and create personal report `report/team/<MSSV_3>_<HoTen_3>.md`
- [ ] T021 [US3] Mark Phase 5 `[X]` in `specs/001-logix-claim-agents/tasks.md`, commit all changes cleanly, and push to `main`

**Handoff Gate 3 → 4**: Cả 3 shape học viên (`workflow`, `single`, `orchestrator`) đều xanh 62/62 trên `main`.

---

## Phase 6: User Story 4 — CP4 Must-Pass Safety Audit, Crash 20/20 & Bonus B7 (Priority: P4)

**Owner**: **Người 4** *(pull `main` sau Người 3, điền Họ tên / MSSV / GitHub vào `TEAM.md`)*  
**Goal**: Kiểm toán toàn diện 3 điều kiện must-pass trên cả 3 shape (`workflow`, `single`, `orchestrator`), tạo `src/reports/crash.json` (`20/20`), và thực hiện phần kỹ thuật của **Bonus B7 (Kiểm toán grader)** trên `grader_a`, `grader_b`, `grader_c` với 3 fixture có sẵn + 1 quan hệ metamorphic mới.  
**Independent Test**: `python -m pytest -q`, `python -m pytest -q tests/test_bonus_grader_audit.py`, và `python -m lab8.crash_test --count 20 --out reports/crash.json` (`crash_safety 20/20`) đều xanh.

### Tests & Verification for User Story 4

- [ ] T022 [P] [US4] Write cross-shape must-pass audit tests (crash windows `before_effect`/`after_effect_before_checkpoint`/`after_checkpoint`, approval mismatch/revoked/expired, per-order cap T13/T14, and canary/PII leak scan across trace + sibling `<run_id>*` files) for `workflow`, `single`, and `orchestrator` in `src/tests/test_must_pass_audit.py`
- [ ] T023 [US4] Run official 20-point crash suite `python -m lab8.crash_test --count 20 --out reports/crash.json` from `src/` and confirm `crash_safety == "20/20"`

### Bonus B7 (Grader Audit) Execution for User Story 4

- [ ] T024 [US4] Inspect `src/grader_audit/README.md`, `grader_a.py`, `grader_b.py`, `grader_c.py`, and `src/grader_audit/fixtures/*.json` (read-only; DO NOT edit any `grader_audit/` files)
- [ ] T025 [US4] Implement Bonus B7 metamorphic test suite in `src/tests/test_bonus_grader_audit.py` parametrizing `["grader_a", "grader_b", "grader_c"]` over `metamorphic_claim_delay.json`, `metamorphic_infra.json`, `metamorphic_duplicate.json`, PLUS one newly designed metamorphic relation catching a defect missed by the first three relations
- [ ] T026 [P] [US4] Run `python -m pytest -q tests/test_bonus_grader_audit.py` (optionally generate deterministic JSON evidence `src/reports/bonus_grader_audit.json` via script without hand-editing) and draft technical findings (exact failing fixtures, numeric deltas, behavioral defect names) in `report/team/bonus_report.md`
- [ ] T027 [P] [US4] Fill Member 4 info in `TEAM.md` (`## Thành viên` & `## Bảng đóng góp`) and create personal report `report/team/<MSSV_4>_<HoTen_4>.md`
- [ ] T028 [US4] Verify `python -m pytest -q` and `python -m pytest -q tests/test_bonus_grader_audit.py`, mark Phase 6 `[X]` in `specs/001-logix-claim-agents/tasks.md`, commit cleanly, and push to `main`

**Handoff Gate 4 → 5**: `src/reports/crash.json` đạt `20/20`, `test_must_pass_audit.py` và `test_bonus_grader_audit.py` chạy xanh ổn định trên `main`.

---

## Phase 7: User Story 5 — CP5 Benchmark, ADR, Research Card, Reports & Submission Gate (Priority: P5)

**Owner**: **Người 5** *(pull `main` sau Người 4, điền Họ tên / MSSV / GitHub vào `TEAM.md`)*  
**Goal**: Chạy benchmark chính thức 4 shape × 14 claim × 5 seed, tự kiểm `student_drop/` (nếu có), hoàn thiện toàn bộ báo cáo nhóm (`decision_adr.md`, `research_card.md`, `group_report.md`, `bonus_report.md`), bổ sung test invariant benchmark, và đưa `python -m lab8.check_submission` về `0 FAIL`.  
**Independent Test**: `python -m lab8.check_submission` ra `0 FAIL`, `python -m pytest -q` và `python -m pytest -q -m student -o addopts=` xanh, commit hash trong `decision_adr.md` khớp `git log`.

### Benchmark & Regression Tests for User Story 5

- [ ] T029 [P] [US5] Add regression/invariant test verifying benchmark metric formulas (`pass_rate`, `pass_5`, `seed_variance`, `cost_per_success_vnd`) and clean trace behavior across shapes in `src/tests/test_benchmark_invariants.py`
- [ ] T030 [US5] Run official crash & benchmark commands from `src/`: `python -m lab8.crash_test --count 20 --out reports/crash.json` and `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json` (DO NOT hand-edit JSON files)
- [ ] T031 [US5] If `src/student_drop/` is provided by instructor at CP5, run `python -m lab8.benchmark --shapes workflow,single,orchestrator --cases student_drop/hidden_claims.jsonl --world student_drop/hidden_world_state.json --out reports/hidden_selfcheck.json` (do NOT commit `student_drop/` or `hidden_grade.json`)

### Reports & Final Submission Gate for User Story 5

- [ ] T032 [US5] Run chosen Research Card ablation (R1–R4) strictly using `lab8.benchmark` / `--extra-shape` if needed and fill `report/team/research_card.md` (keep first two columns and all required `CÂU`, `SOURCE`, `CLAIM`, `BOUNDARY`, `HYPOTHESIS`, `METHOD`, `FAILURE / METRIC` rows non-empty)
- [ ] T033 [US5] Finalize `report/team/bonus_report.md` using the `# Bonus report: B7` template in `docs/bonus_topics.md` (<= 2 pages, exact reproducible command, numbers from tool output, CLAIM/BOUNDARY/MockLLM limits)
- [ ] T034 [US5] Write `report/team/group_report.md` (<= 5 pages excluding appendix, numbers strictly from `src/reports/benchmark.json` and `src/reports/crash.json`)
- [ ] T035 [P] [US5] Fill Member 5 info in `TEAM.md` (`## Thành viên`, `## Bảng đóng góp` with all 5 members verified) and create personal report `report/team/<MSSV_5>_<HoTen_5>.md`
- [ ] T036 [US5] Commit code/reports, capture `git rev-parse --short HEAD`, fill all machine-read fields (`- Shape chọn:`, `- Commit hash:`, `- Run id dẫn chứng:`, metrics, safety) and narrative in `report/team/decision_adr.md`, and update `Commit chốt` in `TEAM.md` & `group_report.md`
- [ ] T037 [US5] Mark Phase 7 `[X]` in `specs/001-logix-claim-agents/tasks.md`, commit docs update, run `python -m pytest -q`, `python -m pytest -q -m student -o addopts=`, `python -m pytest -q tests/test_bonus_*.py`, and `python -m lab8.check_submission` (`0 FAIL`), then push `main` and notify all 5 members to submit the GitHub repo URL on LMS

---

## Dependencies & Sequential Execution Order

```text
Phase 1 & 2 (Setup + Spec Kit) ──► Phase 3 [US1] Người 1: workflow.py + test_workflow_shape.py ──► push main
                                                                                                         │
                               ┌─────────────────────────────────────────────────────────────────────────┘
                               ▼
                         Phase 4 [US2] Người 2: single.py + test_single_shape.py ──► push main
                                                                                         │
                               ┌─────────────────────────────────────────────────────────┘
                               ▼
                         Phase 5 [US3] Người 3: orchestrator.py + test_orchestrator_shape.py ──► push main
                                                                                                     │
                               ┌─────────────────────────────────────────────────────────────────────┘
                               ▼
                         Phase 6 [US4] Người 4: test_must_pass_audit.py + crash.json + Bonus B7 ──► push main
                                                                                                       │
                               ┌───────────────────────────────────────────────────────────────────────┘
                               ▼
                         Phase 7 [US5] Người 5: benchmark.json + ADR + research_card + group_report + check_submission ──► push main
```

### Critical Rules Across All 5 Turns

1. **Always pull `main` first**: Do not start Phase `N+1` until Phase `N` is pushed and verified on `main`.
2. **Every person MUST own at least 1 commit + 1 test in `src/tests/` + 1 `report/team/<MSSV>_<HoTen>.md` + 1 row in `TEAM.md`** (Rubric C8 & `check_submission`).
3. **Never touch protected files**: `src/lab8/metrics.py`, `durability.py`, `policy.py`, `src/config/*.yaml`, `src/data/*`, `src/grader_audit/grader_*.py`, `src/grader_audit/fixtures/*.json`.
4. **Never commit runtime junk**: `src/.venv/`, `src/traces/`, `*.sqlite`, `src/student_drop/`, `src/reports/hidden_grade.json`, `.env`.
5. **Keep `report/team/MSSV_HoTen.md` untouched** as the template for subsequent members.
