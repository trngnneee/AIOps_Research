# AIOps Thesis Research Guide

Nguồn nghiên cứu được rà soát đến 28/10/2026.

Cập nhật cấu trúc và kế hoạch: 29/10/2026. Các đề xuất dưới đây chưa phải kết quả thực nghiệm.

**Mục tiêu:** xác định đề tài khả thi cho nhóm hai người, có research question rõ, đối chứng phù hợp và kết quả kiểm chứng được.

**Hướng đang đề xuất:** nghiên cứu độ tin cậy của LLM agent khi tìm nguyên nhân sự cố Kubernetes từ dữ liệu vận hành thiếu hoặc lỗi thời.

**Trạng thái:** hướng nghiên cứu và research gap cần được xác minh bằng đọc paper và pilot. Tài liệu này là lộ trình để chốt đề tài.

**Cách dùng:** đọc phần tổng quan và ví dụ trước; sau đó đọc paper song song với kiểm tra artifact. Chỉ mở rộng thí nghiệm khi đạt các điều kiện ở mục 8.

## Tổng quan lĩnh vực và kiến thức nền

### AIOps và vị trí của nhóm

AIOps sử dụng AI/ML để hỗ trợ vận hành hệ thống. Sơ đồ dưới đây là khung học cho nhóm, không phải taxonomy đầy đủ của lĩnh vực:

```text
Hệ thống và workload → Thu thập telemetry → Phát hiện bất thường
                                              ↓
                         Gom/ưu tiên cảnh báo → RCA
                                              ↓
                              Remediation → Xác minh phục hồi
```

**Vị trí đề tài:** incident đã được báo → agent điều tra bằng tools chỉ đọc → đưa ra nguyên nhân kèm evidence hoặc chưa kết luận. Nhóm chưa nghiên cứu toàn bộ vòng đời xử lý incident.

Cần phân biệt **AI for Operations** (dùng AI chẩn đoán hệ thống vận hành) với **observability of AI agents** (quan sát execution trace để tìm lỗi bên trong hệ thống agent). TelemetrySuffBench thuộc bối cảnh thứ hai; cơ chế xây nhãn và đánh giá abstention của bài là nguồn tham khảo, cần kiểm chứng khi chuyển sang Kubernetes ([v1, §II–III][suff]).

### Các hướng tiếp cận cần biết

| Hướng | Câu hỏi điển hình | Điều cần cân nhắc với nhóm |
|---|---|---|
| RCA bằng thống kê hoặc dependency/causal graph | Tín hiệu và quan hệ giữa thành phần giúp định vị lỗi thế nào? | Cần hiểu giả định về telemetry và graph; xem [RCAEval][rcaeval] để biết các baseline ngoài LLM. |
| LLM hỗ trợ phân tích | Model tổng hợp telemetry, tài liệu hoặc incident report tốt đến đâu? | Phải phân biệt chất lượng báo cáo với tính đúng của chẩn đoán. |
| Agent RCA qua tools | Agent nên đọc gì tiếp theo để phân biệt các nguyên nhân? | Cần môi trường truy vấn và trace tái lập được; xem [Cloud-OpsBench v2, §3][cloud]. |
| Độ tin cậy của agent RCA | Khi nào evidence đủ để kết luận, cần hỏi thêm hoặc abstain? | Hướng đang ưu tiên; khó nhất là oracle, nhãn tính đủ evidence và đối chứng công bằng. |

**Lý do ưu tiên hướng hiện tại — đề xuất của nhóm:** scope có thể giới hạn ở một task và tận dụng replay; câu hỏi đo được bằng correctness, evidence validity và abstention. Tính khả thi vẫn phụ thuộc vào artifact, baseline, chi phí và khả năng gán nhãn. Các hướng trên có thể kết hợp, không loại trừ nhau.

### Kiến thức tối thiểu trước khi đọc sâu

| Nội dung | Cần giải thích được |
|---|---|
| Kubernetes | Pod, Deployment, Service, EndpointSlice, readiness và rollout liên hệ thế nào? Bắt đầu từ [Debug Services][k8s-debug]. |
| Telemetry | Logs ghi sự kiện; metrics tổng hợp phép đo; traces nối các bước của request; state/events cho biết cấu hình và trạng thái tài nguyên. Xem [OpenTelemetry Observability Primer][otel]. |
| RCA | Phân biệt symptom, thành phần lỗi, cơ chế lỗi và đường lan truyền ảnh hưởng. Tương quan bất thường chưa đủ xác lập nguyên nhân. |
| Agent | Vòng lặp hypothesis → tool query → observation → cập nhật hypothesis → quyết định dừng. |
| Evaluation | Phân biệt gold cause, evidence sufficiency, correctness, coverage và selective error; xem mục 7. |

