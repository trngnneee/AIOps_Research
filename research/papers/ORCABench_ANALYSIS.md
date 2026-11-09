# ORCA-bench: How Ready Are Language Model Agents for Oncall?

> **Đọc nhanh (30 giây):** Đặt các coding agent mạnh nhất (Claude, GPT…) vào vai kỹ sư trực sự cố (on-call) với telemetry thật 6 ngày và source code. Kết quả rất thấp: tốt nhất chỉ **25,3%** ở mức "thực tế" (Medium) và **10%** ở mức Hard. Agent còn **bịa nguyên nhân** trong 7–40% báo cáo. Bỏ quyền đọc source code thì accuracy giảm và bịa nhiều hơn ở mọi model.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2607.28545 **v3** (29/09/2026) |
| Tác giả | Albert Gong, …, Raaz Dwivedi (Cornell Tech, Traversal, Columbia) |
| Venue | Preprint |
| Code / dữ liệu | https://github.com/ORCA-bench/ORCA-bench · public set trên Harbor: https://hub.harborframework.com/datasets/orca-bench/orca-bench |
| PDF | https://arxiv.org/pdf/2607.28545v3 |
| Mức độ đọc | Phần chính §1–§6 và các đoạn kết quả trong appendix; chưa đọc hết appendix (I–L) |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Nguồn bằng chứng về "bịa nguyên nhân" và "bỏ một nguồn dữ liệu" |

**Quy ước:** **[Paper]** / **[Diễn giải]** / **[Chưa kiểm]** như các file khác.

---

## 1. Paper giải quyết vấn đề gì?

**Giải thích cho người mới [Diễn giải]:** benchmark cũ giống đề thi có gợi ý: "service X bị lỗi CPU, hãy tìm". Ngoài đời, kỹ sư on-call nhận tin nhắn mơ hồ ("khách không dùng được giỏ hàng") vài giờ sau khi sự cố bắt đầu. Họ phải tự mở Grafana, Prometheus, Jaeger, đọc code rồi mới đoán. ORCA-bench mô phỏng đúng hoàn cảnh này.

- **[Paper §1, Table 1]** Mỗi benchmark trước (AIOpsLab, OpenRCA, ITBench, Cloud-OpsBench, SREGym, OpenRCA 2.0) đều thiếu ít nhất một trong ba thứ: giao diện telemetry thật, telemetry sinh dưới tải thật, source code. Không benchmark nào thay đổi có hệ thống *độ cụ thể của báo cáo* và *thời gian từ lúc sự cố tới lúc điều tra (TTD)*.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Một báo cáo người dùng bằng ngôn ngữ tự nhiên, độ cụ thể Easy/Medium/Hard, kèm thời điểm báo |
| **Công cụ** | Một phiên `tmux` (harness Terminus-2) truy cập Prometheus, Jaeger, OpenSearch qua Grafana và toàn bộ source code [Paper §5] |
| **Output** | Báo cáo RCA dạng văn bản |
| **Chấm điểm** | LLM-as-judge (GPT-5.4) theo rubric 0–3 cho từng root cause; đối chiếu người chấm: Cohen's κw = 0,91 [Paper Abstract, §4] |

## 3. Môi trường thực nghiệm [Paper §3]

- Hệ thống: **OpenTelemetry Astronomy Shop** (19 microservice), chạy dưới tải người dùng giả lập liên tục, thu **6 ngày telemetry (~50 GB)**.
- Lỗi được tạo bằng **feature flag thật** của ứng dụng, không dùng thư viện chaos tổng hợp.
- **1.079 task**, trong đó **195 control task** ở thời điểm không có sự cố (đáp án đúng là "không có incident") [Paper §3, bước B3].
- Biến đổi có hệ thống: độ cụ thể báo cáo (Easy/Medium/Hard), TTD từ 15 phút tới 24 giờ, 5 kiểu kịch bản (isolated, independent, conflicting, cascading, sequential).
- 5 agent chính: Claude Opus 4.7, Claude Sonnet 4.6, GPT-5.5, GLM-5, DeepSeek-V4-Pro; Claude Fable 5 chạy trên tập con Verified.
- **ORCA-bench Verified:** 40 task có nhãn và điểm từng model được người kiểm tay.

## 4. Cách làm (process)

```text
Chạy Astronomy Shop 6 ngày + bật/tắt feature flag theo lịch
   → ghi metrics/logs/traces
   → sinh task: báo cáo người dùng (3 mức) × TTD × kiểu kịch bản
   → nhãn: tập root cause "plausible" + rubric triệu chứng (SRE chuyên gia ký duyệt)
   → agent điều tra trong tmux → viết báo cáo
   → LLM judge chấm theo rubric (đã đối chiếu người chấm)
```

