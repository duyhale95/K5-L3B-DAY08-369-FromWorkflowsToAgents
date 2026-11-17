# Team

## Thông tin nhóm

- Tên nhóm: 369
- Lớp: L3B *(lưu ý mẫu repo nộp quy ước `K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents`; repo hiện tại: `K5-L3B-Day8-369-FromWorkflows-to-Agents`)*
- Repo nhóm: `K5-L3B-Day8-369-FromWorkflows-to-Agents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: `https://github.com/duyhale95/K5-L3B-Day8-369-From-Workflows-to-Agents` · nhánh `main` · commit chốt: *(Người 5 điền sau khi chạy benchmark & report cuối)*

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Hà Lê Duy | 2A202603851 | haleduy2005@gmail.com | duyhale95 | Trưởng nhóm, chia việc tuần tự (Spec Kit), triển khai Shape A (`workflow`) & unit test |
|   2 | Nguyễn Lê Trọng Mạnh | 2A202603857 | | Tiberu2611 | Triển khai Shape B (`single` ReAct agent) & unit test |
|   3 | *(Thành viên 3 — điền khi nhận lượt)* | *(MSSV)* | | *(GitHub)* | Triển khai Shape C (`orchestrator` + sanitized `handoff.v1`) & unit test |
|   4 | *(Thành viên 4 — điền khi nhận lượt)* | *(MSSV)* | | *(GitHub)* | Kiểm toán Must-Pass (CP4), `crash.json` 20/20 & Bonus B7 (`grader_audit`) |
|   5 | *(Thành viên 5 — điền khi nhận lượt)* | *(MSSV)* | | *(GitHub)* | Benchmark 4 shape (CP5), Research Card ablation, ADR, Group Report & `check_submission` |

## Kế hoạch chia việc tuần tự (5 thành viên — Spec Kit)

Chi tiết checklist từng bước và file sở hữu nằm tại [`specs/001-logix-claim-agents/tasks.md`](specs/001-logix-claim-agents/tasks.md) (theo [constitution](.specify/memory/constitution.md) và [plan](specs/001-logix-claim-agents/plan.md)). **Quy tắc:** Người sau chỉ bắt đầu khi người trước đã push commit xanh lên `main`; trước khi code phải `git pull origin main`.

| Thứ tự | Người phụ trách | Phase / User Story | Việc chính phải làm | Test & bằng chứng bắt buộc | Trạng thái |
| --: | --- | --- | --- | --- | --- |
| 1 | **Hà Lê Duy (`2A202603851`)** | Phase 1–3 · `[US1]` | Init Spec Kit, chia việc tuần tự, kiểm tra `smoke` + host gate, code `src/lab8/shapes/workflow.py` (CP2+CP3), báo cáo cá nhân `2A202603851_HaLeDuy.md` | `src/tests/test_workflow_shape.py`, `pytest -q` xanh, `workflow` 62/62 student pass | **Đã xong** |
| 2 | **Nguyễn Lê Trọng Mạnh (`2A202603857`)** | Phase 4 · `[US2]` | Pull `main`, code `src/lab8/shapes/single.py` (`run_react` max 8 bước, chỉ read tool, không tin prose hơn DB, truyền full quote + `crash_at`), báo cáo cá nhân | `src/tests/test_single_shape.py`, `pytest -q` xanh, `single` 62/62 student pass | Chờ lượt 2 |
| 3 | **Thành viên 3** | Phase 5 · `[US3]` | Pull `main`, code `src/lab8/shapes/orchestrator.py` (`make_handoff`, `run_readonly_investigators`, trace handoff đã sanitize, truyền full quote + `crash_at`), báo cáo cá nhân | `src/tests/test_orchestrator_shape.py`, `pytest -q` xanh, toàn ma trận student 248/248 pass | Chờ lượt 3 |
| 4 | **Thành viên 4** | Phase 6 · `[US4]` | Pull `main`, audit 3 điều kiện must-pass trên cả 3 shape, tạo `src/reports/crash.json` (`20/20`), làm code/test **Bonus B7** (`grader_audit`), nháp số liệu `report/team/bonus_report.md`, báo cáo cá nhân | `src/tests/test_must_pass_audit.py`, `src/tests/test_bonus_grader_audit.py`, `crash.json` 20/20 | Chờ lượt 4 |
| 5 | **Thành viên 5** | Phase 7 · `[US5]` | Pull `main`, chạy `benchmark.json` (4 shape × 14 claim × 5 seed), tự kiểm `student_drop/` (nếu có), hoàn thiện `decision_adr.md`, `research_card.md`, `group_report.md`, `bonus_report.md`, chốt commit hash & `check_submission` `0 FAIL`, báo cáo cá nhân | `src/tests/test_benchmark_invariants.py`, `src/reports/benchmark.json`, `check_submission` `0 FAIL` | Chờ lượt 5 |

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa. Thành viên 2–5 thêm dòng của mình ngay bên dưới khi hoàn thành lượt trên `main`.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Hà Lê Duy (2A202603851) | Trưởng nhóm, Spec Kit & Shape A (`workflow`) | `c4e7175` | `src/tests/test_workflow_shape.py` (21 test unit/contract/crash); `tests/test_public_matrix.py` (`-k workflow` 62/62) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/team/` theo dạng `report/team/MSSV_HoTen.md` (copy từ file mẫu `report/team/MSSV_HoTen.md`, giữ nguyên file mẫu):

- Người 1: [`report/team/2A202603851_HaLeDuy.md`](report/team/2A202603851_HaLeDuy.md)
- Người 2: *(thêm link `report/team/<MSSV_2>_<HoTen_2>.md` khi hoàn thành lượt 2)*
- Người 3: *(thêm link `report/team/<MSSV_3>_<HoTen_3>.md` khi hoàn thành lượt 3)*
- Người 4: *(thêm link `report/team/<MSSV_4>_<HoTen_4>.md` khi hoàn thành lượt 4)*
- Người 5: *(thêm link `report/team/<MSSV_5>_<HoTen_5>.md` khi hoàn thành lượt 5)*
