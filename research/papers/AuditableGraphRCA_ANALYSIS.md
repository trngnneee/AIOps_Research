# Auditable Graph-Guided Root Cause Analysis for Kubernetes Incidents

> **Đọc nhanh (30 giây):** Một agent RCA dựa trên **đồ thị bằng chứng có kiểu** (resource K8s, service, alert, trace, object tiêm lỗi) chạy trên ITBench. F1 tăng từ 0,6087 lên 0,9130. Điểm đáng giá nhất là **tác giả tự kiểm toán mức tăng**: bỏ gợi ý đặc thù kịch bản trong prompt thì còn 0,6958; phần tăng còn lại tập trung ở kịch bản ChaosMesh, nơi **object tiêm lỗi nằm sẵn trong đồ thị bằng chứng**, tức benchmark có "lối tắt".

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2606.08590 **v1** (07/06/2026) |
| Tác giả | Anastasiia Kuvshinova, Seungmin Jin (HSE University) |
| Venue | Preprint (8 trang) |
| PDF | https://arxiv.org/pdf/2606.08590v1 |
| Mức độ đọc | Abstract, §I–§II; chưa đọc §V–§IX chi tiết |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Bài học về **shortcut và rò rỉ nhãn**, áp dụng thẳng cho cách nhóm dùng Cloud-OpsBench |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper Abstract, §I]** Agent RCA có thể trông chính xác vì khai thác định danh đặc thù của benchmark, một quy tắc fallback tất định tự đưa đáp án khi agent không ra được, hoặc một judge dễ tính hơn judge của baseline. Câu hỏi: phần nào của mức tăng **sống sót** sau khi kiểm toán?

**Ví dụ [Diễn giải]:** học sinh đạt điểm cao vì đề thi in nhầm đáp án mờ mờ ở mặt sau. Điểm cao không phản ánh năng lực.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Snapshot sự cố ITBench (OpenTelemetry demo), biểu diễn thành đồ thị có kiểu gồm resource K8s, service, alert, entity từ trace, **object fault injection** |
| **Cơ chế** | State machine LangGraph: triage → duyệt ứng viên → tool chỉ đọc → **validation riêng** cho verdict → dựng chuỗi giải thích |
| **Output** | Tập root-cause entity đã phân loại + chuỗi giải thích |
| **Chấm** | Một LLM judge cố định (qwen-plus) |

## 3. Kết quả và kiểm toán [Paper Abstract]

- F1 root-cause entity: 0,6087 → **0,9130** trên tập chung 23 kịch bản (so với phiên bản trước của chính hệ thống).
- Prompt bỏ gợi ý đặc thù kịch bản: còn **0,6958** trên 19 kịch bản.
- Mức tăng còn lại tập trung ở **ChaosMesh**, nơi root cause đúng chính là object tiêm lỗi đã có sẵn trong đồ thị. Tác giả báo cáo là *benchmark-coupled*, không phải bằng chứng RCA tổng quát.
- Bộ kiểm tra nhẹ: so cùng judge, ablation prompt, kiểm nguồn cascade, **telemetry no-leak test**; mỗi claim gắn nhãn supported / pending / out of scope.
- Thử trên cụm thật không ổn định (alert và trace thay đổi), nên không claim gì về production.

## 4. Hạn chế

**Paper tự nhận:** chỉ ITBench OpenTelemetry-demo; một judge; không claim production hay MTTR.

**Người đọc nhận xét [Diễn giải]:** tập kịch bản rất nhỏ (19–23); judge là LLM; so với phiên bản trước của chính mình, chưa so nhiều baseline ngoài.

## 5. Nhóm khai thác được gì?

1. **Checklist chống rò rỉ cho thí nghiệm của nhóm:** trên Cloud-OpsBench phải kiểm agent **không** thấy fault plan, tên injector, tên file/metadata lộ nhãn (`metadata.json` chứa đáp án; tool không được đọc file này). Ghi rõ trong protocol.
2. **Phong cách báo cáo trung thực:** gắn nhãn supported / pending / out of scope cho từng claim. Rất hợp với yêu cầu của AGENTS.md trong repo.
3. **Liên hệ với hướng chốt [Giả thuyết]:** nếu một phần case Cloud-OpsBench "dễ" vì lộ manh mối mạnh ngay từ alert, thì độ tin cậy cao ở các case đó là **hợp lý**. Bộ dự đoán độ tin cậy cần được báo theo nhóm độ khó để không bị chi phối bởi case dễ.
4. **Phương án lùi "audit shortcut"** trong memo 07/11 đã có tiền lệ một phần ở paper này (ITBench) và ở 2510.04711 (RCA cổ điển).

## 6. Thuật ngữ

- **Shortcut / benchmark coupling:** lợi dụng đặc điểm riêng của benchmark để đạt điểm, không chuyển được sang hệ khác.
- **ChaosMesh:** công cụ tiêm lỗi cho Kubernetes; tạo object (ví dụ `NetworkChaos`) trong cụm, nên object này có thể làm lộ đáp án.
- **No-leak test:** kiểm tra dữ liệu agent thấy không chứa đáp án trực tiếp.
