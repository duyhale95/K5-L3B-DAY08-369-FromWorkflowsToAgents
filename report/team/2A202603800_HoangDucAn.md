# Báo cáo cá nhân — 2A202603800_HoangDucAn

## 1. Thông tin thành viên

- Họ tên: Hoàng Đức An
- MSSV: 2A202603800
- Email: anduchoang2701@gmail.com
- GitHub: https://github.com/katogithub2701

## 2. Phần việc phụ trách

- **Người 4 — Phase 6 / `[US4]` (CP4 Must-Pass Audit + Crash 20/20 + Bonus B7):**
  - Pull `main` sau khi Người 3 hoàn tất Shape C; kiểm toán chéo 3 shape học viên (`workflow`, `single`, `orchestrator`) trên 3 điều kiện must-pass: không refund khi thiếu approval hợp lệ, không lộ `CANARY_SECRET_*`/PII, và crash không tạo quá một refund.
  - Chạy và commit bằng chứng crash chính thức `src/reports/crash.json` (`20/20`).
  - Thực hiện phần kỹ thuật Bonus B7: kiểm toán metamorphic `grader_a`, `grader_b`, `grader_c` trên 3 fixture có sẵn, thiết kế thêm quan hệ mới, sinh bằng chứng JSON và nháp `report/team/bonus_report.md`.
  - Cập nhật `TEAM.md`, đánh dấu Phase 6 trong `specs/001-logix-claim-agents/tasks.md`, viết báo cáo cá nhân và push `main` làm nền cho Người 5.

## 3. Đóng góp cụ thể

- **Cross-shape Must-Pass Audit — `src/tests/test_must_pass_audit.py` (43 test):**
  - Parametrize cả 3 shape qua 4 trường hợp approval xấu: thiếu approval, approval mượn của claim khác, approval bị thu hồi, approval hết hạn. Mỗi case khẳng định: `status == denied`, `proposal_amount` vẫn là quote đầy đủ 35.000 VND, **không có dòng ledger**, **không có audit `refund_committed`**, và có audit `policy_denied` đúng lý do.
  - Parametrize 3 shape × 3 cửa sổ crash (`before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`) trên claim `C-012`. Kiểm tra trace được flush trước khi `InjectedCrash` lan ra, ledger có tối đa 1 dòng, resume xong đúng 1 refund 35.000 VND + đúng 1 audit `refund_committed` + checkpoint đúng trạng thái.
  - Kiểm tra trần theo đơn T13/T14 cho từng shape: T13 bị host từ chối vì đơn đã hoàn đủ (`order_already_refunded`), T14 chỉ được top-up phần chênh lệch (150.000 quote → 120.000 thực trả). Điều này chứng minh shape truyền **full quote** cho `durability.issue_refund`, không tự trừ trước.
  - Quét rò rỉ trên `RunResult`, file trace và mọi sibling `<run_id>*` cho 5 claim đại diện (`C-001`, `C-004`, `C-005`, `C-010`, `C-013`) × 3 shape: không có `CANARY_SECRET_*`, `CANARY_INTERNAL_*`, header, SĐT, địa chỉ, tên hàng hay `SECRET_ITEM_VANG`.
  - Thêm test tổng hợp khẳng định ma trận gồm đúng 3 shape và 3 crash point, làm checklist CP4 có thể kiểm bằng máy.

- **Crash evidence — `src/reports/crash.json`:**
  - Chạy `python -m lab8.crash_test --count 20 --out reports/crash.json`; kết quả `crash_safety 20/20`, cả 20 scenario `passed: true` (5 `before_effect`, 7 `after_effect_before_checkpoint`, 5 `after_checkpoint`, cộng 3 case conflict/thiếu approval/swarm).

- **Bonus B7 — `src/bonus/grader_audit.py`, `src/tests/test_bonus_grader_audit.py` (19 test), `src/reports/bonus_grader_audit.json`:**
  - Áp 3 quan hệ chính thức từ `src/grader_audit/README.md` cho từng bản `grader_a/b/c`: `claim_delay` (2 vs 3 ngày), `infra` (thêm trial `infra_error`), `duplicate` (nhân đôi danh sách).
  - Thiết kế **quan hệ metamorphic mới `trial_order`**: đảo thứ tự cùng một multiset trial, mọi metric tổng hợp phải bất biến. Kèm mutant có kiểm soát (xử lý `infra_error` đúng nhưng cộng chi phí theo vị trí chẵn) để chứng minh quan hệ mới bắt được lỗi mà 3 quan hệ cũ bỏ sót: mutant qua Q1–Q3 nhưng trượt Q4 (283,5 → 285,0 VND).
  - Kết luận có bằng chứng số: **`grader_b` đúng duy nhất**; `grader_a` **đếm chi phí mô phỏng hai lần** (Q3: tổng 283,5 → 473,0 thay vì 567,0; cost/success 31,5 → 26,278; Q4 đổi 283,5 → 285,0 khi đảo thứ tự); `grader_c` **đưa trial chết vì hạ tầng vào mẫu số như quyết định sai** (Q2: `graded_trials` 12 → 16, `pass_rate` 0,75 → 0,5625, `pass_5` 0,667 → 0,5).
  - Phát hiện thêm giới hạn của chính thước đo: `lab8.metrics.summarize` chỉ tính `pass_5` khi mỗi claim có đúng `len(seeds)` dòng, nên khi nhân đôi danh sách thì `pass_5` rơi 0,667 → 0,0 ở **cả ba** bản. Đây là lỗi cấu trúc của reference ruler (file bảo vệ, không sửa), không phải lỗi riêng của ứng viên nào; đã ghi rõ trong `bonus_report.md`.
  - Sinh `src/reports/bonus_grader_audit.json` bằng `python -m bonus.grader_audit --out reports/bonus_grader_audit.json` (script deterministic, không đọc clock/random/network), không sửa tay JSON.

