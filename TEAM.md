# Team

## Thông tin nhóm

- Tên nhóm: 369
- Lớp: L3B
- Repo nhóm: `K5-L3B-Day8-369-From-Workflows-to-Agents` *(đã xác nhận đúng tên repo nộp của nhóm)*.
- URL repo, nhánh nộp, commit chốt: `https://github.com/duyhale95/K5-L3B-Day8-369-From-Workflows-to-Agents` · nhánh nộp: `main` · commit chốt code và số liệu: `5c027d8` (đã merge vào `main` qua PR #6 tại `aa24aca`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Hà Lê Duy | 2A202603851 | 26ai.duyhl2@vinuni.edu.vn | duyhale95 | Trưởng nhóm, chia việc tuần tự (Spec Kit), triển khai Shape A (`workflow`), rà soát & merge PR |
|   2 | Nguyễn Lê Trọng Mạnh | 2A202603857 | 26ai.manhnlt@vinuni.edu.vn | Tiberu2611 | Triển khai Shape B (`single` ReAct agent) & unit test |
|   3 | Nguyễn Hoàng Gia An | 2A202603799 | 26ai.annhg@vinuni.edu.vn | AnK17-UIT | Triển khai Shape C (`orchestrator` + sanitized `handoff.v1`) & unit test |
|   4 | Hoàng Đức An | 2A202603800 | anduchoang2701@gmail.com | katogithub2701 | Kiểm toán Must-Pass (CP4), `crash.json` 20/20 & Bonus B7 (`grader_audit`) |
|   5 | Nguyễn Thiên Bảo | 2A202603861 | 26ai.baont5@vinuni.edu.vn | Limdim1604 | Benchmark CP5, ablation R2, ADR, báo cáo nhóm và kiểm tra bài nộp |

## Kế hoạch chia việc tuần tự (5 thành viên — Spec Kit)

Chi tiết checklist từng bước và file sở hữu nằm tại [`specs/001-logix-claim-agents/tasks.md`](specs/001-logix-claim-agents/tasks.md) (theo [constitution](.specify/memory/constitution.md) và [plan](specs/001-logix-claim-agents/plan.md)).

| Thứ tự | Người phụ trách | Phase / User Story | Việc chính đã thực hiện (đối chiếu lịch sử commit) | Test & bằng chứng bắt buộc | Trạng thái & Xác nhận PR / `main` |
| --: | --- | --- | --- | --- | --- |
| 1 | **Hà Lê Duy (`2A202603851`)** | Phase 1–3 · `[US1]` | Init Spec Kit, chia việc tuần tự, kiểm tra `smoke` + host gate, code `src/lab8/shapes/workflow.py` (CP2+CP3), báo cáo cá nhân `2A202603851_HaLeDuy.md`, duyệt PR & kiểm tra tổng thể | `src/tests/test_workflow_shape.py` (21 test), `pytest -q` xanh, `workflow` 62/62 student pass | **Đã xong trên `main`** (`c4e7175`, `09e21f6`) |
| 2 | **Nguyễn Lê Trọng Mạnh (`2A202603857`)** | Phase 4 · `[US2]` | Pull `main`, code `src/lab8/shapes/single.py` (`run_react` max 8 bước, `_readonly`, host validation, full quote + `crash_at`), báo cáo cá nhân `2A202603857_NguyenLeTrongManh.md` | `src/tests/test_single_shape.py` (34 test), `pytest -q` xanh, `single` 62/62 student pass | **Đã xác nhận & merge vào `main`** (PR #1 `3406566`; commits `47e48cf`, `72f91d9`) |
| 3 | **Nguyễn Hoàng Gia An (`2A202603799`)** | Phase 5 · `[US3]` | Pull `main`, code `src/lab8/shapes/orchestrator.py` (`make_handoff`, `run_readonly_investigators`, trace handoff đã sanitize, full quote + `crash_at`), báo cáo cá nhân `2A202603799_NguyenHoangGiaAn.md` | `src/tests/test_orchestrator_shape.py` (12 test), `pytest -q` xanh, ma trận student 248/248 pass | **Đã xác nhận & merge vào `main`** (PR #3 `ade768d`, PR #4 & #5 `0bb0e08`; commits `0d6ac71`, `8038518`, `45bf255`, `f42562e`) |
| 4 | **Hoàng Đức An (`2A202603800`)** | Phase 6 · `[US4]` | Audit 3 điều kiện must-pass trên cả 3 shape, tạo `src/reports/crash.json` (`20/20`), Bonus B7 (`src/bonus/grader_audit.py`, `bonus_grader_audit.json`), nháp `report/team/bonus_report.md`, báo cáo cá nhân `2A202603800_HoangDucAn.md` | `src/tests/test_must_pass_audit.py` (43 test), `src/tests/test_bonus_grader_audit.py` (19 test), `crash.json` 20/20 | **Đã kiểm tra trên `main`** (push trực tiếp `dd3ae22`, `23f7734`, không qua PR; lưu ý `23f7734` sửa regex `B[1-7]` trong `check_submission.py`) |
| 5 | **Nguyễn Thiên Bảo (`2A202603861`)** | Phase 7 · `[US5]` | Chạy `benchmark.json`, biến thể `src/bonus/swarm_order_only.py` & ablation R2 (`research_r2.json`), hoàn thiện `decision_adr.md`, `research_card.md`, `group_report.md`, `bonus_report.md`, `2A202603861_NguyenThienBao.md` | `src/tests/test_benchmark_invariants.py` (9 test), `src/reports/benchmark.json`, `check_submission` `0 FAIL` | **Đã xác nhận & merge vào `main`** (PR #6 `aa24aca`; commits `5c027d8`, `eb5837c`, `a39c589`, `5b81fd1`) |

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Hà Lê Duy (2A202603851) | Trưởng nhóm, Spec Kit & Shape A (`workflow`) | `c4e7175` | `src/tests/test_workflow_shape.py` (21 test unit/contract/crash); `tests/test_public_matrix.py` (`-k workflow` 62/62) |
| Nguyễn Lê Trọng Mạnh (2A202603857) | Shape B (`single` ReAct agent) | `47e48cf` (PR #1 `3406566`) | `src/tests/test_single_shape.py` (34 test unit/contract/crash); `tests/test_public_matrix.py` (`single` 62/62) |
| Nguyễn Hoàng Gia An (2A202603799) | Shape C (`orchestrator` + `handoff.v1`) | `0d6ac71` (PR #3 `ade768d`) | `src/tests/test_orchestrator_shape.py` (12 test); `tests/test_public_matrix.py` (`orchestrator` 62/62) |
| Hoàng Đức An (2A202603800) | Must-Pass Audit (CP4), `crash.json` 20/20 & Bonus B7 (`grader_audit`) | `dd3ae22` | `src/tests/test_must_pass_audit.py` (43 test); `src/tests/test_bonus_grader_audit.py` (19 test) |
| Nguyễn Thiên Bảo (2A202603861) | Benchmark CP5, ablation R2, ADR và chốt báo cáo | `5c027d8` (PR #6 `aa24aca`) | `src/tests/test_benchmark_invariants.py` (9 test) |

## Xác nhận PR & kiểm duyệt trên `main`

| PR / Luồng | Người tạo | Nhánh nguồn → đích | Commit merge / trên `main` | Trạng thái xác nhận (Trưởng nhóm `duyhale95`) |
| --- | --- | --- | --- | --- |
| Setup & Phase 1–3 | `duyhale95` (Hà Lê Duy) | Push trực tiếp `main` | `c4e7175`, `09e21f6` | Đã hoàn thành Spec Kit + Shape A (`workflow`) + `test_workflow_shape.py` |
| **PR #1** | `Tiberu2611` (Nguyễn Lê Trọng Mạnh) | `NguyenLeTrongManh` → `main` | Merged `3406566` (`47e48cf`, `72f91d9`) | Đã duyệt & merge; Shape B (`single`) pass 62/62 student + 34 unit test |
| **PR #2** | `Tiberu2611` (Nguyễn Lê Trọng Mạnh) | `NguyenLeTrongManh` → `main` | Closed (không merge) | Đã đóng vì gộp xong ở PR #1 |
| **PR #3** | `AnK17-UIT` (Nguyễn Hoàng Gia An) | `fix/an-nguyen-work-orchestrator` → `main` | Merged `ade768d` (`0d6ac71`, `8038518`) | Đã duyệt & merge; Shape C (`orchestrator`) pass 62/62 student + 12 unit test |
| **PR #4 & PR #5** | `AnK17-UIT` (Nguyễn Hoàng Gia An) | `fix/an-nguyen-work-personal-report` / `fix/an-nguyen-work-orchestrator` → `main` | Merged `0bb0e08` (`45bf255`, `f42562e`) | Đã duyệt & merge; hoàn thiện báo cáo cá nhân Thành viên 3 |
| Audit & Bonus B7 | `katogithub2701` (Hoàng Đức An) | Push trực tiếp `main` | `dd3ae22`, `23f7734` | Đã kiểm chứng trên `main`: 43 test must-pass + 19 test B7 + `crash.json` 20/20 *(lưu ý `23f7734` sửa `check_submission.py`)* |
| **PR #6** | `Limdim1604` (Nguyễn Thiên Bảo) | `nguyenthienbao` → `main` | Merged `aa24aca` (`5c027d8`, `eb5837c`, `a39c589`) + `5b81fd1` | Đã duyệt, tái lập byte-for-byte 4 file JSON trong `src/reports/` & merge vào `main` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/team/` theo dạng `report/team/MSSV_HoTen.md` (copy từ file mẫu `report/team/MSSV_HoTen.md`, giữ nguyên file mẫu):

- Người 1: [`report/team/2A202603851_HaLeDuy.md`](report/team/2A202603851_HaLeDuy.md)
- Người 2: [`report/team/2A202603857_NguyenLeTrongManh.md`](report/team/2A202603857_NguyenLeTrongManh.md)
- Người 3: [`report/team/2A202603799_NguyenHoangGiaAn.md`](report/team/2A202603799_NguyenHoangGiaAn.md)
- Người 4: [`report/team/2A202603800_HoangDucAn.md`](report/team/2A202603800_HoangDucAn.md)
- Người 5: [`report/team/2A202603861_NguyenThienBao.md`](report/team/2A202603861_NguyenThienBao.md)
