# Finding: TelemetrySuffBench - Telemetry có đủ để tìm nguồn gốc lỗi không?

**Paper:** *TelemetrySuffBench: Is Agent Telemetry Sufficient for Failure-Origin Diagnosis?* (Yuxuan Zhu, Peng Pu - East China Normal University)
**Mã:** arXiv:2608.07899v1 [cs.AI], 8/8/2026 · **PDF:** `paper/TelemetrySuffBench.pdf` (10 trang)
**Artifact:** `https://anonymous.4open.science/r/TelemetrySuffBench-E635/README.md`
**Quy ước đọc file này:** nhãn **[Paper]** là điều paper nói (kèm §/Bảng/Hình). Nhãn **[Diễn giải]** là ví dụ, nhận xét hoặc đề xuất của reader, không phải kết luận của paper.

---

## 📌 CHEATSHEET (đọc lại trong 2 phút)

**Một câu:** Có telemetry theo chuẩn công nghiệp (OpenTelemetry…) giúp *phát hiện* lỗi gần như hoàn hảo, nhưng **không đủ để chỉ ra nguồn gốc lỗi**; và khi dữ liệu mập mờ, LLM thường **đoán bừa thay vì nói "không đủ bằng chứng"**.

**Thiết lập [Paper §III]:** lỗi *delayed-binding* (chọn sai tham chiếu ở đầu, nổ ở cuối) · 5 model (GPT-5.5, GPT-5.6 Sol, DeepSeek-V4-Pro, Claude Opus 5, Qwen 3.7 Max) · 6 định dạng log · 7 nhân tố ngữ nghĩa · 5 chặng nhân quả.

**5 chặng nhân quả:** `Origin (gốc) → Intermediate → Activation → Symptom → Terminal (báo động)`. Câu trả lời đúng cho "lỗi bắt nguồn từ đâu?" **chỉ là Origin**.

**7 nhân tố telemetry:**

| Ký hiệu | Tên | Hiểu nhanh |
| --- | --- | --- |
| **I** | Identity & Event | AI làm? (actor, component, tool) |
| **D** | Decision Content | Chọn tham chiếu nào? |
| **P** | Provenance & Registry | Tham chiếu tra từ đâu? |
| R | Propagation Relations | Quan hệ cha-con giữa sự kiện |
| S | Tool Inputs & State | Tham số/kết quả tool |
| V | Verifier Evidence | Kỳ vọng vs thực tế |
| T | Terminal Status | Mã lỗi/exception cuối |

**Con số cần nhớ:**

| Câu hỏi | Kết quả [Paper] |
| --- | --- |
| Phát hiện lỗi (Detection F1) ở mọi định dạng | **99.3-100%** |
| Tìm đúng Origin với Metadata/OTel/OpenInference | **≤ 0.5%** (component chỉ ~9.7-11.1%, ngang đoán mù 1/9) |
| Tìm đúng Origin với `Full` | Opus 5 và GPT-5.6 Sol **97.2%** · GPT-5.5 90.3% · DeepSeek 84.7% · Qwen **33.8%** |
| Bỏ nhân tố **D** (`Full-D`) | **Cả 5 model rớt về 0.0%** |
| Chỉ có dữ liệu hạ nguồn `S+V+T` | **0.0%** cả 5 model |
| `I+D+P+V` | 86.1-100.0% |
| Bỏ `I` (`D+P+V`) | rớt còn 5.6-61.8% |
| FAR (đoán bừa) trên hồ sơ rich-ambiguous, prompt P0 | DeepSeek **100%** · Qwen **100%** · GPT-5.5 87.5% · GPT-5.6 Sol 44.4% · Opus 5 **12.5%** |
| FAR sau prompt P3 (loại trừ đối chứng) | GPT-5.5 → 38.9% · GPT-5.6 Sol → 13.9% · Opus 5 → 0.0% · DeepSeek/Qwen **vẫn 100%** |