**Mức đạt:** mỗi người tự giải thích được một incident bằng sơ đồ nguyên nhân–triệu chứng, chỉ ra evidence phân biệt giả thuyết và nêu rõ điều chưa biết. Học thêm theo case, không cần học toàn bộ Kubernetes trước.

## 1. Bài toán cần nghiên cứu

Agent có thể đưa ra một nguyên nhân nghe hợp lý khi dữ liệu quan sát chưa đủ để phân biệt nó với các nguyên nhân khác. Thậm chí kết luận trùng với đáp án, bằng chứng được viện dẫn vẫn có thể sai đối tượng hoặc sai thời điểm.

**Mục tiêu nghiên cứu:** đánh giá và cải thiện khả năng quyết định khi nào nên kết luận, lấy thêm dữ liệu hoặc báo chưa đủ cơ sở để xác định một nguyên nhân duy nhất.

### Ví dụ xuyên suốt: điều tra lỗi 503

**Ví dụ minh họa, chưa phải case đã chạy:** gateway báo 503 khi gọi service `checkout`. Xét hai giả thuyết ban đầu: H1 — Service selector không khớp pod labels; H2 — `targetPort` không trỏ đến cổng ứng dụng đang lắng nghe. Đây chưa phải toàn bộ tập nguyên nhân có thể có.

| Bước | Quan sát cần lấy | Cách diễn giải và hành động tiếp |
|---|---|---|
| Xác định symptom | Thời gian lỗi, request path và upstream được gateway báo lỗi | Xác định đúng service và khoảng incident; chưa chọn nguyên nhân chỉ từ mã 503. |
| Kiểm tra H1 | Service selector, labels của pod hiện tại và EndpointSlice tương ứng | Selector không khớp pod dự kiến hỗ trợ H1. Thiếu endpoint một mình chưa đủ: cần kiểm tra cả readiness. |
| Kiểm tra H2 | `targetPort`, endpoint port, cổng thực tế ứng dụng lắng nghe và kết quả kiểm tra kết nối nếu tools hỗ trợ | Đối chiếu cấu hình với runtime để kiểm tra H2; chỉ đọc `containerPort` chưa chứng minh ứng dụng đang lắng nghe. |
| Đánh giá evidence | Nguồn, đối tượng và thời điểm của các quan sát | Log từ pod trước rollout cần được đối chiếu với pod/phiên bản hiện tại trước khi dùng làm bằng chứng. |
| Quyết định | Evidence đã phân biệt các giả thuyết chưa? | Đủ thì kết luận kèm evidence; còn phép đọc hữu ích trong budget thì truy vấn tiếp; còn mơ hồ thì chưa kết luận. |

Luồng kiểm tra selector, EndpointSlice và port tham khảo [Kubernetes Debug Services, các mục về Service configuration và EndpointSlices][k8s-debug]. Cách ra quyết định selective RCA là đề xuất cho thí nghiệm của nhóm.

**Biến thể missing:** nếu không đọc được selector, phải kiểm tra các tools khác có còn trả cùng thông tin không. Agent chưa hỏi đúng khác với dữ liệu thực sự không khả dụng. **Biến thể stale:** một log cũ vẫn có thể liên quan; chỉ gọi evidence là không còn áp dụng khi có căn cứ về thay đổi trạng thái hoặc đối tượng.

Tên đề tài làm việc:

> **Selective Root Cause Analysis under Incomplete Telemetry in Kubernetes**

Chỉ bổ sung “Stale Telemetry” vào tên đề tài chính thức khi dữ liệu lịch sử và protocol hỗ trợ nhánh này.

Trong tài liệu này:

- **RCA:** xác định thành phần gây lỗi và cơ chế gây lỗi. `503` hoặc `CrashLoopBackOff` mới là triệu chứng/trạng thái.
- **Telemetry:** dữ liệu vận hành như Kubernetes state/events, logs, metrics và traces.
- **Selective RCA:** agent được phép kết luận hoặc chưa kết luận; đánh giá cả độ đúng và tỷ lệ case được kết luận.

## 2. Phạm vi nên chốt

