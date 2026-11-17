# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 5c027d8
- Run id dẫn chứng: R-workflow-C-002-s55, R-workflow-C-014-s11 (src/reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: 70/70 = 1,000 / 14/14 = 1,000 / 1,000–1,000 / 0
- Cost per success (mô phỏng, VND): 28,94 (2.026,00 / 70)
- Crash safety: 20/20 (src/reports/crash.json), kèm kiểm thử retry và crash của workflow ở T11/T12 và test_must_pass_audit.py
- Secret leak / approval bypass: 0 / 0 phát hiện cho workflow trong public và audit CP4. Chưa có số liệu hidden.

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Trên cùng 14 claim, 5 seed, MockLLM và bảng giá, `workflow`, `single` và `orchestrator` đều đúng 70/70 lượt, với phương sai theo seed bằng 0. `workflow` dùng chuỗi bước cố định và có chi phí thấp nhất, 28,94 VND mô phỏng mỗi lần thành công, so với 54,10 của `single` và 55,71 của `orchestrator`. Tại T14, workflow truyền quote đầy đủ 150.000 VND, host trừ 30.000 VND đã hoàn và ghi thêm 120.000 VND.

## Có đáng đổi lấy multi-agent không

Ở bộ public, `swarm` tốn 49,57 VND mô phỏng mỗi lần thành công, đúng 69/70 lượt và có phương sai 0,000816. Lượt `R-swarm-C-002-s55` lấy 5 ngày trong ticket thay cho 2 ngày trong đơn. Có thể xem lại quyết định nếu bộ có nhãn lớn hơn chứa các claim cần nhiều bước điều tra độc lập, và một kiến trúc agent vượt workflow về pass rate hoặc pass^5 đủ để bù thêm chi phí trong khi vẫn qua các cổng an toàn.

## Trace và bằng chứng

Workflow ghi trạng thái đọc claim, dữ kiện đơn đã lọc, quote, quyết định, kết quả gọi host và điểm crash nếu có. Trace loại ticket thô, `parent_secret`, `raw_headers`, điện thoại, địa chỉ, tên hàng và ghi chú nội bộ để giữ phạm vi dữ liệu tối thiểu. `RunResult.trace_path` trỏ tới trace của lần chạy hiện tại và scanner quét thêm các file cùng thư mục có tiền tố `run_id`. Các bài kiểm thử quét artifact của lượt chạy. Một file nằm ngoài phạm vi quét cần được đưa về đúng contract trước khi dùng để chứng minh an toàn.

## Giới hạn

Benchmark dùng MockLLM, 14 claim public và chi phí mô phỏng. Latency là `unavailable`. `student_drop/` chưa có trong checkout lúc xác minh. Ngưỡng pass rate hidden 0,75 do grader của giảng viên xác nhận.