## 5. Câu hỏi nghiên cứu và câu trả lời [Paper §5]

| Finding | Nội dung |
|---|---|
| #1 | Agent còn xa mới thành SRE giỏi. RCA depth cao nhất 48,8% (GPT-5.5); RCA accuracy cao nhất 30,9% (Sonnet 4.6, toàn bộ 884 incident task). Trên Verified, Claude Fable 5 đạt accuracy 40,6 ± 8,8% |
| #2 | Giảm ngữ cảnh báo cáo (Easy → Hard) làm accuracy giảm **19–50 điểm %** |
| #3 | Bỏ source code làm accuracy giảm **9–16 điểm %** và tăng tỷ lệ bịa ở mọi model |
| #4 | **26–40%** lệnh truy vấn telemetry bị lỗi hoặc trả rỗng |

## 6. Kết quả chính [Paper Abstract, Figure 1, §5]

- **Hallucination rate** (nêu root cause không khớp bất kỳ nguyên nhân plausible nào): từ 7% (DeepSeek-V4-Pro) tới 40% (GLM-5).
- Agent hay **bám vào triệu chứng ồn nhất** và bỏ sót root cause; khó lượng hóa mức tăng nghiêm trọng [Paper §5, Finding #1].
- Claude Opus 4.7 và GLM-5 chỉ dành 16–20% lệnh để đọc source code, 70–72% cho telemetry [Paper Appendix J].
- Đổi harness (Terminus-2 sang OpenSRE) không đổi accuracy của Opus 4.7 trên Verified (cùng 25,0%) [Paper §5, App. L.1].

## 7. Hạn chế

**Paper tự nhận [Abstract, §1]:** testbed 50 GB/6 ngày, task điều tra riêng lẻ, hệ thống có code và instrumentation công khai. Hệ production thật lớn và biến động hơn nhiều.

**Người đọc nhận xét [Diễn giải]:**
- Chấm bằng LLM judge. κw cao (0,91) nhưng chỉ kiểm trên 40 task Verified.
- Chạy rất nặng: cần stack Grafana/Prometheus/Jaeger/OpenSearch và dữ liệu 50 GB. Khó với nhóm sinh viên.
- "Bỏ source code" là ablation theo **cả kênh dữ liệu**, chưa phải mô phỏng cơ chế mất dữ liệu thực tế (log bị xoay vòng, event hết hạn…).
- Có control task "không có incident", nhưng đó là **abstention theo kiểu "không có lỗi"**, chưa phải "có lỗi nhưng chưa đủ bằng chứng để biết là lỗi nào".

## 8. Nhóm khai thác được gì?

1. **Số liệu động lực mạnh:** agent mạnh nhất vẫn sai đa số case thực tế và bịa 7–40%. Điều này cho thấy cần một lớp quyết định **"có nên tin chẩn đoán này không"** (hướng chốt trong báo cáo).
2. **Finding #4 (26–40% truy vấn rỗng/lỗi):** truy vấn rỗng là **tín hiệu nhìn thấy được mà không cần nhãn**. Có thể dùng làm đặc trưng dự đoán agent sắp sai. Đây là giả thuyết cần kiểm.
3. **Finding #3 (bỏ code):** tiền lệ cho thí nghiệm "bớt kênh dữ liệu". Nếu nhóm làm phần telemetry suy giảm, phải trích ORCA-bench và nói rõ mình khác ở đâu: profile cụ thể của Kubernetes, môi trường replay tương tác.
4. **Control task:** ý tưởng hay để đo **từ chối đúng**. Trên Cloud-OpsBench không có case "không lỗi"; nếu cần có thể cân nhắc thêm (chưa chắc khả thi).
5. **Không chọn làm môi trường chính:** quá nặng so với nguồn lực 2 người.

## 9. Thuật ngữ

- **On-call:** kỹ sư trực, nhận cảnh báo và xử lý sự cố ngoài giờ.
- **TTD (time-to-detection):** khoảng từ lúc sự cố bắt đầu tới lúc bắt đầu điều tra; càng lâu thì dữ liệu càng "trôi".
- **Feature flag:** công tắc bật/tắt tính năng trong code; ở đây dùng để gây lỗi có kiểm soát.
- **LLM-as-judge:** dùng một LLM chấm bài của LLM khác; phải đối chiếu người chấm mới tin được.
- **Cohen's κw:** chỉ số đồng thuận có trọng số giữa hai người (hoặc người với máy) chấm; 1 là hoàn toàn đồng ý.
