# Research Direction Memo: Blame the Agent or the Telemetry?

**Tên làm việc:** *Diagnosability-Grounded Evaluation of LLM Agents for Kubernetes Root Cause Analysis under Realistic Observability Gaps*

- **Ngày lập:** 07/11/2026. Nguồn được tra cứu trong cùng ngày; danh sách truy vấn ở mục 13.
- **Trạng thái:** đề xuất để nhóm và giảng viên thảo luận, **chưa được giảng viên duyệt**, **chưa có kết quả thực nghiệm**. Mọi con số trong mục 5 là giả thuyết cần kiểm chứng.
- **Quan hệ với roadmap:** không sửa `roadmap/AIOps_Thesis_Research_Guide.md`. Memo này giữ phần lớn roadmap (selective RCA, telemetry thiếu, Cloud-OpsBench, bộ metric) nhưng đổi trục câu hỏi. Chi tiết ở mục 11.
- **Quy ước nhãn:** **[Nguồn]** là điều paper hoặc artifact nói, kèm vị trí. **[Diễn giải]** là nhận định của người viết memo. **[Giả thuyết]** là điều cần thực nghiệm. **[Chưa xác minh]** là chưa đọc được bản gốc hoặc chỉ đọc qua tóm tắt.

---

## 1. Tóm tắt

**Câu hỏi trung tâm:** khi telemetry Kubernetes bị thiếu theo những cách thường gặp ngoài đời (events hết hạn, log của container trước khi restart bị mất, không có log ứng dụng, không có source code…):

1. Bao nhiêu incident **còn chẩn đoán được về mặt thông tin**, tính độc lập với mọi agent?
2. Trong mức giảm accuracy của LLM agent, phần nào **không tránh được** (thông tin không còn), phần nào **tránh được** (agent không tìm, hoặc tìm thấy nhưng đọc sai)?
3. Agent có **biết dừng hoặc trả tập ứng viên** khi không thể phân biệt nguyên nhân không? Các cơ chế bảo vệ hiện có có giúp được ở cùng coverage và budget không?

**Vì sao không chỉ là "đưa input cho agent rồi chấm":** đối tượng nghiên cứu là *quan hệ giữa thông tin quan sát được và khả năng chẩn đoán*, agent chỉ là đối tượng đo. RQ1 không cần chạy LLM. RQ2 dùng sức mạnh model làm một biến. Phần lỗi do thiếu thông tin thì model mạnh hơn cũng không vượt qua được.

**Đóng góp dự kiến:**

- **C1, protocol và artifact:** observability profile có căn cứ thực tế, discriminator catalog, bộ tính trần identifiability và leak audit trên Cloud-OpsBench.
- **C2, thực nghiệm:** đo mức giảm có thể tránh được và không thể tránh được; tỷ lệ đúng-thiếu-cơ-sở theo sức mạnh model; hành vi selective ở cùng coverage.
- **C3 (tùy chọn):** đánh giá một can thiệp tối thiểu, chỉ khi pilot cho thấy failure pattern rõ.

---

## 2. AIOps có phải chỉ là RCA?

AIOps rộng hơn RCA. Survey CSUR (arXiv 2507.12472, bản mở rộng của 2406.11213) trải từ tiền xử lý dữ liệu, phát hiện lỗi, đến RCA và remediation **[Nguồn: abstract; chưa đọc full text]**.