| Thành phần | Phạm vi đề xuất |
|---|---|
| Tác vụ | Chẩn đoán một incident đã được báo; đầu vào có khoảng thời gian sự cố. |
| Hệ thống | Một ứng dụng microservices trên Kubernetes. |
| Agent | Một pipeline RCA dùng model API, truy vấn bằng công cụ chỉ đọc. |
| Dữ liệu | Kubernetes state/events và logs; bổ sung metrics/traces khi cần phân biệt nguyên nhân. |
| Benchmark ban đầu | Thử subset của [Cloud-OpsBench][cloud]. |
| Fault | Pilot hai nhóm, sau đó cân nhắc khoảng bốn nhóm: service routing/configuration, startup/rollout, resource pressure, downstream dependency. |
| Điều kiện quan sát | Dữ liệu chuẩn; dữ liệu thiếu; dữ liệu lỗi thời nếu có lịch sử thật để kiểm chứng. |
| Đầu ra agent | Nguyên nhân kèm evidence; yêu cầu quan sát thêm; hoặc báo chưa đủ cơ sở. |
| Đầu ra nghiên cứu | Protocol, dữ liệu/nhãn, baseline, phương pháp đề xuất và đánh giá thực nghiệm. |

**Phần bắt buộc:** RCA và đánh giá độ tin cậy. Remediation chỉ mở rộng sau khi phần này hoàn chỉnh. Huấn luyện model, multi-agent và xây nền tảng vận hành tổng quát nằm ngoài phạm vi ban đầu.

**Ưu tiên missing trước.** Với nhánh stale, phải có dữ liệu trước/sau thay đổi, timestamp, danh tính tài nguyên và căn cứ giải thích vì sao evidence không còn áp dụng. Nếu benchmark không cung cấp, cân nhắc thu snapshot thật hoặc thu hẹp phạm vi. Không đổi timestamp tùy ý rồi coi đó là dữ liệu đến trễ thực tế.

## 3. Research gap cần xác minh

### 3.1. Những phần đã có tiền lệ

| Nghiên cứu và vị trí nguồn | Phần đã đối chiếu | Cần kiểm tra tiếp |
|---|---|---|
| [Cloud-OpsBench v2, §3.3.2–3.3.3][cloud] | Snapshot replay và nhãn quá trình bên cạnh đáp án cuối. | Artifact có đủ dữ liệu và metadata cho từng điều kiện thử không? |
| [DiagGuard v2, §5.3–6.1][diag] | Grounder/Verifier xử lý lỗi thu thập, diễn giải và suy luận từ evidence. | Adapter sang Kubernetes replay và độ bền khi telemetry thiếu. |
| [TelemetrySuffBench v1, §II-C, III][suff] | Observational ambiguity và abstention khi trace không xác định được nguồn lỗi. | Cách chuyển thiết kế từ agent traces sang incident Kubernetes. |
| [JustDiag v1, §1–3][just] | Evidence, giả thuyết cạnh tranh, xung đột, next checks và non-closure. | Mức chồng lấn với can thiệp dự kiến; protocol và oracle có phù hợp không? |

[VerifyRCA][verify] là nguồn cần đọc thêm; chưa xác minh đầy đủ full text và artifact trong lần cập nhật này. Chưa dùng mô tả cơ chế của bài để kết luận novelty.

Vì vậy, **verifier, truy vấn thêm và abstention riêng lẻ chưa đủ để nhận là đóng góp mới**.

### 3.2. Khoảng trống đề xuất để kiểm tra

> Độ tin cậy của các phương pháp kiểm chứng RCA khi evidence Kubernetes bị thiếu hoặc thuộc sai thời điểm/phiên bản tài nguyên: chúng có phát hiện được lúc chưa nên kết luận, và có thể cải thiện bằng kiểm tra thời gian, nguồn gốc evidence cùng các truy vấn phân biệt nguyên nhân hay không?

Đây là **candidate gap**, chưa phải kết luận rằng các paper hiện có chưa giải quyết bài toán.

Khi đọc các bài gần, nhóm phải xác minh:

1. Bài có thử dữ liệu thiếu/lỗi thời hay chỉ dữ liệu chuẩn?
2. Bài kiểm tra thời gian sự kiện và danh tính/phiên bản tài nguyên đến mức nào?
3. Nhãn “đủ bằng chứng” được thiết lập độc lập ra sao?
4. Có so sánh kết luận sai ở cùng tỷ lệ trả lời và ngân sách không?
5. Có tách dữ liệu chưa được truy vấn khỏi dữ liệu thực sự không khả dụng không?

Ghi section, bảng hoặc đoạn nguồn cho từng câu trả lời. “Không thấy trong abstract” chưa đủ để kết luận paper không làm.

