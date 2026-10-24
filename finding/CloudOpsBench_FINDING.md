# Finding: Cloud-OpsBench

**Paper:** Cloud-OpsBench: A Reproducible Benchmark for Agentic Root Cause Analysis in Cloud Systems (arXiv 2603.00468, preprint)

**Trạng thái:** nhận xét của người đọc, chưa xác nhận hết với bản gốc. Đây không phải kết luận của paper.

## Finding 1: Nhãn quá trình (D*) có phần chủ quan

**Vị trí trong paper:** §3.3.3 (Ground-Truth Annotation).

### Phần khách quan
- R* lấy từ fault plan đã verify, không cần phán đoán.
- Chuỗi nhân quả gốc (cơ chế lỗi đến triệu chứng) đã được xác lập lúc verify (§3.3.1).
- Mỗi evidence clause trỏ tới một mục có thật trong kho response, và replay kiểm tra được bằng chứng đó đạt được.

### Phần chủ quan
Chuỗi nhân quả cho biết lỗi xảy ra thế nào, còn D* phải trả lời agent cần biết những gì để tin vào kết luận. Bước chuyển này phụ thuộc phán đoán của người gán nhãn ở các điểm:
- Sự thật nào là cần thiết, sự thật nào là thừa.
- Cắt thế nào là nguyên tử.
- Hai sự thật nào thay thế nhau (gom cùng nhóm).
- Thứ tự phụ thuộc giữa các nhóm.

Replay tự động chỉ kiểm tra được bằng chứng đạt được, không kiểm tra được nhãn có đầy đủ và đúng mức cần thiết hay không.

### Biện pháp của paper
- Hai auditor review độc lập, bị che fault plan.
- Một chuyên gia cấp cao phân xử bất đồng.
- 9,4% đồ thị bị sửa, cho thấy lỗi hoặc bất đồng là có thật.

### Điểm yếu còn lại
1. Chưa thấy chỉ số đồng thuận giữa người gán nhãn (inter-annotator agreement) trong phần đã đọc.
2. Người gán nhãn đều thuộc nhóm tác giả. Paper không nói rõ hai auditor có độc lập với ba người gán nhãn hay không.
3. Chưa thấy kiểm chứng ngoài, ví dụ so nhãn với đánh giá của người khác hoặc thử nhãn của người gán khác.
4. ECR là 0/1 theo case nên khuếch đại sự chủ quan: thêm một nhóm bắt buộc là case có thể rớt từ 1 về 0.
5. Agent đoán đúng nhờ kiến thức sẵn có mà không đi theo milestone vẫn bị tính thiếu quá trình (paper nhắc trong phần threats).

### Hàm ý cho đề tài
- Proposal đã ghi rủi ro "oracle chủ quan". Đây là chỗ cụ thể để xử lý.
- Dùng hai người gán nhãn độc lập và báo cáo chỉ số đồng thuận (ví dụ Cohen's kappa).
- Thêm phân tích độ nhạy: đổi cách gán nhãn và xem kết luận có đổi không.
- Với nhãn "evidence đủ/không đủ", chốt tiêu chí trước, dùng oracle độc lập, không dùng LLM judge.
- Khi viết luận văn, nói đúng mức: "paper không báo cáo chỉ số đồng thuận", không viết "nhãn sai".

### Chưa kiểm chứng
- Appendix của paper có thể có số liệu về độ đồng thuận mà chưa đọc (khoảng 29.000 ký tự cuối của bản HTML chưa được đọc).
- Chưa kiểm tra mức độc lập giữa auditor và người gán nhãn.
