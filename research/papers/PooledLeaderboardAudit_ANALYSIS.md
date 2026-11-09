# What a Pooled Leaderboard Does Not Say: Auditing the Scope and Provenance of Method Comparisons in Microservice RCA Benchmarks

> **Đọc nhanh (30 giây):** Bảng xếp hạng RCA thường cộng gộp điểm trên nhiều hệ thống con. Tác giả chạy lại 16 phương pháp trên 11 hệ thống con và phát hiện: nhiều "chiến thắng" **đảo ngược** khi tách theo từng hệ thống; một lựa chọn nhỏ trong pipeline (đọc nhầm bảng input, phụ thuộc không ghim phiên bản) có thể **lật kết quả**. Trong 23 paper RCA được kiểm, **không paper nào** công bố output theo từng case để người khác kiểm tra.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2606.29159 **v2** (13/10/2026) |
| Tác giả | Lining Hu, Ting Liu, Yuzhuo Fu (Shanghai Jiao Tong University) |
| Venue | Preprint (21 trang) |
| PDF | https://arxiv.org/pdf/2606.29159v2 |
| Mức độ đọc | Abstract, §1, RQ1–RQ2; chưa đọc chi tiết bảng |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ **Hướng dẫn báo cáo kết quả** cho thesis; RCA cổ điển (không LLM) |

---

## 1. Input → Output

| | Nội dung |
|---|---|
| **Input** | Mã đã công bố của 16 phương pháp RCA; 3 họ benchmark (OpenRCA, RCAEval, PetShop); 11 hệ thống con + bản phát hành thứ hai của 3 ứng dụng |
| **Output** | Mức ổn định của các so sánh theo hệ thống con (RQ1 – scope) và theo lựa chọn pipeline (RQ2 – provenance) |

## 2. Kết quả chính [Paper Abstract]

- Một lợi thế gộp có giữ ở mọi hệ thống con hay không được quyết định bởi **độ phân tán** của lợi thế đó giữa các hệ thống (bảng xếp hạng không báo). 15 lợi thế có biên lớn hơn độ phân tán: 14 giữ ở mọi nơi. 8 lợi thế có biên nhỏ hơn: **6 đảo chiều**.
- Bản phát hành thứ hai: **một phần ba** so sánh đổi dấu.
- Ở vài hệ thống con, một **probe đơn giản** hoặc baseline có sẵn thắng mọi phương pháp đã công bố.
- Runner công bố đọc một bảng input khác với tài liệu mô tả; riêng lựa chọn này đã lật một so sánh. Phụ thuộc không ghim phiên bản và header cột trùng làm một phương pháp trả về thứ tự cột input mà không báo lỗi.

## 3. Khuyến nghị của paper

Khi so sánh gộp, phải nêu: các hệ thống con được phủ và độ phân tán giữa chúng; bảng input; cách xử lý output lỗi; mẫu số; và công bố **output theo từng case**.

## 4. Nhóm khai thác được gì?

1. **Checklist báo cáo cho thesis (áp dụng ngay):**
   - Báo kết quả **riêng từng hệ thống** (OnlineBoutique, TrainTicket) và từng fault category, không chỉ trung bình.
   - Báo **mẫu số** (case nào timeout/sai schema vẫn tính).
   - Ghim **commit** của Cloud-OpsBench, phiên bản model, phiên bản thư viện.
   - Công bố **output từng case** (trajectory, dự đoán, điểm tin cậy) trong repo.
2. **Luôn có baseline "probe đơn giản":** trong hướng chốt, một quy tắc đơn giản (ví dụ "số bước ≥ 15 thì không tin") phải được so sánh. Nếu nó ngang phương pháp phức tạp, đó là kết quả phải báo.
3. **Câu dùng trong related work:** việc thiếu output từng case là phổ biến (0/23 paper theo audit này), nên nhóm công bố output từng case là một đóng góp nhỏ về tính tái lập.

## 5. Thuật ngữ

- **Pooled score:** điểm gộp trung bình qua nhiều hệ thống.
- **Provenance:** nguồn gốc, cách tạo ra một con số (input nào, code phiên bản nào).
- **Spread:** độ phân tán của chênh lệch giữa các hệ thống con.