**Related-work matrix cần hoàn thiện:** mỗi dòng gồm paper/version; task và dữ liệu; cơ chế verification; missing/stale; abstention; oracle; model/tools/budget; artifact/commit; khác biệt còn cần kiểm tra. Mỗi ô ghi nguồn và một trạng thái: **đã xác minh**, **chưa kiểm tra** hoặc **nguồn chưa báo cáo rõ**. Ưu tiên bốn bài ở mục 3.1; không điền các ô chưa kiểm tra bằng suy đoán.

### 3.3. Đóng góp có thể hướng tới

- **Thực nghiệm:** xác định điều kiện làm các verifier hiện có vẫn chấp nhận kết luận thiếu cơ sở.
- **Protocol và dữ liệu:** tạo các điều kiện quan sát có nguồn gốc, nhãn và quy trình đánh giá tái lập được.
- **Phương pháp:** kiểm tra thời gian/nguồn gốc evidence và chọn quan sát bổ sung; chứng minh giá trị so với phương pháp gần và rule đơn giản.

Chỉ chốt claim về đóng góp sau khi đối chiếu paper và chạy pilot. Giá trị không được suy ra chỉ từ việc ghép các thành phần thành một pipeline.

## 4. Research question đề xuất

| RQ | Câu hỏi | Kết quả cần đo |
|---|---|---|
| **RQ1 — Ưu tiên xác minh** | Telemetry thiếu có kiểm soát ảnh hưởng thế nào đến correctness, evidence validity và quyết định abstain của các phương pháp RCA hiện có? | Accuracy, selective error, unsupported commit và coverage theo điều kiện dữ liệu. |
| **RQ2 — Chốt sau pilot** | Can thiệp tối thiểu nhắm vào failure pattern đã quan sát có giảm kết luận thiếu cơ sở so với self-check, verifier gần và rule đơn giản, ở cùng coverage và budget không? | Selective error, evidence validity và chi phí; ablation cho cơ chế được thêm. |
| **RQ3 — Mở rộng** | Truy vấn evidence có mục tiêu giúp giải quyết thêm bao nhiêu case so với truy vấn cố định hoặc chỉ abstain? | Số case được giải quyết đúng có cơ sở, số truy vấn và chi phí tăng thêm. |

RQ1 là câu hỏi chính trong giai đoạn khảo sát. Chỉ chốt can thiệp của RQ2 khi pilot cho thấy failure pattern cụ thể và đối chiếu được phương pháp gần. Kiểm tra thời gian/nguồn gốc và giả thuyết cạnh tranh là các ứng viên, không mặc định ghép tất cả vào một phương pháp.

Chỉ nhận RQ3 khi replay hỗ trợ truy vấn bổ sung công bằng. Nhánh stale mở rộng RQ1–RQ2 sau khi đạt điều kiện dữ liệu ở mục 2.

Nếu rule thời gian/nguồn gốc đơn giản làm tốt tương đương phương pháp phức tạp, đó là kết quả cần báo cáo.

## 5. Luồng đọc paper và phân công

**Owner** chịu trách nhiệm đọc, viết note và giải thích lại cho người còn lại. Hai người cùng đọc phần method và evaluation của Cloud-OpsBench và DiagGuard.

### Chặng 1 — Hiểu tác vụ, kiểm tra artifact và chạy một case

| Paper | Owner | Phải lấy được gì sau khi đọc? |
|---|---|---|
| **[Cloud-OpsBench][cloud]** · [Code][cloud-code] | Nguyên | Một case có gì? Agent thấy gì qua tools? Nhãn nào chỉ evaluator được thấy? JRA/ECR đo gì? Có đủ metadata cho missing/stale experiments không? |
| **[Beyond Fault Localization / DiagGuard][diag]** | Lộc | Grounder/Verifier can thiệp lúc nào? Dùng dữ liệu gì? Baseline được giữ cố định ra sao? Cần những gì để áp dụng protocol vào task của nhóm? |

**Làm song song:** Nguyên kiểm tra một artifact Cloud-OpsBench, ghi commit và ranh giới agent/evaluator, rồi chạy một replay case nếu môi trường và ngân sách cho phép. Lộc kiểm tra yêu cầu tái lập/adapt DiagGuard. Hai người đọc lướt [RCAEval][rcaeval] để hiểu các baseline ngoài LLM trước khi chọn đối chứng.

**Đầu ra:** task definition, sơ đồ episode, một trace end-to-end và chi phí; nếu chưa chạy được, ghi blocker cụ thể. Không chờ đọc hết paper mới kiểm tra dữ liệu.

### Chặng 2 — Kiểm tra gap và thiết kế nhãn

