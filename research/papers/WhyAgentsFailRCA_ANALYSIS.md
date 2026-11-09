# Why Do AI Agents Systematically Fail at Cloud Root Cause Analysis?

> **Đọc nhanh (30 giây):** Chạy agent mẫu của OpenRCA với 5 LLM (1.675 lần chạy) rồi phân loại lỗi thành **12 "cạm bẫy" (pitfall)**. Hai lỗi phổ biến nhất xuất hiện ở **mọi** model: *diễn giải dữ liệu theo kiểu bịa chuyện* (71,2%) và *khám phá không đủ* (63,9%). Kết luận: lỗi nằm ở **khung agent** chứ không chỉ ở model. Sửa prompt không chữa được; sửa giao thức trao đổi giữa các agent thì giúp.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2602.09937 **v2** (04/03/2026) |
| Tác giả | Taeyoon Kim, Woohyeok Park, Hoyeong Yun, Kyungyong Lee (Hanyang University, OKESTRO) |
| Venue | Bản workshop AIOps 2026: https://cloudintelligenceworkshop.org/papers/aiops26-Kim.pdf (theo kết quả tìm kiếm; chưa đối chiếu nội dung hai bản) |
| PDF | https://arxiv.org/pdf/2602.09937v2 (6 trang) |
| Mức độ đọc | Full text |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Taxonomy lỗi, nguồn đặc trưng dự đoán thất bại |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper §1, Table 1]** Agent mẫu của OpenRCA đạt *perfect accuracy* (đúng cả component, thời điểm, lý do) chỉ **3,9%–12,5%** trên 335 incident. Các framework đánh giá chỉ chấm đáp án cuối nên không ai biết **vì sao** agent sai. Người làm thực tế không biết nên đầu tư vào model mạnh hơn, prompt tốt hơn hay thiết kế lại agent.

**Ví dụ [Diễn giải]:** giống bác sĩ chẩn đoán sai. Biết "sai 88%" chưa giúp gì. Cần biết sai vì *không hỏi đủ triệu chứng*, vì *đọc nhầm xét nghiệm*, hay vì *hai bác sĩ truyền đạt cho nhau sai*.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input của nghiên cứu** | 1.675 trajectory của agent OpenRCA (Controller lập kế hoạch bằng ngôn ngữ tự nhiên, Executor viết và chạy code Python trên telemetry) |
| **Output** | Taxonomy 12 pitfall, tần suất từng loại theo model, thí nghiệm giảm thiểu |

## 3. Môi trường thực nghiệm [Paper §2, §4]

- Benchmark **OpenRCA**: 335 incident ở 3 miền Telecom (51), Bank (136), Market (148); 68,5 GB dữ liệu, hơn 523 triệu dòng.
- 5 model: Claude Sonnet 4, GPT-5 mini, Gemini 2.5 Pro, Solar Pro 2, GPT-OSS 120B.
- **Chi phí thật của một nghiên cứu cỡ này:** 609,9 giờ chạy, khoảng 1,38 tỷ token, ước tính **$1.394** [Paper §3]. Con số này hữu ích để nhóm ước lượng ngân sách.

## 4. Cách làm (process) [Paper §3]

```text
1. Chạy toàn bộ OpenRCA với 5 model → 1.675 run (trung bình 11,1 bước/run)
2. Dùng Claude Code (Opus 4.5) làm "agent phân tích":
   giai đoạn 1: khám phá tự do, chỉ có schema JSON → tìm ra nhiều kiểu lỗi
   giai đoạn 2: gom thành các loại loại trừ nhau, hỏi lại bằng câu hỏi CÓ/KHÔNG
               (ví dụ "Agent có bỏ qua KPI/component liên quan không?")
3. Người kiểm tra lại mọi phân loại (human-in-the-loop)
4. Thí nghiệm giảm thiểu cho từng nhóm lỗi (trên miền Bank)
```

**12 pitfall theo 3 giao diện [Paper Table 2, Table 3]:**

