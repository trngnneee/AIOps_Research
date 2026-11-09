# TRACER: Trajectory Risk Aggregation for Critical Episodes in Agentic Reasoning

> **Đọc nhanh (30 giây):** Agent dùng tool thường hỏng vì **vài khoảnh khắc then chốt** (lặp vòng, gọi tool không khớp kết quả, lệch ý người dùng), không phải vì cả quá trình đều kém. TRACER chấm **rủi ro từng bước** bằng 4 tín hiệu rồi lấy **phần tệ nhất** (tail) thay vì trung bình. Trên τ²-bench, AUROC tăng tới 37,1% và AUARC tăng tới 55% so với baseline, dùng được cho việc **từ chối thực thi có chọn lọc**.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2602.11409 **v1** (11/02/2026) |
| Tác giả | Sina Tayebati, …, Amit Ranjan Trivedi (University of Illinois Chicago; Capital One AI Labs) |
| Venue | ICML 2026 poster (theo trang ICML) |
| Code | https://github.com/sinatayebati/agent-tracer |
| PDF | https://arxiv.org/pdf/2602.11409v1 |
| Mức độ đọc | Abstract, §I–§II, phương pháp (Figure 1), câu kết luận chính; chưa đọc chứng minh |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★★ Ý tưởng "rủi ro tập trung ở vài bước" và tín hiệu lặp/không khớp rất hợp với agent RCA |

---

## 1. Paper giải quyết vấn đề gì?

**Ví dụ [Diễn giải]:** một chuyến bay an toàn 99% thời gian, nhưng tai nạn xảy ra vì 30 giây sai sót lúc hạ cánh. Lấy trung bình độ an toàn cả chuyến sẽ che mất 30 giây đó. TRACER nhìn vào "30 giây tệ nhất".

- **[Paper Abstract, §I]** Thất bại của agent thường do *sparse critical episodes* (lặp vòng, dùng tool không mạch lạc, lệch phối hợp với user) trong khi từng đoạn sinh văn bản vẫn có vẻ tự tin. Các proxy bất định cũ được làm cho sinh văn bản một lần nên bỏ sót.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Trajectory nhiều lượt Tool–Agent–User kèm log-prob |
| **Tín hiệu mỗi bước** | (1) surprisal có trọng số theo nội dung; (2) lặp lại của agent (ngữ nghĩa, từ vựng); (3) **lệch hành động–quan sát** (tool-grounded coherence gap); (4) lệch phối hợp user–agent |
| **Gộp** | Rủi ro bước = MAX của các tín hiệu đã chuẩn hóa; rủi ro trajectory = trung bình top-K và chuẩn vô cùng (tail-focused) |
| **Output** | Một điểm rủi ro cho cả trajectory, dùng để dự đoán thất bại hoặc quyết định có thực thi không |

## 3. Môi trường thực nghiệm

- **τ²-bench** (agent chăm sóc khách hàng: hàng không, bán lẻ, viễn thông) với user giả lập.
- Đo bằng **AUROC** (dự đoán thất bại) và **AUARC** (độ chính xác theo mức coverage khi từ chối có chọn lọc).

## 4. Kết quả chính [Paper §IV]

- TRACER đạt AUROC và AUARC cao nhất ở **mọi** thiết lập đã thử; so với baseline mạnh nhất: AUROC +4,7% tới +37,1%, AUARC +6% tới +55%.
- Ablation: bỏ tín hiệu phía agent làm mất khoảng 85% mức lợi so với baseline; bỏ tín hiệu phía user mất khoảng 70%.

## 5. Hạn chế

**Người đọc nhận xét [Diễn giải]:**
- Cần log-prob cho thành phần surprisal.
- Domain chăm sóc khách hàng có user giả lập; RCA không có user nhưng có **nhiều tool chẩn đoán** và dữ liệu hệ thống.
- Chưa thấy so sánh với đặc trưng đặc thù domain.

## 6. Nhóm khai thác được gì?

1. **Chuyển tín hiệu sang RCA [Giả thuyết]:**
   - *Agent repetition* ↔ gọi lặp cùng tool + tham số (giống RAR của Cloud-OpsBench), không cần log-prob.
   - *Action–observation mismatch* ↔ agent gọi tool vào object không tồn tại, nhận `Not Found` hoặc `UnsupportedQuery`, hoặc kết luận về component mà nó chưa từng quan sát.
   - *Tail aggregation* ↔ một bước tồi (ví dụ kiểm tra connectivity sai port, như Cloud-OpsBench §4.6) có thể đủ làm hỏng cả chẩn đoán.
2. **Thước đo cần dùng:** AUROC + AUARC/AURC + risk–coverage. Có code mở để tham khảo cách tính.
3. **Ý tưởng "MAX thay vì trung bình":** đáng thử như một biến thể đặc trưng trong hướng chốt.

## 7. Thuật ngữ

- **Surprisal:** −log xác suất của token; càng cao nghĩa là model càng "bất ngờ" khi sinh ra nó.
- **Tail risk:** rủi ro ở phần tệ nhất của phân phối, thay vì mức trung bình.
- **AUARC (Area Under Accuracy–Rejection Curve):** từ chối dần các case kém tin cậy nhất, accuracy trên phần còn lại tăng nhanh thì điểm cao.
- **Selective execution:** chỉ cho agent làm tiếp những task mà điểm rủi ro thấp.
