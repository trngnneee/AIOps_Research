# UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing

> **Đọc nhanh (30 giây):** **Cascade** = để model nhỏ (rẻ) làm trước, case nào khó thì **chuyển lên model lớn** (đắt). Muốn chuyển đúng case thì điểm tin cậy phải **được hiệu chỉnh**. UCCI biến độ bất định thô thành xác suất sai bằng isotonic regression, rồi chọn ngưỡng chuyển bằng bài toán tối thiểu chi phí. Trên tác vụ NER thật 75.000 truy vấn: giảm **31% chi phí** mà giữ chất lượng, và tốt hơn entropy, conformal, FrugalGPT.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2605.18796 **v1** (11/05/2026) |
| Tác giả | Varun Kotte (nghiên cứu độc lập, một tác giả) |
| Venue | Preprint |
| Code | https://github.com/varunkotte6/ucci |
| PDF | https://arxiv.org/pdf/2605.18796v1 (9 trang) |
| Mức độ đọc | Abstract, §1–§2, kết quả chính, kết luận |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ **Công thức ra quyết định** chuyển tiếp (escalation) mượn được; domain khác hẳn |

---

## 1. Paper giải quyết vấn đề gì?

**Ví dụ [Diễn giải]:** tổng đài có nhân viên mới (rẻ) và chuyên gia (đắt). Nhân viên mới xử lý câu hỏi dễ, câu khó chuyển chuyên gia. Nếu nhân viên mới **tự tin sai** (không biết mình không biết) thì khách nhận câu trả lời tệ. Nếu chuyển **quá nhiều** thì tốn tiền chuyên gia. Cần một thước đo "khả năng mình sai" đáng tin.

- **[Paper §1]** Router đang dùng thường dựa trên điểm tin cậy chưa hiệu chỉnh và phải chỉnh ngưỡng thủ công cho từng workload.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Truy vấn; output của model nhỏ kèm token-margin uncertainty |
| **Bước 1** | Isotonic regression trên tập calibration: điểm bất định → xác suất sai |
| **Bước 2** | Chọn ngưỡng chuyển bằng tối thiểu chi phí kỳ vọng, có ràng buộc chất lượng |
| **Output** | Quyết định: giữ kết quả model nhỏ hay chuyển model lớn |

## 3. Môi trường và kết quả [Paper Abstract, §6]

- Workload NER production 75.000 truy vấn, 6 loại thực thể; model 4B và 12B trên GPU H100; chi phí đo bằng **latency thật**, không giả lập.
- ECE giảm 0,12 → 0,03. Tại micro-F1 = 0,91: chi phí 2,08 so với 3,02 khi chỉ dùng model lớn (giảm 31%, CI 95% [27%, 35%]).
- Ở cùng điểm vận hành, tốt hơn entropy thresholding (2,31), conformal routing (2,18), FrugalGPT-style (2,24).
- Thông điệp: **hiệu chỉnh trước, chọn ngưỡng sau**; phần lớn giá trị đến từ việc biến điểm thành xác suất.

## 4. Hạn chế

**Người đọc nhận xét [Diễn giải]:** một tác giả, chưa bình duyệt; tác vụ NER một bước, không phải agent; cần log-prob (token margin).

## 5. Nhóm khai thác được gì?

1. **Khung đánh giá cascade cho RCA [Giả thuyết]:** agent rẻ (ví dụ DeepSeek-V4-Flash, Qwen3.5-27B) chẩn đoán trước; chẩn đoán kém tin cậy chuyển lên agent mạnh (ví dụ GPT-5.x) hoặc **người**. Đo: JRA toàn hệ thống theo chi phí, so với "chỉ dùng model rẻ", "chỉ dùng model mạnh", "chuyển ngẫu nhiên cùng tỷ lệ".
2. **Công thức chọn ngưỡng có nguyên tắc:** chọn trên dev theo ràng buộc (ví dụ "selective error ≤ 10%"), khóa lại, rồi test. Tránh chỉnh ngưỡng trên tập test.
3. **Isotonic regression** là công cụ hiệu chỉnh đơn giản (có sẵn trong scikit-learn), hợp với sinh viên.
4. **Bài học báo cáo:** chi phí phải đo thật (token, latency) chứ không suy từ giá niêm yết.

## 6. Thuật ngữ

- **Cascade / routing:** chuỗi model từ rẻ tới đắt; router quyết định dừng ở đâu.
- **Isotonic regression:** hồi quy đơn điệu tăng; biến điểm thô thành xác suất mà vẫn giữ thứ tự.
- **Learning to defer:** học khi nào nên nhường quyết định cho chuyên gia (người hoặc model mạnh).
- **FrugalGPT:** phương pháp cascade nổi tiếng (2023) học ngưỡng dừng cho chuỗi LLM.
