# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 · Failure taxonomy |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Cemri et al., NeurIPS 2025, [Why Do Multi-Agent LLM Systems Fail?](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html). Nghiên cứu thực nghiệm trên trace được gán nhãn. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | MAST phân 14 dạng lỗi quan sát được thành ba nhóm. Một nhóm là lỗi kiểm chứng kết quả hoặc kết thúc tác vụ. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Taxonomy hình thành từ 150 trace phân tích có người gán nhãn. MAST-Data có hơn 1.600 trace từ 7 framework, trên tác vụ lập trình, toán và agent tổng quát. LogiX dùng MockLLM và một luồng hoàn tiền giả lập. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Tắt việc ghi đè số ngày trong đơn bằng số ngày từ ticket sẽ sửa đúng một lượt public. Pass rate dự kiến tăng 1/70, pass^5 tăng 1/14 và variance về 0. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Chạy `swarm` và `swarm_order_only` trên cùng 14 claim, 5 seed, MockLLM, tool, giá và evaluator. Biến thể chỉ vô hiệu hóa đầu vào `parsed_delay` mà swarm dùng để quyết định ghi đè dữ liệu đơn. Lượt model `parse` vẫn chạy. Mỗi lượt có SQLite mới. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | `C-002` seed 55 trả `resolved` khi nhãn là `denied`. Nhóm diễn giải theo MAST là lỗi kiểm chứng dữ kiện trước khi tính quote. So sánh lượt ghép cặp, pass rate, pass^5, seed variance và cost/success. |

## Kết quả ablation

Chạy từ `src/` với Python trong môi trường ảo.

```powershell
python -m lab8.benchmark --shapes 'swarm,swarm_order_only' --extra-shape 'swarm_order_only=bonus.swarm_order_only:run_claim' --cases data/public_claims.jsonl --seeds '11,22,33,44,55' --out reports/research_r2.json
```

| Biến thể | Pass rate | Pass^5 | Seed variance | Cost/success (VND mô phỏng) |
| --- | ---: | ---: | ---: | ---: |
| `swarm` | 69/70 | 13/14 | 0,000816 | 49,57 |
| `swarm_order_only` | 70/70 | 14/14 | 0 | 48,72 |

Kết quả khớp giả thuyết. Trong `src/reports/research_r2.json` tại commit `5c027d8`, `R-swarm-C-002-s55` sai và `R-swarm_order_only-C-002-s55` đúng. Cả hai gọi model 3 lần. Biến thể bỏ lượt tính lại quote ở nhánh ghi đè, giảm số lượt tool trên cặp này từ 6 xuống 5. Tác động đo được trên một lỗi cố ý của swarm và 14 claim public. Latency là `unavailable` và kết quả chưa kiểm chứng trên model hoặc dữ liệu sản xuất.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
