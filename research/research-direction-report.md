# Báo cáo định hướng nghiên cứu khóa luận AIOps

- **Ngày lập:** 09/11/2026. Nguồn tra cứu đến cùng ngày; chi tiết trong [literature-search-log.md](literature-search-log.md).
- **Dành cho:** nhóm 2 người làm khóa luận cử nhân trong 6 tháng (khoảng 16/11/2026 – 15/05/2027).
- **Trạng thái:** đề xuất để nhóm và giảng viên thảo luận. **Chưa có kết quả thực nghiệm. Chưa được giảng viên duyệt.** Mọi con số "dự kiến" là giả thuyết cần kiểm chứng.
- **Quy ước nhãn:** **[Nguồn]** là điều paper hoặc artifact nói, kèm vị trí. **[Diễn giải]** là nhận định của người viết. **[Giả thuyết]** là điều cần thực nghiệm. **[Chưa kiểm]** là chưa xác minh bằng bản gốc.
- **Cách đọc:** 5 phút đọc **Mục 0**. 30–40 phút đọc cả báo cáo. Khi cần hiểu sâu một paper, mở file trong [`research/papers/`](papers/).

---

## Mục lục

0. [Kết luận trong 5 phút](#0-kết-luận-trong-5-phút)
1. [Vì sao nhóm đang bế tắc](#1-vì-sao-nhóm-đang-bế-tắc)
2. [Kiến thức nền tối thiểu](#2-kiến-thức-nền-tối-thiểu)
3. [Bức tranh nghiên cứu 2025–2026](#3-bức-tranh-nghiên-cứu-20252026)
4. [So sánh các hướng ứng viên](#4-so-sánh-các-hướng-ứng-viên)
5. [Hướng chốt: chi tiết để bắt tay vào làm](#5-hướng-chốt-chi-tiết-để-bắt-tay-vào-làm)
6. [Quan hệ với roadmap và memo cũ](#6-quan-hệ-với-roadmap-và-memo-cũ)
7. [Năm điều cần nhớ](#7-năm-điều-cần-nhớ)
8. [Phụ lục](#8-phụ-lục)

---

## 0. Kết luận trong 5 phút

### Hướng nên làm

> **"Biết khi nào nên tin AI": phân tích nguyên nhân sự cố *có chọn lọc* (selective RCA) cho LLM agent trên Kubernetes, bằng cách ước lượng độ tin cậy của từng chẩn đoán mà không cần biết đáp án, rồi quyết định *chấp nhận* hay *chuyển tiếp* (cho model mạnh hơn hoặc cho kỹ sư).**

**Tên làm việc (tiếng Anh):** *Knowing When to Trust the Agent: Selective Root Cause Analysis with Label-Free Confidence Estimation for LLM Agents in Kubernetes*

### Bài toán bằng một ví dụ [Diễn giải]

Một AI agent chẩn đoán 100 sự cố Kubernetes. Nó đúng khoảng 70 case và sai 30. Đáng sợ là khi sai, nó vẫn viết báo cáo rất tự tin. Kỹ sư trực sự cố (SRE) không biết tin case nào. Nhóm sẽ xây một **"cổng tin cậy"**: đọc *cách agent điều tra* (nó gọi tool gì, bao nhiêu lần, có lỗi không, kết luận có dựa trên quan sát thật không…) rồi cho điểm "khả năng đúng". Điểm cao thì chấp nhận; điểm thấp thì chuyển cho người hoặc model mạnh. Mục tiêu: **giảm số chẩn đoán sai bị chấp nhận**, mà vẫn để AI tự xử lý được nhiều case nhất có thể, với chi phí hợp lý.

### Các câu hỏi nghiên cứu (chi tiết ở Mục 5.5)

| RQ | Câu hỏi ngắn | Vai trò |
|---|---|---|
| **RQ1** | Agent RCA có "biết mình sai" không? Độ tự tin tự báo, tự chấm lại, đồng thuận giữa nhiều lần chạy phân biệt đúng/sai tốt đến đâu? | Nền tảng, đo hiện trạng |
| **RQ2 (chính)** | Các tín hiệu **trong quá trình điều tra**, đo tự động và không cần nhãn, có dự đoán chẩn đoán sai **tốt hơn hoặc bổ sung** cho tín hiệu tự báo không? Có chuyển được giữa hệ thống và model không? | Đóng góp chính |
| **RQ3** | Dùng điểm tin cậy để **chuyển tiếp** thì đánh đổi giữa độ đúng, tỷ lệ chuyển và chi phí ra sao, so với các chính sách đơn giản? | Giá trị thực tế |
| RQ4 (tùy chọn) | Khi telemetry bị thiếu theo cơ chế Kubernetes thật, điểm tin cậy có còn đáng tin không? | Mở rộng, nối với memo 07/11 |

### Vì sao chọn hướng này

1. **Vấn đề có thật, nhiều nguồn độc lập cùng chỉ ra:** agent mạnh nhất vẫn sai nhiều; "đúng" thường không có căn cứ; agent tự tin khi sai (Mục 3.3).
2. **Khoảng trống (tạm thời) có bằng chứng:** phương pháp đo độ tin cậy cho agent đã có ở domain khác (QA, chăm sóc khách hàng), nhưng **chưa thấy** áp dụng và đánh giá đầy đủ cho agent RCA trên benchmark tương tác. Một survey 119 trang về uncertainty cho agent không nhắc tới AIOps lần nào (Mục 5.4). Đây là nhận định tạm thời, còn phải kiểm thêm.
3. **Khả thi cho 2 sinh viên:** dùng **Cloud-OpsBench** (chạy không cần cụm Kubernetes, giấy phép MIT, có **nhãn đúng/sai khách quan**). Không phải tự xây nhãn "đủ bằng chứng", phần khó nhất của memo cũ. Phần ML chỉ là logistic regression và hiệu chỉnh xác suất.
4. **Không bỏ công sức cũ:** giữ nguyên tinh thần *selective RCA*, bộ metric coverage / selective error / risk–coverage, Cloud-OpsBench, và hiểu biết về TelemetrySuffBench, DiagGuard. Hướng "telemetry thiếu" trở thành RQ4 tùy chọn.

### Việc làm ngay trong 2 tuần đầu (chi tiết ở Mục 5.13)

1. Clone Cloud-OpsBench, **ghi commit**, chạy agent mẫu trên 3 case với một model rẻ; đo token và thời gian mỗi case.
2. Thêm trường `confidence` (0–100) vào output của agent; chạy pilot 50 case; vẽ biểu đồ "độ tự tin so với tỷ lệ đúng" đầu tiên.
3. Kiểm novelty: đọc full text Süerkan et al. (IEEE Access 2026), Xuan et al. (ACL 2026), tìm thêm trên Google Scholar.
4. Viết 1 trang pitch gửi giảng viên (mẫu ở Mục 6.3).

---

## 1. Vì sao nhóm đang bế tắc

**[Diễn giải]** Đọc roadmap (29/10) và memo (07/11), nhóm đã đi khá xa và đúng hướng về tinh thần. Bế tắc đến từ ba điểm cụ thể:

1. **Phần khó nhất không phải phần có thể làm nhanh.** Memo 07/11 đặt trọng tâm vào "trần chẩn đoán" (identifiability): xây *discriminator catalog* cho từng cặp lỗi dễ nhầm, rồi tính xem case nào còn phân biệt được khi thiếu dữ liệu. Ý tưởng hay, nhưng đòi hỏi kiến thức Kubernetes rất sâu, nhiều phán đoán của người gán nhãn, kiểm đồng thuận, kiểm rò rỉ… Nhóm phải hoàn thành toàn bộ phần này rồi mới có kết quả đầu tiên. Rủi ro cao cho 6 tháng.
2. **Tiền đề "thiếu dữ liệu là vấn đề chính" bị lung lay.** Hai paper độc lập mới đọc lần này kết luận **lỗi chủ yếu nằm ở suy luận trên bằng chứng đã có**, không phải do thiếu dữ liệu: *How Far Can RCA Go…* (2607.13548v2) và *EviRCA* (2609.19825). Xem [HowFarRCA](papers/HowFarRCA_ANALYSIS.md), [EviRCA](papers/EviRCA_ANALYSIS.md).
3. **Khoảng trống của hướng "telemetry thiếu" đang hẹp lại.** CTBench (viễn thông) đã gắn nhãn mức observability O1/O2. ORCA-bench đã thử bỏ source code. OpenRCA 2.0 nêu đúng trục này là future work, và nhóm tác giả đó (CUHK) có thể tự làm sớm. Xem [CTBench](papers/CTBench_ANALYSIS.md), [ORCA-bench](papers/ORCABench_ANALYSIS.md), [OpenRCA 2.0](papers/OpenRCA2_ANALYSIS.md).

**Lối ra:** đổi trục câu hỏi từ *"dữ liệu có đủ để chẩn đoán không?"* (cần oracle phức tạp) sang *"có biết được khi nào chẩn đoán của agent là sai không?"*. Câu hỏi mới dùng **nhãn khách quan có sẵn** (đáp án R* của Cloud-OpsBench), vẫn là selective RCA, và cho kết quả đầu tiên ngay từ tuần 2.

---

## 2. Kiến thức nền tối thiểu

### 2.1. AIOps và vị trí của đề tài

AIOps (AI for IT Operations) là dùng AI để hỗ trợ vận hành hệ thống. Vòng đời một sự cố:

```text
Hệ thống chạy → thu telemetry → phát hiện bất thường → gom cảnh báo → RCA (tìm nguyên nhân)
                                                                        │
                                              ★ Đề tài nằm ở đây: SAU khi agent RCA chẩn đoán,
                                                quyết định CÓ TIN chẩn đoán đó không
                                                                        │
                                                       khắc phục (remediation) → kiểm tra phục hồi
```

- **Telemetry:** dữ liệu vận hành: *logs* (nhật ký sự kiện), *metrics* (số đo như CPU, độ trễ), *traces* (hành trình một request qua các service), *events/state* của Kubernetes.
- **RCA (Root Cause Analysis):** tìm **thành phần** gây lỗi và **cơ chế** lỗi. Mã 503 hay `CrashLoopBackOff` chỉ là **triệu chứng**.

### 2.2. LLM agent làm RCA như thế nào

Agent là LLM được phép **gọi công cụ** (tool) theo vòng lặp, kiểu *ReAct*:

```text
(Minh họa, không phải trace thật)
Đề bài: "Người dùng báo lỗi 503 khi thanh toán"
 ┌─► Thought: "Có thể service checkout không có endpoint"
 │   Action: GetResources(type=endpoints, name=checkout)
 │   Observation: "endpoints: []"   ← kết quả trả về từ hệ thống
 └── (lặp lại vài lần, mỗi lần chọn tool tiếp theo)
     Submit: {rank 1: app/checkout – ServiceSelectorMismatch, rank 2: …, rank 3: …}
```

Trên Cloud-OpsBench, agent có 12 tool chỉ đọc với OnlineBoutique và 10 tool với TrainTicket (không có tool đọc code), gồm xem Pod, Service, YAML, logs, alerts, kiểm tra kết nối…, và tối đa 20 bước [Nguồn: Cloud-OpsBench v3 §3, §4.1; [reading report](../CloudOpsBench_reading_report.md)].

### 2.3. Benchmark "replay" là gì

Muốn so sánh công bằng nhiều agent, mọi agent phải gặp **cùng một sự cố y hệt**. Cloud-OpsBench gây lỗi thật trên cụm Kubernetes, **chụp lại** toàn bộ câu trả lời của tool (snapshot), rồi khi đánh giá thì **phát lại** (replay). Nhờ vậy nhóm chạy được trên laptop, không cần cụm, cùng truy vấn luôn cùng kết quả.

**Đáp án** của mỗi case (component + fault type) lấy từ kế hoạch tiêm lỗi đã kiểm chứng. Đây là **nhãn khách quan**, không cần ai phán đoán. Chính điều này làm hướng chốt khả thi.

### 2.4. Vì sao "đúng" chưa đủ: chẩn đoán không có căn cứ

Agent có thể đoán đúng nhờ "kinh nghiệm" có sẵn trong model mà không kiểm chứng. Cloud-OpsBench v3 cho thấy GPT-5 **đúng nhưng thiếu bằng chứng** ở 33,1% case OnlineBoutique [Nguồn: v3 §4.3, Figure 6]. Ngoài đời, kỹ sư không biết case nào "đúng có căn cứ", case nào "đúng do may", case nào "sai mà tự tin".

### 2.5. Selective prediction: các thước đo cần hiểu

**Ý tưởng:** cho phép hệ thống **không trả lời** (hoặc chuyển cho người) ở những case nó không chắc. Một ví dụ số **(do người viết dựng, không phải kết quả)**:

| Chính sách với 100 sự cố (agent đúng 70, sai 30) | Tự xử lý (coverage) | Sai bị chấp nhận | Tỷ lệ sai trong phần tự xử lý (selective error) |
|---|---|---|---|
| Tin hết | 100 | 30 | 30% |
| Chuyển ngẫu nhiên 30 case cho người | 70 | khoảng 21 | khoảng 30% (không cải thiện) |
| Cổng hoàn hảo chuyển đúng 30 case sai | 70 | 0 | 0% |
| Cổng thực tế (giả sử) chuyển 30 case | 70 | 8 | 11,4% |

Các thước đo sẽ dùng:

- **Coverage** = số case hệ thống tự chấp nhận / tổng số case.
- **Selective error (risk)** = số case **sai** trong phần được chấp nhận / số case được chấp nhận.
- **Risk–coverage curve** và **AURC:** vẽ selective error theo coverage khi thay đổi ngưỡng; diện tích dưới đường cong càng **nhỏ** càng tốt.
- **AUROC:** lấy ngẫu nhiên một case đúng và một case sai; AUROC là xác suất điểm tin cậy của case đúng **cao hơn** case sai. 0,5 là đoán mò; 1,0 là hoàn hảo.
- **ECE (calibration):** khi model nói "80% chắc chắn", thì khoảng 80% số lần đó phải đúng. ECE đo độ lệch; càng nhỏ càng tốt.
- **Brier score:** sai số bình phương giữa xác suất dự đoán và kết quả thật (0/1); càng nhỏ càng tốt.

> **Giải thích thêm:** AUROC trả lời "điểm có **xếp hạng** đúng không"; ECE trả lời "điểm có **đúng nghĩa xác suất** không". Một điểm có thể xếp hạng tốt (AUROC cao) mà vẫn quá tự tin (ECE cao). Khi đó chỉ cần hiệu chỉnh lại thang điểm (ví dụ bằng isotonic regression).

---

## 3. Bức tranh nghiên cứu 2025–2026

### 3.1. Bản đồ năm nhóm nghiên cứu

```text
LLM agent cho vận hành (AIOps), 2025–2026
├── (1) Benchmark / môi trường đo agent
│     Cloud-OpsBench · OpenRCA 2.0 · ORCA-bench · CTBench · SREGym · ITBench · AIOpsLab · SRE-World
├── (2) Phân tích vì sao agent sai
│     Kim et al. (12 pitfall) · Riddell et al. (16 lỗi suy luận) · How Far RCA · EviRCA · DiagGuard
├── (3) Phương pháp làm agent RCA đáng tin hơn
│     DiagGuard · JustDiag · STAR · Auditable Graph RCA · TriFleetRCA · AOI · (TopoEvo, GALA, KRCA, LATS-RCA…)
├── (4) Độ tin cậy / uncertainty của agent nói chung (ngoài AIOps)
│     HTC · TRACER · Trajectory-UQ · UQ-Agents survey · UCCI (cascade) · PACE-LM (AIOps, không phải agent)
└── (5) Kiểm toán cách đánh giá
      Pooled-Leaderboard Audit · Auditable Graph RCA · Passing Without Repairing
```

**Hướng chốt nằm ở giao điểm của nhóm (1), (2) và (4):** dùng benchmark của (1), tín hiệu lỗi từ (2), phương pháp đo độ tin cậy từ (4), cho bài toán RCA mà (4) chưa đụng tới.

### 3.2. Bảng tổng hợp các paper đã phân tích

Cột "Vai trò" cho biết paper giúp gì cho đề tài. Đọc file phân tích khi cần chi tiết.

| Paper (phiên bản) | Loại | Ý chính một câu | Con số đáng nhớ | Vai trò với đề tài | File |
|---|---|---|---|---|---|
| **Cloud-OpsBench** (2603.00468 v3) | Benchmark K8s replay | 754 case, 57 loại lỗi; chấm cả quá trình | JRA trung bình 11 model: 0,59 (OB), 0,49 (TT); GPT-5 đúng-thiếu-bằng-chứng 33,1% | **Môi trường chính** | [v3 changes](papers/CloudOpsBench_v3_CHANGES.md), [finding](../finding/CloudOpsBench_FINDING.md) |
| OpenRCA 2.0 (2606.27154 v2) | Benchmark tĩnh | Gán nhãn đường lan truyền; agent đúng thủ phạm, sai đường đi | EM 20,7%; AnySvc 76,0% nhưng PR 61,5% | Động lực; "information availability" là future work | [file](papers/OpenRCA2_ANALYSIS.md) |
| ORCA-bench (2607.28545 v3) | Benchmark on-call | Agent coding mạnh nhất ở điều kiện on-call thật | Tốt nhất 25,3% (Medium), 10% (Hard); bịa 7–40%; 26–40% truy vấn rỗng/lỗi | Động lực; tín hiệu "truy vấn rỗng" | [file](papers/ORCABench_ANALYSIS.md) |
| CTBench (2608.12002 v2) | Benchmark viễn thông | Gắn mức observability O1/O2 cho task | Chuyên gia 80,95%; harness quan trọng | Tiền lệ cho trục "thiếu dữ liệu" | [file](papers/CTBench_ANALYSIS.md) |
| SREGym (2605.07161 v3) | Benchmark live | Chẩn đoán + khắc phục trên hệ thật | Agent "tham lam", bám nhiễu đầu tiên | Lý do không chọn remediation | [file](papers/SREGym_ANALYSIS.md) |
| TelemetrySuffBench (2608.07899 v1) | Benchmark trace tĩnh | Telemetry đủ để báo động, không đủ để tìm gốc | FAR 100% ở DeepSeek/Qwen khi hồ sơ mơ hồ | Metric FAR/UAR; ý tưởng nhãn mơ hồ khách quan | [finding](../finding/TelemetrySuffBench_FINDING.md) |
| Kim et al. (2602.09937 v2) | Phân tích lỗi | 12 pitfall trên 1.675 run OpenRCA | Hallucination in Interpretation 71,2%; prompt không chữa được | Nguồn đặc trưng; chi phí tham chiếu $1.394 | [file](papers/WhyAgentsFailRCA_ANALYSIS.md) |
| **Riddell et al.** (2601.22208, FORGE'26) | Phân tích lỗi | 16 lỗi suy luận; **lỗi suy luận dự báo kết quả sai** | 48.000 kịch bản | **Tiền lệ gần nhất** cho RQ2 | [file](papers/StalledBiasedConfused_ANALYSIS.md) |
| How Far RCA (2607.13548 v2) | Phân tích lỗi | Giữ bằng chứng cố định: tri thức thắng quy trình | Full Score 14,10 → 35,90 nhờ rule khai thác | Lỗi do suy luận, không do dữ liệu | [file](papers/HowFarRCA_ANALYSIS.md) |
| EviRCA (2609.19825) | Phương pháp | Tách trích bằng chứng khỏi suy luận | 40,6–43,9% so với ≤ 15,2%; token ít hơn 15–26 lần | Nút thắt là phán đoán | [file](papers/EviRCA_ANALYSIS.md) |
| DiagGuard (2608.21310 v2) | Phân tích + phương pháp | 5.000 trajectory; taxonomy OMIT/MIS/GEN; verifier | Acc@1 tăng trung vị 10,5% | Baseline verifier; "thất bại tốn nhiều bước hơn" | [finding](../finding/BeyondFaultLocalization_FINDING.md) |
| JustDiag (2606.19407) | Phương pháp | Hồ sơ lập luận + được phép không chốt | Outcome 51,0 → 57,7 (LLM judge, 66 case kín) | Tiền lệ non-closure | [file](papers/JustDiag_ANALYSIS.md) |
| STAR (2605.15581) | Phương pháp | Tìm giai đoạn hỏng rồi sửa; có **audit score với ngưỡng** | Acc@1 mABC 37,2 → 56,2% | Gần nhất về "cổng", nhưng không đánh giá cổng | [file](papers/STAR_ANALYSIS.md) |
| Auditable Graph RCA (2606.08590) | Phương pháp + audit | Tự kiểm toán mức tăng trên ITBench | F1 0,61 → 0,91, còn 0,70 khi bỏ gợi ý; phụ thuộc object ChaosMesh | Checklist chống rò rỉ | [file](papers/AuditableGraphRCA_ANALYSIS.md) |
| TriFleetRCA (2609.23766) | Phương pháp | RCA trên một GPU, model 14B, cụm thật | Hit 0,85–0,95; một lỗi "đúng nhưng trích sai" mọi lần | Khả thi model local | [file](papers/TriFleetRCA_ANALYSIS.md) |
| AOI (2603.03378 v4) | Huấn luyện | GRPO cho model 14B, học từ thất bại | 14B 42,9% so với Sonnet 4.5 41,3% (2×A100) | Lý do không chọn fine-tune | [file](papers/AOI_ANALYSIS.md) |
| PACE-LM (2309.05833) | Confidence cho RCA | Microsoft chấm độ tin cậy gợi ý RCA của GPT-4 | 121.308 sự cố kín | **Tiền lệ AIOps**; không phải agent | [file](papers/PACELM_ANALYSIS.md) |
| **HTC** (2601.15778, ICML'26) | UQ cho agent | 48 đặc trưng log-prob → logistic regression | 8 benchmark QA/reasoning | **Phương pháp mượn được**; cần log-prob | [file](papers/AgenticConfidenceCalibration_ANALYSIS.md) |
| **TRACER** (2602.11409, ICML'26) | UQ cho agent | Rủi ro tập trung ở vài bước; lấy phần tệ nhất | AUROC +4,7–37,1% trên τ²-bench | Ý tưởng tín hiệu lặp, lệch hành động–quan sát | [file](papers/TRACER_ANALYSIS.md) |
| **Trajectory-UQ** (2608.11552) | UQ cho agent | So 3 họ UQ cho agent dùng tool | Self-consistency thường mạnh nhất; không họ nào ổn định mọi domain | **Danh sách baseline**; lý do phải kiểm lại trên RCA | [file](papers/TrajectoryUQ_ANALYSIS.md) |
| UQ-Agents survey (2609.07395) | Survey | Taxonomy UQ cho agent; metric TC-ECE | 0 lần nhắc AIOps/SRE/incident/root cause | Bằng chứng gián tiếp về khoảng trống | [file](papers/UQAgentsTaxonomy_ANALYSIS.md) |
| UCCI (2605.18796) | Cascade | Hiệu chỉnh trước, chọn ngưỡng sau | Giảm 31% chi phí ở cùng F1 | Công thức chính sách chuyển tiếp | [file](papers/UCCI_ANALYSIS.md) |
| Pooled-Leaderboard Audit (2606.29159 v2) | Audit | Xếp hạng gộp hay đảo chiều khi tách hệ thống | 0/23 paper RCA công bố output từng case | Checklist báo cáo kết quả | [file](papers/PooledLeaderboardAudit_ANALYSIS.md) |

Các paper chỉ biết qua abstract (ITBench, AIOpsLab, STRATUS, SRE-World, Süerkan et al. IEEE Access 2026, The Confidence Dichotomy ACL 2026…) liệt kê ở [Phụ lục 8.1](#81-paper-chỉ-biết-qua-abstract-hoặc-trang-hội-nghị).

### 3.3. Bảy điều cả lĩnh vực đang thấy

Mỗi điều có ít nhất hai nguồn độc lập. Đây là "nền móng" để lập luận cho đề tài.

**(1) Agent RCA còn sai nhiều, kể cả model mạnh nhất.**
- Cloud-OpsBench v3: JRA trung bình 11 model 0,59 (OnlineBoutique) và 0,49 (TrainTicket); cao nhất 0,78 và 0,68 [Nguồn: v3 §1].
- ORCA-bench: tốt nhất 25,3% ở mức Medium, 10% ở Hard [Nguồn: Abstract].
- OpenRCA 2.0: khớp chính xác tập root cause trung bình 20,7% [Nguồn: Abstract].
- SRE-World (NeurIPS 2026, bài toán khắc phục trên cụm live): GPT 5.6 giải 29% episode [Nguồn: trang NeurIPS, chỉ abstract].

**(2) "Đúng" thường không có căn cứ.**
- Cloud-OpsBench v3: GPT-5 đúng nhưng thiếu bằng chứng 33,1% (OB), 29,4% (TT) [Nguồn: v3 §4.3].
- OpenRCA 2.0: đúng ít nhất một service 76,0%, có đường lan truyền kiểm chứng 61,5% [Nguồn: Abstract].
- CTBench: kể cả khi đúng, agent thường thiếu bằng chứng chuyên gia yêu cầu [Nguồn: §6].
- TriFleetRCA: một lỗi được chẩn đoán đúng nhưng trích dẫn sai ở mọi lần chạy [Nguồn: Abstract].

**(3) Agent tự tin khi sai, và hay bịa.**
- ORCA-bench: nêu root cause không khớp nguyên nhân nào ở 7–40% báo cáo [Nguồn: Abstract].
- Kim et al.: *Hallucination in Interpretation* ở 71,2% run [Nguồn: Table 3].
- TelemetrySuffBench: trên hồ sơ mơ hồ, DeepSeek và Qwen vẫn chốt một nguyên nhân 100% số lần [Nguồn: Table IV, qua [finding](../finding/TelemetrySuffBench_FINDING.md)].
- SREGym: mọi agent coi bất thường đầu tiên là lỗi cần sửa, kể cả khi đó là nhiễu [Nguồn: §3.1, Appendix D].

**(4) Nút thắt chủ yếu là suy luận trên bằng chứng đã có, không phải thiếu dữ liệu.**
- How Far RCA: trong 130 chiều bị gán lỗi (Market CB1), chỉ 7,7% là "Data Ambiguity" (không nguồn nào chứa tín hiệu); còn lại là "Reasoning Gap" (bằng chứng có, suy luận sai). Thêm tri thức phân biệt lỗi giúp nhiều nhất [Nguồn: Table 12, Appendix D.2, §6].
- EviRCA: *"the binding difficulty lies in judging evidence that the extraction stage has already surfaced"* [Nguồn: Abstract].

**(5) Thêm prompt hoặc quy trình không chắc giúp, có khi còn hại.**
- How Far RCA: bỏ quy trình 5 bước làm điểm **tăng** ở cả 3 điều kiện [Nguồn: Abstract].
- Kim et al.: prompt engineering không giảm lỗi diễn giải [Nguồn: §5–§6].
- TelemetrySuffBench: prompt P3 không giúp DeepSeek và Qwen [Nguồn: Table IV].
- Riddell et al.: workflow agent (ReAct, Plan-and-Execute) thường không hơn hỏi thẳng một lần [Nguồn: §4.1].

**(6) Cách tổ chức agent (harness) ảnh hưởng mạnh, kể cả khi giữ nguyên model.**
- Cloud-OpsBench v3 RQ4: cùng GLM-5.1, ECR của ReAct 0,68 so với Codex 0,83 [Nguồn: Table 7].
- CTBench: cùng model, harness khác giải những tập task khác nhau [Nguồn: Appendix, Table 23–24].

**(7) Quá trình chạy chứa tín hiệu dự báo đúng hay sai.**
- Riddell et al.: anchoring, lặp không tiến triển, chọn bằng chứng tùy tiện, không cập nhật niềm tin đi kèm tỷ lệ đúng thấp hơn rõ [Nguồn: §4.4, Observation 12].
- DiagGuard: lượt thất bại tốn nhiều round và token hơn lượt thành công [Nguồn: §5, qua [finding](../finding/BeyondFaultLocalization_FINDING.md)].
- Ở domain khác: HTC và TRACER dùng đặc trưng trên toàn trajectory và dự đoán thất bại tốt hơn các baseline chỉ nhìn đầu ra; trong Trajectory-UQ, thước đo đồng thuận dựa trên cấu trúc trajectory (tập hành động, tương đương trajectory) thường dẫn đầu [Nguồn: các paper tương ứng].

**[Diễn giải]** Từ (1)–(7): agent RCA **sẽ còn sai** trong tương lai gần; khi sai thường vẫn tự tin; nhưng **dấu vết điều tra** của nó có thể tiết lộ lúc nó sai. Chưa ai (theo những gì nhóm tìm được) biến điều (7) thành một **cổng tin cậy được đánh giá đầy đủ** cho agent RCA. Đó là chỗ đề tài bước vào.

---

## 4. So sánh các hướng ứng viên

Đánh giá định tính theo bốn tiêu chí: (a) có bằng chứng về vấn đề chưa giải quyết, (b) còn chỗ trống, (c) khả thi với 2 sinh viên trong 6 tháng, (d) hữu ích. Không cho điểm số vì sẽ tạo cảm giác chính xác giả.

| Hướng | (a) Vấn đề | (b) Chỗ trống | (c) Khả thi | (d) Hữu ích | Quyết định |
|---|---|---|---|---|---|
| **A. Độ tin cậy và chuyển tiếp cho agent RCA (selective RCA)** | Mạnh (Mục 3.3) | Khá rõ, tạm thời (Mục 5.4) | **Cao:** replay, nhãn khách quan, ML đơn giản | Cao: đúng cách AI SRE được dùng (AI xử lý trước, người duyệt khi cần) | **CHỌN** |
| B. Trần chẩn đoán khi telemetry thiếu (memo 07/11) | Mạnh | Đang hẹp lại (CTBench, ORCA-bench, OpenRCA 2.0) | Trung bình–thấp: oracle phức tạp | Cao về khoa học | Giữ thành **RQ4 tùy chọn** |
| C. Agent RCA mới chính xác hơn (verifier, graph, multi-agent) | Mạnh | Thấp: rất đông (DiagGuard, STAR, TopoEvo, GALA, KRCA, LATS-RCA, EviRCA, JustDiag…) | Trung bình | Trung bình | Không chọn |
| D. Khắc phục sự cố trên cụm thật (remediation) | Mạnh | Trung bình | Thấp: cần cụm, reset, tốn | Cao | Không chọn (đã có SREGym, SRE-World, ITBench, STRATUS; phần lớn từ nhóm có hạ tầng lớn) |
| E. Fine-tune model nhỏ cho RCA | Mạnh | Thấp–trung bình (AOI, NeurIPS 2026, Edge Delta) | Thấp: cần GPU A100 | Cao | Không chọn |
| F. Audit lối tắt của benchmark | Trung bình | Trung bình (2510.04711, 2606.29159, Auditable Graph RCA đã làm một phần) | Rất cao | Trung bình | **Phương án lùi** và phân tích phụ trong A |
| G. Sửa cấu hình Kubernetes sai bằng LLM | Trung bình | Thấp (GenKubeSec, LLMSecConfig, 2609.27030) **[chỉ đọc abstract]** | Cao | Trung bình | Không chọn: lệch khỏi công sức đã bỏ ra |

**Vì sao A thắng B, dù B có tính khoa học cao [Diễn giải]:** B cần xây oracle "đủ bằng chứng" trước khi có kết quả đầu tiên; A dùng nhãn đúng/sai có sẵn và có kết quả từ tuần 2. A vẫn có thể làm B ở dạng nhẹ (RQ4) khi đã có hạ tầng. Ngược lại, nếu làm B mà oracle không đạt đồng thuận, nhóm gần như không còn gì để báo cáo.

---

## 5. Hướng chốt: chi tiết để bắt tay vào làm

### 5.1. Tên đề tài

- **Tiếng Việt:** *Biết khi nào nên tin AI: Phân tích nguyên nhân sự cố có chọn lọc cho LLM agent trên Kubernetes bằng ước lượng độ tin cậy không cần nhãn*
- **Tiếng Anh:** *Knowing When to Trust the Agent: Selective Root Cause Analysis with Label-Free Confidence Estimation for LLM Agents in Kubernetes*

Tên giữ cụm **Selective Root Cause Analysis** của roadmap để giảng viên thấy sự liên tục.

### 5.2. Bài toán

**Đầu vào:** một sự cố Kubernetes được báo bằng câu mô tả triệu chứng (query của Cloud-OpsBench).

**Quy trình:**

```text
Sự cố ──► Agent RCA (rẻ) điều tra bằng các tool chỉ đọc ──► Chẩn đoán top-3 + toàn bộ trajectory
                                                              │
                                   Trích tín hiệu tin cậy (CHỈ từ những gì agent thấy và làm)
                                                              │
                                         Mô hình tin cậy → p = xác suất chẩn đoán đúng
                                                              │
                        p ≥ ngưỡng ──► CHẤP NHẬN (báo kỹ sư "AI chắc chắn", hoặc chuyển bước khắc phục)
                        p < ngưỡng ──► CHUYỂN TIẾP: cho agent mạnh hơn, hoặc cho kỹ sư
```

**Đầu ra của nghiên cứu:** (1) mức độ agent "biết mình sai"; (2) bộ tín hiệu và mô hình tin cậy; (3) đánh đổi độ đúng – tỷ lệ chuyển – chi phí; (4) bộ dữ liệu trajectory công khai.

**"Không cần nhãn" nghĩa là gì?** Lúc vận hành thật, không ai biết đáp án. Vì vậy tín hiệu chỉ được tính từ query, các lệnh agent đã gọi, kết quả trả về, suy nghĩ và câu trả lời của agent. Nhãn đúng/sai **chỉ dùng để huấn luyện và đánh giá** mô hình tin cậy, giống như huấn luyện bộ lọc thư rác bằng thư đã gắn nhãn.

### 5.3. Vì sao hữu ích và có giá trị khoa học

**Hữu ích trong thực tế:**
- Microsoft đã coi "độ tin cậy của gợi ý RCA" là vấn đề thật của kỹ sư on-call: gợi ý sai làm mất thời gian và dẫn sai hướng [Nguồn: PACE-LM §1, [file](papers/PACELM_ANALYSIS.md)].
- Các sản phẩm "AI SRE" hiện nay đặt AI ở bước xử lý đầu tiên rồi chuyển cho người khi không chắc **[Bối cảnh: blog doanh nghiệp, không phải bằng chứng bình duyệt]**. Đề tài cung cấp cách **đo** xem việc chuyển đó có hiệu quả không.
- Chẩn đoán sai mà được tin có thể dẫn tới khắc phục sai. SREGym và *Passing Without Repairing* cho thấy hậu quả ở bước khắc phục **[Nguồn: SREGym §3.1, Appendix D; trang NeurIPS 2026]**.

**Giá trị khoa học:**
- Trajectory-UQ (2608.11552) kết luận phương pháp UQ *"should be revalidated at the trajectory level"* và **không họ phương pháp nào ổn định ở mọi domain**. Kiểm lại trên RCA là câu hỏi chính đáng, không phải lặp lại [Nguồn: Abstract].
- UQ-Agents survey (2609.07395): độ tự tin agent tự báo không luôn hơn baseline đơn giản; toàn văn không nhắc AIOps [Nguồn: Abstract; tìm toàn văn].
- *The Confidence Dichotomy* (ACL 2026): tool **lấy bằng chứng** làm agent **quá tự tin**, tool **kiểm chứng** thì giảm **[Nguồn: kết quả tìm kiếm và trích dẫn trong 2608.11552; chưa đọc full text]**. Agent RCA dùng hầu hết là tool lấy bằng chứng, nên **[Giả thuyết]** agent RCA đặc biệt dễ quá tự tin. Đây là móc lý thuyết đẹp cho H1.

### 5.4. Khoảng trống nghiên cứu (tạm thời)

| Thành phần | Đã có ở đâu | Còn thiếu (theo những gì đã đọc) |
|---|---|---|
| Độ tin cậy cho chẩn đoán RCA | PACE-LM (2023): RCA một bước, dữ liệu Microsoft kín, dựa vào kho sự cố lịch sử | Agent **nhiều bước**, benchmark **mở**, dựa vào **quá trình điều tra** |
| UQ cho trajectory của agent | HTC, TRACER, Trajectory-UQ, UQ-Agents survey | Chưa kiểm trên RCA/AIOps; nhiều phương pháp cần log-prob (API như Claude không cung cấp) |
| Abstention trong RCA | TelemetrySuffBench (trace tĩnh, agent tự từ chối); JustDiag (non-closure, chấm bằng LLM judge); ORCA-bench (control task "không có sự cố") | Chưa có đánh giá **cổng bên ngoài** bằng risk–coverage với nhãn khách quan trên môi trường **tương tác** |
| Cổng chấp nhận trong agent RCA | STAR: audit score với ngưỡng τ để quyết định sửa | Không đánh giá chính cái cổng (AUROC, calibration, coverage) |
| Dấu hiệu báo trước chẩn đoán sai | Riddell et al.: LLM judge gán lỗi suy luận sau khi chạy, đo tương quan | Chưa có đặc trưng **tự động, rẻ** và **chính sách quyết định** được đánh giá |
| Cascade / chuyển tiếp | UCCI, FrugalGPT (NER, QA) | Chưa có cho agent RCA |
| Benchmark kiểm abstain/escalate theo ngưỡng | Tìm kiếm mở rộng (truy vấn #20 trong search log) không thấy trên OpenRCA, ITBench, Cloud-OpsBench | — |

**Cảnh báo trung thực:** đây là **candidate gap**. "Không tìm thấy" khác "không tồn tại". Trước khi viết proposal, phải làm xong các kiểm tra sau (ước tính 2–3 ngày):

1. Đọc full text **Süerkan et al., IEEE Access 2026** (DOI 10.1109/access.2026.3743626; ResearchGate chặn truy cập tự động). Abstract cho thấy bài này về Reflexion cho **khắc phục**, không phải độ tin cậy của chẩn đoán, nhưng phải kiểm phần "self-verification".
2. Đọc full text **Xuan et al., ACL 2026** (arXiv 2601.07264) và **Oh et al., ACL 2026**.
3. Tìm trên Google Scholar và ACM DL: `"root cause" calibration agent`, `"learning to defer" incident`, `conformal "root cause analysis"`, `selective prediction AIOps`; xem danh sách bài ICSE/FSE/ASE 2026 và workshop AIOps 2026.
4. Đọc kỹ phần audit của STAR (RQ3–RQ4) và TopoEvo (cùng nhóm tác giả).
5. Xem trang kết quả của OpenSRE trên Cloud-OpsBench (có báo confidence không).

Nếu tìm thấy paper làm đúng việc này, **không bỏ hướng**: chuyển thành "tái lập + mở rộng" (ví dụ thêm RQ3 cascade, RQ4 telemetry thiếu, hoặc model khác). Với khóa luận cử nhân, tái lập cẩn thận vẫn có giá trị.

### 5.5. Câu hỏi nghiên cứu, giả thuyết và điều kiện bác bỏ

**Câu hỏi trung tâm:** *Có thể biết, mà không cần đáp án, khi nào chẩn đoán của LLM agent RCA trên Kubernetes là sai không; tín hiệu nào làm tốt nhất; và dùng nó để chuyển tiếp thì được lợi bao nhiêu?*

---

**RQ1 — Agent có biết mình sai không?** *(mô tả hiện trạng)*

> Trên Cloud-OpsBench, các tín hiệu do chính agent cung cấp (độ tự tin tự báo 0–100, tự chấm lại trajectory, đồng thuận giữa K lần chạy) phân biệt chẩn đoán đúng và sai tốt đến đâu, và có được hiệu chỉnh không?

- **Đo:** AUROC, AURC, ECE, Brier; reliability diagram; tách theo model × hệ thống × nhóm lỗi.
- **[Giả thuyết] H1:** độ tự tin tự báo **quá tự tin** (nhiều chẩn đoán sai có confidence ≥ 80%, ECE lớn). Self-consistency phân biệt tốt hơn nhưng tốn gấp K lần chi phí.
- **Bác bỏ khi:** độ tự tin tự báo đã có AUROC cao và ECE thấp, ngang phương pháp tốt nhất. Thông điệp đổi thành "agent RCA đã khá biết mình sai". Vẫn là kết quả công bố được.

---

**RQ2 (câu hỏi chính) — Quá trình điều tra có tiết lộ chẩn đoán sai không?** *(dự đoán)*

> Các đặc trưng không cần nhãn trích từ trajectory (nỗ lực, chất lượng quan sát, mức bám bằng chứng của kết luận, động học giả thuyết) có dự đoán chẩn đoán sai **tốt hơn hoặc bổ sung** cho tín hiệu ở RQ1 không, và có **chuyển** được giữa hệ thống và model không?

- **Đo:** AUROC/AURC của mô hình đặc trưng so với các baseline RQ1, trên cùng tập test; so sánh theo cặp bằng bootstrap; ablation từng nhóm đặc trưng; chuyển giao OnlineBoutique → TrainTicket, model A → model B, bỏ-một-nhóm-lỗi.
- **[Giả thuyết] H2:** mô hình gộp (quá trình + tự báo) có AURC thấp hơn mọi họ đơn lẻ; nhóm "bám bằng chứng" và "chất lượng quan sát" đóng góp nhiều nhất.
- **Bác bỏ khi:** không cải thiện có ý nghĩa so với self-consistency hoặc độ tự tin tự báo (khoảng tin cậy của chênh lệch chứa 0). Khi đó báo cáo "tín hiệu quá trình không thêm thông tin": một kết quả âm tính có giá trị, vì nó cho biết nên đầu tư vào đâu.

---

**RQ3 — Chuyển tiếp theo điểm tin cậy thì được gì?** *(giá trị thực tế)*

> Dùng điểm tin cậy làm chính sách "chấp nhận hoặc chuyển tiếp" (agent rẻ chạy trước; case kém tin cậy chuyển cho agent mạnh hoặc cho người), đánh đổi giữa độ đúng, tỷ lệ chuyển và chi phí ra sao so với: luôn dùng agent rẻ, luôn dùng agent mạnh, chuyển ngẫu nhiên cùng tỷ lệ, chuyển theo độ tự tin tự báo?

- **Đo:** số chẩn đoán sai bị chấp nhận trên 100 sự cố; độ đúng toàn hệ thống; tổng token/chi phí; số sự cố cần người xem trên 100; đường Pareto. Ngưỡng chọn trên tập dev rồi khóa lại.
- **[Giả thuyết] H3:** ở cùng tỷ lệ chuyển, chính sách theo điểm tin cậy giảm rõ số chẩn đoán sai bị chấp nhận so với chuyển ngẫu nhiên, và tiến gần độ đúng của agent mạnh với chi phí thấp hơn.
- **Bác bỏ khi:** không hơn chuyển ngẫu nhiên; hoặc agent mạnh **sai cùng những case** agent rẻ sai (lỗi tương quan). Khi đó chuyển sang model mạnh vô ích, chỉ chuyển cho người mới có ích. Đây cũng là một phát hiện thực tế.

> **Giải thích thêm:** Cloud-OpsBench v3 cho thấy model "đắt" chưa chắc đúng hơn: trên OnlineBoutique, GPT-5 có JRA 0,68, thấp hơn DeepSeek-V4-Flash (0,73) [Nguồn: v3 Table 5]. EviRCA còn thấy **81–87% case sai trùng nhau giữa hai LLM** trên OpenRCA [Nguồn: EviRCA §V-A]. Vì vậy RQ3 không mặc định "model mạnh luôn đúng". Phải đo xem hai model có sai **khác case** nhau không, trước khi kết luận chuyển sang model khác có ích.

---

**RQ4 (tùy chọn) — Khi telemetry thiếu, điểm tin cậy có còn đáng tin không?** *(mở rộng, chỉ làm nếu qua gate tháng 4)*

> Dưới các profile mất dữ liệu có căn cứ cơ chế Kubernetes (events hết hạn, mất log của container trước restart, không có log ứng dụng; xem memo 07/11 §6.2), độ đúng giảm bao nhiêu, và điểm tin cậy có giảm tương ứng không, khi giữ nguyên ngưỡng chọn trên dữ liệu đầy đủ?

- **Đo:** ECE, AURC và số chẩn đoán sai bị chấp nhận trên dữ liệu suy giảm.
- **[Giả thuyết] H4:** độ tự tin tự báo **vẫn cao** dù độ đúng giảm; đặc trưng "output rỗng/lỗi" bắt được một phần.
- **Lưu ý:** tạo view thiếu dữ liệu phải theo quy tắc của memo (response thay thế giống hệ thật, không chuỗi "MASKED", có manifest). Đây là thí nghiệm **can thiệp nhân tạo**, không đại diện cho phân bố mất dữ liệu ngoài đời.

### 5.6. Phương pháp

#### 5.6.1. Dữ liệu

- **Cloud-OpsBench v3** (754 case: OnlineBoutique 550, TrainTicket 204; 57 loại lỗi; 8 nhóm). Repo MIT: https://github.com/LLM4Ops/Cloud-OpsBench. **Ghim commit** khi clone (commit mới nhất thấy ngày 09/11/2026: `ec1d4f38b952…`, 03/11/2026).
- **Nhãn chính:** chẩn đoán rank-1 đúng cả component và fault type (JRA = 1) hay không, tính bằng `evaluation.py` của repo.
- **Nhãn phụ (chỉ để phân tích):** CA (đúng component), và cặp JRA × ECR để xem cổng có bắt được "đúng nhưng thiếu bằng chứng" không. ECR **không** dùng làm đặc trưng.
- **Cấm dùng làm đặc trưng:** mọi thứ agent không thấy, gồm `metadata.json` (trừ câu query), `process-label/`, `golden-trajectory/`, tên thư mục category.

#### 5.6.2. Agent và model

- Agent: **ReAct mặc định của Cloud-OpsBench** (`agents/cloudops_agent`), giữ nguyên prompt và tool. Chỉ thêm trường `confidence` vào JSON của `Submit`. Lý do: harness ảnh hưởng mạnh (v3 RQ4), nên cố định harness để so sánh công bằng.
- Model (chốt sau pilot; giao diện OpenAI-compatible nên đổi model dễ):
  - **Agent rẻ chính:** một model rẻ có JRA khá, ví dụ DeepSeek-V4-Flash (v3: 0,73 OB / 0,63 TT) hoặc Qwen3.5-27B (0,72 / 0,56).
  - **Agent rẻ thứ hai** (cho thí nghiệm chuyển giao): một model họ khác, ví dụ Gemini-2.5-Flash hoặc GLM-5.1.
  - **Agent mạnh** (cho cascade, chạy trên tập con): một model frontier.
  - Tùy chọn: một model chạy local (ví dụ Qwen3-8B/14B) nếu có GPU. Model yếu sai nhiều hơn nên cho thêm ví dụ "sai" để huấn luyện cổng.
- Chạy chính ở temperature 0 như paper. Các lần chạy cho self-consistency dùng temperature > 0 (ví dụ 0,7). **Ghi rõ** vì đây là thay đổi so với thiết lập gốc.

#### 5.6.3. Tín hiệu tin cậy (đặc trưng)

Agent của Cloud-OpsBench đã lưu từng bước: thought, action, tham số, observation, lỗi, token, latency, và câu trả lời top-3 kèm `key_evidence_summary` (đã kiểm trong mã nguồn `runtime/core.py`, `runtime/contracts.py`). Danh sách ứng viên **v0**, chốt sau pilot và **đóng băng trước khi xem tập test**:

| Nhóm | Đặc trưng (ví dụ) | Lấy cảm hứng từ |
|---|---|---|
| **A. Nỗ lực và kiểm soát** | Số bước; có chạm trần 20 bước không; tỷ lệ gọi lặp y hệt (cùng tool + tham số); số hành động không hợp lệ | Cloud-OpsBench (Steps, RAR); DiagGuard F3; Riddell RF-12; Kim "Meaningless Repetition", "Max Step Exhaustion" |
| **B. Chất lượng quan sát** | Tỷ lệ output lỗi/rỗng (`Not Found`, `UnsupportedQuery`, danh sách rỗng); số kênh bằng chứng đã dùng (state/events, logs, alerts, connectivity, node, code); có xem events/alerts không | ORCA-bench Finding #4; Kim "Limited Telemetry Coverage"; Cloud-OpsBench "tool-grounding failure" |
| **C. Mức bám bằng chứng của kết luận** | Object bị đổ lỗi (rank-1) có từng là đích của tool call nào không; tên object có xuất hiện trong output nào không; output về object đó có từ khóa bất thường (`CrashLoopBackOff`, `OOMKilled`, `Pending`, `refused`, `timeout`, 5xx…) không; bước kiểm tra cuối có nhắm vào object đó không | OpenRCA 2.0 (ungrounded); TriFleetRCA (grounded citation); prompt Cloud-OpsBench yêu cầu rank-1 phải có output tool chứng minh |
| **D. Động học giả thuyết** | Số object khác nhau đã kiểm; bước đầu tiên object kết luận xuất hiện (quá sớm có thể là neo); rank-1 và rank-2 cùng object khác cơ chế (mơ hồ cơ chế) hay khác object (mơ hồ vị trí) | Riddell RF-13 anchoring, RF-09; DiagGuard GEN1; Cloud-OpsBench §4.6 (nhầm cơ chế gần nhau) |
| **E. Tự báo và đồng thuận** | Confidence 0–100 trong `Submit`; tự chấm lại (P(True)); tỷ lệ K lần chạy cho cùng rank-1; độ giống tập tool đã gọi giữa các lần (Jaccard) | Trajectory-UQ (reflexive, consistency, action-set); HTC |
| **F. Độ khó từ đầu vào** (chỉ làm baseline) | Từ khóa triệu chứng trong query (latency, 503, pending…); hệ thống OB/TT | Pooled-Leaderboard Audit (probe đơn giản) |

> **Giải thích thêm:** nhóm F đo xem chỉ nhìn **đề bài** đã đoán được bao nhiêu. Nếu mô hình chỉ dùng query đã dự đoán tốt bằng mô hình quá trình, thì "tín hiệu quá trình" không mang thông tin mới. Đây là phép thử chống tự lừa mình.

#### 5.6.4. Mô hình tin cậy và chính sách

- **Mô hình chính:** logistic regression có điều chuẩn L1 (thưa, dễ giải thích, ổn khi ít dữ liệu, giống HTC). Kiểm thêm một mô hình cây nhỏ (ví dụ gradient boosting của scikit-learn) để xem có quan hệ phi tuyến đáng kể không.
- **Hiệu chỉnh:** isotonic regression trên tập dev (như UCCI) để điểm thành xác suất đúng nghĩa.
- **Chính sách:** chọn ngưỡng trên dev theo ràng buộc, ví dụ "selective error ≤ 10%", hoặc "tỷ lệ chuyển ≤ 30%". **Khóa ngưỡng** rồi mới chạy test.

#### 5.6.5. Các phương pháp so sánh

| Mã | Bộ chấm điểm tin cậy | Chi phí thêm |
|---|---|---|
| S0 | Ngẫu nhiên (mốc AUROC 0,5) | 0 |
| S1 | Độ tự tin tự báo (trường `confidence`) | Gần 0 |
| S2 | Tự chấm lại: cùng model đọc trajectory, trả lời "chẩn đoán này đúng không?" (P(True)) | 1 lần gọi |
| S3 | Self-consistency: tỷ lệ đồng ý rank-1 giữa K = 5 lần chạy | K lần chạy agent |
| S4 | LLM judge mạnh: model khác đọc trajectory, cho xác suất đúng (phiên bản hiện đại của PACE-LM) | 1 lần gọi model mạnh |
| S5 | Luật đơn giản chọn trên dev, ví dụ "≥ 12 bước hoặc ≥ 2 output lỗi thì không tin" | 0 |
| S6 | Chỉ dùng đầu vào (nhóm F) | 0 |
| **M1** | Mô hình đặc trưng quá trình (nhóm A–D) | 0 (chỉ tính toán) |
| **M2** | M1 + nhóm E | Bằng chi phí phần E dùng tới |
| (M3) | HTC rút gọn dùng log-prob, nếu API của model chọn hỗ trợ | 0 |

Mọi phương pháp chấm **trên cùng tập case**, cùng agent, cùng trajectory (trừ S3 cần thêm lần chạy). Báo AURC **kèm chi phí** để thấy đánh đổi.

### 5.7. Thiết kế thí nghiệm

**Chia dữ liệu (quan trọng nhất):**
- Đơn vị độc lập là **case** (một sự cố gốc). Các lần chạy lặp K của cùng case **không** phải mẫu độc lập.
- Chia dev/test **theo case**, phân tầng theo fault type (ví dụ 50/50), **trước** khi xem kết quả.
- Thêm ba kiểu chia để kiểm chuyển giao: (1) huấn luyện trên OnlineBoutique, kiểm trên TrainTicket; (2) huấn luyện trên trajectory của model A, kiểm trên model B; (3) bỏ ra một nhóm lỗi (ví dụ Performance) để kiểm.

> **Giải thích thêm:** nếu cổng chỉ học được "case nhóm Code Defect thì agent hay sai", nó sẽ đẹp trên tập test cùng phân bố nhưng vô dụng với loại lỗi mới. Kiểu chia (3) phát hiện điều này.

**Thống kê:**
- Khoảng tin cậy 95% bằng bootstrap **theo case** (1.000–10.000 lần lấy mẫu lại).
- So sánh hai bộ chấm trên cùng case: bootstrap theo cặp cho chênh lệch AUROC/AURC; McNemar cho số chẩn đoán sai bị chấp nhận ở cùng coverage.
- Chạy lặp 3 lần trên một tập con để ước lượng phương sai giữa các lần chạy.

**Kiểm soát rò rỉ và kiểm tra vô lý (sanity check):**
- Rà mã trích đặc trưng: không đọc file nhãn.
- Xáo trộn nhãn đúng/sai rồi huấn luyện lại: AUROC phải về gần 0,5.
- Kiểm agent không thấy fault plan hay tên injector trong output tool (bài học từ Auditable Graph RCA).

**Báo cáo (theo Pooled-Leaderboard Audit):**
- Kết quả riêng từng hệ thống, từng nhóm lỗi, từng model; không chỉ trung bình gộp.
- Mẫu số rõ ràng: case timeout hoặc sai schema vẫn tính, báo riêng tỷ lệ lỗi thực thi.
- Nếu coverage = 0 thì selective error là "N/A", không phải 0.
- Công bố trajectory, đặc trưng, điểm của **từng case**.

### 5.8. Ngân sách và tính khả thi

**Phần cứng:** laptop là đủ cho agent replay, trích đặc trưng, scikit-learn. Không cần cụm Kubernetes, không cần GPU (trừ khi muốn model local).

**Token (ước lượng thô, phải đo lại ở pilot):**
- Cloud-OpsBench v3 Table 7: agent ReAct với GLM-5.1 dùng trung bình khoảng **55K token/case (OnlineBoutique)** và **129K token/case (TrainTicket)**, với ngân sách 50 tool call. Thí nghiệm chính dùng trần 20 bước nên có thể ít hơn.
- Một lần chạy **toàn bộ 754 case** ≈ 550 × 55K + 204 × 129K ≈ **57 triệu token**.
- Một lần chạy **tập con 300 case** (200 OB + 100 TT) ≈ **24 triệu token**.

| Hạng mục | Khối lượng | Token ước tính |
|---|---|---|
| Agent rẻ chính, 1 lần × 754 case | Dữ liệu RQ1–RQ2 | khoảng 57M |
| + 4 lần lặp (T = 0,7) × 300 case | Self-consistency (S3) | khoảng 96M |
| Agent rẻ thứ hai, 1 lần × 754 case | Chuyển giao model | khoảng 57M |
| Agent mạnh, 1 lần × 300 case | Cascade (RQ3) | khoảng 24M |
| Tự chấm và judge (S2, S4) | Đọc lại trajectory | vài chục triệu |
| **Tổng kế hoạch đầy đủ** | | **khoảng 250M token** |

**Chi phí = tổng token × đơn giá của nhà cung cấp tại thời điểm chạy.** Báo cáo không ghi giá cụ thể vì giá thay đổi nhanh. Tham chiếu: Kim et al. tốn khoảng **$1.394** cho 1.675 run trên OpenRCA, với dữ liệu nặng hơn nhiều (khoảng 0,8 triệu token mỗi run) [Nguồn: Kim et al. §3]. Cách giảm khi vượt ngân sách, theo thứ tự:
1. Giảm K của self-consistency (5 → 3).
2. Bớt case TrainTicket (đắt gấp khoảng 2,3 lần mỗi case).
3. Dùng **prompt caching** nếu nhà cung cấp hỗ trợ. Agent gửi lại toàn bộ lịch sử ở mỗi bước nên phần lặp rất lớn.
4. Dùng model local cho agent rẻ thứ hai.

**Kỹ năng cần:** Python, đọc JSON, scikit-learn cơ bản, vẽ biểu đồ; hiểu Kubernetes ở mức Pod/Service/Deployment/Event (đủ để đọc trajectory và phân tích lỗi). Không cần RL, không cần huấn luyện LLM.

### 5.9. Kế hoạch 6 tháng và phân vai

**Phân vai đề xuất** (giữ khung của roadmap; hai bạn có thể đổi):
- **Nguyên – Hạ tầng và thí nghiệm:** chạy agent, sửa output contract, quản lý API, log chi phí, mô phỏng cascade, đóng gói artifact.
- **Lộc – Tín hiệu và đánh giá:** trích đặc trưng, mô hình tin cậy, hiệu chỉnh, thống kê, phân tích lỗi định tính.
- **Cả hai:** đọc paper cốt lõi, viết khóa luận, họp tuần 30 phút để xem lại số liệu.

| Tháng | Việc chính | Sản phẩm | Gate (điều kiện đi tiếp) |
|---|---|---|---|
| **T1** (16/11–15/12/2026) | Clone và ghim commit; chạy 3 case rồi pilot 50 case; thêm `confidence`; viết trích đặc trưng v0; kiểm novelty (Mục 5.4); đọc Cloud-OpsBench v3 §4, Riddell §4.4, Trajectory-UQ §3–§5, HTC §2 | Trace mẫu; chi phí đo thật mỗi case; reliability diagram đầu tiên; bảng novelty | **G1:** pipeline chạy đầu-cuối; chi phí/case trong trần; tỷ lệ sai của agent rẻ ≥ 20% (đủ ví dụ "sai"); không có paper trùng hoàn toàn |
| **T2** (16/12/2026–15/01/2027) | Chạy agent rẻ chính trên 754 case; K lần lặp trên 300 case; chia dev/test; **đóng băng** danh sách đặc trưng | Bộ trajectory hoàn chỉnh cho RQ1–RQ2; tài liệu đặc trưng v1 | **G2:** dữ liệu đủ, mẫu số rõ; đặc trưng đã đóng băng trước khi nhìn test |
| **T3** (16/01–15/02/2027) | RQ1 (S1–S4) và RQ2 (M1, M2, ablation, chuyển giao); hiệu chỉnh isotonic. Trừ hao **Tết Nguyên Đán** (đầu tháng 2/2027) | Bảng và hình RQ1–RQ2 trên dev, rồi test | **G3:** M2 tốt hơn S1 và S0 trên dev. Nếu không, chuyển thông điệp sang kết quả âm tính và phân tích vì sao |
| **T4** (16/02–15/03/2027) | Chạy agent rẻ thứ hai và agent mạnh (300 case); RQ3 cascade; phân tích định tính 30–50 case "sai mà rất tự tin" theo taxonomy DiagGuard/Kim/Riddell | Đường Pareto; codebook lỗi; bản nháp chương Kết quả | **G4:** quyết định có làm RQ4 không (đủ thời gian, đủ ngân sách) |
| **T5** (16/03–15/04/2027) | RQ4 tùy chọn (1–2 profile thiếu dữ liệu) **hoặc** củng cố: chạy lặp, phân tích độ nhạy; viết chương 1–3 | Kết quả RQ4 hoặc phân tích bổ sung | Kết luận đứng vững qua kiểm tra độ nhạy |
| **T6** (16/04–15/05/2027) | Viết hoàn chỉnh; công bố artifact; chuẩn bị bảo vệ; (tùy chọn) bản thảo workshop | Khóa luận; repo artifact; slide | Giảng viên đồng ý claim và phạm vi |

**Nguyên tắc:** mốc ngày để quản lý; **đạt gate** mới là căn cứ mở rộng.

### 5.10. Rủi ro và phương án lùi

| Rủi ro | Dấu hiệu sớm | Cách xử lý |
|---|---|---|
| Agent rẻ đúng quá nhiều, ít ví dụ "sai" | T1: tỷ lệ sai < 20% | Thêm model yếu hơn (Qwen3-8B/14B có JRA khoảng 0,2–0,4 theo v3 Table 5); tăng tỷ trọng nhóm Hard (Performance, Code Defect) và TrainTicket |
| Cổng chỉ học "nhóm lỗi nào khó" | T3: chuyển giao bỏ-một-nhóm-lỗi kém | Báo cáo trung thực; tách đặc trưng theo nhóm; nhấn mạnh kết quả theo từng nhóm |
| Temperature > 0 làm đổi độ đúng | T2 | Chạy chính ở T = 0; báo riêng độ đúng của các lần lặp |
| Chi phí vượt trần | T1–T2 | Theo thứ tự giảm ở Mục 5.8 |
| Có paper trùng phần lõi | Kiểm novelty T1, tìm lại hằng tháng | Chuyển thành tái lập + mở rộng (RQ3, RQ4, model khác) |
| Model API đổi phiên bản hoặc ngừng | Bất kỳ lúc nào | Ghim tên/phiên bản model; lưu mọi output; chạy xong một model trong một đợt |
| Kết quả không ổn định giữa các lần chạy | T3 | Báo khoảng tin cậy; tăng số lần lặp trên tập con; không claim chênh lệch nhỏ |
| **Phương án lùi tổng thể** (G3 thất bại nặng) | T3 | **Audit benchmark:** bao nhiêu case Cloud-OpsBench giải được chỉ từ query và một hai tool đầu (S6 và S5 đã là một phần thí nghiệm này); viết thành nghiên cứu thực nghiệm về độ khó và lối tắt |

### 5.11. Đóng góp dự kiến và giới hạn claim

**Đóng góp dự kiến (tất cả là tạm thời, chờ kết quả):**
- **C1:** nghiên cứu có hệ thống (theo những gì nhóm tìm được, là đầu tiên) về **mức "tự tin sai"** của LLM agent RCA trên benchmark Kubernetes tương tác, tái lập được.
- **C2:** bộ **tín hiệu tin cậy không cần nhãn, đặc thù vận hành**, kèm mô hình tin cậy đơn giản, đã hiệu chỉnh, được so sánh với độ tự tin tự báo, self-consistency và LLM judge.
- **C3:** đánh giá **chính sách chuyển tiếp** (agent rẻ → agent mạnh hoặc người) theo độ đúng, tỷ lệ chuyển và chi phí.
- **C4:** **artifact mở:** trajectory, đặc trưng, điểm tin cậy của từng case.
- (C5, nếu làm RQ4): độ bền của điểm tin cậy khi telemetry thiếu theo cơ chế K8s.

**Không được claim:**
- Không claim kết quả đúng cho production: chỉ 2 ứng dụng demo, lỗi được tiêm.
- Không claim cổng dùng được cho mọi model hay harness: cổng học trên trajectory của model và harness cụ thể; chuyển giao là câu hỏi được đo, không phải giả định.
- Không claim "agent RCA tốt hơn". Đề tài không làm agent chẩn đoán đúng hơn; nó giúp **biết lúc nào tin**.

### 5.12. Câu hỏi phản biện dự kiến

| Câu hỏi | Gợi ý trả lời |
|---|---|
| "Sao không làm agent chẩn đoán chính xác hơn?" | Agent tốt nhất vẫn sai 22–32% số case trên Cloud-OpsBench v3 (JRA tốt nhất 0,78 và 0,68) và sai phần lớn task thực tế trên ORCA-bench (tốt nhất 25,3%). Quyết định "khi nào tin" luôn cần, dù agent tiến bộ. Hướng tăng accuracy rất đông và phụ thuộc model mới nhất (Mục 4) |
| "Khác HTC, TRACER thế nào?" | Domain RCA Kubernetes; đặc trưng **black-box** (không cần log-prob), **đặc thù vận hành** (bám bằng chứng, output lỗi của tool); có đánh giá chuyển tiếp và chi phí; môi trường replay tương tác |
| "Khác PACE-LM?" | Agent nhiều bước thay vì gợi ý một bước; benchmark mở thay vì dữ liệu kín; dựa vào quá trình điều tra thay vì kho sự cố lịch sử |
| "Khác TelemetrySuffBench, JustDiag?" | Họ cho agent tự từ chối, đánh giá bằng trace tĩnh hoặc LLM judge. Nhóm đánh giá **một cổng bên ngoài** bằng nhãn khách quan, ở cùng coverage, trên môi trường tương tác |
| "Đặc trưng có rò rỉ đáp án không?" | Chỉ dùng thứ agent thấy; có sanity check xáo trộn nhãn; rà mã đọc file |
| "Nếu không dự đoán được thì sao?" | Đó là kết quả âm tính có giá trị: cho thấy UQ không chuyển sang RCA, đúng như Trajectory-UQ cảnh báo. Hai giả thuyết bác bỏ đã được định nghĩa trước |
| "Chỉ là logistic regression, có đơn giản quá?" | Đóng góp là câu hỏi, thiết kế đánh giá, bộ đặc trưng và phát hiện. HTC (ICML 2026) cũng chọn mô hình đơn giản có chủ đích vì giải thích được và ổn khi ít dữ liệu |

### 5.13. Việc làm ngay trong 2 tuần đầu

**Tuần 1 (16–22/11/2026):**
- [ ] **Nguyên:** clone Cloud-OpsBench, ghi commit; tạo môi trường ảo Python; cấu hình một model rẻ qua giao diện OpenAI-compatible; chạy 3 case OnlineBoutique ở 3 nhóm lỗi khác nhau; mở file trace JSON; ghi token, latency, thời gian; chạy `evaluation.py`.
- [ ] **Lộc:** đọc Cloud-OpsBench v3 §4.1 và §4.6, Riddell et al. §4.4, Trajectory-UQ §3–§5; từ 3 trace của Nguyên, viết thử 10 đặc trưng nhóm A–C bằng tay để xem có tính được không.
- [ ] **Cả hai:** làm 5 kiểm tra novelty ở Mục 5.4; gửi giảng viên pitch 1 trang (Mục 6.3) kèm 4 câu hỏi.

**Tuần 2 (23–29/11/2026):**
- [ ] Thêm `confidence` (0–100) vào `runtime/contracts.py` và prompt; **lưu diff** của thay đổi.
- [ ] Pilot 50 case OnlineBoutique, phân tầng đủ 8 nhóm lỗi: đo JRA, phân bố confidence, reliability diagram.
- [ ] Script trích đặc trưng v0 và AUROC của confidence tự báo trên 50 case. Chỉ để kiểm pipeline; **chưa kết luận gì** từ 50 case.
- [ ] Họp đánh giá **Gate G1**.

---

## 6. Quan hệ với roadmap và memo cũ

### 6.1. Giữ, đổi, hoãn

| Thành phần | Roadmap 29/10 và memo 07/11 | Đề xuất này |
|---|---|---|
| Tinh thần selective RCA (kết luận hoặc không) | Có | **Giữ**, thêm "chuyển tiếp" |
| Cloud-OpsBench làm môi trường | Có (v2) | **Giữ**, chuyển sang v3 và ghim commit |
| Metric coverage, selective error, risk–coverage, cùng coverage | Có | **Giữ**, thêm AUROC, ECE, Brier, chi phí |
| Oracle "đủ bằng chứng" / trần identifiability | Trọng tâm | **Đổi** sang nhãn đúng/sai khách quan; ECR chỉ dùng phân tích phụ |
| Telemetry thiếu theo cơ chế K8s | RQ chính (memo) | **Hoãn** thành RQ4 tùy chọn |
| Stale telemetry | Đã thu hẹp | **Bỏ** khỏi claim |
| Verifier hoặc can thiệp mới | RQ2 (roadmap), C3 (memo) | Thành **baseline** (S2, S4), không bắt buộc xây phương pháp mới |
| Phân vai Nguyên / Lộc | Có | **Giữ khung** |

Roadmap và memo **không bị sửa**. Nếu nhóm đồng ý hướng này, cập nhật roadmap là một việc riêng.

### 6.2. Cập nhật ghi chú cũ do Cloud-OpsBench v3

Xem [CloudOpsBench_v3_CHANGES.md](papers/CloudOpsBench_v3_CHANGES.md). Tóm tắt: số liệu nhiều ô đã đổi (ví dụ GPT-5 OB ECR 0,21 → 0,39); Finding 3 (Base của RQ3 có thể khác tập case) **đã được tác giả sửa** ở v3; Finding 2 (không báo tỷ lệ "đúng nhưng ECR = 0") **đã được bổ sung** ở v3; Finding 1 (không có chỉ số đồng thuận người gán nhãn) **vẫn đúng**.

### 6.3. Pitch một trang gửi giảng viên (mẫu)

> Em xin đề xuất đề tài *"Biết khi nào nên tin AI: phân tích nguyên nhân sự cố có chọn lọc cho LLM agent trên Kubernetes"*. Các benchmark 2026 (Cloud-OpsBench, ORCA-bench, OpenRCA 2.0) cho thấy agent RCA tốt nhất vẫn sai khoảng 1/4 tới 1/3 số case trên Cloud-OpsBench và đa số task trên ORCA-bench, thường "đúng mà không có căn cứ", và tự tin cả khi sai. Nhóm em sẽ dùng Cloud-OpsBench (chạy offline, có đáp án khách quan) để đo (1) agent có biết mình sai không, (2) các tín hiệu tự động trong quá trình điều tra có dự đoán được chẩn đoán sai không, và (3) dùng tín hiệu đó để chuyển case khó cho kỹ sư hoặc model mạnh thì giảm được bao nhiêu chẩn đoán sai, tốn bao nhiêu chi phí. Phương pháp đo độ tin cậy cho agent đã có ở các domain khác (ICML 2026) nhưng nhóm chưa thấy áp dụng cho RCA. Đề tài không cần cụm Kubernetes; chi phí chủ yếu là API, ước tính sau pilot 2 tuần.
>
> Em xin hỏi thầy/cô: (1) đóng góp ở mức "nghiên cứu thực nghiệm + phương pháp đơn giản" có đủ cho khóa luận không; (2) có hỗ trợ ngân sách API không, hay nhóm tự túc; (3) nếu kết quả âm tính (tín hiệu không dự đoán được) thì có chấp nhận không; (4) có yêu cầu chạy trên cụm thật không.

---

## 7. Năm điều cần nhớ

1. **Agent RCA sẽ còn sai**, kể cả model mạnh nhất (JRA tốt nhất 0,78 trên Cloud-OpsBench v3; 25,3% trên ORCA-bench). Vì vậy câu hỏi "khi nào tin?" luôn có giá trị.
2. **Agent tự tin cả khi sai và hay "đúng mà không có căn cứ".** Nhiều nguồn độc lập cùng thấy.
3. **Dấu vết điều tra chứa tín hiệu** về đúng/sai (Riddell et al.; HTC và TRACER ở domain khác). Chưa ai, theo những gì nhóm tìm được, biến nó thành cổng tin cậy được đánh giá đầy đủ cho agent RCA.
4. **Cloud-OpsBench làm đề tài khả thi:** chạy offline, nhãn khách quan, mã mở. Chỉ cần sửa một trường output.
5. **Trung thực là lợi thế:** khóa trước đặc trưng và ngưỡng, báo theo từng hệ thống, công bố output từng case, chấp nhận kết quả âm tính. Hội đồng đánh giá cao điều này hơn một con số đẹp.

---

## 8. Phụ lục

### 8.1. Paper chỉ biết qua abstract hoặc trang hội nghị

Chưa đọc full text; chỉ dùng để định vị, **không trích số liệu vào khóa luận** trước khi đọc bản gốc.

| Paper | Nội dung (theo abstract/trang) | Liên quan |
|---|---|---|
| ITBench (2502.05352, ICML 2025) và ITBench-AA (05/2026) | Benchmark tự động hóa IT/SRE; ITBench-AA có 59 task SRE | Benchmark thay thế |
| AIOpsLab (2501.06706, MLSys 2025) | Khung đánh giá agent trên hệ live | Benchmark thay thế |
| STRATUS (2506.02009, NeurIPS 2025) | Hệ multi-agent cho SRE tự động (chẩn đoán và khắc phục trên cloud) | Remediation |
| SRE-World (NeurIPS 2026) | 44 task live trên cụm tạm; GPT 5.6 giải 29% | Remediation |
| Passing Without Repairing (NeurIPS 2026) | Oracle khắc phục của một benchmark live chấp nhận cả hệ chưa sửa | Kiểm toán đánh giá |
| Süerkan, Kugu, Emekci, IEEE Access 2026 (DOI 10.1109/access.2026.3743626) | Reflexion cho khắc phục sự cố K8s; 1.500 run, 5 model Claude; lần thử thứ hai tăng thành công 38,6% → 68,4%, Reflexion chỉ 69,2% | **Phải đọc full text** khi kiểm novelty |
| The Confidence Dichotomy, ACL 2026 (arXiv 2601.07264) | Tool lấy bằng chứng làm agent quá tự tin; tool kiểm chứng giảm lệch | Móc lý thuyết cho H1; **phải đọc** |
| Oh et al., ACL 2026 | Nền tảng UQ cho LLM agent | Lý thuyết |
| CURA (2608.27808), Towards Risk-free AI Agent Deployment (2608.16411), CHAP (2606.09751) | Giám sát, cảnh báo và chuyển cho người với agent nói chung | Related work phần escalation |
| TopoEvo (2605.15611), GALA (2608.08968, ASE'26), LATS-RCA (2605.03505, SEAA'26), KRCA (2607.01788), ARGUS (2608.23084) | Các phương pháp agent RCA mới | Bức tranh hướng C |
| ARBITER (2607.19182), Can LLMs Really Recover Microservice Failures? (2607.04623) | Remediation có kiểm soát | Bức tranh hướng D |
| 2510.04711 (FSE'26) *Rethinking the Evaluation of Microservice RCA with a Fault Propagation-Aware Benchmark* | Benchmark RCA cổ điển có lan truyền lỗi. Memo cũ ghi tên khác; tên ở v2 là tên này | Hướng F |
| RCAEval (2412.17015), OpenRCA (ICLR 2025) | Benchmark RCA cổ điển và LLM | Nền |
| GenKubeSec (2405.19954), 2609.27030 (AIware 2026) | Phát hiện và sửa cấu hình Kubernetes sai bằng LLM | Hướng G |

### 8.2. Thuật ngữ

| Thuật ngữ | Nghĩa ngắn gọn |
|---|---|
| Agent | LLM được gọi công cụ theo vòng lặp để tự điều tra |
| Trajectory | Toàn bộ chuỗi bước của agent: suy nghĩ, lệnh, kết quả, câu trả lời |
| Harness | "Vỏ" điều khiển agent (vòng lặp, quản lý context, cách gọi tool) |
| JRA / CA / FA | Đúng cả component lẫn fault type / chỉ component / chỉ fault type |
| ECR | Agent có thu đủ mọi nhóm bằng chứng cần thiết không (0/1) |
| Selective prediction | Chỉ trả lời khi đủ tin cậy; còn lại từ chối hoặc chuyển tiếp |
| Coverage | Tỷ lệ case hệ thống tự chấp nhận |
| Selective error | Tỷ lệ sai trong các case được chấp nhận |
| AURC | Diện tích dưới đường risk–coverage; càng nhỏ càng tốt |
| AUROC | Khả năng xếp case đúng cao hơn case sai; 0,5 là ngẫu nhiên |
| ECE, Brier | Mức "độ tự tin khớp tỷ lệ đúng"; càng nhỏ càng tốt |
| Calibration (hiệu chỉnh) | Biến điểm thô thành xác suất đúng nghĩa (ví dụ isotonic regression) |
| Self-consistency | Chạy nhiều lần; nhiều lần cùng đáp án thì tin hơn |
| Verbalized confidence | Model tự nói "tôi chắc X%" |
| LLM-as-judge | Dùng một LLM chấm câu trả lời hoặc quá trình của LLM khác |
| Cascade / escalation | Model rẻ trước; case khó chuyển lên model đắt hoặc người |
| Label-free | Tính được lúc chạy thật, không cần biết đáp án |
| Ungrounded diagnosis | Đúng đáp án nhưng không có chuỗi bằng chứng hỗ trợ |
| Replay / snapshot | Chụp lại output của tool khi có lỗi thật, phát lại khi đánh giá |
| Bootstrap | Lấy mẫu lại nhiều lần để ước lượng khoảng tin cậy |

### 8.3. Danh mục file của lần nghiên cứu này

```text
research/
├── research-direction-report.md        ← file này (đọc chính)
├── literature-search-log.md            ← nhật ký tìm kiếm, nguồn gốc paper
├── research-question-memo.md           ← memo cũ 07/11 (không sửa)
└── papers/                             ← phân tích từng paper (đọc khi cần sâu)
    ├── CloudOpsBench_v3_CHANGES.md     ← thay đổi v2→v3, ảnh hưởng ghi chú cũ
    ├── OpenRCA2_ANALYSIS.md · ORCABench_ANALYSIS.md · CTBench_ANALYSIS.md · SREGym_ANALYSIS.md
    ├── WhyAgentsFailRCA_ANALYSIS.md · StalledBiasedConfused_ANALYSIS.md
    ├── HowFarRCA_ANALYSIS.md · EviRCA_ANALYSIS.md
    ├── JustDiag_ANALYSIS.md · STAR_ANALYSIS.md · AuditableGraphRCA_ANALYSIS.md
    ├── TriFleetRCA_ANALYSIS.md · AOI_ANALYSIS.md
    ├── PACELM_ANALYSIS.md · AgenticConfidenceCalibration_ANALYSIS.md · TRACER_ANALYSIS.md
    ├── TrajectoryUQ_ANALYSIS.md · UQAgentsTaxonomy_ANALYSIS.md · UCCI_ANALYSIS.md
    └── PooledLeaderboardAudit_ANALYSIS.md
```

**Gợi ý thứ tự đọc file phân tích cho hướng chốt:** (1) CloudOpsBench_v3_CHANGES → (2) StalledBiasedConfused → (3) TrajectoryUQ → (4) AgenticConfidenceCalibration → (5) PACELM → (6) TRACER → (7) UCCI → (8) PooledLeaderboardAudit. Các file còn lại đọc khi viết related work.