| Paper | Owner | Phải lấy được gì sau khi đọc? |
|---|---|---|
| **[TelemetrySuffBench][suff]** | Lộc | Cách chứng minh dữ liệu không phân biệt được nguyên nhân; cách chấm abstention và tránh thưởng cho việc từ chối tất cả. Phân biệt bài toán trace lỗi agent với incident Kubernetes. |
| **[JustDiag][just]** | Lộc | Tiêu chí đóng case, giữ giả thuyết cạnh tranh và xử lý xung đột. Oracle/judge có giới hạn gì? Hướng nhóm khác ở đâu? |
| **[VerifyRCA][verify]** | Nguyên | Verifier kiểm tra gì? Truy vấn được ưu tiên ra sao? Ngân sách và confidence được định nghĩa thế nào? Method/artifact có đủ để tái lập không? |
| **[Auditable Graph-Guided RCA][graph]** | Nguyên | Cách kiểm tra verdict, ảnh hưởng của injector objects và cách tách cải thiện thực khỏi shortcut của benchmark. |

**Đầu ra:** bảng so sánh theo năm câu hỏi ở mục 3.2; bản nháp annotation guide; một đoạn mô tả khác biệt đề xuất có dẫn nguồn.

### Chặng 3 — Xây khung phân tích lỗi

| Paper | Owner | Phải lấy được gì sau khi đọc? |
|---|---|---|
| **[Why Do AI Agents Systematically Fail at Cloud RCA?][kim]** | Lộc | Các pitfall liên quan trực tiếp đến chọn/diễn giải evidence; cách gán nhãn; lỗi nào do kiến trúc thay vì chỉ do prompt. |
| **[Stalled, Biased, and Confused][riddell]** · [Code][riddell-code] | Lộc | Định nghĩa evidential insufficiency, lỗi thời gian và suy luận nhân quả; cách đánh giá reasoning; giới hạn của judge. |
| **[TriFleetRCA][tri]** | Nguyên | Phạm vi lấy evidence ảnh hưởng RCA và citation thế nào; cách tách kết luận đúng khỏi dẫn chứng đúng; giới hạn thí nghiệm nhỏ. |

**Đầu ra:** codebook ngắn cho các lỗi cần phân tích trong thesis. Kế thừa taxonomy phù hợp, không tạo taxonomy mới chỉ để đổi tên.

### Chặng 4 — Bổ sung nền thực nghiệm khi cần

Nếu replay không đáp ứng điều kiện dữ liệu, Nguyên đọc chọn lọc **[AIOpsLab][lab]** · [Code][lab-code], tập trung vào workload, fault injection, reset, telemetry và giao diện agent. Đối chiếu với phần cần bổ sung cho Cloud-OpsBench.

**Đầu ra:** quyết định giữ replay, thu thêm dữ liệu hay đổi benchmark. Không cần tái tạo toàn bộ testbed của paper.

### Chỉ đọc thêm khi phục vụ một quyết định cụ thể

| Cần quyết định | Nguồn đọc |
|---|---|
| Ghi trace agent thế nào? | [AgentTelemetry][agent-telemetry] |
| Có mở rộng remediation không? | [ARBITER][arbiter], [STRATUS][stratus] |
| Cloud-OpsBench không phù hợp hoặc cần benchmark thứ hai? | [RCAEval][rcaeval], [OpenRCA][openrca], [ITBench][itbench] |
| Cần tham khảo degraded telemetry/abstention ở tác vụ khác? | [root-cause-bench][root-bench] |

## 6. Cách đọc để phục vụ thesis

### Quy trình cho mỗi paper

1. **Xác định câu hỏi cần lấy từ paper** bằng bảng ở mục 5.
2. **Đọc abstract và problem formulation:** xác định task, input/output và claim chính.
3. **Đọc method:** tìm chính xác cơ chế tạo ra cải thiện; phân biệt thuật toán, prompt, tool và dữ liệu bổ sung.
4. **Đọc experiments và limitations:** kiểm tra oracle, baseline, budget, số incident độc lập, cách chia tập và phạm vi kết luận.
5. **Xem code/data khi cần kế thừa hoặc tái lập.** Ghi khác biệt giữa bản công bố và phiên bản repository.
6. **Viết note trước khi chuyển bài.** Chỉ lần theo references liên quan trực tiếp đến câu hỏi đang thiếu.

### Mẫu note một trang

