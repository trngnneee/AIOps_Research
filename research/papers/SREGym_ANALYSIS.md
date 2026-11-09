# SREGym: A Live Benchmark for AI SRE Agents with High-Fidelity Failure Scenarios

> **Đọc nhanh (30 giây):** Benchmark **chạy trên hệ thống thật** (live) cho agent SRE, gồm cả **chẩn đoán và khắc phục**. 90 bài toán, lỗi ở nhiều tầng (phần cứng, kernel, thao tác sai, ứng dụng), có **nhiễu nền** và lỗi tương quan/metastable. Agent đều **tham lam**: coi bất thường đầu tiên thấy được là lỗi cần sửa, kể cả khi đó chỉ là nhiễu. Bài toán chép từ AIOpsLab/ITBench quá dễ với model mạnh; bài toán mới của SREGym khó hơn hẳn.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2605.07161 **v3** (30/07/2026) |
| Tác giả | Jackson Clark, Yiming Su, …, Yinfang Chen, Tianyin Xu (UIUC; University of Toronto); cùng nhóm làm AIOpsLab, STRATUS |
| Venue | Preprint; mã nguồn mở, đang được duy trì |
| PDF | https://arxiv.org/pdf/2605.07161v3 |
| Mức độ đọc | Abstract, §1, các câu kết quả chính; chưa đọc chi tiết kiến trúc injector và appendix |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★☆☆ Tham khảo cho hướng remediation (không chọn) và cho hiện tượng "bám nhiễu" |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper §1]** Benchmark SRE hiện tại quá đơn giản (chủ yếu lỗi tầng ứng dụng) và khó mở rộng. Benchmark RCA tĩnh chỉ đo chẩn đoán, không đo **khắc phục**.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Hệ cloud-native thật (ví dụ Astronomy Shop) đang chạy, có lỗi và nhiễu được tiêm |
| **Agent làm** | Gọi `kubectl`, xem traces/metrics/logs, **sửa hệ thống** |
| **Output** | Chẩn đoán + hệ thống sau khi khắc phục |
| **Chấm** | Oracle kiểm **trạng thái hệ thống** cho mitigation; chẩn đoán chấm bằng **LLM-as-a-judge theo checklist** (tách thành câu hỏi nhỏ) |

## 3. Kết quả chính [Paper §3, Appendix D]

- Năng lực agent khác nhau nhiều theo loại lỗi, chênh tới 40% kết quả đầu-cuối.
- Mọi agent đánh giá đều **tham lam**: coi bất thường hợp lý đầu tiên là lỗi mục tiêu (có thể chỉ là nhiễu) [Paper §3.1, Appendix D]. Ví dụ Figure 1: STRATUS + Sonnet-4.6 bám vào giới hạn memory thấp (nhiễu) và bỏ qua biến môi trường `CART_ADDR` bị xóa; Codex + GPT-5.4 lần theo trace và sửa đúng. Appendix D: trong mọi lần chạy của Stratus và Claude Code ở bài này, không agent nào kiểm tra component frontend (nơi có lỗi thật).
- Nhiễu làm tỷ lệ chẩn đoán đúng giảm ở mọi cặp agent–model; khắc phục bền hơn chẩn đoán khi có nhiễu [Paper §3.1, Table 3].
- Bài toán chép từ AIOpsLab/ITBench ít thách thức với model mạnh; bài toán mới của SREGym khó hơn rõ.
- Chẩn đoán đúng giúp khắc phục; nhưng chẩn đoán sai đôi khi vẫn khắc phục được nhờ quan sát và chỉnh liên tục.
- Agent khó chẩn đoán lỗi phần cứng.

## 4. Hạn chế

**Người đọc nhận xét [Diễn giải]:** cần cụm Kubernetes thật, reset và tiêm lỗi liên tục: rất tốn tài nguyên cho sinh viên; chấm chẩn đoán bằng LLM judge; lần chạy khác nhau có thể cho biểu hiện lỗi khác nhau (vấn đề Cloud-OpsBench gọi là Gap 2).

## 5. Nhóm khai thác được gì?

1. **Không chọn hướng remediation live:** SREGym, SRE-World (NeurIPS 2026), ITBench, AIOpsLab, STRATUS đều từ các lab lớn có hạ tầng. Hai sinh viên khó cạnh tranh.
2. **Hiện tượng "tham lam, bám nhiễu"** là bằng chứng thêm cho việc **chẩn đoán đầu tiên của agent thường không đáng tin**. Đó là lý do cần đánh giá độ tin cậy trước khi hành động.
3. **Ý tưởng chấm bằng checklist:** nếu nhóm cần chấm phần giải thích, tách thành câu hỏi có/không giúp judge ổn định hơn.

## 6. Thuật ngữ

- **Mitigation / remediation:** hành động khắc phục (rollback, sửa config, restart…).
- **Metastable failure:** hệ rơi vào trạng thái lỗi tự duy trì kể cả khi nguyên nhân ban đầu đã hết.
- **Ambient noise:** bất thường vô hại xảy ra cùng lúc, dễ làm agent nhầm.
