# TriFleetRCA: On-Premise LLM Root Cause Analysis for Kubernetes

> **Đọc nhanh (30 giây):** Nhiều nơi **không được gửi log ra API ngoài**. Paper chạy toàn bộ RCA trên **một GPU tại chỗ** với Qwen2.5-14B, trên **cụm Kubernetes thật** với 4 lỗi tiêm vào (100 lần phân tích). Hit rate 0,85–0,95 tùy phạm vi lấy bằng chứng (pod / namespace / cluster). Thêm hai ý hay: **chống runbook bị đầu độc** và **tách "đúng" với "đúng và trích dẫn đúng"**.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2609.23766 **v1** (20/09/2026), category cs.CR |
| Tác giả | Rohit Patel, Susil Kumar Mohanty, Jeenal Chaudhary (IIT Jodhpur) |
| Venue | Preprint (8 trang) |
| Code | Paper nói công bố pipeline, fault injector và toàn bộ bản ghi từng lần phân tích **[Chưa kiểm link]** |
| PDF | https://arxiv.org/pdf/2609.23766v1 |
| Mức độ đọc | Abstract, §I–§III, các câu kết quả RQ |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★☆☆ Tham khảo về tính khả thi (một GPU, cụm thật nhỏ) và metric trích dẫn |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper §I]** Ở các site xa (nhà máy, trạm viễn thông), bằng chứng nằm rải rác ở pod logs, Kubernetes events và object mức cluster (NetworkPolicy…). Hai ràng buộc: (1) không được gửi log tới model hosted; (2) runbook có thể bị ai đó sửa, chèn lệnh độc.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Sự cố trên cụm K8s; bằng chứng lấy theo **scope** pod / namespace / cluster |
| **Xử lý** | Khử trùng lặp theo template log → xếp hạng BM25 → lọc runbook qua *ingest guard* → LLM local |
| **Output** | Root cause + các dòng bằng chứng hỗ trợ |
| **Metric mới** | *Grounded citation*: chỉ tính đúng khi dòng được trích thật sự chứa tín hiệu lỗi |

## 3. Môi trường thực nghiệm

- Cụm Kubernetes thật; 4 loại lỗi; mỗi trial một namespace mới; cửa sổ log giới hạn theo thời điểm inject để tránh rò bằng chứng giữa các trial.
- **Qwen2.5-14B-Instruct**, temperature 0, một GPU workstation; 100 lần phân tích.

## 4. Kết quả chính [Paper Abstract, §VI]

- Hit rate 0,85 / 0,90 / 0,95 ở pod / namespace / cluster scope; khoảng tin cậy chồng nhau; **toàn bộ** hiệu ứng scope đến từ đúng một lỗi có nguyên nhân là object mức cluster. Cluster scope tốn nhiều prompt token hơn đáng kể.
- Khử trùng lặp template trước khi xếp hạng: hit rate 0,75 → 0,90 với cùng chi phí token.
- Runbook độc yêu cầu xóa namespace: guard chặn ở mọi lần; tắt guard thì model vẫn từ chối làm theo trong cả 20 lần.
- **Một lỗi được chẩn đoán đúng nhưng trích dẫn sai ở mọi trial.** Accuracy một mình che mất lỗi này.
- Latency trung vị 1,6 giây với khoảng 2.200 prompt token.

## 5. Hạn chế

**Paper tự nhận [§VIII]:** 4 loại lỗi, 1 model, 1 cụm, **n = 20 mỗi ô** nên khoảng tin cậy rộng và phần lớn so sánh chồng nhau (không claim khác biệt có ý nghĩa giữa các scope); chỉ một họ model (Qwen2.5-14B); kết quả guard chỉ cho **một kiểu tấn công** viết rất lộ liễu; BM25 khớp từ chứ không khớp nghĩa; chỉ một site.

**Người đọc nhận xét [Diễn giải]:** đây là nghiên cứu khả thi, chưa phải benchmark.

## 6. Nhóm khai thác được gì?

1. **Chứng minh tính khả thi cho sinh viên:** RCA trên K8s chạy được với một GPU và model 14B. Nếu nhóm muốn có **model local** làm "agent rẻ" trong cascade, đây là tham chiếu.
2. **Metric "đúng nhưng trích dẫn sai":** củng cố ý ungrounded diagnosis (OpenRCA 2.0, Cloud-OpsBench). Nhóm có thể dùng như một đặc trưng: chẩn đoán có trích dẫn observation thật không.
3. **Cách tránh rò bằng chứng giữa các trial** (namespace mới, cửa sổ log giới hạn) là bài học tốt nếu nhóm phải dựng cụm thật. Hướng chốt dùng replay nên không cần.
4. **Prompt injection qua runbook:** một hướng an toàn AIOps thú vị nhưng **ngoài phạm vi** đề tài chính.

## 7. Thuật ngữ

- **On-premise:** chạy trên máy chủ của chính tổ chức, không gửi dữ liệu ra ngoài.
- **BM25:** thuật toán xếp hạng văn bản theo từ khóa (cổ điển, không cần học sâu).
- **Runbook:** tài liệu hướng dẫn xử lý sự cố từng bước.
- **Prompt injection / knowledge poisoning:** chèn chỉ dẫn độc vào tài liệu mà model sẽ đọc.
