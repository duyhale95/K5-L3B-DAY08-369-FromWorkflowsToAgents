# Bonus report: B7

- **Topic và nguồn:** Kiểm toán grader theo [đề Bonus B7](../../docs/bonus_topics.md#b7--kiểm-toán-grader) và [hướng dẫn fixture](../../src/grader_audit/README.md). Tài liệu lab liên hệ chủ đề với *Rethinking Evaluation of MAS Efficiency* (slide 44, 59).
- **CLAIM:** Cách tính mẫu số và chi phí có thể làm lệch kết luận so sánh agent, kể cả khi kết quả nghiệp vụ của từng lượt giữ nguyên.
- **BOUNDARY:** Ba bản grader xử lý danh sách trial tổng hợp trên shape `workflow`, seed 11 và 22. Cặp claim đổi số ngày giao trễ được kiểm bằng code tính quote. Phạm vi kết luận là các quan hệ đã thử trên fixture.
- **HYPOTHESIS:** Grader đúng giữ pass rate khi thêm lượt chưa chấm do lỗi hạ tầng, giữ các tỷ lệ và nhân đôi tổng chi phí khi nhân đôi danh sách, và giữ số liệu khi đảo thứ tự. Quote phải đổi từ 0 sang đúng phí ship tại ngưỡng 3 ngày.
- **Biến cố định và biến thay đổi:** Giữ nguyên grader, schema và các trường trial gốc trong từng phép thử. Lần lượt đổi số ngày trễ, thêm lượt có `infra_error`, nhân đôi danh sách và đảo thứ tự.
- **Bằng chứng:** `src/reports/bonus_grader_audit.json` tại commit `5c027d8`. Audit chạy trên fixture tĩnh nên không có run ID. Bộ test B7 đạt 19 test và kiểm kết quả tái tạo khớp JSON đã commit.

Chạy từ thư mục `src/`.

```powershell
python -m pytest -q tests/test_bonus_grader_audit.py
python -m bonus.grader_audit --out reports/bonus_grader_audit.json
```

## Kết quả

| Grader | Q1 Ngưỡng trễ | Q2 Lỗi hạ tầng | Q3 Nhân đôi | Q4 Đảo thứ tự |
| --- | --- | --- | --- | --- |
| `grader_a` | Đạt | Đạt | Lệch | Lệch |
| `grader_b` | Đạt | Đạt | Đạt | Đạt |
| `grader_c` | Đạt | Lệch | Đạt | Đạt |

- **Q1** đổi 2 thành 3 ngày và quote đi từ 0 đến 35.000 VND ở cả ba bản. Phép này xác minh ngưỡng nghiệp vụ độc lập với phần tổng hợp.
- **Q2** đưa thêm 4 lượt lỗi hạ tầng. `grader_c` đưa chúng vào mẫu số như lỗi ra quyết định, nâng số lượt được chấm từ 12 lên 16 trong khi số lượt thành công vẫn là 9. Pass rate tụt từ 0,75 xuống 0,5625. Hai bản còn lại giữ 9/12.
- **Q3** cho thấy `grader_a` cộng lại chi phí theo lượt đầu của mỗi claim. Tổng 283,5 VND thành 473,0 thay vì 567,0 khi nhân đôi. Hai bản còn lại đi từ 189,5 đến 379,0 VND.
- **Q4** giữ nguyên tập trial và chỉ đảo thứ tự. Tổng của `grader_a` đổi từ 283,5 thành 285,0 VND vì khoản cộng lặp phụ thuộc lượt xuất hiện trước. Biến thể kiểm chứng cố ý cộng chi phí ở vị trí chẵn cũng qua Q1–Q3 nhưng trượt Q4, cho thấy Q4 bắt được lỗi phụ thuộc vị trí.

## Kết luận

`grader_b` là bản duy nhất đạt các điều kiện được kiểm trong cả bốn phép. Q3 báo riêng giới hạn `pass_5` chung của các bản. Khi nhân đôi mỗi cặp claim/seed, số dòng mỗi claim vượt số seed, nên `pass_5` giảm từ 0,667 xuống 0 ở cả ba bản. Kiểm riêng chỉ số này cần dữ liệu duy nhất theo cặp claim/seed, hoặc quy tắc xử lý bản ghi trùng được định nghĩa trước. Cách tính của `grader_c` chỉ có thể phù hợp khi rubric quy lỗi hạ tầng đó cho chính shape.

## Giới hạn

Audit đo logic tính điểm trên fixture nhỏ. MockLLM thuộc benchmark chính và không tham gia audit này. Latency của benchmark chính là `unavailable`. Quan hệ metamorphic kiểm tra các tính chất đã chọn. Một lỗi làm sai đồng đều trên mọi đầu vào vẫn có thể qua các quan hệ đó.
