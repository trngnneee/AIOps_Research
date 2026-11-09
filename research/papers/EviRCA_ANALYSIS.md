# EviRCA: Decoupling Evidence Extraction from Reasoning for Microservice Root-Cause Analysis

> **Đọc nhanh (30 giây):** Đừng bắt LLM vừa đào telemetry thô vừa suy luận. EviRCA dùng một bước **tất định** (không LLM) để biến metrics/traces/logs thành vài **"thẻ bằng chứng"** gọn, rồi LLM chỉ suy luận trên các thẻ này qua vài tool chỉ đọc. Trên OpenRCA: đúng 40,6–43,9% (baseline cũ tối đa 15,2%), token giảm 15–26 lần. Phân tích lỗi: khó nhất là **đánh giá bằng chứng đã được đưa ra**, không phải tìm bằng chứng.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2609.19825 **v1** (17/09/2026) |
| Tác giả | Yuhao Wang, Zhen Qin, …, Shuiguang Deng (Zhejiang University; China Telecom Cloud) |
| Venue | Preprint (12 trang) |
| PDF | https://arxiv.org/pdf/2609.19825v1 |
| Mức độ đọc | Abstract, §I, RQ1–RQ4 (câu kết luận), các đoạn phân tích theo hệ thống |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Bằng chứng thứ hai (sau HowFarRCA) rằng nút thắt là **suy luận**, không phải dữ liệu |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper Abstract, §I]** Agent kiểu OpenRCA viết và chạy code Python trên telemetry thô. Một model phải cùng lúc truy xuất bằng chứng, định vị lỗi và suy ra nguyên nhân trên khối dữ liệu khổng lồ. Kết quả: tốn kém (gần một triệu token mỗi case), không ổn định, độ chính xác thấp.

**Ví dụ [Diễn giải]:** thay vì đưa thám tử cả kho băng camera 24 giờ, ta nhờ máy lọc sẵn 10 đoạn có người lạ ra vào, rồi thám tử chỉ cần suy luận trên 10 đoạn đó.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Telemetry thô của OpenRCA (metrics, traces, logs) |
| **Bước 1 (không LLM)** | Trích xuất "evidence cards" đa phương thức, độc lập với hệ thống cụ thể |
| **Bước 2 (LLM)** | Suy luận qua vài tool chỉ đọc trên các thẻ, **không** đọc dữ liệu thô, **không** chạy code |
| **Output** | Thời điểm, component, lý do root cause theo yêu cầu của OpenRCA |

## 3. Môi trường thực nghiệm

- OpenRCA (3 hệ thống doanh nghiệp: Bank, Telecom, Market).
- 2 LLM: **deepseek-v4-pro** và **qwen3.7-plus** [Paper §IV].
- Có một baseline "Oracle Sampling": chỉ lấy KPI đã được kỹ sư chọn sẵn là có giá trị chẩn đoán, như cận trên cho phương pháp lấy mẫu.

## 4. RQ và câu trả lời [Paper §IV]

| RQ | Trả lời |
|---|---|
| RQ1: Hiệu quả? | Correct 40,6–43,9% so với tối đa 15,2% của baseline cùng model |
| RQ2: Chi phí? | Token giảm 15–26 lần, thời gian giảm 3–20 lần (với deepseek-v4-pro) |
| RQ3: Ablation? | Đóng góp từng module khác nhau theo hệ thống; trên Market các module gần như không tác dụng |
| RQ4: Lỗi còn lại? | Nút thắt là **phán đoán** trên bằng chứng đã được đưa ra: chọn sai giữa các manh mối. Oracle Sampling cho thấy "biết chỗ để nhìn" chưa quyết định được ứng viên nào là nguyên nhân |

**Theo hệ thống:** Telecom mạnh nhất (62,7% Correct), lỗi gần như toàn do chọn sai giữa manh mối. Bank 52,2%, lỗi chia cho chọn, quy kết, đa lỗi. Market yếu nhất (29,7%) vì nhiều case đa lỗi và lỗi mạng không được tầng bằng chứng đưa ra.

**Thêm từ §V-A [Paper]:** trong các case một lỗi mà EviRCA sai, component đúng **vắng mặt** trong thẻ bằng chứng chỉ ở 22,5% case, tức phần lớn lỗi là phán đoán sai trên bằng chứng có sẵn. **81–87% case sai là trùng nhau giữa hai LLM**, nên thay model cùng tầm năng lực khó giải quyết được.

## 5. Hạn chế

**Paper tự nhận [§V-B]:** tầng bằng chứng quyết định trần hiệu năng. Nếu tín hiệu lỗi thật không lọt vào thẻ (thiếu modality, độ mịn thô, luật phát hiện không hợp), LLM phía sau không khôi phục được. Với lỗi mạng thất bại ở Market, component đúng vắng mặt trong bằng chứng ở 89,6% case (Bank 8,5%, Telecom 0%). EviRCA kế thừa giả định của OpenRCA (tập ứng viên component và lý do đóng).

**Người đọc nhận xét [Diễn giải]:**
- Chỉ OpenRCA (dữ liệu tĩnh). Bước trích xuất cần thiết kế cho loại telemetry đó.
- Agent luôn phải chốt; không có cơ chế báo "chưa đủ".
- Phân rã lỗi làm **sau khi chạy** và dựa vào nhãn (post-hoc).

## 6. Nhóm khai thác được gì?

1. **Hai paper độc lập (EviRCA và HowFarRCA) cùng kết luận "lỗi chủ yếu ở suy luận trên bằng chứng có sẵn".** Đây là luận cứ mạnh cho hướng chốt: nếu agent thường **có** bằng chứng mà vẫn kết luận sai, thì cần một lớp **kiểm tra/ước lượng độ tin cậy** quyết định khi nào tin kết luận. Thêm dữ liệu không đủ.
2. **Thiết kế "tách trích xuất và suy luận":** nếu nhóm cần giảm chi phí, có thể tiền xử lý tool output trước khi đưa LLM. Không cần cho hướng chốt.
3. **Baseline Oracle Sampling:** ý tưởng cận trên "cho biết chỗ để nhìn" hữu ích khi nhóm muốn tách phần lỗi do tìm kiếm và do phán đoán.
4. **Cảnh báo cho RQ3 (cascade):** 81–87% case sai trùng nhau giữa hai LLM. Nếu điều này cũng đúng trên Cloud-OpsBench, chuyển case khó sang **model khác** sẽ ít tác dụng; chuyển cho **người** mới có ích. RQ3 phải đo mức trùng lỗi giữa các model trước khi kết luận.

## 7. Thuật ngữ

- **Evidence card:** bản tóm tắt có cấu trúc của một bất thường (ví dụ "CPU pod X tăng 300% lúc 10:02").
- **Deterministic extraction:** bước xử lý cho cùng kết quả mỗi lần chạy, không dùng LLM.
- **Multi-fault:** sự cố có nhiều nguyên nhân đồng thời.
