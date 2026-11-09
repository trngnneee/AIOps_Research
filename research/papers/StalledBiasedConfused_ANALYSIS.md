# Stalled, Biased, and Confused: Uncovering Reasoning Failures in LLMs for Cloud-Based RCA

> **Đọc nhanh (30 giây):** Bỏ hết khung agent phức tạp để chỉ đo **khả năng suy luận** của LLM trong RCA. 48.000 lần chạy, 6 model mã nguồn mở. Phát hiện: workflow agent (ReAct, Plan-and-Execute) **không** luôn tốt hơn hỏi thẳng một lần; có **16 kiểu lỗi suy luận**; và sự xuất hiện của một số lỗi (neo vào giả thuyết đầu, lặp lại không tiến triển, chọn bằng chứng tùy tiện, không cập nhật niềm tin) **dự báo** kết quả sai.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2601.22208 **v1** (29/01/2026) |
| Tác giả | Evelien Riddell, James Riddell, Gengyi Sun, Michał Antkiewicz, Krzysztof Czarnecki (University of Waterloo) |
| Venue | **FORGE 2026** (ACM), DOI 10.1145/3793655.3793732 |
| Code | https://github.com/boerste/rca-llm-reasoning (replication package, theo roadmap của nhóm) |
| PDF | https://arxiv.org/pdf/2601.22208v1 (19 trang) |
| Mức độ đọc | Abstract, §1–§2, câu trả lời RQ1–RQ4 (§4), §5–§6, Table 1; chưa đọc chi tiết bảng số theo model |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★★ **Tiền lệ trực tiếp**: dấu hiệu suy luận dự báo đúng/sai |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper §1]** Các hệ RCA bằng LLM thường lồng model vào pipeline nhiều agent phức tạp, nên khi sai không biết do suy luận của model hay do thiết kế xung quanh. Chưa có đánh giá hệ thống về **chất lượng suy luận**.

**Ví dụ [Diễn giải]:** muốn biết một học sinh giỏi toán thật hay không, cho em làm bài một mình với đề rõ ràng, đừng cho làm bài nhóm.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input của agent** | Alert đã tổng hợp từ logs/metrics/traces + knowledge graph có kiểu của hệ thống; tool tất định [Paper §1, §3] |
| **Output của agent** | Các giả thuyết root cause (vị trí, loại lỗi, đường lan truyền) |
| **Output của nghiên cứu** | Accuracy theo model/workflow; taxonomy 16 lỗi suy luận; mức liên hệ giữa lỗi và độ đúng |

## 3. Môi trường thực nghiệm [Paper §3.4]

- 2 case study: hệ A là **MicroSS** (152 mẫu) và hệ B là **Online Boutique** (148 mẫu). Trong abstract tác giả gọi là "GAIA and OpenRCA".
- 6 model mã nguồn mở: Llama 3.2 (3B), Qwen 3 (4B, 32B), Llama 3.3 Instruct (70B), Command R+ (104B), DeepSeek-R1 distilled (70B, chỉ chạy Straight-Shot vì không hỗ trợ tool calling). Lý do chọn mã nguồn mở: RCA nên tự host vì quyền riêng tư.
- 3 workflow: **Straight-Shot** (hỏi một lần, không agent), **ReAct**, **Plan-and-Execute**.
- Tổng cộng 48.000 kịch bản, 228 ngày thời gian chạy.
- Judge: GPT-5 làm LLM-as-a-Judge, có hai tác giả review độc lập một tập con [Paper §5].

## 4. Cách làm (process)

```text
1. Đơn giản hóa RCA: alert-level input, knowledge graph tường minh, tool tất định
2. Chạy 6 model × 3 workflow × 2 hệ thống
3. Đo accuracy: định vị (LA), loại lỗi (TA), giả thuyết (HA), đường lan truyền (PA)
4. Holdout từng modality (bỏ metrics / logs / traces) → đo độ nhạy
5. Dựng taxonomy 16 lỗi suy luận từ 170 mẫu (mã hóa định tính)
6. LLM-as-a-Judge gán lỗi cho mọi trace → tính Risk Difference và Relative Risk
   RD = P(đúng | có lỗi) − P(đúng | không lỗi)
```

