# Beyond Single-Turn Confidence: Trajectory-Adapted Uncertainty Quantification for LLM Agents

> **Đọc nhanh (30 giây):** So sánh có kiểm soát ba họ phương pháp đo độ tin cậy khi chuyển từ "một câu trả lời" sang "cả một trajectory agent": (1) **white-box** dùng log-prob, (2) **black-box consistency** (chạy lại nhiều lần xem có giống nhau không), (3) **reflexive** (hỏi chính model tự chấm). Kết quả: **self-consistency thường mạnh nhất**, **tự chấm là baseline rẻ mạnh nhất**, log-prob rất nhạy cách gộp, và **không họ nào đáng tin ở mọi model, mọi domain**.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2608.11552 **v1** (12/08/2026) |
| Tác giả | Dylan Bouchard, Mohit Singh Chauhan |
| Venue | Preprint |
| PDF | https://arxiv.org/pdf/2608.11552v1 (24 trang) |
| Mức độ đọc | Abstract, §1–§3, phần kết quả chính, Limitations |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★★ Cho biết **nên thử phương pháp nào** và **vì sao phải kiểm lại trên RCA** |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper §1]** Các phương pháp UQ (uncertainty quantification) thường được kiểm trên đầu ra một lượt. Với agent, đơn vị là **trajectory**: agent hỏi lại, gọi tool, cập nhật trạng thái, lỗi sớm lan sang cuối. Chưa ai so sánh ba họ UQ trong cùng điều kiện cho agent.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Trajectory nhiều lượt của agent dùng tool |
| **Scorer** | White-box (log-prob của token hành động, nhiều cách gộp qua các lượt); black-box consistency (lấy mẫu lại nhiều trajectory, đo giống nhau ở câu trả lời cuối, ở **tập hành động** (action-set), hoặc **tương đương trajectory** do model khác phán); reflexive (P(True), verbalized confidence) |
| **Output** | Điểm tin cậy ∈ [0,1] dự đoán trajectory thành công |
| **Đo** | Discrimination (AUROC), calibration (ECE), selective prediction (PRR) |

## 3. Môi trường thực nghiệm

- 5 LLM (có cả model nhỏ như Qwen2.5-7B, Qwen3.5-9B, gpt-4o-mini, gpt-oss-20b, MiniMax; **[Chưa kiểm]** đủ danh sách).
- 4 tập: phần multi-turn của **BFCL-v4** và 3 domain của **τ²-bench** (airline, retail, telecom).

## 4. Kết quả chính [Paper Abstract, §4]

- **Black-box self-consistency** thường mạnh nhất; trong đó *trajectory-equivalence rate* (TER) và *action-set consistency* (AEC) hay dẫn đầu. AUROC consistency tốt nhất có thể tới khoảng 0,87 (airline).
- **Reflexive** (model tự chấm trajectory) là baseline **rẻ** mạnh nhất ở đa số thiết lập, chỉ tốn thêm một lượt đọc transcript.
- **White-box** rất nhạy với cách gộp log-prob qua các lượt.
- Calibration không đều: ECE của reflexive có cell chỉ 0,05 nhưng có cell lên 0,56.
- **Không họ nào đáng tin tuyệt đối** qua mọi model và domain.

## 5. Hạn chế

**Paper tự nhận [Limitations]:** chỉ BFCL-v4 và τ²-bench; nhãn reward có nhiễu; user giả lập gây nhiễu thêm; giao diện hành động dạng text; số task mỗi domain nhỏ nên khoảng tin cậy rộng.

**Người đọc nhận xét [Diễn giải]:** không có domain vận hành hệ thống. Self-consistency tốn thêm chi phí (chạy lại K lần), cần tính vào ngân sách.

## 6. Nhóm khai thác được gì?

1. **Danh sách baseline chuẩn cho hướng chốt:** (a) verbalized confidence (agent tự nói % chắc), (b) P(True) / tự chấm lại trajectory, (c) self-consistency giữa K lần chạy (đồng ý ở đáp án cuối; đồng ý ở tập tool đã gọi). Đây là các đối chứng **bắt buộc** nếu nhóm đề xuất đặc trưng quá trình.
2. **Lý do khoa học cho đề tài:** paper kết luận UQ *"should be revalidated at the trajectory level"* và không họ nào ổn định ở mọi domain. Vậy kiểm lại trên **RCA Kubernetes** là một câu hỏi chính đáng, không phải lặp lại.
3. **Bài học chi phí:** self-consistency cần K lần chạy; trên Cloud-OpsBench replay rẻ nên khả thi, nhưng phải báo chi phí so với lợi ích.
4. **Tài liệu dẫn tiếp:** Oh et al. 2026 (ACL) về nền tảng UQ cho agent; Xuan et al. 2026 (ACL), *The confidence dichotomy*: tool lấy bằng chứng làm agent **quá tự tin**, tool kiểm chứng giảm lệch. Kết quả này rất đáng kiểm trên agent RCA, vốn dùng chủ yếu tool lấy bằng chứng. **[Chưa đọc full text hai bài này]**

## 7. Thuật ngữ

- **Self-consistency:** chạy lại nhiều lần; nếu các lần cho cùng kết quả thì tin hơn.
- **P(True):** hỏi model "câu trả lời này đúng không?" rồi lấy xác suất nó nói "đúng".
- **PRR (Prediction Rejection Ratio):** mức cải thiện khi loại bỏ dần case kém tin cậy, so với loại ngẫu nhiên và loại hoàn hảo.
