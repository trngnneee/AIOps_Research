# Agentic Confidence Calibration (HTC: Holistic Trajectory Calibration)

> **Đọc nhanh (30 giây):** Agent hay **tự tin khi sai**. Paper đề xuất nhìn **toàn bộ quá trình chạy** (không chỉ câu trả lời cuối) để đoán agent đúng hay sai. Từ log-probability của mọi bước, trích **48 đặc trưng** (biến động qua các bước, độ ổn định trong một bước, vị trí, cấu trúc), rồi huấn luyện một **mô hình đơn giản** (logistic regression có L1) dự đoán xác suất thành công. Kết quả vượt các baseline trên 8 benchmark, và chuyển được sang domain khác.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2601.15778 **v1** (22/01/2026) |
| Tác giả | Jiaxin Zhang, Caiming Xiong, Chien-Sheng Wu (Salesforce AI Research) |
| Venue | ICML 2026 poster (theo trang ICML; chưa đối chiếu bản camera-ready) |
| PDF | https://arxiv.org/pdf/2601.15778v1 (37 trang) |
| Mức độ đọc | Abstract, §1–§2, các Takeaway và bảng kết quả chính; chưa đọc chứng minh lý thuyết trong appendix |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★★ **Phương pháp gần nhất** cho bài toán "đoán agent RCA đúng/sai từ trajectory", nhưng ở domain QA/reasoning |

---

## 1. Paper giải quyết vấn đề gì?

**Giải thích cho người mới [Diễn giải]:** nếu một sinh viên làm bài thi và cuối bài ghi "em chắc 95%", ta chưa tin ngay. Ta xem *cách em làm*: có tẩy xóa nhiều không, có đoạn nào lúng túng không, có quay lại làm đi làm lại không. HTC làm đúng việc đó với agent.

- **[Paper §1]** Phương pháp calibration cũ (ví dụ temperature scaling) làm cho đầu ra đơn lẻ. Agent có 3 khó khăn riêng: lỗi **cộng dồn** theo các bước, **bất định từ tool** (API lỗi, dữ liệu nhiễu), và **lỗi bị che** (bước sai nằm giữa trajectory chứ không ở bước cuối).
- Bài toán mới được định nghĩa: **Agentic Confidence Calibration**, tức ước lượng xác suất trajectory thành công bằng cách chẩn đoán toàn bộ quá trình.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Trajectory của agent kèm **log-probability từng token** ở mọi bước (white-box) |
| **Đặc trưng** | Vector 48 chiều: thống kê (trung bình, phương sai, min/max, entropy, độ lệch, sai phân) theo trục trong-bước và qua-các-bước [Paper §2] |
| **Mô hình** | Logistic regression có điều chuẩn L1 (thưa, dễ giải thích, ổn định khi ít dữ liệu) |
| **Output** | Xác suất trajectory thành công, đã hiệu chỉnh |

## 3. Môi trường thực nghiệm

- Framework agent: **smolagents** (kiểu CodeAct, agent sinh code Python để gọi tool).
- Model **có log-prob**: GPT-4.1, GPT-4o và một số model mở.
- 8 benchmark kiểu QA/reasoning như SimpleQA, HotpotQA, StrategyQA, GPQA, MMLU-Pro, MATH500, HLE, và GAIA (dùng làm out-of-domain).
- **Không có benchmark AIOps/RCA** trong danh sách đã đọc.

## 4. Cách làm (process)

```text
Agent chạy → ghi log-prob mọi token mọi bước
        → trích 48 đặc trưng (4 nhóm: dynamics, stability, position, structure)
        → huấn luyện calibrator nhỏ trên tập có nhãn đúng/sai
        → dự đoán xác suất đúng cho trajectory mới
        (+ GAC: calibrator huấn luyện trên nhiều domain để dùng zero-shot)
```

## 5. RQ / Takeaway và câu trả lời

| Takeaway | Nội dung [Paper §3–§4] |
|---|---|
| 1. Đặc trưng nào quan trọng? | Động học theo thời gian và độ ổn định là tín hiệu mạnh nhất; vị trí và cấu trúc bổ sung. **Không nhóm đặc trưng đơn lẻ nào đủ**, kết hợp nhiều nhóm thì tốt hơn rõ |
| 2. Chuyển domain được không? | Có, trong các tác vụ QA gần nhau (train một bộ, dùng cho bộ khác); nhưng lộ giới hạn khi phân bố thay đổi mạnh |
| 3. Calibrator tổng quát? | GAC đạt ECE thấp nhất zero-shot trên GAIA |

## 6. Kết quả chính

- Ví dụ từ bảng chuyển giao [Paper Table 2]: AUROC khoảng 0,66–0,82 tùy bộ; ECE có thể xuống khoảng 0,03–0,08 trong domain, nhưng tăng mạnh (khoảng 0,43–0,50) ở vài trường hợp chuyển giao ngoài domain.

## 7. Hạn chế

**Người đọc nhận xét [Diễn giải]:**
- **Cần log-prob:** nhiều API (ví dụ Claude) không trả log-prob, nên HTC không áp dụng trực tiếp cho mọi model. Đây là chỗ khác biệt quan trọng với hướng của nhóm.
- Domain QA/reasoning: trajectory ngắn, đáp án dễ chấm. RCA có cấu trúc khác: nhiều tool đặc thù, đáp án gồm component + fault type.
- Đặc trưng thuần thống kê log-prob, không dùng **ngữ nghĩa domain** (ví dụ agent đã kiểm tra pod bị nghi ngờ chưa).

## 8. Nhóm khai thác được gì?

1. **Khung phương pháp mượn được ngay:** trajectory → đặc trưng → logistic regression nhỏ → xác suất đúng. Đơn giản, giải thích được, hợp sức sinh viên.
2. **Khoảng trống để nhóm điền [Giả thuyết, cần kiểm novelty kỹ]:** HTC chưa thử trên RCA; chưa có đặc trưng **black-box** (không cần log-prob) và **đặc thù vận hành** (loại tool, truy vấn rỗng/lỗi, có kiểm giả thuyết cạnh tranh không, kết luận có dẫn tới observation thật không).
3. **Baseline cần có:** nếu dùng model có log-prob (ví dụ qua API OpenAI-compatible hỗ trợ `logprobs`), có thể chạy một phiên bản HTC rút gọn làm đối chứng.
4. **Bài học thiết kế:** kết hợp nhiều nhóm đặc trưng; báo cả discrimination (AUROC) lẫn calibration (ECE, Brier).

## 9. Thuật ngữ

- **Calibration (hiệu chỉnh):** khi model nói "80% chắc", thì khoảng 80% số lần đó phải đúng.
- **ECE (Expected Calibration Error):** sai lệch trung bình giữa độ tự tin và tỷ lệ đúng thực tế; càng nhỏ càng tốt.
- **AUROC:** khả năng xếp case đúng lên trên case sai; 0,5 là đoán mò, 1 là hoàn hảo.
- **Log-probability:** độ "chắc" của model khi sinh từng token; chỉ có khi API cho phép xem.
- **White-box / black-box:** có / không nhìn được bên trong model (log-prob, trọng số).
