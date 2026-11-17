# Báo cáo cá nhân — 2A202603799_NguyenHoangGiaAn

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hoàng Gia An
- MSSV: 2A202603799
- Email: 26ai.annhg@vinuni.edu.vn
- GitHub: AnK17-UIT

## 2. Phần việc phụ trách

Thành viên 3 của nhóm 369, phụ trách Phase 5 / `[US3]` với Shape C (`orchestrator`), handoff đã lọc và test hợp đồng.

## 3. Đóng góp cụ thể

- Orchestrator tạo `handoff.v1` với mã claim, phạm vi chủ đơn và ba tool chỉ đọc. Investigator tra cứu đơn hàng, chính sách hiện hành và lịch sử hoàn tiền theo phạm vi này. Các facts được lấy từ DB qua tool và ticket nằm ngoài payload bàn giao. [Mã Shape C](../../src/lab8/shapes/orchestrator.py)
- Orchestrator tính quote từ dữ liệu đơn hàng mà investigator trả về. `durability.issue_refund` xác minh phê duyệt, áp hạn mức theo đơn và xử lý retry dựa trên quote đầy đủ. Trace ghi handoff đã lọc, tóm tắt kết quả tra cứu và lần thử ghi trước khi vào host để truy vết được cả ba cửa sổ crash.
- Thêm 12 test cho allowlist, tool chỉ đọc, trace khi từ chối hoặc crash, retry idempotent và quote đầy đủ ở T13/T14. [Bộ test Shape C](../../src/tests/test_orchestrator_shape.py)

## 4. Bằng chứng

Commit kỹ thuật [`0d6ac71`](https://github.com/duyhale95/K5-L3B-Day8-369-From-Workflows-to-Agents/commit/0d6ac710724fd252ed5376baeb04f2bafa914eb2).

Kết quả chạy từ `src/` bằng Python 3.12.3 trên Linux.

| Lệnh | Kết quả |
| --- | --- |
| `python -m lab8.smoke` | PASS |
| `python -m pytest -q tests/test_orchestrator_shape.py` | 12 passed |
| `python -m pytest -q` | 121 passed |
| `python -m pytest -q -m student -o addopts=` | 248 passed |

Run `R-orchestrator-C-014-s11` từ CLI ghi một khoản hoàn 120.000 VND trên quote 150.000 VND, sau khi host tính khoản đã hoàn 30.000 VND. Lệnh tái hiện trên một DB mới là `python -m lab8.run --shape orchestrator --claim-id C-014 --seed 11 --db reports/orchestrator-t14.sqlite`.

## 5. Công cụ AI đã dùng

Codex hỗ trợ viết code, test và báo cáo. Các lệnh ở mục 4 do Codex trực tiếp chạy và kết quả được đối chiếu với hành vi mong đợi trong kế hoạch Phase 5. [Quy định sử dụng AI](../../RULES.md)

## 6. Tự đánh giá

Phần việc có bằng chứng kiểm thử cho ranh giới dữ liệu, phân quyền tool, trace và phép tính hoàn tiền khi đã có khoản hoàn trước. Kết quả trên bộ ca công khai phản ánh phạm vi xác minh của Phase 5. Nhận xét tự đánh giá cá nhân sẽ do thành viên phụ trách bổ sung sau khi tự rà soát.
