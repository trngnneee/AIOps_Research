# Uncertainty Quantification for LLM Agents: A Taxonomy, an Evaluation Protocol, and an Empirical Study

> **Đọc nhanh (30 giây):** Bài tổng quan (119 trang) về đo độ bất định cho LLM agent. Phân loại tài liệu theo 3 trục: (1) bất định là gì, (2) ước lượng bằng cách nào, (3) phát sinh ở đâu trong pipeline agent. Chứng minh bằng phản ví dụ rằng **calibration từng bước không suy ra calibration cả trajectory**. Đề xuất metric **TC-ECE**. Thực nghiệm: độ tự tin agent tự báo **không luôn hơn một baseline đơn giản**, và **gộp trung bình mọi trajectory có thể che giấu sự quá tự tin ở giai đoạn sau**.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2609.07395 **v1** (07/09/2026), category cs.IR |
| Tác giả | Moule Lin, …, Goetz Botterweck (Trinity College Dublin và cộng sự) |
| Venue | Preprint |
| PDF | https://arxiv.org/pdf/2609.07395v1 (119 trang) |
| Mức độ đọc | Abstract, mục lục; tìm từ khóa AIOps/SRE/incident/root cause trong toàn văn: **0 kết quả** |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Bằng chứng gián tiếp về khoảng trống ở domain vận hành; nguồn thuật ngữ chuẩn |

---

## 1. Nội dung chính [Paper Abstract]

- Lỗi và bất định của agent phát sinh từ hội thoại nhiều lượt, môi trường và tool, không chỉ từ một câu hỏi–đáp. Bất định đến muộn và bị dồn vào **một con số quá thô**.
- Thực nghiệm trên trace thật, 4 model, ngân sách tới 50 bước: TC-ECE tính được; lỗi giữa các bước **liên kết với nhau** dọc trajectory.
- Độ tự tin agent tự báo không luôn hơn baseline đơn giản.
- Gộp mọi trajectory có thể che quá tự tin ở giai đoạn sau; phân tích theo độ dài (horizon) mới thấy.

## 2. Nhóm khai thác được gì?

1. **Bằng chứng (gián tiếp) về khoảng trống:** survey 120 paper về UQ cho agent; toàn văn không chứa các từ AIOps, SRE, incident hay root cause. Viết đúng mức: "một survey rộng gần đây về UQ cho agent không đề cập ứng dụng vận hành/RCA". Đây không phải bằng chứng là chưa ai làm.
2. **Bài học thiết kế:** báo calibration **theo nhóm độ dài trajectory** (ví dụ ≤ 6 bước, 7–12, > 12) thay vì chỉ một con số.
3. **Baseline "đơn giản"** phải luôn có khi đánh giá độ tự tin agent tự báo.
4. **Tài liệu tra thuật ngữ** (aleatoric / epistemic, step-level / trajectory-level calibration) khi viết chương lý thuyết.

## 3. Thuật ngữ

- **Aleatoric uncertainty:** bất định do bản chất dữ liệu (nhiễu, mơ hồ thật), thêm dữ liệu cũng không hết.
- **Epistemic uncertainty:** bất định do thiếu hiểu biết; có thể giảm khi thêm thông tin.
- **TC-ECE:** ECE tính tại các mốc (checkpoint) dọc trajectory, không chỉ ở bước cuối.
