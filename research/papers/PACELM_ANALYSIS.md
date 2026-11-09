# PACE-LM: Prompting and Augmentation for Calibrated Confidence Estimation with GPT-4 in Cloud Incident RCA

> **Đọc nhanh (30 giây):** Bài AIOps **gần nhất về chủ đề "độ tin cậy của chẩn đoán RCA"**, từ Microsoft (2023). Ý tưởng: kỹ sư on-call cần biết **có nên tin** gợi ý root cause của LLM hay không. Họ dùng GPT-4 chấm độ tin cậy qua 2 bước: (1) "dữ liệu sự cố cũ có đủ căn cứ để phán không?", (2) "gợi ý này hợp lý tới đâu so với sự cố cũ?", rồi gộp thành điểm đã hiệu chỉnh.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2309.05833 **v3** (29/09/2023) |
| Tác giả | Shizhuo Dylan Zhang (UIUC), Xuchao Zhang, Chetan Bansal, Pedro Las-Casas, Rodrigo Fonseca, Saravan Rajmohan (Microsoft) |
| Venue | Bản mở rộng/đổi tên **LM-PACE** ở FSE 2024 Industry track (theo kết quả tìm kiếm; chưa đối chiếu nội dung hai bản) |
| PDF | https://arxiv.org/pdf/2309.05833v3 |
| Mức độ đọc | Abstract, §1, RQ, setup §5.1, kết luận; chưa đọc kỹ bảng số |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★★ **Tiền lệ AIOps trực tiếp** cho "confidence của RCA"; khác ở chỗ không phải agent, dữ liệu kín |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper Abstract, §1]** LLM gợi ý root cause có độ chính xác thấp và hay ảo giác "ngụy trang khéo". Kỹ sư khó phân biệt gợi ý tốt và xấu, nên mất thời gian đi theo gợi ý sai.
- Root cause predictor thường là **black-box**, nên không fine-tune hay temperature scaling được. Cần phương pháp chỉ dựa vào prompting.

**Ví dụ [Diễn giải]:** giống trợ lý y khoa AI kèm dòng chữ "độ tin cậy: thấp, vì chưa từng gặp ca tương tự". Bác sĩ biết khi nào nên tự kiểm lại.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Mô tả sự cố hiện tại + root cause do một predictor (LLM) đưa ra + các sự cố lịch sử tương tự (retrieval) |
| **Bước 1 (COE)** | GPT-4 đánh giá "dữ liệu tham chiếu có đủ để phán sự cố này không" (mức grounded-ness) |
| **Bước 2 (RCE)** | GPT-4 chấm gợi ý root cause dựa trên sự cố lịch sử |
| **Bước 3** | Tối ưu cách gộp hai điểm theo tiêu chí ECE trên tập validation |
| **Output** | Điểm tin cậy đã hiệu chỉnh cho từng gợi ý |

## 3. Môi trường thực nghiệm [Paper §5.1]

- **121.308 sự cố** thật của "CompanyX" (Microsoft): 98.308 làm kho truy hồi, 2.000 validation, 3.000 test.
- Ngân sách token cho sự cố truy hồi khoảng 3.896 token mỗi mẫu.
- Không công bố dữ liệu (proprietary).

## 4. RQ và câu trả lời [Paper §5.2]

| RQ | Trả lời (theo tóm tắt kết quả của paper) |
|---|---|
| RQ1: Ước lượng confidence chính xác được không? | Được, sau bước tối ưu gộp điểm; điểm thô của model không được thang hóa đều |
| RQ2: Sự cố lịch sử có giúp calibration? | Có; khi gặp sự cố lặp lại, bộ ước lượng kiểm trực tiếp được gợi ý |
| RQ3: Model tự phân tích có giúp? | Có; phương pháp đầy đủ luôn tốt nhất trong bảng ablation |
| RQ4: Tổng quát qua nhiều predictor? | Có, áp dụng cho nhiều root cause predictor |

Bản FSE 2024 (LM-PACE) báo giảm ECE còn khoảng 31% so với prompting trực tiếp (theo kết quả tìm kiếm, **[Chưa kiểm]** trong bản FSE).

## 5. Hạn chế

**Người đọc nhận xét [Diễn giải]:**
- **Không phải agent:** predictor đưa ra một gợi ý từ mô tả sự cố; không có trajectory gọi tool để phân tích.
- Phụ thuộc **kho sự cố lịch sử lớn** của doanh nghiệp. Benchmark công khai như Cloud-OpsBench không có kho này. Có thể dùng case train làm "lịch sử", nhưng đó là thiết lập khác.
- Dữ liệu kín, không tái lập được. Thời điểm 2023 (GPT-4), model hiện nay đã khác nhiều.

## 6. Nhóm khai thác được gì?

1. **Câu chuyện động lực công nghiệp:** Microsoft đã coi "confidence cho gợi ý RCA" là vấn đề thật của on-call. Dùng để trả lời câu hỏi hội đồng "vấn đề này có ai quan tâm ngoài đời không?".
2. **Khoảng cách cần nói rõ khi viết related work:** PACE-LM làm cho **RCA một bước, dữ liệu kín, dựa vào lịch sử**. Hướng nhóm làm cho **agent nhiều bước, benchmark mở, dựa vào quá trình điều tra**. Đây là khác biệt thật, nhưng phải viết là "theo những gì nhóm tìm được".
3. **Baseline có thể chuyển thể:** "LLM judge chấm chẩn đoán" (một model mạnh đọc trajectory rồi chấm độ tin cậy) là phiên bản hiện đại của RCE. Đưa vào danh sách đối chứng, nhớ tính chi phí judge.
4. **Mục tiêu tối ưu ECE trên validation, khóa lại rồi mới test:** đúng quy trình nhóm cần làm.

## 7. Thuật ngữ

- **Retrieval-augmented:** lấy thêm tài liệu/sự cố tương tự đưa vào prompt.
- **OCE (on-call engineer):** kỹ sư trực sự cố.
- **Grounded-ness:** mức độ kết luận có chỗ dựa trong dữ liệu tham chiếu.
