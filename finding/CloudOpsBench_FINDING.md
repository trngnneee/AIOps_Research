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
4. ECR là 0/1 theo case (định nghĩa ở §4.1.1 mục (2), trang 8) nên khuếch đại sự chủ quan: thêm một nhóm bắt buộc là case có thể rớt từ 1 về 0.
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

## Finding 2: Khoảng cách JRA–ECR không chỉ phản ánh việc agent điều tra nông

**Vị trí trong paper:** §4.3 (RQ2, trang 9–10), Table 4, Fig. 3. Định nghĩa ECR ở §4.1.1; quy trình dựng D* ở §3.3.3.

### Phần khách quan (paper nói)
- JRA cao nhưng ECR thấp, nhất quán qua các model và hệ thống (Table 4):
  - OnlineBoutique: DeepSeek-V4-Flash có JRA 0,76 nhưng ECR 0,38; GPT-5 có 0,68 nhưng 0,21; Qwen3.5-27B có 0,70 nhưng 0,43.
  - TrainTicket: GPT-5 có 0,68 nhưng 0,15; DeepSeek-V4-Flash có 0,63 nhưng 0,24.
- Cách paper diễn giải: agent suy ra đúng cặp component–fault từ tín hiệu cục bộ mạnh (Pod status bất thường, alert, lỗi service) mà không dựng đủ chuỗi chẩn đoán. Paper gọi đây là "ungrounded diagnosis" và cho rằng với SRE, đúng nhãn là chưa đủ, cần biết bằng chứng nào hỗ trợ quyết định can thiệp.
- MC ở mức trung bình đến cao nhưng ECR thấp ("broad but shallow"). Khoảng cách MC → ECR lớn hơn nhiều so với MC → EOC.

### Nhận định của người đọc
- D* được dựng bằng cách đi ngược toàn bộ chuỗi nhân quả, từ triệu chứng về cơ chế lỗi (§3.3.3). Vì vậy ECR đòi agent thiết lập đủ chuỗi giải thích này, nên ECR thấp là dễ hiểu.
- JRA cao cũng dễ hiểu: agent không nhất thiết phải đi hết chuỗi nhân quả mới suy ra được lỗi. Một vài tín hiệu nổi bật có thể đã đủ để xác định đúng component và fault type.
- Tức là JRA và ECR đo hai thứ khác nhau:
  - Đủ bằng chứng để xác định lỗi (sufficiency).
  - Đủ bằng chứng để giải thích theo chuẩn của người gán nhãn (completeness). ECR đo cái này.
- Paper quy toàn bộ khoảng cách JRA–ECR cho hạn chế của agent. Trong §4.3 không thấy paper xét khả năng một phần khoảng cách đến từ việc D* đòi nhiều hơn mức tối thiểu cần để xác định lỗi. Điểm này nối với Finding 1 (tính chủ quan của D* và ECR chấm 0/1).

### Điểm cần cân nhắc (chưa chốt)
- JRA cao chưa chứng minh agent đã có đủ bằng chứng tối thiểu: agent cũng có thể đoán đúng nhờ kiến thức nền. Không có phân tích theo từng case thì không tách được hai trường hợp này.
- Paper khẳng định milestone là "necessary for diagnosis". K* (milestone thay thế nhau) và nhiều evidence bundle được thiết kế để không đòi hỏi quá mức, và tiêu chí audit có "non-redundancy". Vì vậy giả thuyết "nhãn đòi hỏi quá mức" đang mâu thuẫn với claim của paper và cần dữ liệu để kiểm.
- Khoảng cách không chỉ đi theo một chiều. Fig. 3 có trường hợp ECR cao mà JRA thấp: Qwen3-235B-A22B ở TrainTicket mức Hard có JRA 0,09 nhưng ECR 0,52; Qwen3-14B ở OnlineBoutique mức Easy có JRA 0,56 nhưng ECR 0,77. Có đủ bằng chứng nhưng vẫn kết luận sai, nên còn có lỗi ở bước tổng hợp, không chỉ do nhãn.
- Paper so hai tỷ lệ tính riêng trên toàn bộ case, không báo cáo tỷ lệ case "JRA đúng nhưng ECR = 0". Từ Table 4 chỉ suy ra được chặn dưới, ví dụ GPT-5 ở OnlineBoutique có ít nhất 0,68 − 0,21 = 0,47 số case như vậy.

### Hàm ý cho đề tài
- Với selective RCA, câu hỏi "đã đủ bằng chứng để kết luận chưa" gần với sufficiency hơn completeness. Không nên dùng thẳng ECR làm oracle cho quyết định commit hay abstain. Đây là hướng cần kiểm chứng, chưa phải gap đã được chứng minh.
- Khi đánh giá, báo cáo bảng chéo JRA × ECR theo từng case (4 ô), không chỉ hai tỷ lệ riêng.
- Với các case JRA = 1, ECR = 0: xem nhóm milestone nào bị thiếu. Nếu thường là các nhóm xác nhận triệu chứng ở đầu chuỗi thì nghiêng về nhãn đòi hỏi quá mức; nếu là các nhóm gần cơ chế lỗi thì nghiêng về agent đoán.
- Có thể thử gán thêm nhãn "tập bằng chứng tối thiểu đủ để xác định lỗi" trên một mẫu nhỏ, rồi so với D*.

