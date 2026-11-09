# CTBench: Evaluating Troubleshooting Capabilities of AI Agents in Realistic Telecom Network Operations

> **Đọc nhanh (30 giây):** Benchmark xử lý sự cố mạng viễn thông của Huawei: 234 task (126 RCA, 108 khôi phục đường đi) do 15 chuyên gia soạn; agent truy vấn qua **replay output CLI đã ghi** (giống tinh thần snapshot của Cloud-OpsBench). Điểm đáng chú ý: task được gắn **mức observability**. O1 có bằng chứng trực tiếp; O2 thì bằng chứng quyết định **không có hoặc phải suy gián tiếp**. Agent yếu rõ ở O2 và hay **đúng mà không đủ bằng chứng**.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2608.12002 **v2** (21/10/2026); v1 ngày 12/08/2026 |
| Tác giả | Xingyu Yan, …, Xin Chen (Huawei Technologies; Queen Mary University of London) |
| Venue | Preprint, "under review" |
| PDF | https://arxiv.org/pdf/2608.12002v2 |
| Mức độ đọc | Abstract, §1, §3.2, §5–§7, Appendix C.3 (bảng observability) |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ **Tiền lệ "observability là một trục đánh giá"** (ở viễn thông, không phải Kubernetes) |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper Abstract, §1]** Benchmark viễn thông hiện có giả định quan sát đầy đủ và topology đồng nhất; không phân biệt được agent "không định vị được lỗi" với agent "trả nhãn đúng mà không có bằng chứng".

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Mô tả sự cố mạng; agent gọi lệnh CLI của thiết bị đa hãng; backend **replay** output đã ghi |
| **Output** | RCA: node + object bị ảnh hưởng + nhãn root cause chuẩn hóa. Path restoration: endpoint nguồn/đích + đường chuyển tiếp |
| **Nhãn** | Đáp án chuẩn hóa, *golden evidence trajectories* (các bước chẩn đoán cần có), metadata: observability, heterogeneity, độ phức tạp giao thức |

## 3. Môi trường thực nghiệm

- 234 task từ case bảo trì thật đã làm sạch; 15 chuyên gia (khoảng 20 năm kinh nghiệm); chuyên gia độc lập giải mù từng task.
- Chuyên gia người đạt 80,95% RCA (102/126) và 96,30% path restoration, mỗi task 40–60 phút [Paper §5.2].
- Agent = **harness + model**: Codex + GPT-5.5, Claude Code + Sonnet-5.5, HermesAgent + DeepSeek-V4-Pro / Qwen3.7-Max…

## 4. Kết quả chính [Paper §5–§6, Appendix C]

- Agent nhận diện **loại** lỗi tốt hơn **vị trí** (Codex + GPT-5.5: 74,74% so với 63,99%).
- Kể cả khi đúng, agent thường **không thu đủ bằng chứng** chuyên gia yêu cầu.
- **Tốn thêm tính toán không bảo đảm chẩn đoán giỏi hơn.**
- **Harness quan trọng** dù cùng model: các harness giải những tập task khác nhau một phần [Paper Table 23–24].
- **Observability:** O2 (bằng chứng quyết định không có/gián tiếp) làm agent yếu đi. Thí nghiệm O2→O1 trên 19 task: làm phần không quan sát được thành quan sát trực tiếp rồi đo lại. Tác giả lưu ý điểm evidence coverage giữa hai điều kiện **không cùng mẫu số** nên không so trực tiếp được.

## 5. Hạn chế

**Paper tự nhận [Limitations]:** chỉ 2 loại task; replay hữu hạn nên agent không thay đổi được trạng thái thiết bị; chưa phủ RAN, core slicing, cloud-native telecom.

**Người đọc nhận xét [Diễn giải]:** tập O2 nhỏ (19 task trong ablation); nhãn O1/O2 do chuyên gia gán theo task, không tính tự động từ dữ liệu; không có cơ chế abstain.

## 6. Nhóm khai thác được gì?

1. **Ảnh hưởng tới novelty của hướng "thiếu telemetry" (memo 07/11):** ý tưởng "observability là một trục có kiểm soát" **đã có tiền lệ** ở viễn thông (CTBench) và được nêu là future work ở RCA microservice (OpenRCA 2.0 §5). Nếu nhóm theo hướng này cho Kubernetes, phải trích CTBench và nói rõ khác biệt: profile mất dữ liệu theo cơ chế K8s thật, tính trần identifiability tự động.
2. **"Harness quan trọng":** cùng kết luận với Cloud-OpsBench v3 RQ4. Khi so sánh, nhóm phải cố định harness, hoặc coi "harness + model" là một đơn vị.
3. **"Đúng nhưng thiếu bằng chứng":** hiện tượng lặp lại ở nhiều domain (OpenRCA 2.0, Cloud-OpsBench, CTBench, TriFleetRCA). Nó là lý do mạnh cho việc cần **cổng tin cậy**.
4. **Mốc người:** chuyên gia 81% RCA, 40–60 phút/task. Ý tưởng hay: so agent với người cả về độ đúng và thời gian.

## 7. Thuật ngữ

- **NetO&M:** vận hành và bảo trì mạng.
- **Partial observability:** không thấy trực tiếp mọi thứ cần thấy; phải suy từ dấu hiệu gián tiếp.
- **Harness:** "vỏ" điều khiển agent (vòng lặp, quản lý context, cách gọi tool), ví dụ Codex CLI, Claude Code.