**Trả lời 3 RQ:**
- **RQ1:** Telemetry đủ để *báo động*, không đủ để *tìm gốc*. Model bị dắt mũi vào triệu chứng hạ nguồn (~98-99% dự đoán rơi vào Symptom ở 3 định dạng chuẩn).
- **RQ2:** Nhân tố sống còn là **I + D + P** (ai, quyết định gì, từ đâu). Dữ liệu hạ nguồn (S) thậm chí gây **nhiễu**.
- **RQ3:** Khi hồ sơ nhìn "dày" nhưng thực chất mơ hồ, nhiều model vẫn chốt bừa. Prompt **P3** giúp một số model, nhưng làm tăng từ chối oan (UAR).

**Metric abstention:** FAR (đoán bừa trên ca mơ hồ, càng thấp càng tốt) · UAR (từ chối oan trên ca đủ bằng chứng, càng thấp càng tốt) · Safe Accuracy (đúng khi đủ + từ chối đúng khi thiếu) · Coverage · Selective Error.

**Điểm yếu [Diễn giải]:** bài toán nhân tạo/hẹp (gán nhầm tham chiếu trong app đơn hàng/vé giả lập) · trace tĩnh (không cho agent tự truy vấn thêm) · chưa đo telemetry *cũ/trễ* thật của hạ tầng.

**Dùng cho luận văn [Diễn giải]:** kỹ thuật *Exact-Equal Ambiguity* để dựng benchmark thiếu dữ liệu có nhãn khách quan · bộ metric FAR/UAR/Safe Acc/Coverage · prompt P3 · trong K8s, đảm bảo agent có công cụ lấy được tầng **D/P** (config, endpoints) chứ không chỉ log hạ nguồn.

---

## 1. Ý tưởng trung tâm: nhìn thấy hết ≠ biết ai gây lỗi

**Thuật ngữ nền:**
- **Telemetry:** dấu vết phần mềm để lại: *logs* (nhật ký sự kiện), *metrics* (CPU, RAM, request/s), *traces/spans* (hành trình của một request qua các service).
- **Observability:** hệ thống được gắn đủ công cụ (OpenTelemetry, Prometheus…) để thu các dữ liệu trên.

Nhiều người nghĩ: "log đủ, trace đẹp thì agent đọc là ra nguyên nhân". Paper phản bác: *"Observability alone does not establish diagnostic adequacy"* [Paper §I, tr.1].

**Ví dụ nhà máy may [Diễn giải]:**
Khâu kiểm tra cuối báo: "áo này đơm nhầm cúc đen, đơn yêu cầu cúc trắng". Phát hiện lỗi (*detection*) rất dễ. Camera khâu đơm cúc cho thấy máy đơm đúng cái cúc đen được đưa tới. Nếu kết luận "máy đơm cúc hỏng" là sai. Máy làm đúng chức năng, người dán nhầm nhãn hộp cúc ở kho mới là **Origin**.

Với agent nhiều bước cũng thế: phát hiện lỗi thì dễ (verifier báo sai), tìm Origin thì khó vì nó nằm đầu nguồn còn chỗ báo lỗi nằm cuối nguồn. Nếu telemetry chỉ ghi "bước 1 OK, bước 2 OK, bước 3 lỗi" thì trace dài 1.000 dòng vẫn thiếu bằng chứng về bước 1.

---

## 2. Lỗi "quả bom nổ chậm" (Delayed-Binding Faults) [Paper §III-B, Hình 1]

**Khác biệt cốt lõi:**
- *Lỗi chết ngay:* sai cú pháp SQL, chia cho 0 → crash tại chỗ. Dễ bắt, không cần benchmark.
- *Lỗi delayed-binding:* ở bước đầu agent chọn **sai một tham chiếu tượng trưng** (*symbolic reference*) nhưng không có lỗi nào văng ra. Các bước sau xử lý trơn tru. Nhiều bước sau, khi tham chiếu được dùng để ghi dữ liệu thật thì mới "nổ".