```markdown
# Tên paper
- Link, phiên bản, ngày đọc:
- Owner:
- Câu hỏi nhóm cần giải đáp từ paper:
- Task và input/output:
- Phương pháp chính và điểm khác baseline:
- Dữ liệu, oracle và thông tin agent được thấy:
- Baseline, metrics, budget và cách chia tập:
- Kết quả liên quan đến thesis, kèm điều kiện:
- Giới hạn ảnh hưởng trực tiếp đến hướng nhóm:
- Nhóm kế thừa gì? Claim nào đã có tiền lệ?
- Còn điều gì cần kiểm tra bằng code/pilot?
- Section/bảng/trang hỗ trợ các nhận định trên:
```

Một note đạt yêu cầu phải giúp người còn lại trả lời: **paper thay đổi quyết định nghiên cứu nào của nhóm?**

## 7. Pilot để kiểm tra tính khả thi

### 7.1. Bắt đầu bằng một case

1. Chọn incident có cơ chế lỗi và dữ liệu kiểm chứng rõ.
2. Chạy agent gốc trên replay, lưu tool calls, tool outputs, kết luận và chi phí.
3. Xác nhận agent không thấy fault labels, gold trajectories hoặc đối tượng injector làm lộ đáp án.
4. Tạo một điều kiện missing có kiểm soát; kiểm tra agent không lấy lại cùng dữ liệu qua tool khác.
5. Chỉ thêm stale khi có snapshot lịch sử thật và xác định được sự thay đổi liên quan.

| Điều kiện | Cách xây và kiểm tra |
|---|---|
| Chuẩn | Giữ nguyên artifact làm mốc; kiểm tra evidence cần thiết thực sự truy vấn được. |
| Missing — ưu tiên | Chọn nguồn/thuộc tính bị thiếu và lý do mô phỏng; loại bỏ nhất quán trên mọi tool liên quan, giữ phần còn lại cố định. Không mặc định mọi view bị thiếu đều không thể trả lời. |
| Stale — có điều kiện | Dùng lịch sử thật của cùng hệ thống; lưu thời gian sự kiện/thu thập và danh tính/phiên bản tài nguyên khi có. Chỉ rõ thay đổi làm evidence không còn áp dụng; tuổi dữ liệu một mình chưa đủ. |

Các thao tác tạo view là **can thiệp thực nghiệm**, không mặc định đại diện cho phân bố lỗi telemetry ngoài thực tế. Lưu manifest biến đổi để tái lập và tránh dùng tên file/metadata làm lộ nhãn.

### 7.2. Tách nguyên nhân thật khỏi tính đủ bằng chứng

Fault injection cho biết nguyên nhân thực, nhưng chưa chứng minh agent có đủ dữ liệu để nhận ra nguyên nhân đó.

| Trạng thái | Cách hiểu |
|---|---|
| Chưa truy vấn | Dữ liệu có sẵn nhưng agent chưa lấy đúng. Đây có thể là lỗi điều tra. |
| Có thể bổ sung | Hiện còn mơ hồ, nhưng có phép đọc hợp lệ trong budget giúp phân biệt. |
| Không thể phân biệt trong điều kiện thử | Các nguyên nhân khác nhau vẫn phù hợp với toàn bộ dữ liệu khả dụng đã định nghĩa. |

Hai người gán nhãn độc lập trên cùng tool view, lưu lý do và nguồn hỗ trợ. Trường hợp chưa chứng minh được thì giữ nhãn `unknown`.

Nhãn tính đủ bằng chứng chỉ có giá trị trong tập nguyên nhân và tool view đã định nghĩa cho thí nghiệm.

Cặp quan sát giống hệt nhưng nguyên nhân khác nhau có thể hỗ trợ nhãn không thể phân biệt. Phải kiểm tra toàn bộ payload được phép thấy, kể cả truy vấn bổ sung. Ý tưởng này được kế thừa từ [TelemetrySuffBench v1, §II-C và III-F][suff].

### 7.3. Các phương pháp cần so sánh

| Nhánh | Thiết lập |
|---|---|
| B0 | Agent RCA gốc, có cùng quyền trả lời hoặc chưa kết luận. |
| B1 | B0 cộng prompt self-check về evidence và bất định. |
| B2 | Phương pháp kiểm chứng gần, khởi đầu kiểm tra DiagGuard; đối chiếu thêm JustDiag trước khi chốt. Ghi rõ adapter và phần khác bản gốc. |
| B3 | Can thiệp nhắm vào failure pattern từ pilot; bắt đầu bằng một cơ chế chính, chỉ thêm thành phần khi có bằng chứng cần thiết. |

Luôn có **rule đơn giản tương ứng với cơ chế đang thử**. Ví dụ: chỉ kiểm tra thời gian/nguồn gốc khi thử provenance verification. Nếu B3 có nhiều thành phần, ablation từng phần để xác định nguồn cải thiện.

