# How Far Can Root Cause Analysis Go on Real-World Telemetry Data?

> **Đọc nhanh (30 giây):** Trên OpenRCA, khi agent sai thì phần lớn là do **suy luận sai trên bằng chứng đã có**, không phải do thiếu dữ liệu. Tác giả tính sẵn bằng chứng một lần rồi đưa giống hệt cho mọi cấu hình, nên tách được tác dụng của *quy trình* (procedure prompt) và *tri thức phân biệt lỗi* (rules). Tri thức thắng: bộ rule tự khai thác nâng Full Score từ **14,10 lên 35,90** trên cloudbed chưa thấy. Quy trình 5 bước được kê sẵn thì có xu hướng **làm hại**.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2607.13548 **v2** (22/10/2026); v1 ngày 15/07/2026 |
| Tác giả | Athira Gopal, Ashwanth Krishnan (QPIAI India) |
| Venue | Preprint |
| PDF | https://arxiv.org/pdf/2607.13548v2 |
| Mức độ đọc | Abstract, §1–§2, §3.2, §6, §8 (Limitations); chưa đọc kỹ §4–§5 và appendix |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Thiết kế "giữ evidence cố định" và phân loại lỗi Reasoning Gap / Data Ambiguity |

**Lưu ý phiên bản:** memo cũ của nhóm (07/11/2026) mới đọc v1 và abstract v2. Đã xác minh trong **v2 full text**: tác giả tự viết audit của họ *"audits evidence rather than testing forward identifiability"* (Abstract, §1, §8).

---

## 1. Paper giải quyết vấn đề gì?

**Giải thích cho người mới [Diễn giải]:** khi agent chẩn đoán sai, có hai khả năng. (a) Nó *không biết cách làm*: thiếu quy trình, cần prompt tốt hơn. (b) Nó *không biết kiến thức*: ví dụ không biết "CPU cao + log GC dày" nghĩa là gì. Nếu agent vừa tự trích bằng chứng vừa suy luận, ta không tách được hai khả năng này. Tác giả cố định phần trích bằng chứng, rồi thay từng yếu tố một.

- **[Paper §1]** Một nửa giờ telemetry của OpenRCA khoảng 2 GB, vượt xa context của model, nên phải trích bằng chứng trước rồi mới suy luận.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Cửa sổ 30 phút sự cố của OpenRCA; bằng chứng bất thường được tính sẵn offline theo ngưỡng cố định cho từng KPI |
| **Pipeline** | Nhiều giai đoạn; gọi tool đọc log/trace và các sub-agent mesh/runtime khi cần [Paper §1] |
| **Output** | 1–2 root cause, mỗi cái gồm component, lý do lỗi, thời điểm bắt đầu |
| **Chỉ số** | Full Score (đúng đủ các trường) và Partial Score của OpenRCA |

## 3. Môi trường thực nghiệm

- Benchmark **OpenRCA** (ICLR 2025): 3 bộ Market, Telecom, Bank. Market có 2 cloudbed CB1 và CB2, dùng chung topology và từ vựng lỗi nhưng khác instance, nên làm được thí nghiệm chuyển giao [Paper §1].
- CB1 có 70 case gán nhãn trên 57 cửa sổ [Paper §8].

## 4. Cách làm (process)

```text
1. Tính bằng chứng một lần (offline), đưa giống hệt cho mọi nhánh thí nghiệm
2. Thí nghiệm A: bỏ quy trình 5 bước, giữ nguyên mọi thứ khác
3. Thí nghiệm B: thay bộ rule phân biệt lỗi: không rule / rule viết tay / rule tự khai thác / rule "đối chứng"
   (viết chỉ từ tên nhãn + schema KPI)
4. Error analysis: "reverse reasoning agent" ĐƯỢC CHO ĐÁP ÁN, dựng lại chuỗi bằng chứng tới đáp án,
   rồi so với trace của agent → gán mỗi lỗi là:
     • Reasoning Gap  : bằng chứng có, agent suy luận sai
     • Data Ambiguity : không nguồn nào agent truy cập được chứa tín hiệu
5. Khai thác rule từ các báo cáo audit ở CB1 → áp dụng lên CB2 chưa thấy
```

- **[Paper §3.2]** Vì audit được biết đáp án, Data Ambiguity chỉ là **cận dưới**: model biết đáp án có thể dựng một chuỗi mà bằng chứng một mình không chỉ ra, và case đó bị tính là Reasoning Gap.
- Nhãn của audit khớp với 2 SRE trên mẫu phân tầng 30 chiều, mức đồng ý ngang mức hai người đồng ý với nhau [Paper §8, Appendix D.2].

## 5. RQ và câu trả lời