**Ví dụ trong paper (nhiệm vụ: cập nhật Record A; hệ thống có `ref_A → Record A`, `ref_B → Record B`):**

```text
1. ORIGIN        : agent chọn nhầm ref_B* (tưởng đang xử lý A). Không có lỗi cú pháp.
        ↓
2. INTERMEDIATE  : ref_B* đi qua Planner → Memory → Guardrail. Tất cả báo SUCCESS.
        ↓
3. ACTIVATION    : Resolver tra ref_B* → ra Record B. Đây là "First Visible Deviation".
        ↓
4. SYMPTOM       : Update Tool ghi đè lên Record B, trả 200 OK. Record B bị sửa oan.
        ↓
5. TERMINAL      : Verifier mở Record A: "chưa được sửa" → FAILED (final state mismatch).
```

**6 toán tử tiêm lỗi [Paper §III-B]:** Alias binding · Version binding · Namespace handoff · Schema binding · Evidence binding · Retry-token binding. (Version binding và Retry-token binding tạo loại lỗi `stale_reference_state`.)

---

## 3. Năm chặng nhân quả [Paper §III-B, §III-G]

```text
 (1) Origin → (2) Intermediate → (3) Activation → (4) Symptom → (5) Terminal
  Gốc rễ        Lưu chuyển          Hiển lộ đầu      Triệu chứng     Báo động
                                    (First Visible    hạ nguồn
                                     Deviation)
```

| Chặng | Là gì |
| --- | --- |
| 1. Origin | Sự kiện đầu tiên gán sai tham chiếu. **Đáp án duy nhất đúng** cho "lỗi bắt nguồn từ đâu?" |
| 2. Intermediate | Tham chiếu sai được chuyển tiếp, hệ thống vẫn "xanh" |
| 3. Activation | Giá trị sai lần đầu hiện ra trong logic nghiệp vụ (Resolver dịch ra đối tượng sai) |
| 4. Symptom | Hành động gây hậu quả trực tiếp (tool ghi nhầm Record B) |
| 5. Terminal | Verifier phát hiện trạng thái cuối không khớp |

**Causal Stage Collapse:** nếu chỉ nhìn log tool cập nhật (chặng 4) hoặc log báo động (chặng 5) rồi gọi đó là nguyên nhân gốc, thì **Origin-Step Top-1 Accuracy = 0.0%** [Paper §IV, Bảng II].

---

## 4. Bảy nhân tố ngữ nghĩa và thí nghiệm "che bớt" [Paper §III-E, Bảng I]

Thay vì dùng log nguyên khối, tác giả tách mỗi dòng telemetry thành 7 nhân tố (bảng ở Cheatsheet) rồi dùng **mặt nạ (mask)** để che/giữ từng nhân tố:

- **`Full`**: giữ cả 7.
- **Leave-one-factor-out** (`Full-I`, `Full-D`, `Full-P`, `Full-R`, `Full-S`, `Full-V`, `Full-T`): bỏ đúng một nhân tố, giữ 6 còn lại.
- **Targeted subsets**: `I+D+P+V` (bộ thượng nguồn) · `D+P+V` (như trên, bỏ I) · `S+V+T` (bộ hạ nguồn).

Mục đích: tìm nhân tố nào là "linh hồn" để định vị Origin. Phép che là *deterministic projection* trên cùng một lần chạy, nên khác biệt không đến từ may rủi của môi trường.

---

## 5. Kết quả RQ1-RQ3

### 5.1. RQ1: Telemetry phát hiện lỗi có đủ để tìm gốc không? [Paper §V-A, Bảng II, Hình 2]

```text
Detection F1 (phát hiện lỗi)   : 99.3% - 100%   ở MỌI định dạng
Origin-Step Acc (tìm đúng gốc) : ≤ 0.5%         ở Metadata / OTel / OpenInference
```