- **Tài liệu & bàn giao:**
  - Điền thông tin Người 4 vào `TEAM.md` (`## Thành viên`, `## Phân công tuần tự`, `## Bảng đóng góp`, link báo cáo cá nhân).
  - Đánh dấu `[X]` cho `T022`–`T028` trong `specs/001-logix-claim-agents/tasks.md`.
  - Viết `report/team/bonus_report.md` theo đúng khung B7 (≤ 2 trang), dùng số liệu từ JSON do script sinh.
  - Sửa regex tiêu đề bonus trong `src/lab8/check_submission.py` từ `B[1-6]` lên `B[1-7]` để khớp `docs/bonus_topics.md` (B7) — file này không thuộc danh sách bảo vệ.

## 4. Bằng chứng

- **Commit chính:** `dd3ae22` — `feat(audit): add cross-shape must-pass audit, crash evidence, and Bonus B7`
- **File đã thêm/sửa:**
  - `src/tests/test_must_pass_audit.py` (43 test)
  - `src/tests/test_bonus_grader_audit.py` (19 test)
  - `src/bonus/__init__.py`, `src/bonus/grader_audit.py`
  - `src/reports/crash.json` (`crash_safety: "20/20"`)
  - `src/reports/bonus_grader_audit.json` (bằng chứng B7 do script sinh)
  - `report/team/bonus_report.md`, `report/team/2A202603800_HoangDucAn.md`, `TEAM.md`, `specs/001-logix-claim-agents/tasks.md`
- **Kết quả chạy trong `src/` (Python 3.12.6, `.venv`):**
  - `python -m lab8.smoke` → `lab8.smoke pass`
  - `python -m pytest -q` → `183 passed, 248 deselected`
  - `python -m pytest -q tests/test_bonus_grader_audit.py` → `19 passed`
  - `python -m pytest -q -m student -o addopts=` → `248 passed, 183 deselected`
  - `python -m lab8.crash_test --count 20 --out reports/crash.json` → `crash_safety 20/20`
  - `python -m bonus.grader_audit --out reports/bonus_grader_audit.json` → `correct_graders ['grader_b']`; `grader_a` trượt `duplicate` + `trial_order`; `grader_c` trượt `infra`.
- **Run id / trace:** audit chéo dùng trace `R-<shape>-<claim>-s11` cho từng trial; `test_committed_evidence_is_reproducible` khẳng định JSON B7 đã commit khớp lại với lần audit mới.

## 5. Công cụ AI đã dùng

- **Công cụ:** OpenCode AI agent (model DeepSeek V4.1 Flash Free) kết hợp quy trình **GitHub Spec Kit** đã thiết lập ở Phase 1–2 (`.specify/`, `specs/001-logix-claim-agents/`).
- **Mục đích sử dụng:** đọc `grader_audit/README.md` + 3 bản grader + fixture (read-only), gợi ý cấu trúc test must-pass và quan hệ metamorphic mới, soạn code audit/B7 và báo cáo.
- **Cách tự kiểm tra kết quả:**
  - Đối chiếu từng assertion với `docs/business_rules.md`, `docs/contracts.md` (Trace Contract v1) và `docs/metrics.md` trước khi chấp nhận.
  - Chạy thật toàn bộ lệnh trong `src/.venv`: host gate, riêng file must-pass, riêng file bonus, ma trận student, `crash_test` và script sinh JSON; không dùng số liệu tự bịa.
  - Kiểm tra chéo JSON B7 với kết quả pytest (`test_committed_evidence_is_reproducible`) và xác nhận không sửa bất kỳ file nào trong `src/grader_audit/`, `src/lab8/metrics.py`, `durability.py`, `policy.py`, `src/config/*.yaml`, `src/data/*`.
  - Đọc lại diff `TEAM.md`/`tasks.md` để bảo đảm chỉ thêm thông tin Người 4, không đổi cấu trúc bảng máy đọc.

## 6. Tự đánh giá

- Hoàn thành đầy đủ Phase 6: audit must-pass 3 shape xanh, `crash.json` đạt `20/20`, bộ test B7 xanh và có bằng chứng JSON tái lập được; bàn giao `main` xanh cho Người 5.
- Điểm mạnh: kiểm toán không chỉ “test cho xanh” mà chỉ ra đúng lỗi hành vi của từng grader kèm delta số; quan hệ mới có mutant chứng minh tính cần thiết; phát hiện cả giới hạn `pass_5` của reference ruler thay vì quy sai cho ứng viên.
- Hạn chế: audit B7 chạy trên fixture tổng hợp 12–16 trial, không phải benchmark 14 claim × 5 seed; kết luận chỉ nói về thước đo, không nói shape nào tốt hơn. Các hạng mục benchmark/ADR/research card/group report vẫn thuộc lượt Người 5.
