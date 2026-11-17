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

- [X] T001 Initialize GitHub Spec Kit (`specify init --here --integration agy --script ps`) creating `.specify/` and `.agents/skills/` at repository root
- [X] T002 Create project governance rules in `.specify/memory/constitution.md` aligned with `RULES.md`, `RUBRIC.md`, `docs/business_rules.md`, and `docs/contracts.md`
- [X] T003 Verify starter Python 3.11–3.13 environment in `src/.venv` (`python -m pip install -r requirements.txt`, `python -m lab8.smoke`, `python -m pytest -q`)

---

## Phase 2: Foundational Specification & Team Division (Người 1 — Hà Lê Duy, `2A202603851`, `duyhale95`)

**Purpose**: Hoàn thiện bộ tài liệu Spec Kit (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md`) và khởi tạo bảng phân công tuần tự 5 thành viên trong `TEAM.md` trước khi code Shape đầu tiên.

**⚠️ CRITICAL**: Không viết code shape trước khi Spec Kit và bảng chia việc trong `TEAM.md` sẵn sàng.

- [X] T004 Write sequential 5-person feature specification and checklist in `specs/001-logix-claim-agents/spec.md` and `specs/001-logix-claim-agents/checklists/requirements.md`
- [X] T005 Write technical plan, research findings, data model, contracts, and quickstart in `specs/001-logix-claim-agents/plan.md`, `specs/001-logix-claim-agents/research.md`, `specs/001-logix-claim-agents/data-model.md`, `specs/001-logix-claim-agents/contracts/shape-and-trace-contract.md`, and `specs/001-logix-claim-agents/quickstart.md`
- [X] T006 Populate Team 369 header, sequential 5-member roster slots (Member 1 = Hà Lê Duy, slots 2–5 ready for teammates), and `## Phân công tuần tự` in `TEAM.md`

**Checkpoint**: Spec Kit + baseline host gate verified (`54 passed`); ready for Người 1's technical delivery (`[US1]`).

---

## Phase 3: User Story 1 — Shape A (`workflow`) & Phần Đầu Tiên (Priority: P1 🎯 MVP)

**Owner**: **Người 1 — Hà Lê Duy** (`MSSV: 2A202603851`, GitHub: `duyhale95`)  
**Goal**: Hoàn thành **Shape A (`workflow.py`)** chuẩn mực theo CP2 + CP3 (code sở hữu tiền, full quote vào `durability.issue_refund`, truyền `crash_at` và không bắt `InjectedCrash`, trace contract v1 sạch secret/PII), thêm test unit, viết báo cáo cá nhân và push lên `main` làm nền cho Người 2.  
**Independent Test**: `python -m pytest -q` xanh 100% và `python -m pytest -q -m student -o addopts= -k workflow` đạt `62 passed`.

### Tests for User Story 1

- [X] T007 [P] [US1] Write unit & contract tests for Shape A covering edge policies (`SHIP-LATE-OLD`, `SHIP-LATE-FUTURE`), ticket delay override rejection, `needs_info`/`escalated` clean traces, per-order cap T13/T14, and all 3 `crash_at` points in `src/tests/test_workflow_shape.py`

### Implementation & Handoff for User Story 1

- [X] T008 [US1] Implement deterministic claim pipeline `run_claim` in `src/lab8/shapes/workflow.py` (`connect` in `try/finally`, `get_claim_view`, `needs_info`, `lookup_order`, `escalated`, `compute_compensation`, `MockLLM` `draft` only, `durability.issue_refund` with full quote + `crash_at`, flush trace before `InjectedCrash`, return via `finish()`)
- [X] T009 [US1] Verify host gate (`python -m pytest -q`) and Shape A student matrix (`python -m pytest -q -m student -o addopts= -k workflow` = 62 passed) from `src/`
- [X] T010 [P] [US1] Create individual report `report/team/2A202603851_HaLeDuy.md` (copying structure from `report/team/MSSV_HoTen.md` without altering template)
- [X] T011 [US1] Update Hà Lê Duy's contribution row in `TEAM.md` (`## Bảng đóng góp`), mark Phase 1–3 `[X]` in `specs/001-logix-claim-agents/tasks.md`, commit cleanly, and push to `main`

**Handoff Gate 1 → 2**: `main` có commit code + test của Hà Lê Duy; `python -m pytest -q` xanh và `workflow` đạt 62/62 student tests.

---

## Phase 4: User Story 2 — Shape B (`single` ReAct Agent) (Priority: P2)

**Owner**: **Người 2 — Nguyễn Lê Trọng Mạnh** (`2A202603857`, GitHub: `Tiberu2611`) — *PR #1 đã duyệt & merge vào `main` tại `3406566`*  
**Goal**: Implement **Shape B (`single.py`)** dùng `lab8.runtime.run_react(..., max_steps=8)` chỉ dùng read tool, không tin prose trong ticket hơn DB, tính quote bằng `compute_compensation`, gọi `durability.issue_refund` với full quote + `crash_at`, ghi Trace Contract v1 sạch secret/PII.  
**Independent Test**: `python -m pytest -q` xanh 100% và `single` đạt `62/62` trong ma trận student (`python -m pytest -q -m student -o addopts=`).

### Tests for User Story 2

- [X] T012 [P] [US2] Write unit tests for Shape B verifying `max_steps=8` enforcement, read-only tool selection in `decide`, resistance to ticket prompt-injection/inflated delay, `Budget` tracking, and `crash_at` propagation in `src/tests/test_single_shape.py`

### Implementation & Handoff for User Story 2

- [X] T013 [US2] Implement bounded ReAct `run_claim` in `src/lab8/shapes/single.py` using `lab8.runtime.run_react`, `get_claim_view`, `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`, `MockLLM` accounting, and host `durability.issue_refund`
- [X] T014 [US2] Verify host gate (`python -m pytest -q`: 109 passed) and `single` student matrix (62/62) from `src/`
- [X] T015 [P] [US2] Fill Member 2 info in `TEAM.md` (`## Thành viên` & `## Bảng đóng góp`) and create personal report `report/team/2A202603857_NguyenLeTrongManh.md`
- [X] T016 [US2] Confirm the Phase 4 handoff on `main`. PR #1 merged the single agent (`47e48cf`), tests, and personal report (`72f91d9`) in `3406566`.

**Handoff Gate 2 → 3**: `main` có `workflow` + `single` đều đạt 62/62 student tests; host gate xanh.

---

## Phase 5: User Story 3 — Shape C (`orchestrator` & Sanitized Handoff) (Priority: P3)

**Owner**: **Người 3 — Nguyễn Hoàng Gia An** (`2A202603799`, GitHub: `AnK17-UIT`) — *PR #3 (`ade768d`), PR #4 & #5 (`0bb0e08`) đã duyệt & merge vào `main`*  
**Goal**: Implement **Shape C (`orchestrator.py`)** dùng `lab8.handoff.make_handoff` + `lab8.runtime.run_readonly_investigators`, chỉ truyền allowlist facts và read-only tools (có `lookup_refund_history`), không rò rỉ `CANARY_SECRET_*` / `raw_headers` / PII vào worker hay trace, gọi `durability.issue_refund` với full quote + `crash_at`.  
**Independent Test**: `python -m pytest -q` xanh 100% và toàn bộ ma trận `python -m pytest -q -m student -o addopts=` đạt `248 passed` (`workflow`, `single`, `orchestrator` 186/186 pass; `swarm` 62/62 assertion pass).

### Tests for User Story 3

- [X] T017 [P] [US3] Write unit tests for Shape C verifying `handoff.v1` allowlist isolation (dropping `parent_secret`, `raw_headers`, phone, address, internal_note, item_name), read-only investigator enforcement, trace cleanliness on early returns/crashes, and T13/T14 full-quote handoff in `src/tests/test_orchestrator_shape.py`

### Implementation & Handoff for User Story 3

- [X] T018 [US3] Implement orchestrator + read-only investigator `run_claim` in `src/lab8/shapes/orchestrator.py` using `make_handoff`, `run_readonly_investigators`, `safe_dump`, `compute_compensation`, `durability.issue_refund` with `crash_at`, and `finish()`
- [X] T019 [US3] Verify host gate (`python -m pytest -q`: 121 passed), full student matrix (`python -m pytest -q -m student -o addopts=` = `248 passed`), and `test_orchestrator_shape.py` (12 passed) from `src/`
- [X] T020 [P] [US3] Fill Member 3 info in `TEAM.md` (`## Thành viên` & `## Bảng đóng góp`) and create personal report `report/team/2A202603799_NguyenHoangGiaAn.md`
- [X] T021 [US3] Mark Phase 5 `[X]` in `specs/001-logix-claim-agents/tasks.md`; PR #3 (`ade768d`: `0d6ac71`, `8038518`) and PR #4/#5 (`0bb0e08`: `45bf255`, `f42562e`) reviewed and merged into `main`

**Handoff Gate 3 → 4**: Cả 3 shape học viên (`workflow`, `single`, `orchestrator`) đều xanh 62/62 trên `main`.

---

## Phase 6: User Story 4 — CP4 Must-Pass Safety Audit, Crash 20/20 & Bonus B7 (Priority: P4)

**Owner**: **Người 4 — Hoàng Đức An** (`2A202603800`, GitHub: `katogithub2701`) — *Push trực tiếp trên `main`: `dd3ae22`, `23f7734`*  
**Goal**: Kiểm toán toàn diện 3 điều kiện must-pass trên cả 3 shape (`workflow`, `single`, `orchestrator`), tạo `src/reports/crash.json` (`20/20`), và thực hiện phần kỹ thuật của **Bonus B7 (Kiểm toán grader)** trên `grader_a`, `grader_b`, `grader_c` với 3 fixture có sẵn + 1 quan hệ metamorphic mới.  
**Independent Test**: `python -m pytest -q`, `python -m pytest -q tests/test_bonus_grader_audit.py`, và `python -m lab8.crash_test --count 20 --out reports/crash.json` (`crash_safety 20/20`) đều xanh.

### Tests & Verification for User Story 4

- [X] T022 [P] [US4] Write cross-shape must-pass audit tests (crash windows `before_effect`/`after_effect_before_checkpoint`/`after_checkpoint`, approval mismatch/revoked/expired, per-order cap T13/T14, and canary/PII leak scan across trace + sibling `<run_id>*` files) for `workflow`, `single`, and `orchestrator` in `src/tests/test_must_pass_audit.py`
- [X] T023 [US4] Run official 20-point crash suite `python -m lab8.crash_test --count 20 --out reports/crash.json` from `src/` and confirm `crash_safety == "20/20"`

### Bonus B7 (Grader Audit) Execution for User Story 4

- [X] T024 [US4] Inspect `src/grader_audit/README.md`, `grader_a.py`, `grader_b.py`, `grader_c.py`, and `src/grader_audit/fixtures/*.json` (read-only; DO NOT edit any `grader_audit/` files)
- [X] T025 [US4] Implement Bonus B7 metamorphic test suite in `src/tests/test_bonus_grader_audit.py` and `src/bonus/grader_audit.py` parametrizing `["grader_a", "grader_b", "grader_c"]` over `metamorphic_claim_delay.json`, `metamorphic_infra.json`, `metamorphic_duplicate.json`, PLUS `trial_order_does_not_move_metrics`
- [X] T026 [P] [US4] Run `python -m pytest -q tests/test_bonus_grader_audit.py` (19 passed), generate `src/reports/bonus_grader_audit.json` via `python -m bonus.grader_audit`, and draft technical findings in `report/team/bonus_report.md`
- [X] T027 [P] [US4] Fill Member 4 info in `TEAM.md` (`## Thành viên` & `## Bảng đóng góp`) and create personal report `report/team/2A202603800_HoangDucAn.md`
- [X] T028 [US4] Verify `python -m pytest -q` (183 passed) and `python -m pytest -q tests/test_bonus_grader_audit.py` (19 passed), mark Phase 6 `[X]` in `specs/001-logix-claim-agents/tasks.md`, and push commits `dd3ae22` + `23f7734` to `main` *(note: `23f7734` also updated `check_submission.py` regex `B[1-6]` → `B[1-7]`; see submission audit)*

**Handoff Gate 4 → 5**: `src/reports/crash.json` đạt `20/20`, `test_must_pass_audit.py` và `test_bonus_grader_audit.py` chạy xanh ổn định trên `main`.

---

## Phase 7: User Story 5 — CP5 Benchmark, ADR, Research Card, Reports & Submission Gate (Priority: P5)

**Owner**: **Người 5 — Nguyễn Thiên Bảo** (`2A202603861`, `Limdim1604`). Lấy `main` tại `23f7734`, thực hiện Phase 7 trên `nguyenthienbao` (`5c027d8`, `eb5837c`, `a39c589`), và **PR #6 đã duyệt & merge vào `main` tại `aa24aca`**.

**Goal**: Chạy benchmark chính thức 4 shape × 14 claim × 5 seed, tự kiểm `student_drop/` (nếu có), hoàn thiện toàn bộ báo cáo nhóm (`decision_adr.md`, `research_card.md`, `group_report.md`, `bonus_report.md`), bổ sung test invariant benchmark, và đưa `python -m lab8.check_submission` về `0 FAIL`.  
**Independent Test**: `python -m lab8.check_submission` ra `0 FAIL`, `python -m pytest -q` và `python -m pytest -q -m student -o addopts=` xanh, commit hash trong `decision_adr.md` khớp `git log`.

### Benchmark & Regression Tests for User Story 5

- [X] T029 [P] [US5] Verify the public trial grid, benchmark metric formulas, trace artifacts, and the R2 ablation in `src/tests/test_benchmark_invariants.py`.
- [X] T030 [US5] Generate reports with `python -m lab8.crash_test --count 20 --out reports/crash.json` and `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`. Crash safety is 20/20, and the benchmark covers 280 trials.
- [ ] T031 [US5] Optional hidden self-check. `src/student_drop/` was not distributed in the workspace; skip until/unless `student_drop/` is handed out at CP5.

### Reports & Final Submission Gate for User Story 5

- [X] T032 [US5] Run the R2 ablation using `lab8.benchmark` and `--extra-shape` (`src/bonus/swarm_order_only.py`). Record its method, run IDs and results in `report/team/research_card.md` and `src/reports/research_r2.json`.
- [X] T033 [US5] Finalize `report/team/bonus_report.md` (`# Bonus report: B7`) with the audit command, fixture results and limitations.
- [X] T034 [US5] Complete `report/team/group_report.md` using the generated benchmark and crash reports.
- [X] T035 [P] [US5] Update Member 5 and the five-person contribution table in `TEAM.md`. Add `report/team/2A202603861_NguyenThienBao.md`.
- [X] T036 [US5] Record evidence commit `5c027d8` in `decision_adr.md`, `TEAM.md`, and `group_report.md`. Fill the ADR's required shape, run ID, metrics and safety fields.
- [X] T037 [US5] Verify Phase 7 on `nguyenthienbao` and merge PR #6 into `main` at `aa24aca`. Host 192 passed, student matrix 248 passed, Bonus B7 19 passed, submission check `0 FAIL`.

**Handoff & Final Checklist (Lead `duyhale95`):**

- [X] Pull `main` (`aa24aca`), kiểm tra toàn bộ commit/PR (#1, #3, #4, #5, #6 + push trực tiếp của Hoàng Đức An), tái lập byte-for-byte 4 file JSON (`crash.json`, `benchmark.json`, `research_r2.json`, `bonus_grader_audit.json`), kiểm tra 192 host tests + 248 student tests + 19 bonus tests + `check_submission` (`0 FAIL`).
- [ ] Xác nhận quy ước tên repo (`K5-L3B-Day8-369-From-Workflows-to-Agents` vs `K5-L3A-DAY08-369-FromWorkflowsToAgents` theo coach) và quyết định giữ hay revert `src/lab8/check_submission.py` (xem cảnh báo tampered của grader ẩn).
- [ ] Cả 5 thành viên tự nộp cùng link repo nhóm trên LMS bằng tài khoản cá nhân trước deadline.

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
                         Phase 7 [US5] Người 5: benchmark.json + ADR + research_card + group_report + check_submission ──► PR to main
```

### Critical Rules Across All 5 Turns

1. **Always pull `main` first**: Do not start Phase `N+1` until Phase `N` is pushed and verified on `main`.
2. **Every person MUST own at least 1 commit + 1 test in `src/tests/` + 1 `report/team/<MSSV>_<HoTen>.md` + 1 row in `TEAM.md`** (Rubric C8 & `check_submission`).
3. **Never touch protected files**: `src/lab8/metrics.py`, `durability.py`, `policy.py`, `src/config/*.yaml`, `src/data/*`, `src/grader_audit/grader_*.py`, `src/grader_audit/fixtures/*.json`.
4. **Never commit runtime junk**: `src/.venv/`, `src/traces/`, `*.sqlite`, `src/student_drop/`, `src/reports/hidden_grade.json`, `.env`.
5. **Keep `report/team/MSSV_HoTen.md` untouched** as the template for subsequent members.
