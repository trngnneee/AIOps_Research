# Báo cáo quá trình đọc paper: Cloud-OpsBench

**Paper:** Cloud-OpsBench: A Reproducible Benchmark for Agentic Root Cause Analysis in Cloud Systems (arXiv 2603.00468, preprint)

**Tiến độ:** đang đọc §2 (Motivation), phần các gap trong quá trình đánh giá mô hình.

## 2. Motivation: các gap trong đánh giá mô hình

### Gap 1: Benchmark tĩnh (§2.2.1)

1. Thiếu sự tương tác giữa model và hệ thống: benchmark tĩnh chỉ cung cấp sẵn một tập metric/log.
2. Tập metric/log tĩnh có thể dùng để chạy lại đánh giá (tái lập được).
3. Vì evidence đã được cung cấp sẵn, model không phải lựa chọn tool để xử lý, nên benchmark không kiểm tra được khả năng chọn tool đúng đắn.
4. Kết quả: việc đánh giá chỉ dựa trên tập dữ liệu đã được cung cấp.

### Gap 2: Biến thiên giữa các lần chạy live (§2.2.2)

Cho agent làm việc trên hạ tầng thực tế, lấy metric/log trực tiếp thay vì tập tĩnh, thì có hai vấn đề:

**Vấn đề 1: Khó so sánh giữa các model**
- Hai hạ tầng, môi trường ở các thời điểm và điều kiện khác nhau thì fault biểu hiện khác nhau (mức độ, thời gian, phạm vi ảnh hưởng), nên AI có thể đưa ra kết luận khác nhau.
- Vì vậy chênh lệch kết quả không thể quy hoàn toàn cho năng lực của agent, và chạy lặp chỉ ước lượng được trung bình và phương sai, không tạo được điều kiện giống nhau để so sánh từng cặp model.

**Vấn đề 2: Chi phí chuẩn bị môi trường tốn effort**
- Mỗi lần chạy phải: tạo trạng thái hệ thống sạch (clean state), warm up workload, kích hoạt và verify lỗi để monitor, để agent điều tra, rồi khôi phục môi trường trước lần chạy kế tiếp.
- Paper đang so sánh năng lực nhiều AI, nên cần môi trường lặp lại cho mọi tổ hợp fault case × model × cấu hình. Khi mở rộng quy mô ở nhiều khía cạnh, chi phí này tăng theo cấp số nhân, khiến việc so sánh quy mô lớn và lặp nhanh khi cải tiến agent trở nên khó.

**Nhận xét riêng của người đọc (không phải của paper):** kết luận của AI trên hạ tầng thực tế có thể có giá trị hơn kết luận trên tập tĩnh. Paper chỉ thừa nhận live environment có giá trị ở chỗ kiểm tra độ bền trước sự bất định của môi trường thật.

### Gap 3: Chỉ đánh giá theo kết quả cuối (§2.2.3)

**Vấn đề:** các RCA benchmark hiện tại chủ yếu chấm bằng điểm số theo các phương pháp như top-k accuracy, precision, recall, F1, nên không đánh giá được quá trình AI thu thập dữ liệu để có được kết quả đó. Các metric này vẫn cần thiết để đo độ đúng của chẩn đoán.

**Ví dụ:** hai AI agent đưa ra cùng một đáp án nhưng theo hai cách khác nhau:
- Agent A thu thập danh sách observation đúng với tình trạng của hệ thống, nối được triệu chứng với root cause.
- Agent B đoán bừa (unsupported guess).
- Hai bên nhận điểm như nhau, dù quá trình hoàn toàn khác nhau.

**Trường hợp ngược lại:** agent điều tra có cơ sở nhưng kết luận cuối sai thì không phân biệt được với agent không điều tra gì (cả hai cùng bị tính là sai).

**Ý của tác giả:** việc đánh giá không nên chỉ dựa vào kết luận cuối của AI. Cần bổ sung (complement) thêm quá trình AI lấy số liệu quan sát, bên cạnh độ đúng của kết luận.
- "Quá trình" được đo trên các lần gọi tool và observation nhận được (observable tool-mediated investigation), không phải lập luận do agent tự thuật (self-reported reasoning).
- Ba tiêu chí của quá trình: completeness (đủ bằng chứng), causal coherence (đúng thứ tự nhân quả), efficiency (hiệu quả).

**Lý do cốt lõi (construct validity):** khả năng benchmark tuyên bố đo gồm chọn hành động chẩn đoán, thu thập observation và lập luận nhân quả, nhưng metric chỉ đo dự đoán cuối.