Giữ cùng model, task, tools, lịch dữ liệu khả dụng và giới hạn ngân sách. Tính chi phí của cả verifier, retry và chờ dữ liệu.

**Chốt trước khi chạy nhiều:** model/version, giới hạn tokens/tool calls/thời gian mỗi episode, số lần lặp và trần chi phí toàn pilot. Dùng chi phí đo từ case đầu để ước lượng: số incident × số view × số phương pháp × số lần lặp × chi phí trung bình/episode. Ghi riêng công gán nhãn và chi phí thu dữ liệu; nếu vượt ngân sách, giảm phạm vi trước.

### 7.4. Chỉ số cần báo cáo

| Chỉ số | Ý nghĩa |
|---|---|
| RCA accuracy/JRA | Đúng thành phần và cơ chế gây lỗi. |
| Coverage | Số case có diagnosis đúng schema và không abstain / tổng số case; diagnosis có thể đúng hoặc sai. |
| Selective error | Tỷ lệ kết luận sai trong những case được kết luận. |
| Unsupported commit | Tỷ lệ vẫn chọn nguyên nhân duy nhất trong tập đã xác minh không thể phân biệt. |
| Unnecessary abstention | Tỷ lệ chưa kết luận trong tập đã xác minh có thể trả lời với tool view/budget tương ứng. |
| Evidence validity | Citation đúng nguồn, đối tượng, thời gian và hỗ trợ claim. |
| Chi phí | Model/tool calls, tokens, latency và chi phí API của toàn episode. |

So sánh sai số **ở cùng coverage**, không chỉ so accuracy hoặc abstention riêng lẻ. Chọn score/quy tắc abstain và hiệu chỉnh ngưỡng trên development set, rồi giữ cố định khi test. Báo risk–coverage ở vùng coverage so sánh được; không ép khớp bằng cách chọn case theo nhãn test. Nếu phương pháp không hỗ trợ điều chỉnh coverage, báo operating point thực tế và nêu giới hạn so sánh.

Correctness và evidence validity được chấm riêng. Case sai schema/timeout vẫn nằm trong mẫu số tổng số case, không được tính là diagnosis hoặc abstention hợp lệ; báo tỷ lệ lỗi thực thi riêng. Nếu không có case nào được kết luận, selective error là `N/A`, không phải 0.

Chia development/test theo **incident gốc trước khi tạo các biến thể**. Các view và lần chạy lặp không được tính thành incident độc lập. Báo kết quả theo fault family và khoảng tin cậy theo incident gốc.

## 8. Kế hoạch hai tuần và điều kiện chốt đề tài

| Giai đoạn | Việc cần làm | Sản phẩm |
|---|---|---|
| Ngày 1–3 | Đọc overview và Chặng 1; kiểm tra artifact và bắt đầu một replay case. | Task definition, sơ đồ episode, trace/chi phí hoặc blocker cụ thể. |
| Ngày 4–6 | Đọc các bài gần ở Chặng 2; xây missing view và annotation guide. Kiểm tra riêng khả năng làm stale. | Related-work matrix có nguồn; view tái lập được; nhãn thử và bất đồng. |
| Ngày 7–10 | Pilot khoảng 12–20 incident nếu đạt điều kiện dữ liệu, baseline và ngân sách. | So sánh B0/B1/B2 và rule phù hợp; failure patterns và chi phí thực tế. |
| Ngày 11–14 | Phân tích kết quả; đối chiếu lại gap và RQ. | Memo chốt đề tài để trao đổi với giảng viên. |

Đây là kế hoạch **kiểm tra tính khả thi**. Pilot nhỏ giúp phát hiện lỗi protocol và ước lượng nguồn lực; chưa đủ để kết luận phương pháp tốt hơn một cách ổn định.

### Điều kiện chuyển bước (decision gates)

| Gate | Cần đạt trước khi mở rộng | Nếu chưa đạt |
|---|---|---|
| Artifact | Đọc được một case, hiểu tool view/gold labels và ghi phiên bản artifact. | Giải quyết truy cập/format hoặc chọn benchmark khác. |
| Replay | Baseline chạy end-to-end; lưu tool calls, outputs, verdict và chi phí. | Thu hẹp setup, xử lý blocker. |
| Missing | Loại bỏ evidence nhất quán qua các tools, không làm lộ nhãn. | Sửa cách tạo view trước khi chạy nhiều. |
| Annotation | Có tiêu chí answerable/ambiguous/unknown và lý do kiểm chứng được. | Thu hẹp fault family hoặc claim; giữ unknown khi chưa đủ căn cứ. |
| Research decision | Có failure pattern hợp lệ, comparator phù hợp và chi phí trong trần. | Điều chỉnh RQ hoặc đổi hướng. |