### Chưa kiểm chứng
- Paper có công bố trajectory theo từng case (trong artifact) để tính bảng chéo JRA × ECR không: chưa kiểm tra.
- Appendix có phân tích các case đúng nhưng không đóng được đồ thị không: chưa đọc.

## Finding 3: Dòng Base ở RQ3 có thể không cùng tập case với ICL/SOP

**Vị trí trong paper:** §4.4 (RQ3, trang 10–11), Table 5 so với Table 4.

### Phần khách quan
- §4.4: với mỗi root cause, case được chia thành tập train và test riêng biệt, tỷ lệ khoảng 1:1. Kho kinh nghiệm lấy từ trajectory thành công của GPT-5 trên tập train; tập test "reserved for evaluation".
- Dòng Base ở Table 5 trùng từng chữ số với Table 4 cho cả 3 model (DeepSeek-V4-Flash, Gemini-2.5-Flash, Qwen3.5-27B), cả 2 hệ thống và mọi metric. Ví dụ DeepSeek-V4-Flash ở OnlineBoutique: 0,88 / 0,77 / 0,76 / 0,74 / 0,64 / 0,38 / 0,62 / 6,45 ở cả hai bảng.
- Phần đã đọc không nói Table 4 được tính trên toàn bộ 754 case hay chỉ trên tập test.

### Nhận định của người đọc
- Nếu Table 4 tính trên toàn bộ case thì Base ở Table 5 được chấm trên train + test, còn ICL và SOP chỉ được chấm trên tập test. Hai bên không cùng tập case.
- Vấn đề không phải Base được học gì: Base không học, chạy trên case train không gian lận. Vấn đề là điểm là trung bình trên một tập case, đổi tập case thì điểm đổi theo dù agent giữ nguyên. Muốn đo tác dụng của kinh nghiệm thì Base, ICL, SOP phải cùng chạy trên đúng một tập case.
- Cũng không phải do số lượng khác nhau: điểm là tỷ lệ, nên vấn đề là hai bên chấm trên những case khác nhau.
- Suy luận hỗ trợ (chưa chắc): kho kinh nghiệm lấy từ trajectory của GPT-5 trên tập train, gợi ý lần chạy chính (Table 4) có bao gồm các case train.

### Mức độ ảnh hưởng
- Có thể nhỏ: chia 1:1 theo từng root cause nên hai nửa có thành phần loại lỗi gần giống nhau. Mức tăng lớn như ECR ở OnlineBoutique (0,39 lên 0,59 và 0,61) khó chỉ do chênh tập case.
- Đáng lo với chênh lệch nhỏ: ở TrainTicket, SOP tăng JRA từ 0,58 lên 0,62 và ICL giảm xuống 0,56. Paper không báo cáo chạy lặp hay khoảng tin cậy, và tập test chỉ khoảng một nửa số case, nên các mức này chưa đủ để kết luận.
- Câu viết đúng mức: "Paper không nói rõ dòng Base ở Table 5 được tính trên tập nào. Các số trùng hoàn toàn với Table 4 gợi ý Base có thể được chấm trên tập case khác với ICL/SOP. Nếu đúng vậy, các chênh lệch nhỏ (ví dụ trên TrainTicket) chưa đủ để kết luận." Không viết "kết quả sai".

### Điểm liên quan
- Paper giải thích kết quả không đều ở TrainTicket bằng retrieval granularity nhưng không đo độ chính xác truy vấn (ví dụ tỷ lệ case lấy về có cùng root cause). Đây là diễn giải, chưa được kiểm.
- Train và test có cùng tập root cause, nên RQ3 chỉ đo dùng lại kinh nghiệm cho loại lỗi đã gặp.

### Hàm ý cho đề tài
- Khi so một phương pháp với baseline, chạy baseline lại trên đúng tập đánh giá của phương pháp (paired comparison), và báo cáo rõ tập case của từng bảng.
- Với chênh lệch nhỏ, dùng kiểm định theo cặp trên từng case (ví dụ McNemar cho JRA) hoặc bootstrap khoảng tin cậy.
- Nếu dùng retrieval, đo trực tiếp chất lượng truy vấn thay vì chỉ suy ra từ kết quả cuối.

### Chưa kiểm chứng
- Table 4 tính trên toàn bộ case hay chỉ tập test: chưa thấy paper nói rõ; cần xem appendix hoặc artifact.
- Danh sách case train/test có được công bố không: chưa kiểm tra.