| Câu hỏi (diễn đạt lại) | Trả lời [Paper Abstract, §6] |
|---|---|
| Agent thiếu quy trình hay thiếu tri thức? | Tri thức (rules) cho hiệu ứng lớn nhất; quy trình 5 bước kê sẵn không giúp, còn có xu hướng hại |
| Rule tự khai thác có chuyển giao được không? | Có, CB1 sang CB2: Full Score 14,10 → **35,90**, vẫn có ý nghĩa sau hiệu chỉnh kiểm định bội (Holm) |
| Rule khai thác có hơn rule tay? | Cao hơn (24,36) và hơn đối chứng (19,23), nhưng chênh lệch Full Score giữa các nhánh này chưa có ý nghĩa thống kê |

## 6. Kết quả chính

- Bỏ quy trình 5 bước làm Full Score **tăng** ở cả 3 điều kiện; không rule thì số case giải được tăng từ 11 lên 22. Không so sánh nào trong nhóm này đạt ý nghĩa sau hiệu chỉnh [Paper Abstract, §6].
- Chỉ xóa một tiêu chí "chọn bất thường xuất hiện sớm nhất" đã cho lợi ròng 8 case [Paper Abstract].
- **Phân loại lỗi [Paper Table 12, Appendix D.2]:** trên Market CB1, rules OFF (n = 70), Reasoning Gap chiếm 51,4% (component), 65,7% (reason), 54,3% (timestamp); Data Ambiguity chỉ 1,4%, 11,4%, 1,4%. Trong 130 chiều bị gán lỗi, Data Ambiguity chiếm **7,7%**. Tức là bằng chứng cần thiết **có mặt** trong phần lớn trường hợp sai, và lỗi chủ yếu ở suy luận. Paper tự nói đây không phải phép kiểm tra forward identifiability.
- Model dự đoán và model phân tích lỗi đều là **GPT-5.2** [Paper §8]; hai SRE độc lập (không phải tác giả) kiểm 30 mục: κ = 0,625 giữa hai người, 0,704 và 0,920 giữa bộ phân tích và từng người [Paper Appendix D.2, Table 11].

## 7. Hạn chế

**Paper tự nhận [§8]:**
- Chỉ một benchmark (OpenRCA); chuyển giao chỉ CB1 → CB2.
- Ngưỡng tính bất thường cố định có thể làm rơi bằng chứng.
- Cơ chế giải thích là tương quan; mỗi điểm số là **một lần chạy** (chỉ một nhánh được chạy lại, đổi 1/78 case).
- Mẫu nhỏ: 70 case CB1, 54–55 điểm so sánh mỗi trường.
- Khai thác rule có dùng nhãn (label-supervised).

**Người đọc nhận xét [Diễn giải]:**
- Không cho agent quyền trả lời "chưa đủ bằng chứng".
- OpenRCA là dữ liệu tĩnh (CSV), không phải Kubernetes tương tác.

## 8. Nhóm khai thác được gì?

1. **Thiết kế thí nghiệm mẫu mực:** giữ input cố định, đổi đúng một yếu tố, báo cáo hiệu chỉnh kiểm định bội và thừa nhận chạy một lần. Nhóm nên bắt chước phong cách viết trung thực này.
2. **Kết quả "prompt quy trình có thể hại":** cảnh báo cho mọi phương pháp dựa trên checklist. Nhóm luôn phải có baseline "không thêm gì" và không mặc định thêm hướng dẫn là tốt.
3. **Phân loại Reasoning Gap / Data Ambiguity:** gần với phân loại "thiếu thông tin / điều tra thiếu / diễn giải sai" trong memo 07/11. Paper này là **tiền lệ trực tiếp** cho phân rã kiểu post-hoc. Nếu nhóm làm phân rã, phải chỉ rõ khác biệt: tính trước, không cần biết đáp án.
4. **Bằng chứng ngược với hướng "thiếu telemetry":** trên OpenRCA, dữ liệu thường **đủ**, lỗi chủ yếu do suy luận. Điều này làm yếu luận điểm "thiếu dữ liệu là vấn đề chính", và ủng hộ hướng chốt: **đánh giá xem có tin được chẩn đoán không**, bất kể nguyên nhân sai là gì.

## 9. Thuật ngữ

- **Cloudbed:** một bản triển khai của hệ thống; CB1 và CB2 giống kiến trúc, khác instance.
- **Holm correction:** hiệu chỉnh khi làm nhiều phép kiểm định cùng lúc để tránh "may mắn thấy có ý nghĩa".
- **Forward identifiability:** từ dữ liệu quan sát (không biết đáp án) có xác định duy nhất được nguyên nhân không.
- **Label-conditioned audit:** kiểm tra lỗi khi đã biết đáp án; dễ hơn và không tương đương việc agent có thể tự tìm ra.
