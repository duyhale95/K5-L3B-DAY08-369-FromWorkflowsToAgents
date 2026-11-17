# Bonus report: B7

- **Topic + nguồn (tên, năm, slide):** B7 — Kiểm toán grader. Nguồn: *Rethinking Evaluation of MAS Efficiency* (EMNLP 2026, slide 44 và 59).
- **CLAIM của nguồn (1 câu):** Nếu thước đo sai thì mọi so sánh shape đều sai theo, kể cả khi shape đúng; trial chết vì hạ tầng (timeout, crash) bị tính là quyết định sai, hoặc chi phí bị đếm hai lần, đều làm lệch kết luận mà không test nào kêu.
- **BOUNDARY (model / dataset / setup):** Không gọi model thật. Đầu vào là ba danh sách trial tổng hợp trong `src/grader_audit/fixtures/` (12–16 trial, shape `workflow`, seed 11 và 22) và một cặp claim chỉ khác `delay_days` 2 so với 3 trên policy `POL-2026-11`. Ba ứng viên `grader_a`, `grader_b`, `grader_c` chỉ khác cách xử lý `infra_error` và cộng chi phí; `lab8.metrics.summarize` là mốc tham chiếu. Không sửa file nào trong `src/grader_audit/`.
- **HYPOTHESIS trên LogiX:** Một grader đúng phải (i) không đổi pass rate khi thêm `infra_error`, (ii) giữ nguyên các tỉ lệ và nhân đôi các tổng khi nhân đôi danh sách, (iii) không đổi metric khi chỉ đảo thứ tự trial, và (iv) giữ quyết định nghiệp vụ đúng khi `delay_days` đổi từ 2 sang 3. Grader vi phạm quan hệ nào sẽ bị quan hệ đó bắt.
- **Biến cố định / biến thay đổi:** Cố định shape, `claim_id`, `seed`, `passed`, `cost_estimate`, `steps`, `model_calls`, `tool_calls`. Thay đổi lần lượt: `delay_days` 2 → 3; thêm trial `infra_error: true`; nhân đôi danh sách; đảo thứ tự danh sách.
- **Lệnh tái lặp (copy-paste được):**

  ```bash
  cd src
  python -m pytest -q tests/test_bonus_grader_audit.py
  python -m bonus.grader_audit --out reports/bonus_grader_audit.json
  ```

- **File report + run id:** `report/team/bonus_report.md` và `src/reports/bonus_grader_audit.json`. Không có run id vì đây là audit offline trên fixture tổng hợp; script deterministic, không đọc đồng hồ, random hay mạng, nên chạy lại cho cùng JSON.

## Kết quả

Bảng lấy từ `src/reports/bonus_grader_audit.json` (script sinh, không chép tay). ✓ = giữ đúng quan hệ, ✗ = vi phạm.

| Ứng viên | Q1 `claim_delay` (2 vs 3 ngày) | Q2 `infra` (thêm 4 trial lỗi hạ tầng) | Q3 `duplicate` (nhân đôi danh sách) | Q4 **mới** `trial_order` (đảo thứ tự) |
| --- | :---: | :---: | :---: | :---: |
| `grader_a` | ✓ | ✓ | ✗ | ✗ |
| `grader_b` | ✓ | ✓ | ✓ | ✓ |
| `grader_c` | ✓ | ✗ | ✓ | ✓ |

**Q1 — quyết định nghiệp vụ:** cả ba bản cho `quote` 0 VND ở `delay_days = 2` và 35.000 VND ở `delay_days = 3` (đúng `min_delay_days = 3`, chỉ hoàn phí ship); trial list 1 fail + 1 pass cho `pass_rate = 0.5`. Fixture này không đi qua `summarize`, nên nó kiểm luật chứ không phân biệt ba bản.

**Q2 — lỗi hạ tầng:** `grader_a` và `grader_b` đánh dấu trial `infra_error` là chưa chấm: `graded_trials` 12 → 12, `pass_rate` 0,75 → 0,75, `successes` 9 → 9. `grader_c` chấm trial lỗi hạ tầng thành `passed = False`: `graded_trials` 12 → **16**, `pass_rate` 0,75 → **0,5625**, `pass_5` 0,667 → **0,5**, seed 11: 0,833 → **0,625**, seed 22: 0,667 → **0,5**. Tên lỗi hành vi: *đưa trial chết vì hạ tầng vào mẫu số như quyết định sai của shape*.

