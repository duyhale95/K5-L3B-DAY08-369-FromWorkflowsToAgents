# Báo cáo cá nhân — 2A202603857_NguyenLeTrongManh

## 1. Thông tin thành viên

- Họ tên: Nguyễn Lê Trọng Mạnh
- MSSV: 2A202603857
- Email: 26ai.manhnlt@vinuni.edu.vn
- GitHub: Tiberu2611

## 2. Phần việc phụ trách

- **Người 2 — Phase 4 / `[US2]` (T012–T016):** triển khai Shape B (`src/lab8/shapes/single.py`, một ReAct agent) và bộ test `src/tests/test_single_shape.py`, nối tiếp Shape A của Người 1 trên `main`.

## 3. Đóng góp cụ thể

- **Shape B (`src/lab8/shapes/single.py`, commit `47e48cf`):**
  - Agent chạy trong `lab8.runtime.run_react(..., max_steps=8)`. Một claim đầy đủ dùng 6 lượt `decide`: `get_claim_view` → `lookup_order` → `lookup_policy` → `lookup_refund_history` → `compute_compensation` → `final`.
  - Mỗi lượt `decide` gọi `MockLLM` đúng một lần (`purpose="react"`) để `Budget` phản ánh chi phí thật của vòng lặp, so sánh được với các shape khác.
  - `decide` chỉ chọn read tool. Một lớp chặn trong code (`_readonly`) đối chiếu tên tool với `READONLY_TOOLS` trước khi vòng lặp chạy tool; agent đòi `issue_refund` thì run kết thúc `failed / tool_rejected`, không có dòng ledger nào.
  - Nội dung ticket không được dùng làm bằng chứng: không lưu vào bộ nhớ agent, không đưa vào prompt, không ghi vào trace. Số ngày trễ, hư hỏng, phí ship lấy từ dòng đơn hàng; clause lấy từ policy hiện hành. Vì vậy ticket khai khống ngày trễ (`C-002`), dẫn clause cũ `SHIP-LATE-OLD` (`C-006`) hay prompt injection (`C-009`) đều không đổi kết quả.
  - Sau vòng lặp, host tự tính lại quote bằng `compute_compensation` trên dòng đơn hàng đã quan sát. Con số agent đề xuất phải khớp, lệch thì `failed / quote_mismatch` và không chi tiền.
  - Host là nơi duy nhất gọi `durability.issue_refund`, truyền **quote đầy đủ** và `crash_at`. Trần theo đơn (T13, T14) và ràng buộc approval (T07) do host xử lý.
  - Không bắt `InjectedCrash`: ghi sự kiện `crash`, flush trace, rồi để exception thoát ra.
  - Mọi nhánh trả về đi qua `lab8.shapes.common.finish(...)` nên luôn có trace đúng Trace Contract v1.
- **Test `src/tests/test_single_shape.py` (34 test):**
  - Ticket nói dối / clause cũ / injection trên 5 seed (`C-002`, `C-006`, `C-009`).
  - Sửa ticket `C-001` thành "trễ 99 ngày" kèm lệnh injection: status, số tiền, số model call, tool call và chi phí giống hệt bản gốc.
  - `decide` chỉ phát ra read tool và kết thúc trong 8 bước trên 7 claim; số model call bằng số lượt `decide`.
  - Agent đòi write tool → `tool_rejected`; agent lặp vô hạn → dừng đúng 8 bước với `step_cap`; agent thổi phồng số tiền → `quote_mismatch`. Cả ba đều không tạo refund.
  - `Budget` tất định theo seed (6 model call + 6 tool call cho `C-001`; 2 + 1 cho nhánh `needs_info`).
  - Trace sạch canary/PII ở nhánh `failed`, `needs_info`, `escalated`, `resolved`.
  - Full quote qua host cho `C-007`, `C-013`, `C-014`.
  - Ba điểm crash: trace đã flush trước khi crash, chạy lại chỉ có một refund 35000 và một audit.

## 4. Bằng chứng

- **Commit chính:** `47e48cf` — `src/lab8/shapes/single.py`, `src/tests/test_single_shape.py`, `TEAM.md`.
- **Kết quả chạy trong `src/` (Python 3.14.6 của conda base, pytest 9.0.3, PyYAML 6.0.3):**
  - `python -m lab8.smoke` → `lab8.smoke pass`
  - `python -m pytest -q tests/test_single_shape.py` → `34 passed`
  - `python -m pytest -q` → `109 passed, 248 deselected` (75 của lượt trước + 34 test mới)
  - `python -m pytest -q -m student -o addopts=` → `186 passed, 62 failed`; cả 62 lỗi thuộc `orchestrator` (chưa tới lượt Người 3). `workflow`, `single`, `swarm` mỗi shape đạt 62/62.
- **Lưu ý về lệnh trong `tasks.md`:** `-k "workflow or single"` không lọc được theo shape, vì chuỗi `single` trùng tên hàm `test_public_single_run_cases` nên chọn luôn test của `orchestrator` và `swarm`. Con số `124 passed` vì thế được kiểm bằng cách chạy cả ma trận rồi đếm lỗi theo shape.
- **Lưu ý về môi trường:** máy không có Python 3.11–3.13 (khoảng phiên bản `requirements.txt` ghi là đã thử), nên kết quả trên chạy bằng Python 3.14.6 và pytest 9, ngoài khoảng `pytest<9` của `requirements.txt`.

## 5. Công cụ AI đã dùng

- **Công cụ:** Claude Code.
- **Mục đích sử dụng:** đọc `tasks.md`, `quickstart.md` và code starter (`runtime.py`, `tools.py`, `durability`, Shape A), viết `single.py` và `test_single_shape.py`, chạy các lệnh kiểm chứng.
- **Cách tự kiểm tra kết quả:** chạy `lab8.smoke`, `pytest -q`, ma trận student và `lab8.check_submission` trong `src/`; đếm lỗi ma trận theo shape để xác nhận `single` đạt 62/62.

## 6. Tự đánh giá

- Shape B đạt 62/62 test student, cổng host xanh, và ba đường tấn công từ phía agent (write tool, lặp vô hạn, thổi phồng số tiền) đều bị chặn trong code trước khi tới ledger.
- Chưa làm: chưa chạy lại trên Python 3.11–3.13.
