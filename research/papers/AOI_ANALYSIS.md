# AOI: Turning Failed Trajectories into Training Signals for Autonomous Cloud Diagnosis

> **Đọc nhanh (30 giây):** Doanh nghiệp không muốn gửi dữ liệu vận hành ra ngoài, nên cần **model mở chạy tại chỗ** nhưng vẫn giỏi. AOI huấn luyện model 14B bằng **GRPO** (học tăng cường theo nhóm), tách quyền **đọc–ghi** để an toàn, và biến **trajectory thất bại** thành hướng dẫn sửa sai. Trên AIOpsLab: runtime AOI đạt 66,3% best@5 (SOTA trước 41,9%); model 14B sau huấn luyện đạt 42,9% avg@1 trên task lỗi chưa thấy, nhỉnh hơn Claude Sonnet 4.5 (41,3%).

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2603.03378 **v4** (16/10/2026) |
| Tác giả | Pei Yang, Wanyi Chen, Asuka Yuxi Zheng, …, Bill Shi (Gradient; UC Santa Cruz; Georgia Tech; UCL; ByteDance…) |
| Code | https://github.com/OpenEdgeHQ/aoi |
| PDF | https://arxiv.org/pdf/2603.03378v4 |
| Mức độ đọc | Abstract, §1, kết quả chính, thông số huấn luyện |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★☆☆ Tham khảo cho hướng "huấn luyện model nhỏ" (không chọn) |

---

## 1. Input → Output

| | Nội dung |
|---|---|
| **Input** | Task SRE của AIOpsLab (phát hiện, định vị, phân tích, khắc phục) |
| **Kiến trúc** | Observer (suy luận, được huấn luyện) / Probe (đọc) / Executor (ghi, có kiểm soát) |
| **Huấn luyện** | GRPO trên Qwen3-14B, LoRA rank 64; **2×A100** GPU, vLLM để suy luận [Paper §5.1] |
| **Evolver** | Judge phân loại workflow thành công/thất bại; workflow thất bại được sửa thành chuỗi lệnh đúng để làm hướng dẫn |

## 2. Kết quả chính [Paper Abstract, §5]

- Runtime AOI (chưa huấn luyện) đạt 66,3% best@5 trên 86 task, hơn SOTA trước (41,9%) 24,4 điểm.
- Observer-GRPO: 14B đạt 42,9% avg@1 trên 63 task held-out có loại lỗi chưa thấy, hơn Claude Sonnet 4.5 (41,3%).
- Evolver: biến 37 trajectory thất bại (43% benchmark) thành prompt hướng dẫn, avg@5 +4,8 điểm, phương sai giữa các lần chạy −35%.
- **Đánh đổi:** GRPO giúp phát hiện (+36,4 điểm) nhưng **hại định vị** (−18,2 điểm), vì khám phá quá nhiều gây rối.

## 3. Hạn chế

**Người đọc nhận xét [Diễn giải]:** cần GPU A100 và kỹ năng RL; best@5 là chỉ số lạc quan (lấy lần tốt nhất trong 5); Evolver dùng LLM judge.

## 4. Nhóm khai thác được gì?

1. **Lý do không chọn hướng huấn luyện:** cần GPU lớn, rủi ro kỹ thuật cao, đã có nhiều nhóm mạnh làm (AOI; *Small Language Models as Autonomous Operational Agents* NeurIPS 2026; Edge Delta fine-tune 32B). Hai sinh viên trong 6 tháng không có lợi thế.
2. **Ý tưởng "học từ thất bại":** nếu nhóm có **bộ dự đoán thất bại** tốt (hướng chốt), đó chính là bộ lọc để chọn trajectory đưa vào huấn luyện sau này. Có thể nêu trong mục Future Work.
3. **best@k và avg@k:** khi báo cáo, luôn dùng avg@1 hoặc trung bình nhiều lần; best@k làm kết quả trông đẹp hơn thực tế.

## 5. Thuật ngữ

- **GRPO (Group Relative Policy Optimization):** thuật toán RL so sánh nhiều câu trả lời trong cùng nhóm để cập nhật model; không cần value model riêng.
- **LoRA:** cách fine-tune nhẹ, chỉ học một phần nhỏ tham số.
- **best@5 / avg@5:** chạy 5 lần, lấy kết quả tốt nhất / trung bình.
