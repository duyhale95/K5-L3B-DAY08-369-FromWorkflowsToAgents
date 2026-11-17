# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Nhóm 369. Thành viên và đóng góp xem [TEAM.md](../../TEAM.md).
- Commit chốt code và số liệu: `5c027d8`, trùng [ADR](decision_adr.md).

## 2. Mục tiêu và cách tiếp cận

Nhóm triển khai ba cách xử lý cùng một yêu cầu hoàn tiền vận chuyển và đối chiếu với swarm tham chiếu. Nhóm làm tuần tự từ workflow, single agent, orchestrator đến kiểm toán an toàn và đánh giá. Mục tiêu là chọn cách có ít quyền tự chủ nhất trong số các cách đáp ứng nghiệp vụ và các điều kiện an toàn.

## 3. Giải pháp

| Shape | Cách xử lý |
| --- | --- |
| `workflow` | Python đọc claim và đơn, tính quote từ policy hiện hành rồi gọi host nếu quote dương. MockLLM soạn câu trả lời. |
| `single` | Vòng ReAct tối đa 8 bước dùng tool đọc. Code tính và kiểm tra quote trước khi gọi host. |
| `orchestrator` | Bộ điều phối gửi `handoff.v1` đã lọc cho investigator chỉ đọc, nhận dữ kiện đơn rồi tính quote và gọi host. |
| `swarm` | Mẫu đối chứng gọi MockLLM để mô phỏng trao đổi ngang hàng. Ở seed chia hết cho 5, mẫu có thể dùng số ngày trong ticket khi số đó lệch với dữ liệu đơn. |

Ba shape học viên dùng đơn có cấu trúc và policy hiện hành để tính tiền. Với quote dương, shape chuyển toàn bộ quote cho host. Host kiểm quyền sở hữu, approval thuộc đúng claim, mức đã duyệt và lịch sử hoàn theo đơn. Refund và audit `refund_committed` cùng nằm trong một transaction. Khi chạy lại sau crash, host dùng khóa `refund:{claim_id}` để nhận lại kết quả đã commit. Ví dụ T14 có quote 150.000 VND và 30.000 VND đã hoàn, nên host ghi thêm 120.000 VND.

Trace ghi những bước đọc, quyết định, quote và kết quả host. `single` thêm sự kiện ReAct. `orchestrator` ghi handoff đã lọc theo allowlist. Các artifact loại bỏ ticket thô, secret, header, điện thoại, địa chỉ, tên hàng và ghi chú nội bộ. Grader so `RunResult` với ledger và quét trace cùng các file có tiền tố `run_id`.

## 4. Kết quả

`src/reports/benchmark.json` gồm 280 lượt trên 4 shape, 14 claim và 5 seed `11,22,33,44,55`. Mỗi lượt dùng SQLite mới và cùng bộ dữ liệu, MockLLM, bảng giá và evaluator.

| Shape | Lượt đúng | Pass rate | Pass^5 | Seed min–max | Variance | VND mô phỏng/thành công | Steps mean / p95 |
| --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| `workflow` | 70/70 | 1,000 | 1,000 | 1,000–1,000 | 0 | 28,94 | 3,79 / 4 |
| `single` | 70/70 | 1,000 | 1,000 | 1,000–1,000 | 0 | 54,10 | 12,64 / 14 |
| `orchestrator` | 70/70 | 1,000 | 1,000 | 1,000–1,000 | 0 | 55,71 | 6,71 / 8 |
| `swarm` | 69/70 | 0,986 | 0,929 | 0,929–1,000 | 0,000816 | 49,57 | 2,80 / 3 |

Nhóm chọn `workflow` vì đạt độ đúng cao nhất cùng chi phí thấp nhất trong lần đo. Lượt swarm sai là `R-swarm-C-002-s55`. Đơn ghi trễ 2 ngày, ticket ghi 5 ngày, kết quả thành `resolved` khi nhãn là `denied`. Ablation trong [research card](research_card.md) đo riêng tác động của đường ghi đè này.

`src/reports/crash.json` đạt **20/20**. Audit CP4 và T11/T12 kiểm bổ sung ba shape học viên, gồm retry, crash, approval và bảo mật artifact. Không phát hiện bypass hay rò canary ở workflow trong các ca đã kiểm tra. Host suite đạt 192 test, ma trận student đạt 248 test và Bonus B7 đạt 19 test. Phát hiện về các bản grader xem [báo cáo B7](bonus_report.md).

## 5. Khó khăn và cách xử lý

Ca T02 cho thấy approval hợp lệ vẫn có thể đi kèm một quote sai nghiệp vụ. Nhóm chạy lại trên cùng claim và seed, vô hiệu hóa riêng đầu vào số ngày đọc từ ticket rồi đối chiếu hai lượt trong JSON. Test invariant kiểm tra cả ma trận claim/seed, công thức metric và trace, kể cả trace của lượt swarm sai đã biết.

## 6. Tổng hợp đóng góp

Hà Lê Duy phụ trách Spec Kit và workflow. Nguyễn Lê Trọng Mạnh phụ trách single agent. Nguyễn Hoàng Gia An phụ trách orchestrator và handoff. Hoàng Đức An phụ trách audit Must-Pass, crash suite và Bonus B7. Nguyễn Thiên Bảo phụ trách benchmark, test invariant, ablation và tổng hợp báo cáo. Bằng chứng theo từng người nằm trong [bảng đóng góp](../../TEAM.md#bảng-đóng-góp).

## 7. Hạn chế và hướng cải thiện

Bộ public có 14 claim giả lập, MockLLM có hành vi theo seed, chi phí dựa trên giá mô phỏng và latency là `unavailable`. Số bước là số event trong trace nên phụ thuộc độ chi tiết của từng shape. Chưa có `student_drop/` trong checkout lúc kiểm tra. Nhóm sẽ xem lại ADR nếu grader chính thức cho thấy kiến trúc khác xử lý đúng hơn trên nhóm claim cần điều tra qua nhiều nguồn và vẫn qua các cổng an toàn.

## 8. Tài liệu tham khảo

- [Luật nghiệp vụ](../../docs/business_rules.md), [contract](../../docs/contracts.md), [định nghĩa metric](../../docs/metrics.md) và [đề Bonus B7](../../docs/bonus_topics.md#b7--kiểm-toán-grader).
- Cemri et al., NeurIPS 2025. [Why Do Multi-Agent LLM Systems Fail?](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html).
