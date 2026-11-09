# STAR: A Stage-attributed Triage and Repair Framework for RCA Agents in Microservices

> **Đọc nhanh (30 giây):** Chia quá trình RCA của agent thành **4 giai đoạn** có sản phẩm rõ ràng: gói bằng chứng (EP), tập giả thuyết (HS), cấu trúc phân tích (AS), báo cáo quyết định (DR). Khi trace có dấu hiệu lỗi, STAR **tìm giai đoạn hỏng đầu tiên**, vá nó và **chạy lại chỉ phần phía sau**. Có một **audit score** với ngưỡng τ: đủ cao thì chấp nhận, hơi thấp thì sửa nhanh, rất thấp thì sửa kỹ. Acc@1 của mABC với GPT-5 tăng từ 37,2% lên 56,2%.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2605.15581 **v1** (15/05/2026) |
| Tác giả | Junle Wang, Xingchuang Liao, Wenjun Wu (Beihang University); cùng nhóm với TopoEvo (2605.15611) |
| Venue | Preprint (11 trang) |
| PDF | https://arxiv.org/pdf/2605.15581v1 |
| Mức độ đọc | Abstract, §I–§II, RQ, setup, câu kết quả RQ1–RQ2, cơ chế routing (Eq. 7); chưa đọc kỹ RQ3–RQ4 và phần audit chi tiết |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Có "cổng" chấp nhận/sửa dựa trên audit score, nhưng không đánh giá cổng đó như một bộ ước lượng độ tin cậy |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper Abstract, §I]** Lỗi ở bước sớm (thu bằng chứng, lập giả thuyết, phân tích nhân quả) lan sang cuối và làm hỏng chẩn đoán. Debug từ trace tự do rất khó vì nhiễu và tốn kém khi chạy lại cả trajectory.

**Ví dụ [Diễn giải]:** nấu ăn sai vì nguyên liệu hỏng (giai đoạn 1) thì nêm lại gia vị (giai đoạn 4) không cứu được. Phải tìm đúng khâu hỏng rồi làm lại từ khâu đó.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Trace RCA của một agent có sẵn (mABC hoặc RCAgent) chia thành 4 artifact EP/HS/AS/DR |
| **Cơ chế** | Stage-wise audit tạo audit score S; routing: S ≥ τ thì **Pass**; τ−ε ≤ S < τ thì **Fast Path** (vá một chỗ); S < τ−ε thì **Slow Path** (tìm giai đoạn hỏng bằng counterfactual: thử vá từng giai đoạn, chạy lại phía sau, xem trace có cải thiện không) [Paper Eq. 7] |
| **Output** | Chẩn đoán đã sửa (top-k root cause + loại lỗi) |

## 3. Môi trường thực nghiệm [Paper §V-B]

- **Dataset A:** benchmark công khai của AIOps Challenge trên HipsterShop2 (10 service × 4 replica = 40 pod, 6 node, Kubernetes), có metrics, logs, traces.
- **Dataset B:** dữ liệu production thật của nền tảng quản lý dự án thuộc một doanh nghiệp thông tin điện lực (12 service, 48 pod), sự cố tự nhiên.
- 2 workflow agent (mABC, RCAgent), 3 foundation model (có GPT-5).
- Thư viện: LangGraph.

## 4. RQ và câu trả lời [Paper §V]

| RQ | Trả lời |
|---|---|
| RQ1: Có cải thiện RCA đầu-cuối? | Có. Dataset A, GPT-5: mABC Acc@1/3/5 37,2/45,1/47,8% → 56,2/66,1/70,8%; RCAgent 23,8/30,1/32,6% → 48,7/58,4/62,5% |
| RQ2: Tìm đúng giai đoạn hỏng? | Accuracy 78,7–89,1% theo giai đoạn S1–S4, hơn baseline failure attribution mạnh nhất trên 10 điểm |
| RQ3: Cần bao nhiêu vòng sửa? | Đa số trace sai ban đầu được sửa trong 1–2 vòng |
| RQ4: Thành phần nào quan trọng? | Cả Fast/Slow Routing và counterfactual localization đều đóng góp đáng kể |

## 5. Hạn chế

**Paper:** không thấy mục Limitations/Threats riêng trong bản v1.

**Người đọc nhận xét [Diễn giải]:**
- **Cần kiểm kỹ:** "cải thiện" trong counterfactual được đo bằng tín hiệu gì, và audit có dùng thông tin ngoài trajectory không. Bản v1 chỉ nói *"examining whether the repaired trace improves"*. **[Chưa kiểm]** Nếu có rò rỉ nhãn thì mức tăng có thể bị thổi phồng.
- Audit score là một **bộ ước lượng độ tin cậy ngầm** nhưng paper không báo AUROC, calibration hay risk–coverage của nó; chỉ báo accuracy sau sửa.
- Không báo chi phí tăng thêm (số lần replay, token) một cách tách bạch **[Chưa kiểm ở RQ3/RQ4]**.

## 6. Nhóm khai thác được gì?

1. **Tiền lệ "cổng chấp nhận theo điểm audit":** khi nhóm đề xuất cổng tin cậy, phải trích STAR và nói rõ khác biệt: nhóm **đánh giá chính cái cổng** (nó phân biệt đúng/sai tốt đến đâu, ở coverage nào), STAR dùng cổng làm công cụ để sửa.
2. **Chia 4 giai đoạn EP/HS/AS/DR:** khung gọn để thiết kế đặc trưng. Ví dụ: EP có đủ đa dạng nguồn không; HS có nhiều hơn 1 giả thuyết không; DR có trích dẫn observation không.
3. **Dataset A (AIOps Challenge, HipsterShop trên K8s):** một nguồn dữ liệu công khai khác cần biết, nhưng là dữ liệu tĩnh.
4. **Hướng mở rộng:** "phát hiện sai → chuyển cho người/model mạnh" (hướng chốt) là phiên bản rẻ hơn của "phát hiện sai → tự sửa" (STAR). Có thể so sánh hai chiến lược nếu còn thời gian.

## 7. Thuật ngữ

- **Acc@k:** đáp án đúng nằm trong top-k dự đoán.
- **Failure attribution:** xác định bước/agent nào gây lỗi trong một hệ nhiều agent.
- **Counterfactual evaluation:** thử "nếu sửa chỗ này thì kết quả có tốt lên không" để biết chỗ đó có phải nguyên nhân.
- **LangGraph:** thư viện xây agent dạng đồ thị các node, cho phép chạy lại từng node.