Mốc ngày giúp quản lý công việc; đạt gate mới là căn cứ mở rộng thí nghiệm. Các gates trên chưa được đánh dấu hoàn thành.

**Tiếp tục hướng đề xuất khi:**

- Có dữ liệu và nhãn đủ tin cậy để phân biệt các trạng thái thông tin.
- Có ít nhất một phương pháp gần chạy được để làm đối chứng.
- Hiện tượng cần nghiên cứu xuất hiện trong điều kiện thử hợp lệ.
- Xác định được đóng góp cụ thể của nghiên cứu đối chứng hoặc phương pháp cải thiện.

**Thu hẹp hoặc đổi hướng khi:**

- Không có lịch sử thật: bỏ claim về stale telemetry, tập trung điều kiện được dữ liệu hỗ trợ.
- Phương pháp chỉ khác prompt hoặc lặp lại bài gần: cân nhắc nghiên cứu so sánh độ bền thay vì nhận là verifier mới.
- Phát hiện shortcut chi phối kết quả: cân nhắc audit benchmark leakage nếu tạo được protocol và bằng chứng rõ.

## 9. Hồ sơ cần có trước khi triển khai lớn

- [ ] **Problem statement:** task, đối tượng nghiên cứu và lý do vấn đề đáng giải quyết.
- [ ] **Overview và walkthrough:** mỗi người giải thích được vị trí đề tài, một incident và evidence phân biệt giả thuyết.
- [ ] **Scope:** hệ thống, fault families, dữ liệu và điều kiện quan sát.
- [ ] **Related-work matrix:** khác biệt có dẫn nguồn và section cụ thể.
- [ ] **Một RQ chính:** nêu rõ đối chứng và kết quả cần đo.
- [ ] **Oracle/annotation guide:** nhãn có nguồn gốc, xử lý được bất đồng và trường hợp unknown.
- [ ] **Pilot:** baseline chạy được, chi phí đo thật, trace lỗi và kết quả sơ bộ.
- [ ] **Experimental protocol:** chia tập, budget, repetitions, metrics, quy tắc abstain và thống kê.
- [ ] **Đóng góp dự kiến:** phần nào về dữ liệu/protocol, phần nào về phương pháp; giới hạn tuyên bố.
- [ ] **Thống nhất với giảng viên:** mức đóng góp cần đạt, phạm vi RCA bắt buộc và điều kiện mở remediation.
    
[cloud]: https://arxiv.org/abs/2603.00468v2
[cloud-code]: https://github.com/LLM4Ops/Cloud-OpsBench
[diag]: https://arxiv.org/html/2608.21310v2
[suff]: https://arxiv.org/html/2608.07899v1
[just]: https://arxiv.org/html/2606.19407v1
[verify]: https://www.researchgate.net/publication/407715364_VerifyRCA_LLM-Guided_but_Evidence-Verified_Root_Cause_Analysis_for_Microservice_Backends
[graph]: https://arxiv.org/abs/2606.08590
[kim]: https://arxiv.org/abs/2602.09937v2
[riddell]: https://arxiv.org/abs/2601.22208
[riddell-code]: https://github.com/boerste/rca-llm-reasoning
[tri]: https://arxiv.org/abs/2609.23766
[lab]: https://proceedings.mlsys.org/paper_files/paper/2025/hash/d1f9e4a9f109b6e8b75ed362736f22ec-Abstract-Conference.html
[lab-code]: https://aka.ms/aiopslab-repo
[agent-telemetry]: https://2026.aiwareconf.org/details/aiware-2026-benchmark---dataset-track/10/AgentTelemetry-A-Fault-Detection-Benchmark-and-Toolkit-for-LLM-Agent-Observability
[arbiter]: https://arxiv.org/abs/2607.19182
[stratus]: https://proceedings.neurips.cc/paper_files/paper/2025/hash/47a6e9e2c3019f13ad94a0f259fe4970-Abstract-Conference.html
[rcaeval]: https://github.com/phamquiluan/RCAEval
[openrca]: https://github.com/microsoft/OpenRCA
[itbench]: https://research.ibm.com/publications/itbench-evaluating-ai-agents-across-diverse-real-world-it-automation-tasks
[root-bench]: https://github.com/edgedelta/root-cause-bench
[otel]: https://opentelemetry.io/docs/concepts/observability-primer/
[k8s-debug]: https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/