- **`Full`:** Origin accuracy: GPT-5.6 Sol và Claude Opus 5 **97.2%**, GPT-5.5 90.3%, DeepSeek-V4-Pro 84.7%, Qwen 3.7 Max **33.8%**.
- **Metadata / OpenTelemetry / OpenInference:** detection vẫn 99.5-100%, nhưng Origin-step gần 0; component chỉ 9.7-11.1% (ngang chọn bừa 1 trong 9).
- **Model nhìn vào đâu?** 97.9% (Metadata), 99.0% (OTel), 98.7% (OpenInference) dự đoán rơi vào **Symptom** hạ nguồn.

> **Kết luận RQ1:** chuẩn như OTel/OpenInference tốt cho *alerting*, nhưng thiếu ngữ nghĩa để *tìm gốc*.

### 5.2. RQ2: Nhân tố nào quan trọng nhất? [Paper §V-B, Bảng III, Hình 3]

1. **Bỏ D** (Decision): Origin accuracy của **cả 5 model về 0.0%**; component chỉ 11.1% (ngẫu nhiên). Fault-type Macro-F1 vẫn 40-88%, tức model còn biết *loại lỗi gì* nhưng không biết *ai gây*. 98.1% dự đoán nhảy sang sự kiện Activation.
2. **Bỏ P** (Provenance): accuracy rớt 19.4-79.9 điểm % (DeepSeek mất 79.9, Claude mất 68.8). 66.7% dự đoán trôi về Activation.
3. **Bộ I + D + P:** `I+D+P+V` đạt 86.1-100.0%. Bỏ `I` (`D+P+V`) thì rớt còn 5.6-61.8% (mất 38.2-93.8 điểm). *Hiểu nhanh:* có quyết định sai và sổ tra cứu mà không biết *ai* làm thì không gán được trách nhiệm.
4. **Nhiều log hạ nguồn không giúp, còn gây nhiễu:** `S+V+T` cho **0.0%** ở mọi model. Bỏ `S` khỏi `Full` (`Full-S`) thì 4/5 model *tăng* accuracy (GPT-5.5 từ 93.1% lên 100.0%). Tool state chi tiết ở hạ nguồn như vật gây nhiễu (*distractor*), kéo sự chú ý về hiện trường thay vì nguồn gốc.

### 5.3. RQ3: AI có dám nói "không đủ bằng chứng"? [Paper §III-F, §V-D, Bảng IV]

**Kỹ thuật "vụ án song sinh" (Exact-Equal Ambiguity):**
- Vụ A: lỗi thật được tiêm vào component `Planning`. Vụ B: lỗi thật tiêm vào `Memory`.
- Dùng mặt nạ `m` sao cho phần telemetry model nhìn thấy ở A và B **giống hệt từng byte**:

$$P_m(\tau_a) = P_m(\tau_b) \quad \text{nhưng} \quad \omega_a \neq \omega_b$$

- Vì hai hồ sơ giống hệt mà đáp án thật khác nhau, **không có cách nào đúng ngoài trả `INSUFFICIENT_EVIDENCE`**. Trả "Planning" là sai ở vụ B; ở vụ A dù trúng tên vẫn bị tính là *Unsupported Unique-Origin Answer* vì không có bằng chứng loại trừ `Memory`. Nhãn đúng được xác định khách quan, không cần LLM-judge hay phán đoán chủ quan.

**Metric:**
- **FAR (False-Answer Rate):** tỷ lệ vẫn chốt 1 thủ phạm trên hồ sơ *ambiguous*. Thấp tốt.
- **UAR (Unnecessary-Abstention Rate):** tỷ lệ từ chối trên hồ sơ *answerable*. Thấp tốt.
- **Safe Accuracy:** đúng khi đủ bằng chứng + từ chối đúng khi thiếu.

**Kết quả [Bảng IV]:**