```text
Intra-agent (trong một agent)
├── Hallucination in Interpretation   71,2%  gán ý nghĩa bịa cho dữ liệu
├── Incomplete Exploration            63,9%  bỏ qua KPI/component liên quan
├── Symptom-as-Cause                  39,9%  nhầm triệu chứng là nguyên nhân
├── Code generation error             27,2%
├── Limited Telemetry Coverage        26,9%  chỉ dùng một nguồn telemetry
├── Timestamp Error                   23,3%  sai cửa sổ thời gian
└── No Cross-Validation               18,6%  không kiểm bằng nguồn khác
Inter-agent (giữa Controller và Executor)
├── Instruction-Code Mismatch, Meaningless Repetition, Misattributed Evidence
Agent-environment
└── Out-of-Memory, Max Step Exhaustion
```

Một run có thể mắc nhiều pitfall nên tổng phần trăm vượt 100%.

## 5. RQ và câu trả lời

Paper không đánh số RQ; ba câu hỏi ngầm và câu trả lời [Paper §4–§6]:

| Câu hỏi | Trả lời |
|---|---|
| Agent sai kiểu gì? | 12 pitfall; hai loại đầu chiếm ưu thế ở mọi model |
| Do model hay do khung agent? | Do khung: tần suất hai pitfall chính gần nhau giữa các model khác tầm |
| Sửa thế nào? | Prompt engineering mở rộng phạm vi điều tra nhưng **không** giảm hallucination diễn giải. Bổ sung code và output vào giao thức giữa các agent giảm pitfall giao tiếp tới **15 điểm %** và giảm 22,3% thời gian chạy |

## 6. Kết quả chính

- Giao thức giàu thông tin tăng token mỗi bước 24,8% (68K → 85K) nhưng giảm số bước 22,1% (11,9 → 9,2), tổng token giảm 1,6% [Paper §5].
- Memory watcher loại bỏ toàn bộ lỗi OOM quan sát được ở baseline [Paper §6].

## 7. Hạn chế

**Paper tự nhận [§6]:** thí nghiệm giảm thiểu chỉ trên miền Bank; phân loại bán tự động cần người kiểm nên khó mở rộng; chưa kiểm taxonomy trên framework RCA khác.

**Người đọc nhận xét [Diễn giải]:**
- Agent phân tích là một LLM (Opus 4.5). Paper nói người kiểm mọi phân loại nhưng chưa báo chỉ số đồng thuận giữa người với nhau.
- Chỉ một framework (OpenRCA Controller–Executor), dữ liệu tĩnh, không phải Kubernetes.
- Chỉ phân tích lỗi; không thử dùng pitfall để **dự đoán** run nào sẽ sai.

## 8. Nhóm khai thác được gì?

1. **Danh sách đặc trưng ứng viên để dự đoán agent sai:** nhiều pitfall đo được tự động từ trajectory, không cần nhãn. Ví dụ: *Limited Telemetry Coverage* (số loại tool/kênh dữ liệu đã dùng), *Meaningless Repetition* (gọi lặp), *Max Step Exhaustion* (chạm trần bước), *No Cross-Validation* (kết luận dựa trên một nguồn). Đây là cầu nối sang hướng chốt.
2. **Bài học "prompt không đủ":** hỗ trợ việc nhóm không dựa vào prompt self-check làm phương pháp chính, chỉ dùng làm baseline.
3. **Chi phí tham chiếu:** $1.394 cho 1.675 run trên dữ liệu nặng (68,5 GB, khoảng 0,8 triệu token mỗi run). Cloud-OpsBench nhẹ hơn nhiều (ReAct khoảng 55K token mỗi case theo Cloud-OpsBench v3 Table 7), nên ngân sách của nhóm nhỏ hơn đáng kể. Phải đo lại bằng pilot.
4. **Phương pháp gán nhãn lỗi bán tự động:** LLM hỏi câu có/không, rồi người kiểm. Nhóm có thể dùng cho phân tích định tính, nhưng phải báo đồng thuận giữa người.

## 9. Thuật ngữ

- **Pitfall:** kiểu lỗi lặp lại có tên gọi và tiêu chí nhận diện.
- **Controller–Executor:** kiến trúc 2 agent; một bên ra lệnh bằng lời, một bên viết code chạy.
- **Human-in-the-loop:** máy làm trước, người kiểm và quyết định cuối.
