# Team

## Thông tin nhóm

- Tên nhóm: 369
- Lớp: L3B
- Repo nhóm hiện tại: `K5-L3B-Day8-369-From-Workflows-to-Agents`. Tên nộp theo mẫu trong [SUBMISSION.md](SUBMISSION.md) là `K5-L3A-DAY08-369-FromWorkflowsToAgents`. Nhóm trưởng xác nhận với coach nếu lớp có quy ước riêng và gửi cho cả nhóm URL cuối cùng sau khi duyệt PR.
- URL repo, nhánh nộp, commit chốt: `https://github.com/duyhale95/K5-L3B-Day8-369-From-Workflows-to-Agents` · nhánh nộp `main` sau khi duyệt PR · commit chốt code và số liệu `5c027d8` trên `nguyenthienbao`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Hà Lê Duy | 2A202603851 | haleduy2005@gmail.com | duyhale95 | Trưởng nhóm, chia việc tuần tự (Spec Kit), triển khai Shape A (`workflow`) & unit test |
|   2 | Nguyễn Lê Trọng Mạnh | 2A202603857 | | Tiberu2611 | Triển khai Shape B (`single` ReAct agent) & unit test |
|   3 | Nguyễn Hoàng Gia An | 2A202603799 | 26ai.annhg@vinuni.edu.vn | AnK17-UIT | Triển khai Shape C (`orchestrator` + sanitized `handoff.v1`) & unit test |
|   4 | Hoàng Đức An | 2A202603800 | anduchoang2701@gmail.com | katogithub2701 | Kiểm toán Must-Pass (CP4), `crash.json` 20/20 & Bonus B7 (`grader_audit`) |
|   5 | Nguyễn Thiên Bảo | 2A202603861 | 26ai.baont5@vinuni.edu.vn | Limdim1604 | Benchmark CP5, ablation R2, ADR, báo cáo nhóm và kiểm tra bài nộp |

## Kế hoạch chia việc tuần tự (5 thành viên — Spec Kit)

Chi tiết checklist từng bước và file sở hữu nằm tại [`specs/001-logix-claim-agents/tasks.md`](specs/001-logix-claim-agents/tasks.md) (theo [constitution](.specify/memory/constitution.md) và [plan](specs/001-logix-claim-agents/plan.md)). **Quy tắc:** Người sau chỉ bắt đầu khi người trước đã push commit xanh lên `main`; trước khi code phải `git pull origin main`.

| Thứ tự | Người phụ trách | Phase / User Story | Việc chính phải làm | Test & bằng chứng bắt buộc | Trạng thái |
| --: | --- | --- | --- | --- | --- |
| 1 | **Hà Lê Duy (`2A202603851`)** | Phase 1–3 · `[US1]` | Init Spec Kit, chia việc tuần tự, kiểm tra `smoke` + host gate, code `src/lab8/shapes/workflow.py` (CP2+CP3), báo cáo cá nhân `2A202603851_HaLeDuy.md` | `src/tests/test_workflow_shape.py`, `pytest -q` xanh, `workflow` 62/62 student pass | **Đã xong** |
| 2 | **Nguyễn Lê Trọng Mạnh (`2A202603857`)** | Phase 4 · `[US2]` | Pull `main`, code `src/lab8/shapes/single.py` (`run_react` max 8 bước, chỉ read tool, không tin prose hơn DB, truyền full quote + `crash_at`), báo cáo cá nhân | `src/tests/test_single_shape.py`, `pytest -q` xanh, `single` 62/62 student pass | **Đã merge vào `main`** (`3406566`) |
| 3 | **Nguyễn Hoàng Gia An (`2A202603799`)** | Phase 5 · `[US3]` | Pull `main`, code `src/lab8/shapes/orchestrator.py` (`make_handoff`, `run_readonly_investigators`, trace handoff đã sanitize, truyền full quote + `crash_at`), báo cáo cá nhân | `src/tests/test_orchestrator_shape.py`, `pytest -q` xanh, toàn ma trận student 248/248 pass | **Đã merge vào `main`** (`ade768d`, `0bb0e08`) |
| 4 | **Hoàng Đức An (`2A202603800`)** | Phase 6 · `[US4]` | Pull `main`, audit 3 điều kiện must-pass trên cả 3 shape, tạo `src/reports/crash.json` (`20/20`), làm code/test **Bonus B7** (`grader_audit`), nháp số liệu `report/team/bonus_report.md`, báo cáo cá nhân | `src/tests/test_must_pass_audit.py`, `src/tests/test_bonus_grader_audit.py`, `crash.json` 20/20 | **Đã xong** |
| 5 | **Nguyễn Thiên Bảo (`2A202603861`)** | Phase 7 · `[US5]` | Chạy benchmark và crash suite, thực hiện ablation R2, chốt ADR, báo cáo nhóm, bonus B7 và báo cáo cá nhân | `src/tests/test_benchmark_invariants.py`, `src/reports/benchmark.json`, `src/reports/research_r2.json`, `check_submission` | Hoàn thành trên `nguyenthienbao`, chờ PR |

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa. Thành viên 2–5 thêm dòng của mình ngay bên dưới khi hoàn thành lượt trên `main`.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Hà Lê Duy (2A202603851) | Trưởng nhóm, Spec Kit & Shape A (`workflow`) | `c4e7175` | `src/tests/test_workflow_shape.py` (21 test unit/contract/crash); `tests/test_public_matrix.py` (`-k workflow` 62/62) |
| Nguyễn Lê Trọng Mạnh (2A202603857) | Shape B (`single` ReAct agent) | `47e48cf` | `src/tests/test_single_shape.py` (34 test unit/contract/crash); `tests/test_public_matrix.py` (`single` 62/62) |
| Nguyễn Hoàng Gia An (2A202603799) | Shape C (`orchestrator` + `handoff.v1`) | `0d6ac71` | `src/tests/test_orchestrator_shape.py` (12 test) |
| Hoàng Đức An (2A202603800) | Must-Pass Audit (CP4), `crash.json` 20/20 & Bonus B7 (`grader_audit`) | `dd3ae22` | `src/tests/test_must_pass_audit.py` (43 test); `src/tests/test_bonus_grader_audit.py` (19 test) |
| Nguyễn Thiên Bảo (2A202603861) | Benchmark CP5, ablation R2, ADR và chốt báo cáo | `5c027d8` | `src/tests/test_benchmark_invariants.py` (9 test) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/team/` theo dạng `report/team/MSSV_HoTen.md` (copy từ file mẫu `report/team/MSSV_HoTen.md`, giữ nguyên file mẫu):

- Người 1: [`report/team/2A202603851_HaLeDuy.md`](report/team/2A202603851_HaLeDuy.md)
- Người 2: [`report/team/2A202603857_NguyenLeTrongManh.md`](report/team/2A202603857_NguyenLeTrongManh.md)
- Người 3: [`report/team/2A202603799_NguyenHoangGiaAn.md`](report/team/2A202603799_NguyenHoangGiaAn.md)
- Người 4: [`report/team/2A202603800_HoangDucAn.md`](report/team/2A202603800_HoangDucAn.md)
- Người 5: [`report/team/2A202603861_NguyenThienBao.md`](report/team/2A202603861_NguyenThienBao.md)
