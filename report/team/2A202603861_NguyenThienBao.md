# Báo cáo cá nhân — Nguyễn Thiên Bảo

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thiên Bảo
- MSSV: 2A202603861
- Email: 26ai.baont5@vinuni.edu.vn
- GitHub: Limdim1604

## 2. Phần việc phụ trách

Thành viên thứ 5 nhóm 369, Phase 7 / US5. Chạy benchmark CP5 và crash suite, viết test invariant, thực hiện ablation R2 và hoàn thiện báo cáo nộp nhóm.

## 3. Đóng góp cụ thể

Commit kỹ thuật `5c027d8` bổ sung 9 test trong `src/tests/test_benchmark_invariants.py` để kiểm tra ma trận claim/seed, công thức metric, trace và lượt sai của swarm. Biến thể `swarm_order_only` tắt riêng khả năng dùng số ngày ghi trong ticket để tính quote và giữ các lượt gọi MockLLM. Tôi chọn `workflow` trong ADR vì ba shape học viên đều đạt 70/70 lượt trên public, còn `workflow` có cost/success thấp nhất.

## 4. Bằng chứng

- Benchmark public và ablation nằm trong `src/reports/benchmark.json` và `src/reports/research_r2.json`.
- `R-swarm-C-002-s55` trả `resolved`. `R-swarm_order_only-C-002-s55` trả `denied` và đạt nhãn.
- Crash suite đạt 20/20. Host suite đạt 192 test, ma trận student đạt 248 test và bộ Bonus B7 đạt 19 test.

## 5. Công cụ AI đã dùng

Codex hỗ trợ đọc Spec Kit, viết test và biến thể R2, chạy công cụ của lab và soạn báo cáo. Kiểm chứng dựa vào kết quả pytest, đối chiếu số liệu với JSON do công cụ sinh ra và kiểm tra bài nộp bằng `lab8.check_submission`.

## 6. Tự đánh giá

Phần kiểm thử giúp xác định lỗi ở `C-002` theo đúng cặp claim/seed và đo được tác động khi tắt một đường dùng dữ liệu thiếu tin cậy. Kết luận chọn shape dựa trên tập public và MockLLM. Cần kết quả grader của giảng viên để xác nhận độ đúng và điều kiện an toàn trên hidden.