| Mảng | Câu hỏi điển hình | Đánh giá cho nhóm **[Diễn giải]** |
|---|---|---|
| Log parsing, anomaly detection | Có gì bất thường? | Đông, nhiều bài LLM; khó tìm novelty |
| Gom cảnh báo, incident triage | Cảnh báo nào cùng một sự cố? Ai xử lý? | Quan trọng; dữ liệu chủ yếu proprietary |
| **RCA** | Lỗi ở đâu, cơ chế gì? | Sôi động nhất cho LLM agent vì có benchmark công khai |
| Mitigation, remediation | Sửa thế nào cho an toàn? | STRATUS (NeurIPS 2025), AIOpsLab, ITBench; cần cụm chạy thật, cạnh tranh với lab lớn |
| Change management | Thay đổi có gây sự cố không? | Rất quan trọng (*Site Reliability Engineering*, O'Reilly 2016, Ch. 1, ước khoảng 70% outage do thay đổi **[Chưa xác minh trang]**); không có dữ liệu công khai |
| Observability engineering | Thu thập, sampling bao nhiêu là đủ chẩn đoán? | Painpoint thật về chi phí; bằng chứng chủ yếu từ vendor và preprint (Gleaner 2604.16810) |

Nghiên cứu LLM-AIOps tập trung vào "cho agent tools rồi chấm RCA" vì dữ liệu production bị khóa, còn benchmark thì công khai **[Diễn giải]**. Lối ra không phải bỏ benchmark. Lối ra là hỏi một câu mà benchmark hiện tại **không trả lời được**.

---

## 3. So sánh các hướng ứng viên

| Hướng | Mức quan trọng | Khả thi trong 6–8 tháng, 2 người | Còn chỗ trống | Quyết định |
|---|---|---|---|---|
| Remediation an toàn | Cao | Thấp: cần cụm K8s, reset và inject liên tục | Trung bình | Không chọn |
| Change-risk prediction | Rất cao | Rất thấp: không có dữ liệu | Cao | Không chọn |
| Log, anomaly với LLM | Trung bình | Cao | Thấp | Không chọn |
| Audit shortcut của benchmark agentic RCA | Trung bình | Rất cao | Trung bình (2510.04711 đã làm cho RCA cổ điển) | **Phương án lùi** |
| **Diagnosability-grounded evaluation** | Cao | Cao (Cloud-OpsBench MIT, kho response hữu hạn) | Cao: hai nhóm tác giả độc lập tự nêu là chưa làm | **Chọn** |

Đánh giá trên là định tính, theo ba tiêu chí: bằng chứng về vấn đề chưa giải quyết, giá trị khoa học, và khả thi. Không có điểm số.

---

## 4. Vấn đề và động lực

### 4.1 Benchmark hiện tại đo trên tập case được chọn lọc

Ba benchmark độc lập đều loại bỏ case không có đủ dấu vết telemetry:

| Benchmark | Bằng chứng **[Nguồn]** |
|---|---|
| Cloud-OpsBench (2603.00468v2) | §3.3.2: case chỉ được giữ khi mọi diagnostic fact cần thiết đều quan sát được qua snapshot (ghi trong `CloudOpsBench_reading_report.md`) |
| OpenRCA 2.0 (2606.27154v1) | §3.1: "After filtering silent injections"; A.5: không dành cho "faults that leave no telemetry signature"; 8.137 run lọc còn 500 instance |
| Multi-Dataset Benchmark (2606.29193v1) | §6.1: chỉ nhận case có "complete, expert-traceable observability footprint" |

**Hệ quả [Diễn giải]:** accuracy công bố là accuracy trên tập case lý tưởng. Chưa có nghiên cứu nào đo agent khi dữ liệu không đầy đủ theo cách có kiểm soát và có trần thông tin.

### 4.2 Hai nhóm tác giả tự nêu chỗ trống

- **OpenRCA 2.0 §5 [Nguồn]:** việc biến information availability thành *"a controllable evaluation axis that we leave to future work"*. Bài cũng ghi bước annotation cần full telemetry còn bước evaluation thì không.
- **2607.13548 v2 [Nguồn: chỉ abstract v2, chưa xác minh full text]:** audit của họ là *"label-conditioned"* và không kiểm *"forward identifiability"*.

### 4.3 Kubernetes tự làm mất bằng chứng theo mặc định [Chưa xác minh, phải trích docs chính thức trước khi dùng]

- Events chỉ được giữ trong một khoảng TTL mặc định ngắn (flag `--event-ttl` của kube-apiserver, mặc định được biết là 1 giờ).
- Khi container restart, kubelet chỉ giữ log của một container đã kết thúc. Pod bị evict thì mất log (Kubernetes docs, *Logging Architecture*).
- Log rotation (`containerLogMaxSize`, `containerLogMaxFiles`) có thể cắt mất phần log đầu sự cố.
- Tổ chức cắt log và sampling trace vì chi phí: hướng dẫn của Datadog và Grafana; Gleaner (2604.16810) cho thấy sampler không biết đến log có thể bỏ mất trace chứa log lỗi quan trọng **[Nguồn: vendor blog và preprint]**.

### 4.4 Agent hay "đúng mà thiếu cơ sở" và hay chốt bừa khi dữ liệu mơ hồ

| Bằng chứng | Nguồn |
|---|---|
| GPT-5 trên OnlineBoutique: JRA 0,68 nhưng ECR 0,21 | Cloud-OpsBench Table 4 (xem `finding/CloudOpsBench_FINDING.md`, Finding 2) |
| FAR trên hồ sơ rich-ambiguous: DeepSeek, Qwen 100%; GPT-5.5 87,5%; GPT-5.6 Sol 44,4%; Opus 5 12,5% | TelemetrySuffBench Table IV (xem `finding/TelemetrySuffBench_FINDING.md`) |
| Trung bình 11 model: chỉ đúng service 76,0%, có path đã verify 61,5% | OpenRCA 2.0 Abstract, §3.2, Table 2 |
| Bỏ source code: accuracy giảm 9–16 điểm, hallucination tăng (Opus 4.7: 12,6% lên 31,3%) | ORCA-bench §5 Finding #3 **[Chưa xác minh: chỉ đọc qua tóm tắt]** |

**Lưu ý trung thực:** bằng chứng chủ yếu đến từ benchmark học thuật. Phía công nghiệp mới có blog và benchmark của doanh nghiệp (Edge Delta RCA Bench), chưa có khảo sát SRE được bình duyệt. Khi bảo vệ, viết "benchmark cho thấy", không viết "ngành đang gặp".

---

## 5. Research questions, giả thuyết và điều kiện bác bỏ

### RQ1: Trần chẩn đoán (không cần LLM)

> Với các incident Kubernetes trong Cloud-OpsBench, dưới từng observability profile thực tế (mục 6.2), bao nhiêu case và cặp nguyên nhân dễ nhầm còn phân biệt được bằng dữ liệu trong giao diện tool, tính độc lập với mọi agent?

- **Loại claim:** mô tả.
- **Đầu ra:** ma trận diagnosability (cặp fault type × profile); tỷ lệ case non-identifiable theo profile và fault family.
- **[Giả thuyết] H1:** các profile mất events hoặc mất log của container trước restart làm một phần không nhỏ các cặp thuộc nhóm startup/runtime không còn phân biệt được. Ngưỡng "không nhỏ" phải chốt trước khi tính.
- **Bác bỏ khi:** hầu như mọi case vẫn identifiable vì K8s state dư thừa thông tin. Khi đó báo cáo "state đủ bù", chuyển trọng tâm sang RQ2 ("mọi mức giảm đều tránh được").

### RQ2: Phân rã mức giảm accuracy

> So với trần ở RQ1, lỗi và các chẩn đoán đúng-thiếu-cơ-sở của agent phân bố thế nào giữa ba loại, và phân bố đó đổi ra sao theo sức mạnh model?
> (i) **information-limited:** không còn discriminator.
> (ii) **investigation-limited:** còn discriminator nhưng agent không truy vấn.
> (iii) **interpretation-limited:** đã truy vấn nhưng kết luận sai.

- **Loại claim:** mô tả, so sánh có kiểm soát giữa các profile; không claim nhân quả ngoài phạm vi profile.
- **[Giả thuyết] H2a:** dưới profile thực tế, phần lớn mức giảm accuracy là loại (ii) và (iii), tức tránh được.
- **[Giả thuyết] H2b:** model mạnh giảm (ii) và (iii) nhưng tỷ lệ đúng-thiếu-cơ-sở **không giảm**, thậm chí tăng, vì đoán trúng nhờ prior.
- **Bác bỏ khi:** mức giảm chủ yếu là (i); hoặc tỷ lệ đúng-thiếu-cơ-sở giảm đều theo sức mạnh model. Cả hai đều là kết quả công bố được nhưng đổi thông điệp.

### RQ3: Hành vi selective

> Trên các biến thể non-identifiable, agent có trả tập ứng viên hoặc "chưa đủ bằng chứng" không? Self-check, contrastive elimination (P3), verifier kiểu DiagGuard và ngưỡng confidence có giảm FAR so với B0 **ở cùng coverage và budget** không, và tăng UAR bao nhiêu?

- **[Giả thuyết] H3:** các cơ chế này giảm FAR chủ yếu nhờ tăng UAR; ở cùng coverage, chúng không vượt rule đơn giản R.
- **Bác bỏ khi:** một cơ chế giảm selective error rõ ở cùng coverage trên test set. Khi đó làm ablation để tìm nguồn cải thiện.

**Câu headline nếu kết quả ủng hộ [mẫu, chưa có số]:**
> "Trên benchmark đã chọn lọc, accuracy là X. Dưới telemetry thực tế, accuracy giảm Y điểm. Trong đó chỉ Z điểm là không tránh được, phần còn lại do agent điều tra hoặc diễn giải sai, và agent hiếm khi nhận ra khi nào mình không thể biết."

---

## 6. Thiết kế nghiên cứu

### 6.1 Dữ liệu: Cloud-OpsBench

**[Nguồn: repo README, đọc ngày 07/11/2026; reading report §3.3.2]**

- **Repo:** `https://github.com/LLM4Ops/Cloud-OpsBench`, MIT, commit mới nhất thấy được `ec1d4f38b952a4dcb057af094290b4d35128c100` (03/11/2026). **Phải ghi lại commit dùng thật khi clone.**
- **Quy mô:** 754 case (OnlineBoutique 550, TrainTicket 204), 57 fault type, 8 nhóm.
- **Cấu trúc case:** `benchmark/<system>/<fault_category>/<case_id>/` gồm `metadata.json`, `tool_cache.json`, `code/` (chỉ Boutique), và `raw_data/{alert.json, k8s_states.json, logs.json, metrics.csv}`. Nhãn quá trình ở `process-label/.../milestone.json`; `golden-trajectory/.../path1.json, path2.json`.
- **Kho response:** hữu hạn, trung bình 599 response/case (OnlineBoutique) và 1.708 response/case (TrainTicket). Truy vấn vào object không tồn tại trả về lỗi đã chụp, ví dụ `Not Found`.
- **[Chưa xác minh]:** cách `tool_cache.json` được key, cách xử lý truy vấn không có trong kho. Phải đọc `agents/cloudops_agent/tools/`. Repo không có traces trong `raw_data`, nên không có profile "trace sampling".

**Phạm vi đề xuất:** 3–4 fault family của OnlineBoutique có triệu chứng chồng lấn (ứng viên: service, startup, runtime, scheduling; phải kiểm trong taxonomy thật), khoảng 12–20 fault type, khoảng 150–250 case cho RQ1, khoảng 100–150 base case cho RQ2/RQ3.

### 6.2 Observability profiles

| Mã | Profile | Cơ chế thực tế làm căn cứ | Cách tạo view |
|---|---|---|---|
| P0 | Đầy đủ | — | Giữ nguyên |
| P1 | Events đã hết hạn | Event TTL của kube-apiserver | Bỏ entry events; trả kết quả rỗng như hệ thống thật |
| P2 | Mất log container trước restart | Kubelet chỉ giữ một container đã kết thúc; evict làm mất log | Bỏ log `--previous` / log của instance cũ |
| P3 | Không có log ứng dụng | Cắt log vì chi phí hoặc không thu log | Bỏ mọi entry logs |
| P4 | Chỉ state + metrics | Chỉ có kube-state và Prometheus | Bỏ logs, events, code |
| P5 | Không có source code | Agent không được đọc repo | Bỏ entry code (giống ORCA-bench) |

- Danh sách profile chốt cuối tháng 2, mỗi profile **phải có trích dẫn docs hoặc thực tiễn**.
- Profile là **can thiệp thực nghiệm**, không đại diện cho phân bố lỗi thu thập thật.
- **Quy tắc tạo view:** response thay thế phải là thứ hệ thống thật trả về trong điều kiện đó (danh sách rỗng, lỗi không tìm thấy container cũ…). Không dùng chuỗi kiểu "MASKED", vì nó làm lộ thí nghiệm. Lưu manifest biến đổi; tên file không được chứa nhãn.

### 6.3 Discriminator catalog và trần identifiability

- **Tập ứng viên dễ nhầm C(r):** với mỗi fault type r, chọn 2–3 nguyên nhân dễ nhầm, lấy từ fault type cùng nhóm, tài liệu K8s và lỗi thật của agent trên **dev split**. **Đóng băng trước khi chạy test.**
- **Discriminator d(r, r′):** predicate trên response đã chuẩn hóa, đúng dưới r và sai dưới r′, gắn với kênh dữ liệu và loại tool.
  - Ví dụ minh họa: d(*selector sai*, *targetPort sai*) = "selector của Service không khớp label của pod nào", đọc từ entry describe/get Service và Pod. Đây là ví dụ, chưa đối chiếu với taxonomy thật.
- **Định nghĩa:** case c với nguyên nhân r là *identifiable dưới profile P* khi với mọi r′ ∈ C(r), tồn tại ít nhất một discriminator d(r, r′) đánh giá được từ view V_P(c).
- **Cơ sở lý thuyết:** diagnosability trong hệ sự kiện rời rạc (Sampath et al., IEEE TAC 1995); conflict set và model-based diagnosis (Reiter 1987; de Kleer & Williams 1987). **[Chưa xác minh bản gốc, nhóm phải tự đọc]**

**Giới hạn hiệu lực:** trần chỉ đúng *tương đối với catalog và C(r)*; nó không chặt bằng exact-equal của TelemetrySuffBench (§III-F). Cách giảm thiểu:

1. Hai người gán discriminator độc lập; báo Cohen's kappa; tranh chấp ghi lý do.
2. **Leak audit tự động:** quét mọi entry còn lại xem có đường vòng lộ cùng sự thật không.
3. **Audit đối kháng:** cho agent mạnh chạy trên view non-identifiable. Nếu nó biện minh đúng r bằng một observation ngoài catalog, đó là discriminator bị sót: sửa catalog, ghi số vòng sửa.
4. Phân tích độ nhạy: bỏ hoặc thêm discriminator, đổi C(r), kiểm tra kết luận có đổi không.

### 6.4 Phân rã lỗi tự động (không dùng LLM judge)

Với mỗi episode (case, profile, model, method), dựa trên trace tool call:

| Điều kiện | Nhãn |
|---|---|
| Case non-identifiable dưới P | Commit một nguyên nhân là **unsupported commit**; trả tập ứng viên đúng hoặc "insufficient" là **safe** |
| Identifiable, nhưng agent không truy vấn entry nào đánh giá được discriminator cần thiết | **(ii) investigation-limited** (nếu sai) hoặc **unsupported-correct** (nếu đúng) |
| Identifiable, đã truy vấn discriminator, nhưng kết luận sai | **(iii) interpretation-limited** |
| Kết luận nằm ngoài C(r) ∪ {r} | **out-of-catalog**, đối chiếu mã GEN2 của DiagGuard |
| Sai schema, timeout | **execution failure**, vẫn tính vào mẫu số |

Mức giảm accuracy từ P0 sang P được chia thành phần do (i) và phần do (ii)+(iii).

### 6.5 Output schema của agent

```json
{
  "status": "diagnosis | candidates | insufficient",
  "root_cause": {"component": "...", "fault_type": "..."},
  "candidates": [{"component": "...", "fault_type": "..."}],
  "evidence": ["<tool_call_id>", "..."]
}
```

- Phải sửa evaluator của Cloud-OpsBench để chấp nhận `candidates` và `insufficient`.
- Mọi phương pháp, kể cả B0, đều được quyền dùng schema này.

### 6.6 Metrics

| Metric | Định nghĩa |
|---|---|
| JRA | Theo Cloud-OpsBench §4.1 (đúng component + fault type) |
| Coverage | Số episode có `status = diagnosis` hợp lệ / tổng số episode |
| Selective error | Số diagnosis sai / số diagnosis. N/A nếu không có diagnosis nào |
| FAR | Tỷ lệ commit một nguyên nhân trên các case non-identifiable |
| UAR | Tỷ lệ `candidates`/`insufficient` trên các case identifiable |
| Safe accuracy | (diagnosis đúng trên identifiable + safe trên non-identifiable) / tổng |
| Unsupported-correct rate | Diagnosis đúng nhưng trace không chứa discriminator cho mọi r′ ∈ C(r) |
| Phân rã | Tỷ lệ (i), (ii), (iii), out-of-catalog trong mức giảm accuracy |
| AURC / risk–coverage | Cho các phương pháp có score điều chỉnh được; ngưỡng chọn trên dev |
| Chi phí | Tokens, số tool calls, latency, chi phí API của **toàn episode**, kể cả verifier |

### 6.7 Phương pháp so sánh

| Mã | Thiết lập |
|---|---|
| B0 | Agent ReAct gốc của Cloud-OpsBench + schema mục 6.5 |
| B1 | B0 + prompt self-check về evidence và bất định |
| B2 | B0 + contrastive elimination kiểu P3 (TelemetrySuffBench §V-D), ghi rõ là bản chuyển thể |
| B3 | Verifier kiểu DiagGuard (Grounder + Soundness Check, 2608.21310v2 §6.1), ghi rõ adapter |
| B4 | Ngưỡng confidence (self-consistency hoặc verbalized), để vẽ risk–coverage |
| R | Rule đơn giản chỉ dùng thông tin agent thấy được, chọn trên dev. Ví dụ: không commit khi truy vấn liên quan giả thuyết đứng đầu trả rỗng hoặc hết hạn. **Không được dùng catalog/oracle** |
| M (tùy chọn) | Differential ledger: agent giữ tập ứng viên; checker tất định kiểm rằng mỗi ứng viên bị loại có observation đã truy vấn được trích dẫn. Chỉ làm nếu pilot cho thấy cần; báo rõ mức gần với JustDiag/P3 |

**Model:** ít nhất 3 mức sức mạnh (một frontier, một open-weight, một nhỏ), vì hành vi abstain phụ thuộc mạnh vào model (TelemetrySuffBench Table IV). Chốt model/version trước khi chạy chính.

### 6.8 Thống kê và kiểm soát

- Chia dev/test **theo base incident trước khi tạo biến thể profile**. Biến thể và lần chạy lặp không tính là incident độc lập.
- So sánh theo cặp trên cùng tập case: McNemar cho kết quả nhị phân, bootstrap khoảng tin cậy theo base incident. Đây là bài học từ Cloud-OpsBench Finding 3 (Base của RQ3 có thể không cùng tập case).
- Chạy lặp 3 lần trên một subset để ước lượng phương sai giữa các lần chạy.
- Báo kết quả theo fault family; báo operating point thật nếu phương pháp không điều chỉnh được coverage.
- Ngân sách mỗi episode (tokens, tool calls, thời gian) giống nhau giữa các phương pháp. Chi phí verifier tính vào episode.

---

## 7. Related work và stress test "trùng 70%"

### 7.1 Bảng đối chiếu

| Công trình (version) | Tương tác? | K8s? | Thay đổi thông tin có sẵn? | Trần identifiability tính trước? | Abstention, nhãn khách quan? | Phân rã lỗi? | Vị trí nguồn, mức xác minh |
|---|---|---|---|---|---|---|---|
| Cloud-OpsBench (2603.00468v2) | Có (replay) | Có | Không | Không; lọc case | Không | Không (JRA, ECR) | §3.3.2–3.3.3, §4.1; đọc full text qua reading report |
| TelemetrySuffBench (2608.07899v1) | Không (trace tĩnh) | Không (agent traces) | Có (mask factor) | Có (exact-equal) | Có (FAR/UAR) | Không | §III-E/F, §V; đọc full text |
| OpenRCA 2.0 (2606.27154v1) | Không (parquet tĩnh) | Có (Chaos Mesh) | Không, nêu là future work | Không | Không | Không | §2–3, §5, A.2–A.5; HTML v1, appendix B–F chỉ đọc tóm tắt; **chưa đọc v2** |
| JustDiag (2606.19407v1) | Không rõ | Không thấy nhắc | Không | Không | Non-closure, nhưng LLM judge + silver narrative | Không | §3.3, §4, §6; HTML v1, appendix D/E qua tóm tắt |
| DiagGuard (2608.21310v2) | Có | Có | Không | Không | Không (luôn chốt) | Taxonomy OMIT/MIS/GEN | §5.3, §6; xem finding của nhóm |
| ORCA-bench (2607.28545v1) | Có (tmux) | Không thấy nhắc | **Có** (bỏ code, giảm context) | Không | Control task "empty set" (không có sự cố) | Không | §3, §5; khoảng 40k ký tự đầu verbatim, phần sau qua tóm tắt |
| EviRCA (2609.19825v1) | Không | Không thấy nhắc | Không (module ablation) | Không | Không (luôn chốt) | **Có, post-hoc** (not surfaced vs reasoning) | §I, §III, §IV-E; một phần qua tóm tắt |
| 2607.13548 (v1; có v2 22/10/2026) | Một phần (tool trên CSV) | Không rõ | Không | Không; v2 abstract nói không kiểm forward identifiability | Không | **Có, post-hoc**, LLM được xem đáp án | §III-D; v1 khoảng 40k ký tự đầu verbatim; **v2 chưa đọc** |
| 2606.29193v1 | Không (file) | Có | Không | Không; có thống kê mô tả modality necessity (§4.5) | Không | Không | §4–6; đọc đủ HTML |
| ARMOR (2603.25538) | Không | — | Có (missing modality, mô hình tự giám sát) | Không | Không | Không | Chỉ snippet tìm kiếm **[Chưa xác minh]** |
| Edge Delta RCA Bench | — | — | Có (degraded telemetry) | Không rõ | 1 "abstention trap" | Không rõ | Trang web doanh nghiệp, không bình duyệt |

### 7.2 Phần nào không phải đóng góp của nhóm

- "Bỏ một nguồn dữ liệu rồi đo accuracy giảm": ORCA-bench và ARMOR đã có.
- Phân rã "thiếu evidence" vs "suy luận sai" theo kiểu post-hoc: EviRCA, 2607.13548 đã có.
- Metric FAR/UAR và ý tưởng ambiguity khách quan: TelemetrySuffBench.
- Verifier, contrastive prompt, non-closure: DiagGuard, TelemetrySuffBench, JustDiag.

### 7.3 Phần còn lại là lõi **[Diễn giải, novelty tạm thời]**

1. Trần identifiability **tính trước** (forward), không phụ thuộc agent, trên môi trường K8s **tương tác**.
2. Observability profile có căn cứ cơ chế thật của Kubernetes.
3. Chia mức giảm accuracy thành **tránh được và không tránh được**, chấm tự động không cần LLM judge.
4. Đánh giá selective **so với trần**, ở cùng coverage và budget, theo trục sức mạnh model.

Nếu một paper mới làm "mask telemetry K8s rồi chạy agent", bốn điểm trên vẫn còn giá trị. Novelty chỉ thành chắc chắn sau khi kiểm xong các việc ở mục 12.

---

## 8. Lộ trình và decision gates

Mốc thời gian là ước lượng, bắt đầu từ 11/2026. Đạt gate mới mở rộng thí nghiệm. Phân vai: **Nguyên** lo hạ tầng (harness, view, chạy thí nghiệm, chi phí); **Lộc** lo oracle (profile, discriminator, gán nhãn, phân rã). Cả hai cùng đọc phần method và evaluation của Cloud-OpsBench, TelemetrySuffBench.

| Tháng | Đọc (cần lấy gì) | Xây | Sản phẩm | Gate |
|---|---|---|---|---|
| **T1** (≈11/2026) | Cloud-OpsBench §3.3, §4.1 + `agents/cloudops_agent/tools/`; TelemetrySuffBench §III-F; Reiter 1987; Sampath 1995; K8s docs (events, Logging Architecture); kiểm novelty ở mục 12 | Loader case (metadata, tool_cache, milestone); chạy 1 case end-to-end | Sơ đồ episode, trace mẫu, chi phí thật/episode, ghi chú cache key và cache miss | Chạy được 1 case; hiểu cache miss; novelty chưa bị chiếm |
| **T2** (≈12/2026) | 2606.29193 §4.5; DiagGuard Bảng 3; taxonomy Cloud-OpsBench Table 2 | Định nghĩa profile P0–P5 có trích dẫn; discriminator catalog; masker + manifest; leak checker; bộ tính trần | **Kết quả RQ1** (không tốn API); annotation guide; kappa | Kappa chấp nhận được (chốt ngưỡng trước); leak rate thấp sau audit |
| **T3** (≈01/2027) | Kim et al. 2602.09937; EviRCA §IV-E | Harness với schema mục 6.5, budget cap, log trace; scorer tự động | Pilot: 20 base case × {P0 + 2 profile} × B0 × 1 model | Thấy tín hiệu H2/H3; chi phí nằm trong trần |
| **T4–T5** (≈02–03/2027) | Geifman & El-Yaniv 2017 (risk–coverage); DiagGuard §6 (adapter) | B1, B2, B3, B4, R (và M nếu cần) | Thí nghiệm chính: 100–150 base case, 3 model, mọi profile với B0; đủ method grid trên 1–2 model | Dev/test đã khóa; ngưỡng chọn trên dev |
| **T6** (≈04/2027) | Đọc thêm cho related work | Phân tích độ nhạy (catalog, C(r)); tùy chọn lặp RQ1 trên benchmark thứ hai (RCA100 của 2606.29193, CC BY-NC-SA) | Bảng, hình, kiểm định, phân tích lỗi theo DiagGuard taxonomy | Kết luận đứng vững qua phân tích độ nhạy |
| **T7** (≈05/2027) | — | Công bố catalog, profile, manifest, code | Bản thảo paper + chương thesis; chọn venue theo deadline lúc đó (ISSRE, ASE, FSE; workshop AIOps làm dự phòng) | Giảng viên đồng ý claim và phạm vi |
| T8 | Dự phòng | — | — | — |

**Ước lượng chi phí:** dùng số đo thật từ T1.
- Chi phí API ≈ số base case × số profile × số model × số phương pháp × số lần lặp × chi phí trung bình/episode.
- Đặt trần cho toàn đề tài trước T3. Nếu vượt: giảm model frontier xuống subset, chạy method grid trên model rẻ.

---

## 9. Rủi ro và phương án lùi

| Rủi ro | Dấu hiệu sớm | Xử lý |
|---|---|---|
| Cache miss trả response lạ, làm hỏng masking hoặc lộ thí nghiệm | T1, đọc code tools | Tự viết lớp view trả response thực tế; nếu không được thì chỉ mask ở mức tool |
| Discriminator không đạt đồng thuận | T2, kappa thấp | Thu hẹp về fault family có discriminator rõ ràng |
| K8s state dư thừa, RQ1 gần như luôn identifiable | T2 | Thông điệp chuyển thành "mức giảm đều tránh được"; tăng trọng số RQ2; thêm phương án audit shortcut |
| Agent frontier đã biết dừng gần hoàn hảo | T3 | Báo cáo theo trục model; nhấn mạnh UAR, chi phí và model open/nhỏ |
| Chi phí API vượt trần | T3 | Giảm quy mô theo thứ tự: số method, rồi số model frontier, rồi số profile |
| Có paper trùng phần lõi | Tìm lại mỗi tháng | Báo khác biệt; chuyển thành replication, mở rộng sang profile K8s |
| Phương án lùi tổng thể | Gate T2 hoặc T3 không đạt | **Audit shortcut agentic RCA:** đo bao nhiêu case giải được chỉ từ alert và pod status, dùng lại toàn bộ hạ tầng T1–T2 |

---

## 10. Bằng chứng chống lại đề xuất và câu hỏi phản biện

### 10.1 Bằng chứng chống lại

- ORCA-bench đã thay đổi thông tin có sẵn và đo hallucination. Phần "mask rồi đo" không mới.
- EviRCA và 2607.13548 đã phân rã lỗi. Nếu v2 của 2607.13548 hoặc một bài mới làm forward identifiability, lõi 7.3(1) mất tính mới.
- Oracle dựa trên catalog vẫn có phán đoán của người; hội đồng có thể cho là "chủ quan theo kiểu khác".
- Cloud-OpsBench chỉ có 2 hệ thống demo, lỗi do inject, không có traces. External validity hạn chế.

### 10.2 Câu hỏi phản biện dự kiến

| Câu hỏi | Trả lời |
|---|---|
| "Mask dữ liệu là nhân tạo?" | Profile là can thiệp có kiểm soát, căn cứ vào cơ chế mặc định của K8s; nhóm không claim đại diện phân bố thật. OpenRCA 2.0 §5 tự đề xuất trục này |
| "Discriminator vẫn chủ quan?" | Câu hỏi hẹp theo từng cặp, kiểm tự động trên kho response, có kappa, leak audit và audit đối kháng; có phân tích độ nhạy |
| "Khác TelemetrySuffBench?" | Môi trường tương tác, incident K8s đã capture, agent tự chọn truy vấn, profile thực tế, có phân rã lỗi |
| "Khác EviRCA / 2607.13548?" | Họ phân rã post-hoc, có điều kiện theo nhãn; nhóm tính trần **trước**, có kiểm soát, không cần judge |
| "Model mạnh hơn thì công trình còn ý nghĩa?" | RQ1 không phụ thuộc model; phần (i) không model nào vượt được; sức mạnh model là một biến của RQ2 |
| "Không có phương pháp mới?" | Đóng góp chính là đo lường và phát hiện. Nếu rule đơn giản thắng, đó vẫn là kết quả có giá trị |

---

## 11. Quan hệ với roadmap hiện tại

| Roadmap (`roadmap/AIOps_Thesis_Research_Guide.md`) | Memo này |
|---|---|
| Selective RCA, telemetry thiếu, Cloud-OpsBench | **Giữ** |
| Bộ metric coverage, selective error, unsupported commit, unnecessary abstention, cùng coverage | **Giữ**, thêm unsupported-correct và phân rã |
| Oracle "đủ bằng chứng" do 2 người gán theo case | **Đổi** thành discriminator catalog theo cặp fault type + trần tính tự động |
| Missing telemetry do nhóm tự chọn cách bỏ | **Đổi** thành profile có căn cứ cơ chế K8s |
| Stale telemetry | **Bỏ khỏi claim chính** (không có lịch sử thật) |
| Verifier hoặc can thiệp mới là RQ2 | **Hạ xuống tùy chọn (C3)** |

Roadmap chưa được sửa. Nếu nhóm đồng ý hướng này, cập nhật roadmap là một việc riêng.

---

## 12. Việc cần làm ngay

1. **Nguyên:** clone Cloud-OpsBench, ghi commit; đọc `agents/cloudops_agent/tools/` (cache key, cache miss); chạy 1 case, ghi tokens và chi phí.
2. **Lộc:** mở `metadata.json`, `tool_cache.json`, `milestone.json` của 3 case thuộc nhóm service/startup; viết thử 3 discriminator; tìm thủ công đường leak qua tool khác.
3. **Cả hai:** trích Kubernetes docs chính thức về event TTL, log khi container restart, log rotation để chốt P1–P2.
4. **Kiểm novelty, phải xong trong T1:**
   - Đọc 2607.13548 **v2** full text, chú ý phần "forward identifiability".
   - Đọc phần còn lại của ORCA-bench (Finding #3–4, Appendix I–K).
   - Đọc EviRCA §IV-E, Fig. 4.
   - Đọc OpenRCA 2.0 v2.
   - Tìm thêm theo các cụm "diagnosability LLM agent", "information availability RCA benchmark", "observability profile root cause".

---

## 13. Nhật ký tra cứu (07/11/2026)

**Truy vấn web:**

1. `LLM agent root cause analysis abstention incomplete telemetry missing observability Kubernetes 2026`
2. `JustDiag justified diagnosis non-closure competing hypotheses arXiv 2606.19407`
3. `edgedelta root-cause-bench degraded telemetry abstention benchmark`
4. `VerifyRCA LLM-guided evidence-verified root cause analysis microservice`: không tìm được nguồn tên VerifyRCA ngoài link ResearchGate trong roadmap
5. `RCA benchmark shortcut leakage fault injection artifacts LLM agent ...`
6. `selective prediction risk-coverage LLM agent incident diagnosis value of information query selection SRE`
7. `survey AIOps large language models failure management incident lifecycle ...`
8. `LLM agent root cause analysis missing telemetry modality ablation ...`
9. `observability cost reduction trace sampling log reduction impact on root cause analysis diagnosability`
10. `agentic incident mitigation remediation safety LLM benchmark Kubernetes 2026 STRATUS ITBench`
11. `"root cause analysis" "missing modality" OR "modality dropout" OR "partial observability" LLM agent microservice evaluation`

**Full text đã đọc (qua công cụ fetch, có giới hạn độ dài):**

- Cloud-OpsBench repo README, `cloudopsbench_mcp/README.md`, danh sách commit.
- JustDiag HTML v1; PDF không giải mã được.
- OpenRCA 2.0 HTML v1.
- 2607.13548 HTML v1 (một phần) và trang abstract (có v2).
- 2606.29193 HTML v1.
- ORCA-bench HTML v1 (một phần).
- EviRCA HTML v1 (một phần).

Các phần chỉ đọc qua tóm tắt đã đánh dấu ở mục 7.1. **Trước khi trích dẫn trong thesis, phải đối chiếu lại PDF hoặc bản HTML đúng version.**

---

## 14. Tài liệu tham khảo

**Benchmark và các bài gần nhất**

- Cloud-OpsBench: https://arxiv.org/abs/2603.00468v2 · https://github.com/LLM4Ops/Cloud-OpsBench
- TelemetrySuffBench: https://arxiv.org/html/2608.07899v1 (PDF local: `paper/TelemetrySuffBench.pdf`)
- Beyond Fault Localization / DiagGuard: https://arxiv.org/html/2608.21310v2 (PDF local: `paper/Beyond Fault Localization.pdf`)
- OpenRCA 2.0: https://arxiv.org/html/2606.27154v1
- JustDiag!: https://arxiv.org/html/2606.19407v1
- How Far Can Root Cause Analysis Go on Real-World Telemetry Data?: https://arxiv.org/abs/2607.13548
- A Multi-Dataset Benchmark for Evaluating LLM Agents in Microservice Failure Diagnosis: https://arxiv.org/html/2606.29193v1
- ORCA-bench: https://arxiv.org/html/2607.28545v1
- EviRCA: https://arxiv.org/html/2609.19825v1
- Why Do AI Agents Systematically Fail at Cloud Root Cause Analysis?: https://arxiv.org/html/2602.09937v2
- Auditable Graph-Guided RCA for Kubernetes Incidents: https://arxiv.org/abs/2606.08590

**Thiếu dữ liệu và observability**

- ARMOR (missing modality RCA): https://arxiv.org/pdf/2603.25538
- Gleaner (log-aware trace sampling): https://arxiv.org/pdf/2604.16810
- Datadog, Optimizing Distributed Tracing: https://www.datadoghq.com/architecture/optimizing-distributed-tracing-best-practices-for-remaining-within-budget-and-capturing-critical-traces/
- Grafana Adaptive Telemetry: https://grafana.com/blog/adaptive-telemetry-suite-in-grafana-cloud/
- Edge Delta RCA Bench: https://edgedelta.com/benchmark/rca-bench

**Toàn cảnh và remediation**

- A Survey of AIOps in the Era of LLMs (CSUR): https://arxiv.org/abs/2507.12472
- A Survey of AIOps for Failure Management in the Era of LLMs: https://arxiv.org/html/2406.11213v4
- STRATUS (NeurIPS 2025): https://proceedings.neurips.cc/paper_files/paper/2025/hash/47a6e9e2c3019f13ad94a0f259fe4970-Abstract-Conference.html
- Can LLMs Really Recover Microservice Failures?: https://arxiv.org/pdf/2607.04623

**Phê bình benchmark**

- An Empirical Study of SOTA RCA Models: https://arxiv.org/html/2510.04711v1
- Traversal, OpenRCA Isn't Root Cause Analysis (blog): https://www.traversal.com/blog/openrca-isnt-root-cause-analysis-why-that-matters

**Nền lý thuyết [chưa đối chiếu bản gốc]**

- M. Sampath et al., "Diagnosability of discrete-event systems," *IEEE Transactions on Automatic Control*, 1995.
- R. Reiter, "A theory of diagnosis from first principles," *Artificial Intelligence*, 1987.
- J. de Kleer, B. C. Williams, "Diagnosing multiple faults," *Artificial Intelligence*, 1987.
- R. El-Yaniv, Y. Wiener, "On the foundations of noise-free selective classification," *JMLR*, 2010.
- Y. Geifman, R. El-Yaniv, "Selective classification for deep neural networks," *NeurIPS*, 2017.

**Tài liệu kỹ thuật [chưa trích dẫn vị trí cụ thể]**

- Kubernetes docs: Logging Architecture; kube-apiserver reference (`--event-ttl`); Debug Services.
- B. Beyer et al. (eds.), *Site Reliability Engineering*, O'Reilly, 2016, Ch. 1.