```text
FAR trên hồ sơ rich-ambiguous, prompt P0 (hồ sơ nhìn dày nhưng thực chất mơ hồ)
DeepSeek-V4-Pro : 100.0%   Qwen 3.7 Max : 100.0%
GPT-5.5         :  87.5%   GPT-5.6 Sol  :  44.4%   Claude Opus 5 : 12.5%
```

1. **Hồ sơ sơ sài (sparse-ambiguous):** cả 5 model FAR = 0%, đều biết nói "không đủ".
2. **Hồ sơ nhìn dày (rich-ambiguous):** nhiều model chốt bừa dù prompt P0 đã cảnh báo.
3. **Prompt P3 (Contrastive Elimination: phải tìm bằng chứng loại trừ giả thuyết khác trước khi chốt):**
   GPT-5.5 87.5% → **38.9%** · GPT-5.6 Sol 44.4% → **13.9%** · Opus 5 12.5% → **0.0%** · DeepSeek, Qwen: **không đổi, vẫn 100%**.
4. **Đánh đổi an toàn - hữu ích:** P3 làm model "đa nghi" hơn, tăng từ chối oan (UAR của GPT-5.6 Sol 24.3% → 34.0%).

---

## 6. Đánh giá phản biện [Diễn giải của reader]

**Điểm mạnh**
1. *Internal validity chặt:* cùng một lần chạy, chỉ đổi "kính lọc" → loại bỏ nhiễu từ môi trường.
2. *Chuẩn vàng khách quan cho abstention:* hai kịch bản khác nhau có cùng biểu diễn byte → đáp án đúng xác định bằng logic, không cần judge.
3. *Kỷ luật thống kê:* frozen blind holdout, bootstrap 10.000 lần, output sai JSON bị tính 0 điểm.

**Điểm hạn chế**
1. *Miền hẹp, nhân tạo:* lỗi chủ yếu là gán nhầm tham chiếu trong app giả lập; chưa có OOM, nghẽn mạng, race condition…
2. *Trace tĩnh, không tương tác:* SRE ngoài đời sẽ chạy thêm `kubectl logs/describe` khi thiếu thông tin. Paper chưa đo khả năng *chủ động truy vấn để giải quyết mơ hồ*.
3. *Chưa giải quyết stale telemetry thật:* nhãn `stale_reference_state` vẫn là tham chiếu sai về logic, chưa phải log trễ hay metric bị cache ở hạ tầng.

---

## 7. Áp dụng cho luận văn Kubernetes [Diễn giải / đề xuất, chưa được paper kiểm chứng]

> Đề tài: *Selective Root Cause Analysis under Incomplete Telemetry in Kubernetes*. Mọi ví dụ K8s dưới đây là **giả thuyết do reader dựng**, cần thực nghiệm riêng mới khẳng định. Paper chỉ chứng minh trong benchmark nhân tạo của nó.

**Vai trò ba nguồn:**

| Nguồn | Lấy gì |
| --- | --- |
| TelemetrySuffBench | Vì sao thiếu dữ liệu thì phải abstain · Exact-Equal Ambiguity · metric FAR/UAR/Safe Acc/Coverage · prompt P3 |
| Cloud-OpsBench | Môi trường K8s thật, agent tương tác bằng read-only tools |
| DiagGuard (xem `BeyondFaultLocalization_FINDING.md`) | Taxonomy OMIT/MIS/GEN · cơ chế Verifier trước khi chốt |

### 7.1. Ánh xạ 5 chặng sang một sự cố K8s (ví dụ minh họa)

```text
1 ORIGIN       : YAML Service selector viết nhầm `app: payment-v2` thành `app: payment-v1` (≈ nhân tố D sai)
2 INTERMEDIATE : control plane reconcile, Service tạo thành công, không lỗi cú pháp
3 ACTIVATION   : EndpointSlice rỗng (`endpoints: []`) vì không pod nào khớp nhãn
4 SYMPTOM      : Ingress Nginx không có endpoint → HTTP 503
5 TERMINAL     : Prometheus thấy tỷ lệ 5xx vượt ngưỡng → Alertmanager báo Slack
```