**Q3 — nhân đôi danh sách:** `grader_b` và `grader_c` giữ `pass_rate`, `pass_5`, `seed_pass_rates`, `seed_variance`, `cost_per_success_vnd` và các giá trị trung bình; `trials`, `graded_trials`, `successes`, `total_simulated_cost_vnd` đều gấp đôi (189,5 → 379,0 VND; cost/success 21,056 VND không đổi). `grader_a` cộng thêm chi phí “lần đầu thấy mỗi claim” vào tổng đã có: tổng 283,5 → **473,0** thay vì **567,0** (thiếu 94,0), cost/success 31,5 → **26,278**. Tên lỗi hành vi: *đếm chi phí mô phỏng hai lần*.

**Q4 — quan hệ mới (đảo thứ tự):** cùng một multiset trial, chỉ đổi thứ tự. `grader_b` và `grader_c` bất biến (189,5 → 189,5). `grader_a` đổi tổng 283,5 → **285,0** và cost/success 31,5 → **31,667**: khoản cộng thêm phụ thuộc trial nào xuất hiện trước trong danh sách. Tên lỗi hành vi: *tổng chi phí phụ thuộc thứ tự trial*.

## Kết luận

- **`grader_b` là bản đúng duy nhất**: chỉ bản này qua cả ba quan hệ chính thức và quan hệ mới.
- **`grader_a` sai ở Q3 và Q4**, cùng một nguyên nhân: lấy chi phí theo “first-seen” của từng claim rồi cộng lên tổng đã tính trên mọi trial. Trên Q3 nó làm tổng không gấp đôi; trên Q4 nó làm tổng phụ thuộc thứ tự.
- **`grader_c` sai ở Q2**: treatment `infra_error` thành fail của shape, làm pass rate và pass^5 tụt giả tạo. Đây là lỗi nguy hiểm nhất cho kết luận kiến trúc vì hạ tầng chết nhiều sẽ “trừ điểm” shape mà không liên quan chất lượng quyết định.
- **Vì sao Q4 bắt được lỗi mà ba quan hệ cũ bỏ sót:** Q3 chỉ nối thêm một bản sao nên thứ tự không đổi; Q2 chỉ đổi thành phần danh sách; Q1 không đi qua `summarize`. Ta thêm một **mutant có kiểm soát** (xử lý `infra_error` đúng, nhưng cộng chi phí các trial ở vị trí chẵn) — mutant này qua Q1, Q2, Q3 nhưng trượt Q4 (283,5 → 285,0). Vì vậy Q4 là quan hệ duy nhất trong bộ hiện tại bắt được lỗi phụ thuộc vị trí/thứ tự.
- **Một lỗi của chính thước đo lọt qua mọi quan hệ?** Có, ở `pass_5`: `metrics.summarize` chỉ tính một claim khi số dòng đã chấm đúng bằng `len(seeds)`. Q3 tạo 4 dòng/claim trên 2 seed nên `pass_5` rơi từ 0,667 xuống 0,0 ở **cả ba** ứng viên — không phải lỗi của ứng viên nào mà là giới hạn cấu trúc của thước đo chuẩn. Quan hệ Q3 như văn bản README phát biểu (pass_5 không đổi) là không thỏa được với chính baseline. Muốn audit `pass_5` công bằng phải nhân bản theo seed (giữ 1 dòng/claim/seed) hoặc dedupe theo `(claim_id, seed)` trước khi tính.
- **Điều kiện làm kết luận đảo:** nếu lỗi hạ tầng thực sự thuộc trách nhiệm shape (shape tự quản timeout/crash) thì cách tính của `grader_c` có thể biện hộ; nếu chi phí được định nghĩa là “một lần mỗi claim” thay vì “mỗi trial” thì phần cộng thêm của `grader_a` không sai. Theo `docs/metrics.md`, cost là tổng cost mô phỏng của **mỗi trial** nên cả hai đều là lỗi.

## Giới hạn

- Fixture tổng hợp 12–16 trial, không phải benchmark 14 claim × 5 seed; kết quả này nói về **thước đo**, không nói shape nào tốt hơn.
- MockLLM không tham gia audit này; mọi khác biệt đến từ code `summarize`, không từ chất lượng sinh câu trả lời.
- Quan hệ metamorphic là điều kiện **cần**, không **đủ**: một bản sai hằng số ở mọi metric có thể qua vài quan hệ; ta chỉ kết luận được bản nào lệch trên các phép biến đổi đã chọn.
- Chưa kiểm `secret_leak_count`, `approval_bypass_count` hay hidden grading (ngoài phạm vi B7); các cổng đó do `crash.json` và audit must-pass của Phase 6 phụ trách.
- `python -m pytest -q tests/test_bonus_grader_audit.py` hiện chạy **19 passed**; JSON bằng chứng được kiểm tra khớp lại với lần audit mới trong `test_committed_evidence_is_reproducible`.