**16 lỗi suy luận (Table 1)** gồm: RF-01 Fabricated evidence, RF-02 Metric interpretation error, RF-03 Confused provenance, RF-04 Temporal misordering, RF-05 Spurious causal attribution, RF-06 Unjustified instance specificity, RF-07 Arbitrary evidence selection, **RF-08 Evidential insufficiency**, RF-09 Failure to update belief, RF-10 Simulation/role confusion, RF-11 Excessive speculation, RF-12 Repetition or failure to resume, RF-13 Anchoring bias, RF-14 Invalid inference pattern, RF-15 Internal contradiction, RF-16 Arithmetic/aggregation error.

## 5. RQ và câu trả lời [Paper §4]

| RQ | Trả lời |
|---|---|
| RQ1: LLM agent làm RCA tốt đến đâu? | Vẫn khó. Workflow agent cho lợi ích giảm dần hoặc âm với LA/TA/HA, có trường hợp **dưới mức đoán ngẫu nhiên**. Straight-Shot thường bằng hoặc hơn. Agent chỉ giúp đường lan truyền (PA). Model nhỏ bị lỗi thực thi và giới hạn đệ quy |
| RQ2: Nhạy với modality thế nào? | Bỏ metrics làm hỏng định vị; bỏ logs làm hỏng nhận diện loại lỗi; **bỏ traces thường làm tốt hơn** (traces gây nhiễu) |
| RQ3: Có những lỗi suy luận nào? | 16 lỗi, 3 nhóm: procedural, RCA-specific, general. Lỗi đặc thù RCA nhất quán giữa model; lỗi procedural thay đổi theo model và workflow |
| RQ4: Lỗi có báo trước kết quả sai? | **Có.** Dự báo âm rõ nhất: anchoring (RF-13), repetition/stalled (RF-12), arbitrary evidence selection (RF-07), failure to update belief (RF-09) |

## 6. Kết quả chính

- Fabricated evidence (RF-01) và evidential insufficiency (RF-08) phổ biến nhất (theo trang dự án của Waterloo và kết quả tìm kiếm; **[Chưa kiểm]** số chính xác trong bảng).
- Mô hình "thinking" ít lỗi cross-cutting hơn khi chạy agentic [Paper Observation 11].

## 7. Hạn chế

**Paper tự nhận [§5]:** chỉ kịch bản một lỗi; alert không phải gold label nên có nhiễu; nhạy với cách viết prompt; taxonomy từ 170 mẫu; LLM judge có thiên lệch (giảm bằng GPT-5 và review hai tác giả).

**Người đọc nhận xét [Diễn giải]:**
- Thiết lập đơn giản hóa (alert-level, knowledge graph cho sẵn) khác xa môi trường tương tác như Cloud-OpsBench.
- RQ4 là **tương quan** (RD/RR), không phải nhân quả. Lỗi được phát hiện bằng **LLM judge sau khi chạy**, tức tốn thêm một lần gọi model mạnh.
- Chưa biến các dấu hiệu này thành **quy tắc quyết định** (ví dụ "nếu có RF-12 thì chuyển cho người") và chưa đo bằng risk–coverage.

## 8. Nhóm khai thác được gì?

1. **Tiền lệ quan trọng nhất cho hướng chốt:** RQ4 cho thấy dấu hiệu trong quá trình suy luận **dự báo** đúng/sai. Hướng của nhóm đi tiếp: (a) dùng dấu hiệu **đo tự động, không cần judge** (ví dụ lặp tool call thay cho RF-12); (b) dùng để **ra quyết định** chấp nhận hay chuyển tiếp; (c) đánh giá bằng AUROC và risk–coverage trên môi trường K8s tương tác. Khi viết related work, phải nói rõ Riddell et al. đã chứng minh mối liên hệ ở mức tương quan.
2. **"Agent workflow không luôn tốt hơn":** baseline Straight-Shot (một lần gọi) đáng có trong mọi thí nghiệm.
3. **RF-08 Evidential insufficiency** là tên chuẩn cho hiện tượng "kết luận trên bằng chứng yếu". Dùng thuật ngữ này thay vì tự đặt tên mới.
4. **Bỏ modality:** traces có thể gây nhiễu. Cùng xu hướng với TelemetrySuffBench ("dữ liệu hạ nguồn gây nhiễu").

## 9. Thuật ngữ

- **Straight-Shot:** đưa hết thông tin, hỏi model một lần, không cho gọi tool.
- **Plan-and-Execute:** lập kế hoạch nhiều bước trước rồi thực hiện từng bước.
- **Risk Difference (RD):** chênh lệch xác suất đúng giữa nhóm có lỗi và không có lỗi; âm nghĩa là có lỗi thì dễ sai hơn.
- **Anchoring bias:** bám chặt giả thuyết đầu tiên, bỏ qua giả thuyết khác.