**Hàm ý thiết kế:** nếu agent chỉ có log Nginx + alert (tầng 4-5, tương đương `S+V+T`) thì trong benchmark của paper loại dữ liệu này cho 0% Origin accuracy. Trong K8s, *giả thuyết* là agent cần tool cho tầng 3 và 1 (`kubectl get endpoints`, `kubectl describe svc`). Cần pilot để kiểm tra.

### 7.2. Dựng benchmark "Incomplete Telemetry" bằng Exact-Equal Ambiguity (ví dụ minh họa)

- **Sự cố 1:** Service trỏ sai `targetPort` (8080 thay vì 80).
- **Sự cố 2:** app trong container bị deadlock, không listen port 80.
- **Cố ý hạn chế công cụ:** tắt `kubectl exec` và tool xem cấu hình runtime; chỉ cho log Ingress + trạng thái Pod.
- Cả hai đều cho cùng quan sát: Ingress 502/503, Pod `Running 1/1`. Nếu telemetry agent nhìn thấy hai bên giống hệt, thì đáp án đúng duy nhất là `INSUFFICIENT_EVIDENCE`, và mọi kết luận "targetPort" hay "deadlock" đều tính là FAR.

**Cần kiểm chứng:** đảm bảo thật sự hai trace giống nhau (kể cả timestamp, tên pod…), như paper làm với byte-stable equality (công thức 2, §III-F).

### 7.3. Bộ chỉ số nên dùng

1. **Coverage** = số ca có kết luận / tổng số ca.
2. **Selective Error** = tỷ lệ sai *trong số ca đã kết luận*.
3. **FAR** (trên ca thiếu bằng chứng) · 4. **UAR** (trên ca đủ bằng chứng).
5. **Safe Accuracy** = (đúng trên ca đủ + từ chối đúng trên ca thiếu) / tổng số ca.

### 7.4. Prompt mẫu dựa trên P3 (bản của reader, chưa phải P3 nguyên văn của paper)

```markdown
### QUY TẮC LOẠI TRỪ (CONTRASTIVE ELIMINATION)
Trước khi kết luận Root Cause, bạn BẮT BUỘC:
1. Liệt kê ít nhất 2 giả thuyết có thể dẫn tới triệu chứng này.
2. Với mỗi giả thuyết, chỉ ra bằng chứng cụ thể (log, metric, cấu hình) bạn ĐÃ THU THẬP
   để ủng hộ hoặc bác bỏ.
3. Nếu dữ liệu hiện có không loại trừ được một giả thuyết nào, hoặc thiếu bằng chứng trực tiếp
   về cấu hình/trạng thái K8s → trả về "INSUFFICIENT_EVIDENCE". KHÔNG đoán một nguyên nhân duy nhất.
```

Lưu ý: kết quả paper cho thấy P3 không giúp DeepSeek và Qwen. Không nên giả định prompt đủ cho mọi model; cần thêm cơ chế gác cổng ngoài prompt.

---

## 8. Năm điều ghi nhớ

1. **Có log ≠ chẩn đoán được.** Observability ≠ diagnostic adequacy.
2. **Origin khác Symptom/Terminal.** Thiếu `D` và `P` thì Origin accuracy gần 0 (trong benchmark của paper).
3. **Nhiều log hạ nguồn (`S+V+T`) không giúp, còn gây nhiễu.**
4. **Dữ liệu mơ hồ → LLM hay đoán bừa.** Cần loại trừ đối chứng (P3) và cơ chế **abstain**.
5. **Cho luận văn:** Exact-Equal Ambiguity để dựng benchmark có nhãn khách quan; đo bằng FAR/UAR/Coverage; xây agent biết dừng đúng lúc khi telemetry K8s suy giảm.
