# Báo cáo quá trình đọc paper: Cloud-OpsBench

**Paper:** Cloud-OpsBench: A Reproducible Benchmark for Agentic Root Cause Analysis in Cloud Systems (arXiv 2603.00468, preprint)

**Tiến độ:** đã đọc xong §4.5 (Failure Modes of Cloud RCA Agents), tiếp theo là §5 (Discussion).

## 2. Motivation: các gap trong đánh giá mô hình

### Gap 1: Benchmark tĩnh (§2.2.1)

1. Thiếu sự tương tác giữa model và hệ thống: benchmark tĩnh chỉ cung cấp sẵn một tập metric/log.
2. Tập metric/log tĩnh có thể dùng để chạy lại đánh giá (tái lập được).
3. Vì evidence đã được cung cấp sẵn, model không phải lựa chọn tool để xử lý, nên benchmark không kiểm tra được khả năng chọn tool đúng đắn.
4. Kết quả: việc đánh giá chỉ dựa trên tập dữ liệu đã được cung cấp.

### Gap 2: Biến thiên giữa các lần chạy live (§2.2.2)

Cho agent làm việc trên hạ tầng thực tế, lấy metric/log trực tiếp thay vì tập tĩnh, thì có hai vấn đề:

**Vấn đề 1: Khó so sánh giữa các model**
- Hai hạ tầng, môi trường ở các thời điểm và điều kiện khác nhau thì fault biểu hiện khác nhau (mức độ, thời gian, phạm vi ảnh hưởng), nên AI có thể đưa ra kết luận khác nhau.
- Vì vậy chênh lệch kết quả không thể quy hoàn toàn cho năng lực của agent, và chạy lặp chỉ ước lượng được trung bình và phương sai, không tạo được điều kiện giống nhau để so sánh từng cặp model.

**Vấn đề 2: Chi phí chuẩn bị môi trường tốn effort**
- Mỗi lần chạy phải: tạo trạng thái hệ thống sạch (clean state), warm up workload, kích hoạt và verify lỗi để monitor, để agent điều tra, rồi khôi phục môi trường trước lần chạy kế tiếp.
- Paper đang so sánh năng lực nhiều AI, nên cần môi trường lặp lại cho mọi tổ hợp fault case × model × cấu hình. Khi mở rộng quy mô ở nhiều khía cạnh, chi phí này tăng theo cấp số nhân, khiến việc so sánh quy mô lớn và lặp nhanh khi cải tiến agent trở nên khó.

**Nhận xét riêng của người đọc (không phải của paper):** kết luận của AI trên hạ tầng thực tế có thể có giá trị hơn kết luận trên tập tĩnh. Paper chỉ thừa nhận live environment có giá trị ở chỗ kiểm tra độ bền trước sự bất định của môi trường thật.

### Gap 3: Chỉ đánh giá theo kết quả cuối (§2.2.3)

**Vấn đề:** các RCA benchmark hiện tại chủ yếu chấm bằng điểm số theo các phương pháp như top-k accuracy, precision, recall, F1, nên không đánh giá được quá trình AI thu thập dữ liệu để có được kết quả đó. Các metric này vẫn cần thiết để đo độ đúng của chẩn đoán.

**Ví dụ:** hai AI agent đưa ra cùng một đáp án nhưng theo hai cách khác nhau:
- Agent A thu thập danh sách observation đúng với tình trạng của hệ thống, nối được triệu chứng với root cause.
- Agent B đoán bừa (unsupported guess).
- Hai bên nhận điểm như nhau, dù quá trình hoàn toàn khác nhau.

**Trường hợp ngược lại:** agent điều tra có cơ sở nhưng kết luận cuối sai thì không phân biệt được với agent không điều tra gì (cả hai cùng bị tính là sai).

**Ý của tác giả:** việc đánh giá không nên chỉ dựa vào kết luận cuối của AI. Cần bổ sung (complement) thêm quá trình AI lấy số liệu quan sát, bên cạnh độ đúng của kết luận.
- "Quá trình" được đo trên các lần gọi tool và observation nhận được (observable tool-mediated investigation), không phải lập luận do agent tự thuật (self-reported reasoning).
- Ba tiêu chí của quá trình: completeness (đủ bằng chứng), causal coherence (đúng thứ tự nhân quả), efficiency (hiệu quả).

**Lý do cốt lõi (construct validity):** khả năng benchmark tuyên bố đo gồm chọn hành động chẩn đoán, thu thập observation và lập luận nhân quả, nhưng metric chỉ đo dự đoán cuối.

## 2.3 Evaluation Requirements: yêu cầu đối với benchmark (§2.3)

Từ các gap ở trên, paper đưa ra 3 yêu cầu đối với benchmark đánh giá agentic RCA.

### R1: System-facing evidence acquisition
- AI phải tương tác với hệ thống thông qua tools và tự thu thập dữ liệu.
- Agent tự chọn cả tool lẫn target thông qua một tập diagnostic interface chuẩn, nhận về các observation đã được ghi lại (captured) từ hệ thống, và điều chỉnh hành động tiếp theo dựa trên kết quả trả về.

### R2: Matched and reusable incident evidence
- Nhiều model AI cùng điều tra một sự cố trên một tập quan sát chung, thay vì phải deploy và setup lại hạ tầng có điều kiện lỗi cho từng model.
- Điều kiện: cùng một bằng chứng sẵn có và cơ chế truy vấn–phản hồi mang tính xác định (deterministic query-response mapping, cùng truy vấn thì cùng kết quả), không cần redeploy hay inject lại lỗi cho mỗi lần đánh giá. Nhờ vậy các model được so sánh trong cùng điều kiện.

### R3: Tool-sequence-neutral process evaluation
- Ngoài kết quả cuối cùng, benchmark phải truy cập được bằng chứng và thứ tự thực hiện của model, nên quá trình thực hiện của AI cũng được đánh giá song song với kết luận cuối cùng.
- Ba khía cạnh được đánh giá: evidential completeness, causal order, efficiency.
- Không áp đặt một chuỗi lệnh chuẩn: "thứ tự" là thứ tự nhân quả của các fact đã thiết lập, không phải thứ tự gọi lệnh. Các fact tương đương bằng chứng và các thứ tự điều tra độc lập nhận điểm như nhau.

**Nhận xét riêng của người đọc (không phải của paper):** R1, R2, R3 tương ứng lần lượt với Gap 1, Gap 2, Gap 3. Paper chỉ nói các gap "yield" ba yêu cầu này, và §3 ghép mỗi yêu cầu với một thành phần của Cloud-OpsBench (R1: snapshot-backed diagnostic interfaces; R2: replay cùng một evidence; R3: milestone evidence graph).

## 3. Cloud-OpsBench (§3)

### 3.1 Design Philosophy và Task Formulation (§3.1)

**Ý tưởng thiết kế: State Snapshot paradigm**
- Thực nghiệm trên cluster thật thì sát thực tế (real), nhưng khó tái lập và tốn chi phí khi mở rộng quy mô (Gap 2).
- Làm trên tập static thì thiếu tương tác giữa agent và hệ thống (Gap 1).
- Vì vậy tác giả tạo sẵn các bản snapshot của hệ thống đã được inject fault. Khi thực nghiệm, snapshot được phát lại như một môi trường giả lập (mocked operational interface), và AI agent được đánh giá trên đó.
- Snapshot gồm trạng thái hệ thống sau khi verify (resource, config, topology, trạng thái component) và event, log, metric theo thời gian trong khoảng từ lúc xác nhận hệ thống khỏe đến lúc lỗi biểu hiện.
- Thiết kế này không loại bỏ nhiễu có sẵn trong dữ liệu sự cố gốc, mà chỉ loại bỏ sự không xác định của môi trường lúc đánh giá (evaluation-time environmental nondeterminism): dữ liệu đến từ lỗi thật, còn không gian quan sát được cố định để so sánh các agent.

**Công thức hóa một lần đánh giá (episode)**

`Φ : ⟨U, S⟩ → ⟨T, R̂⟩`

| Ký hiệu | Ý nghĩa |
|---|---|
| U | User query: mô tả triệu chứng mà agent nhận được |
| S | Snapshot (trạng thái hệ thống đã đóng băng); agent không thấy trực tiếp, chỉ truy cập qua tool |
| T | Quá trình thực tế của agent: danh sách các cặp (tool đã gọi, observation trả về) |
| R̂ | Kết luận cuối của agent: (component, fault type) |

**Cách chấm**
- R\* = (component thật, fault type thật) là đáp án kỳ vọng về kết quả. So R̂ với R\* để chấm kết luận cuối.
- D\* = diagnostic evidence graph là quá trình kỳ vọng, gồm các trạng thái chẩn đoán trung gian cần có để biện minh cho R\* (xây ở §3.3.3). So T với D\* để chấm quá trình thực tế của agent.

### 3.2 Phase 1: Fault Knowledge Base Construction (§3.2)

Phase 1 xây một nền tri thức về fault, làm đầu vào cho Phase 2. Output là **fault knowledge base**: mỗi fault type có một entry có cấu trúc.

**Quy trình**
1. **Nguồn tri thức (3 nguồn):**
   - Tài liệu chính thức của Kubernetes, cho các lỗi cấu hình theo đặc tả (ví dụ selector của Service sai).
   - Cộng đồng developer (Stack Overflow, KodeKloud Notes), cho các lỗi vận hành thực tế.
   - Tài liệu học thuật, cho các failure mode kinh điển.
2. **LLM tổng hợp:** dùng Gemini 3 Pro (few-shot prompting) để trích xuất thành dữ liệu có cấu trúc mô tả từng loại fault.
3. **Kiểm tra trước khi sang Phase 2 (hai lớp):**
   - LLM consistency check: tìm chỗ thiếu, sai định dạng hoặc mâu thuẫn kỹ thuật, và chỉnh lại mô tả.
   - Reviewer có kinh nghiệm vận hành cloud-native: đánh giá logic nhân quả của fault và tính khả thi kỹ thuật của template.

**Mỗi entry gồm hai phần**
- **Metadata:** tên fault, cơ chế gây lỗi, trạng thái lỗi cục bộ dự kiến, các biểu hiện có thể thấy ở tầng trên.
- **Reproduction template (có tham số):** điều kiện tiên quyết, thao tác gây lỗi, logic kích hoạt, viết bằng biến có kiểu thay vì tên resource cụ thể. Ví dụ template *service selector mismatch* yêu cầu selector của Service khác label của các Pod backend, còn namespace, Service, Pod, label key và value để trống cho Phase 2 điền.

**Entry ở Phase 1 mới chỉ là ứng viên, chưa được coi là hợp lệ.** Validation thật diễn ra ở Phase 2 trên cluster. Một fault type chỉ được giữ trong taxonomy cuối khi có ít nhất một case cụ thể chạy thật và vượt kiểm chứng, nhằm tránh coi một template do LLM trích xuất là hợp lệ khi chưa được thử.

**Kết quả:** 57 fault type thuộc 8 nhóm (Table 2), mỗi nhóm được gán nhãn độ khó (Easy/Medium/Hard) lúc xây dựng, dựa trên mức độ dễ quan sát triệu chứng và khoảng cách chẩn đoán. Mọi case trong một nhóm dùng chung nhãn.

**8 nhóm fault (Table 2)**

| Nhóm | Mô tả | Số fault type | Độ khó | Số case |
|---|---|---|---|---|
| Admission Control | Request bị API server từ chối do vượt quota hoặc thiếu quyền | 6 | Medium | 58 |
| Scheduling | Pod kẹt ở Pending do không thỏa ràng buộc node hoặc affinity | 12 | Easy | 164 |
| Startup | Tạo Pod thất bại | 5 | Easy | 86 |
| Runtime | Ứng dụng crash hoặc fail health probe khi đang chạy | 12 | Easy | 141 |
| Service Routing | Lỗi định tuyến traffic giữa các thành phần nội bộ | 6 | Medium | 91 |
| Performance | Suy giảm hiệu năng do quá tải hoặc mất gói mạng | 4 | Hard | 76 |
| Infrastructure | Sự cố ở control plane hoặc thành phần nền của cluster | 4 | Medium | 40 |
| Application Code Defect | Lỗi code ở logic nghiệp vụ chính | 8 | Hard | 98 |
| **Tổng** | | **57** | | **754** |

Ghi chú phần "hiểu là" bên dưới: paper chỉ liệt kê tên fault type trong Table 2, không giải thích từng cái. Phần giải thích là người đọc suy ra từ tên và kiến thức Kubernetes. Đã điền đủ 8 nhóm. Mục có dấu (?) là phần suy đoán từ tên, chưa chắc, cần kiểm tra lại.

**Fault type: hiểu là**

*Admission Control*
- `NamespaceCPUQuotaExceeded`: tổng CPU request trong namespace vượt quota CPU
- `NamespaceMemoryQuotaExceeded`: vượt quota memory
- `NamespacePodQuotaExceeded`: số Pod vượt quota số Pod
- `NamespaceServiceQuotaExceeded`: số Service vượt quota số Service
- `NamespaceStorageQuotaExceeded`: dung lượng storage vượt quota
- `MissingServiceAccount`: không phải quota mà là lỗi quyền, Pod tham chiếu một ServiceAccount không tồn tại nên bị từ chối

*Scheduling*
- `NodeCordonMismatch` (?): node bị cordon (đánh dấu không nhận Pod mới) nên Pod không được xếp vào
- `NodeAffinityMismatch`: nodeAffinity của Pod không khớp label của node nào
- `NodeSelectorMismatch`: nodeSelector của Pod không khớp label của node nào
- `PodAntiAffinityConflict`: luật anti-affinity khiến không còn node nào thỏa để đặt Pod
- `TaintTolerationMismatch`: node có taint mà Pod không có toleration tương ứng
- `CPUCapacityMismatch`: CPU request của Pod lớn hơn CPU còn trống trên node
- `MemoryCapacityMismatch`: memory request của Pod lớn hơn memory còn trống trên node
- `PVBindingOccupied` (?): PersistentVolume cần bind đã bị PVC khác chiếm
- `PVCSelectorMismatch`: selector của PVC không khớp label của PV nào
- `PVCStorageClassMismatch`: storageClass PVC yêu cầu không khớp với PV/StorageClass có sẵn
- `PVCCapacityMismatch`: dung lượng PVC yêu cầu lớn hơn dung lượng PV có sẵn
- `PVCAccessModeMismatch`: access mode PVC yêu cầu không khớp access mode của PV

*Startup*
- `VolumeMountPermissionDenied`: Pod mount volume nhưng bị từ chối quyền truy cập
- `MissingSecretBinding`: Pod tham chiếu một Secret không tồn tại nên container không khởi tạo được
- `IncorrectImageReference`: tên hoặc tag image sai nên không pull được image
- `ImageRegistryDNSFailure`: không phân giải được DNS của registry nên không pull được image
- `MissingImagePullSecret`: registry riêng (private) nhưng Pod thiếu imagePullSecret

*Runtime*
- `OOMKilled`: container dùng vượt memory limit nên bị kill
- `LivenessProbeIncorrectProtocol`: liveness probe cấu hình sai protocol nên probe fail và container bị restart
- `LivenessProbeIncorrectPort`: liveness probe trỏ sai port
- `LivenessProbeIncorrectTiming` (?): liveness probe cấu hình timing (delay, timeout, period) không phù hợp nên bị kill sớm
- `ReadinessProbeIncorrectProtocol`: readiness probe sai protocol nên Pod không Ready, không nhận traffic
- `ReadinessProbeIncorrectPort`: readiness probe trỏ sai port
- `ServiceSidecarPortConflict` (?): sidecar xung đột port với container ứng dụng
- `MysqlInvalidCredentials`: ứng dụng dùng sai user hoặc mật khẩu MySQL
- `MysqlInvalidPort`: ứng dụng kết nối sai port MySQL
- `DBReadOnly`: database ở chế độ chỉ đọc nên thao tác ghi thất bại
- `DBConnectionExhaustion`: hết số connection tới database
- `DeploymentZeroReplicas`: Deployment bị scale về 0 replica nên không còn Pod nào chạy

*Service Routing*
- `ServiceSelectorMismatch`: selector của Service không khớp label của Pod nên Service không có endpoint
- `ServicePortMappingMismatch`: port hoặc targetPort của Service không khớp port của container
- `ServiceProtocolMismatch`: protocol khai báo ở Service không khớp với thực tế
- `ServiceEnvVarAddressMismatch` (?): biến môi trường chứa địa chỉ của service khác trỏ sai
- `GatewayMisroute` (?): gateway định tuyến traffic sai đích
- `ServiceDNSResolutionFailure`: không phân giải được tên Service qua DNS

*Performance*
- `PodCPUOverload`: Pod bị quá tải CPU
- `PodNetworkDelay`: độ trễ mạng tăng ở mức Pod
- `NodeNetworkDelay`: độ trễ mạng tăng ở mức node
- `NodeNetworkPacketLoss`: mất gói tin mạng ở mức node

*Infrastructure*
- `ContainerdUnavailable`: container runtime containerd trên node ngừng hoạt động
- `KubeletUnavailable`: kubelet trên node ngừng hoạt động
- `KubeProxyUnavailable`: kube-proxy ngừng hoạt động nên routing của Service bị lỗi
- `KubeSchedulerUnavailable`: scheduler ngừng hoạt động nên Pod mới không được xếp vào node

*Application Code Defect*
- `CodeMissingParameter`: code thiếu một tham số cần thiết
- `CodeBusyLoop`: vòng lặp bận làm CPU tăng cao
- `CodeExcessiveFileReads`: đọc file quá mức
- `CodeWrongReturn`: hàm trả về giá trị sai
- `CodeExcessiveFileWrites`: ghi file quá mức
- `CodeWrongArgumentOrder`: truyền sai thứ tự đối số
- `CodeArtificialDelay`: chèn độ trễ nhân tạo vào code
- `CodeMemoryLeak`: rò rỉ bộ nhớ

Ví dụ fault type: Scheduling gồm TaintTolerationMismatch, PVCSelectorMismatch; Service Routing gồm ServiceSelectorMismatch, ServicePortMappingMismatch; Infrastructure gồm KubeletUnavailable, KubeProxyUnavailable; Application Code Defect gồm CodeBusyLoop, CodeMemoryLeak. Danh sách đầy đủ ở Table 2 của paper.

**Quan hệ nhóm, fault type và case**
- Một nhóm có nhiều fault type, một fault type có nhiều case. Ví dụ nhóm Admission Control có 6 fault type và 58 case, tức là 58 case là tổng của cả 6 fault type, trung bình khoảng 9–10 case mỗi fault type.
- Fault type là một entry (template) trong knowledge base ở Phase 1. Case là một lần áp dụng template đó lên một mục tiêu cụ thể trên cluster, kèm snapshot và nhãn, và là đơn vị mà agent được đánh giá.
- Template để trống tên resource. Ở Phase 2, Generator tạo fault plan riêng cho từng case từ entry và workload đích, chọn resource cụ thể và tham số vận hành. Vì vậy cùng một fault type có thể cho nhiều case, tùy ứng dụng đích (OnlineBoutique hoặc TrainTicket), component bị inject và tham số.
- Table 2 chỉ cho số case theo nhóm, không cho theo từng fault type, nên chưa biết số case của mỗi fault type có đều nhau không. Việc các case cùng fault type khác nhau ở những yếu tố nào là suy ra từ §3.3.1, chưa thấy paper nêu rõ, cần kiểm tra thêm ở §3.3 hoặc appendix.

### 3.3 Phase 2: Automated Fault Case Generation (§3.3)

**Testbed: hạ tầng**
- Cluster Kubernetes v1.31, 4 node, triển khai trên Huawei Cloud ECS.
- Hai ứng dụng microservice làm workload: OnlineBoutique (11 service) và TrainTicket (41 service, có các service dùng database).
- Quan sát (observability): Prometheus và Istio cho metric, native API của Kubernetes cho log và trạng thái object.
- Tạo traffic người dùng: Locust.
- Giả lập lỗi hạ tầng: ChaosBlade, cho các nhiễu loạn ở mức hạ tầng như network loss và disk pressure. Các lỗi cấu hình thì dùng các lệnh `kubectl` đơn lẻ (atomic).

**Testbed: phần code**
- Với nhóm fault lỗi code, tác giả sửa chính code của service bằng các mẫu bug có chủ đích như thiếu giá trị tham số, hàm trả về sai giá trị, xử lý exception sai (theo ref [51] trong paper).
- Mỗi bản sửa được đóng gói thành một service image có thể deploy ngay lên Kubernetes.

**Lý do chọn Kubernetes:** Kubernetes có control plane phân tán phức tạp để inject fault và có kho tài liệu chuẩn hóa, nên kiểm tra được khả năng lập luận dựa trên tri thức, khác với benchmark xây trên hệ thống độc quyền hoặc ít người biết.

#### 3.3.1 Fault Injection Loop (§3.3.1)

Quy trình tạo case là một vòng lặp gồm 3 agent: Generator, Executor, Verifier.

**Generator Agent (Gemini 3 Pro)**
- Đầu vào: một entry trong fault knowledge base (kết quả Phase 1) và workload đích (OnlineBoutique hoặc TrainTicket).
- Đầu ra: fault plan riêng cho từng case. Mỗi plan gồm:
  - Required pre-injection state: trạng thái hệ thống phải có trước khi inject (ví dụ Service `checkout` tồn tại, các Pod đang chạy bình thường).
  - Resource selectors: nhắm vào resource nào (ví dụ Service `checkout` ở namespace `default`).
  - Operational parameters: giá trị cụ thể của thao tác (ví dụ đổi selector thành giá trị sai).
  - Ordered injection operations: các bước inject theo thứ tự.
  - Runtime validation assertions: điều kiện kiểm tra sau khi inject để biết lỗi đã thật sự xảy ra. Gồm 3 loại: mechanism activation (điều kiện gây lỗi đang hoạt động ở đúng component), expected local failure state (trạng thái lỗi cục bộ xuất hiện, ví dụ Service không có endpoint), upper-layer manifestation (biểu hiện ở tầng trên nếu có, ví dụ request trả 503).

**Executor Agent**
- Trước mỗi lần inject: khôi phục testbed về trạng thái deploy sạch (clean state), gán selector vào trạng thái cluster vừa khôi phục, thiết lập điều kiện tiên quyết, xác nhận hệ thống khỏe (với case hướng service thì phải có một request end-to-end thành công).
- Sau đó mới apply fault plan.

**Verifier Agent**
- Đánh giá các validation assertion dựa trên trạng thái cluster sau khi inject: object state, event, log, metric, kết quả connectivity.
- Chỉ chấp nhận khi đủ 3 điều kiện: fault-inducing condition đang hoạt động ở đúng component, expected local failure state có mặt, và upper-layer manifestation (nếu có chỉ định) được quan sát thấy. Khi đó target và điều kiện lỗi đã verify được ghi vào verified fault plan.

**Vì sao cần verify**
- Cơ chế tự phục hồi của Kubernetes có thể che mất fault vừa inject. Ví dụ trong paper: Pod được chuyển sang node khác nên né được lỗi scheduling do taint.
- Nếu không verify, benchmark sẽ có case mà lỗi thực tế đã tự biến mất, agent không thể chẩn đoán.

**Vòng phản hồi**
- Nếu verify thất bại, Verifier so sánh trạng thái runtime với cơ chế lỗi dự kiến rồi trả phản hồi có cấu trúc cho Generator (thiếu điều kiện tiên quyết, cường độ chưa đủ, hoặc có đường phục hồi ngoài ý muốn).
- Generator được sửa selector hoặc tham số vận hành, nhưng giữ nguyên cơ chế lỗi và tiêu chí kiểm tra của entry. Quy trình clean deploy, inject, verify lặp lại.
- Tối đa 3 lần sửa, quá 3 lần mà vẫn fail thì loại case.

**Sau khi verify thành công**
- Case được đưa sang bước tạo snapshot (§3.3.2).
- User query U được tạo từ biểu hiện quan sát được, không để lộ component bị lỗi, cơ chế lỗi và các thông tin chỉ dùng lúc xây dựng.
- Verified fault plan được giữ làm bằng chứng gốc (provenance), không đưa cho agent đánh giá và không được chấp nhận làm bằng chứng chẩn đoán.

**Kết quả:** 800 fault plan ứng viên được tạo, 46 plan bị loại vì không biểu hiện triệu chứng ổn định hoặc không chẩn đoán được (stable or diagnosable symptoms).

#### 3.3.2 State Snapshots (§3.3.2)

Sau khi một fault plan được verify, hệ thống chạy trước (pre-execute) bộ tool chẩn đoán T1–T12 trên sự cố đã verify. Mỗi tool trả về response phản ánh trạng thái cụm tại thời điểm đó, và toàn bộ response được lưu vào một kho JSON. Kho JSON này là snapshot, đóng vai trò lớp lưu trữ cho việc replay có tính xác định (deterministic replay).

**Mục đích:** khi đánh giá các model về sau, model nào gọi tool cũng nhận về cùng một response, tương ứng với cùng một trạng thái hệ thống.

**Danh sách 12 tool (Table 3)**

| Tool | Trả về |
|---|---|
| T1. `GetResources(type, namespace, name, flags)` | Danh sách resource hoặc object được chọn, kèm status, metadata và thuộc tính mở rộng |
| T2. `DescribeResource(type, name, namespace)` | Chi tiết runtime của một object Kubernetes: state, conditions, events |
| T3. `GetAppYAML(service_name)` | File YAML cấu hình Deployment của service |
| T4. `GetServiceDependencies(service_name)` | Đồ thị phụ thuộc của service, gốc là service đích |
| T5. `GetRecentLogs(service_name, namespace)` | Log gần đây của service để xem lỗi runtime |
| T6. `CheckConnectivity(namespace, svc_name, port)` | Kết quả kiểm tra TCP reachability tới endpoint của service |
| T7. `GetClusterConfiguration()` | Thông tin các node của cluster: tài nguyên, label, taint, trạng thái |
| T8. `GetAlerts()` | Cảnh báo bất thường về metric, sinh bởi bộ phát hiện theo ngưỡng |
| T9. `GetErrorLogs(service_name, namespace)` | Tóm tắt các dòng log khớp mẫu error, exception hoặc failure |
| T10. `CheckNodeServiceStatus(node_name, component_name)` | Trạng thái hoạt động của thành phần ở mức node hoặc control plane |
| T11. `ListCodeFiles(app_name)` | Các file source có sẵn của service, kèm mô tả ngắn |
| T12. `GetSourceCode(app_name, file_path)` | Nội dung source code của một file đã chọn |

**Bốn kênh bằng chứng của snapshot**
1. Trạng thái resource và event: T1, T2, lấy trên các object Kubernetes trong namespace đích.
2. Topology ứng dụng và telemetry: cấu hình tĩnh (T3), đồ thị phụ thuộc (T4), log (T5, T9), kết quả reachability (T6).
3. Ngữ cảnh mức cluster: sức khỏe node và component (T7, T10), metric được chuyển thành cảnh báo có cấu trúc (T8).
4. Bằng chứng từ source code: T11, T12, dùng cho các lỗi mức ứng dụng.

**Phạm vi dữ liệu theo thời gian**
- Snapshot chụp trạng thái hệ thống sau khi verify, kèm event, log, metric có timestamp trong khoảng của riêng case đó. Khoảng này từ lúc xác nhận hệ thống khỏe (baseline) đến lúc xác nhận lỗi biểu hiện (manifestation).
- Snapshot builder ghi lại hai mốc thời gian này và dùng chúng làm biên khi truy xuất dữ liệu theo thời gian.

**Cách giao diện replay xử lý truy vấn**
- Replay không phải simulator viết tay: với truy vấn được hỗ trợ, response là output thật chụp từ sự cố đã verify trên cluster thật.
- Trước khi tra kho, giao diện kiểm tra request theo schema của tool và chuẩn hóa các tham số quan trọng, để các request tương đương cùng trỏ về một mục trong kho.
- Truy vấn vào object không tồn tại: trả response lỗi đã chụp, ví dụ `Not Found`.
- Truy vấn hợp lệ nhưng ngoài phạm vi đã chạy trước: trả `UnsupportedQuery`, và không được hiểu là bằng chứng về trạng thái hệ thống.

**Phạm vi và giới hạn**
- Phạm vi của kho là hữu hạn: chỉ gồm response cho các truy vấn đã được chạy trước, lấy từ các object, namespace, service endpoint, node và source file có trong case. Không phải mọi truy vấn có thể có đều có response.
- Agent vẫn phải tự chọn tool và tham số, không có danh sách truy vấn hay chuỗi lệnh định sẵn.
- Quy mô: trung bình 599 response mỗi case (OnlineBoutique, 3,46 MiB) và 1.708 response mỗi case (TrainTicket, 8,75 MiB).
- Một case chỉ được giữ lại khi bước annotation xác nhận mọi diagnostic fact cần thiết đều quan sát được qua giao diện snapshot.

**Liên hệ với các gap:** cơ chế này giải quyết Gap 1 (agent điều tra qua tool hướng hệ thống thay vì đọc bản dump telemetry) và Gap 2 (các agent khác nhau gặp cùng một bằng chứng và cùng một ánh xạ truy vấn–phản hồi).

#### 3.3.3 Ground-Truth Annotation (§3.3.3)

Mỗi case đã verify có hai loại nhãn chuẩn, ký hiệu G* = ⟨R*, D*⟩. Nhãn được tạo lúc xây benchmark, trước khi có bất kỳ agent nào chạy, và dựa trên dữ liệu của hệ thống (chuỗi nhân quả đã verify và kho response của snapshot), không dựa trên log gọi tool của agent.

```
G* = ⟨R*, D*⟩                       bộ đáp án chuẩn của 1 case
│
├── R*  (outcome label)             đáp án kết quả  → so với R̂ của agent
│   ├── C*   component bị lỗi
│   └── F*   fault type
│
└── D*  (process label)             đồ thị bằng chứng → so với T của agent
    ├── M*   milestone              1 sự thật chẩn đoán nguyên tử
    ├── K*   nhóm milestone
    │   ├── nhóm 1 phần tử          bắt buộc phải biết
    │   └── nhóm nhiều phần tử      thay thế nhau, chỉ cần biết 1
    ├── ≺*   thứ tự nhân quả giữa các nhóm (đồ thị có hướng)
    └── Q*   evidence bundle        cách chứng minh 1 milestone
        └── q   clause              tool + tham số + điều kiện trên response
            ├── bundle 1 clause     q1
            └── bundle nhiều clause q2 ∧ q3 (cần đủ cả hai)
```

**Outcome label R\***
- R* = ⟨C*, F*⟩: component bị lỗi và fault type thật.
- Lấy trực tiếp từ fault plan đã verify ở §3.3.1.

**Process label D\***
- Lý do cần: chỉ có R* thì không phân biệt được chẩn đoán có bằng chứng với đoán bừa, nên cần nhãn mô tả các sự thật chẩn đoán cần có để biện minh cho R*.
- Không dùng một chuỗi lệnh chuẩn duy nhất (gold tool sequence), vì như vậy gắn đánh giá vào workflow mà người gán nhãn ưa thích và phạt những agent đi đường khác nhưng vẫn đến cùng chẩn đoán. Thay vào đó chấm các sự thật đã thiết lập và quan hệ phụ thuộc giữa chúng. Đây là cách đáp ứng R3 và giải quyết Gap 3.
- D* được biểu diễn là một đồ thị bằng chứng (diagnostic evidence graph) D* = ⟨M*, K*, ≺*, Q*⟩:
  - **Milestone (M\*):** một sự thật chẩn đoán nguyên tử, không phải quan sát thô, giả thuyết tạm thời hay nhánh có điều kiện. Ví dụ "PVC đang Pending" là milestone, còn "xem PVC" là hành động gọi tool nên không được gán nhãn. Một mệnh đề chỉ được tách ra khi các phần của nó có thể được thiết lập độc lập hoặc dẫn tới các phụ thuộc khác nhau.
  - **Nhóm milestone (K\*):** phân hoạch các milestone thành nhóm. Nhóm một phần tử là sự thật bắt buộc. Nhóm nhiều phần tử gồm các sự thật có thể thay thế nhau, cùng tạo ra một bước tiến chẩn đoán. Quá trình biện minh hoàn tất khi mỗi nhóm có ít nhất một milestone được thiết lập.
  - **Quan hệ phụ thuộc (≺\*):** đồ thị có hướng không chu trình, ghi các điều kiện tiên quyết về bằng chứng giữa các nhóm. Bao đóng bắc cầu của nó xác định thứ tự chẩn đoán bắt buộc. Các nhóm không nối với nhau bằng đường có hướng thì không có thứ tự.
  - **Evidence bundle (Q\*(m)):** các cách chấp nhận được để thiết lập milestone m. Mỗi evidence clause q gồm một tool, các tham số chấp nhận được, và một điều kiện (predicate) trên response đã chuẩn hóa. Một bundle được thỏa khi mọi clause của nó đã được quan sát. Milestone được thiết lập khi ít nhất một bundle được thỏa.
- Ví dụ của paper: `U → M1 → (M2 ∨ M3) → M4 → (M5, M6) → R*`. Khi đó K* gồm {M1}, {M2, M3}, {M4}, {M5}, {M6}. Nhóm {M2, M3} hoàn thành khi có M2 hoặc M3, và là điều kiện tiên quyết của {M4}. M5 và M6 cùng phụ thuộc M4 nhưng không phụ thuộc nhau nên làm thứ tự nào cũng được.
- Phân biệt hai tầng "hoặc": K* là các sự thật thay thế nhau, còn Q*(m) là các cách chứng minh thay thế nhau cho cùng một sự thật. Ví dụ Q*(m) = {q1}, {q2, q3} nghĩa là q1 ∨ (q2 ∧ q3): m được thiết lập bằng q1 một mình, hoặc bằng q2 cùng q3.
- Nhờ đó nhãn cho phép nhiều sự thật, nguồn bằng chứng và thứ tự điều tra độc lập, không áp đặt một chuỗi lệnh chuẩn.

**Quy trình gán nhãn**
- Người gán nhãn: 3 thành viên của nhóm benchmark, mỗi người có ít nhất 3 năm kinh nghiệm chẩn đoán lỗi cloud.
- Với mỗi case, bắt đầu từ chuỗi nhân quả đã xác lập lúc verify (§3.3.1), nối cơ chế lỗi đã kích hoạt với triệu chứng trong user query.
- Đi ngược chuỗi này từ triệu chứng về cơ chế lỗi, chỉ giữ các sự thật nguyên tử, quan sát được trong snapshot và cần thiết cho chẩn đoán làm milestone.
- Chia milestone thành các nhóm K*. Hai milestone chỉ được xếp cùng nhóm khi mỗi cái độc lập thỏa cùng một phụ thuộc phía sau, với cùng các nhóm tiên quyết. Quan hệ giữa các nhóm cho ra ≺*.
- Để dựng Q*(m): duyệt toàn bộ kho response của case (kết quả của các tool chạy trước, với các tham số hợp lệ đã liệt kê). Mỗi clause trỏ tới một mục trong kho và khớp một thuộc tính của response đã chuẩn hóa, thuộc tính đó thiết lập sự thật mà m biểu diễn. Response tự đủ thì tạo bundle một clause, các response bổ trợ nhau thì gộp thành bundle chung.

**Kiểm tra nhãn (validation)**
- Tự động: phát lại mỗi annotation trên snapshot đóng băng để kiểm tra cấu trúc đồ thị, tính nhất quán tham số theo case, mỗi clause thực thi được, và bằng chứng thỏa được.
- Hai auditor có kinh nghiệm vận hành Kubernetes và chẩn đoán lỗi cloud review độc lập từng annotation theo các tiêu chí: đủ nhân quả, milestone nguyên tử và không dư thừa, phụ thuộc đúng, không thiên vị đường đi nào giữa các lựa chọn thay thế. Họ xem U, R*, D* và snapshot, nhưng không được xem fault plan dùng lúc xây dựng.
- Bất đồng và đề xuất sửa được một chuyên gia cấp cao về cloud-native phân xử.
- Kết quả: 9,4% đồ thị được sửa và replay-validate lại, phần còn lại được chấp nhận nguyên trạng. Trung bình mỗi đồ thị có 3,3 milestone và mỗi milestone có 2,7 evidence bundle.

**Nhận xét của người đọc (không phải của paper): tính khách quan và chủ quan của việc gán nhãn**

Phần khách quan, có căn cứ:
- R* lấy từ fault plan đã verify, không cần phán đoán.
- Chuỗi nhân quả gốc (từ cơ chế lỗi đến triệu chứng) đã được xác lập lúc verify trên cluster thật.
- Mỗi evidence clause trỏ tới một mục có thật trong kho response, và replay kiểm tra được bằng chứng đó đạt được.

Phần chủ quan:
- Chuỗi nhân quả cho biết lỗi xảy ra thế nào, còn D* phải trả lời agent cần biết những gì để tin vào kết luận. Bước chuyển này phụ thuộc phán đoán của người gán nhãn: sự thật nào là cần thiết, cắt thế nào là nguyên tử, hai sự thật nào thay thế nhau, thứ tự phụ thuộc ra sao.
- Replay chỉ kiểm tra được bằng chứng đạt được, không kiểm tra được nhãn có đầy đủ và đúng mức cần thiết hay không.
- Biện pháp của paper: hai auditor độc lập bị che fault plan và một người phân xử. Con số 9,4% đồ thị bị sửa cho thấy lỗi hoặc bất đồng là có thật.
- Chưa thấy chỉ số đồng thuận giữa người gán nhãn trong phần đã đọc. Người gán nhãn đều thuộc nhóm tác giả, paper không nói rõ auditor có độc lập với họ hay không.

Chi tiết xem `finding/CloudOpsBench_FINDING.md`.

## 4. Evaluation (§4)

**Ba câu hỏi nghiên cứu**
- RQ1 (Outcome Effectiveness): agent xác định đúng component bị lỗi và fault type đến mức nào.
- RQ2 (Evidence Process): agent có thu thập đủ bằng chứng cần thiết và đúng thứ tự nhân quả không.
- RQ3 (Experience Reuse): agent có được lợi khi dùng kinh nghiệm chẩn đoán từ các case trước không.
- Ngoài ra phân tích các kiểu lỗi (failure modes) lặp lại trong những chẩn đoán sai.

### 4.1 Experimental Setup (§4.1)

**Agent và cấu hình**
- Agent nền do tác giả tự viết theo kiểu ReAct, dùng Pydantic để kiểm tra chặt tham số tool. Ghi được toàn bộ trace gồm reasoning và các lần gọi tool.
- Để tái lập được: temperature = 0, tối đa 20 bước tương tác, mặc định tắt extended thinking.

**10 model**
- Proprietary: GPT-5, Claude-Sonnet-4, Gemini-2.5-Pro, Qwen3.5-Plus, Gemini-2.5-Flash.
- Open-weight: DeepSeek-V4-Flash, Qwen3-235B-A22B, Qwen3.5-27B, Qwen3-14B, Qwen3-8B.

**Phân tầng theo độ khó**
- Mỗi case lấy nhãn Easy/Medium/Hard của nhóm fault ở Table 2, không gán lại theo điểm của agent.
- Trong mỗi tổ hợp hệ thống × mức độ khó: tính metric cho từng model, rồi lấy trung bình đều trên 10 model.

#### 4.1.1 Evaluation Metrics (§4.1.1)

```
Metrics
├── (1) Outcome Correctness       so R̂ với R*
│   ├── JRA   đúng cả component lẫn fault type (metric chính)
│   ├── CA    đúng component
│   └── FA    đúng fault type
├── (2) Process Grounding         so T với D*
│   ├── MC    số nhóm hoàn thành / tổng số nhóm
│   ├── EOC   số nhóm hoàn thành đúng thứ tự nhân quả / tổng số nhóm
│   └── ECR   1 nếu hoàn thành mọi nhóm, ngược lại 0
└── (3) Diagnostic Efficiency
    ├── EE    tỷ lệ lần gọi tool góp bằng chứng cho nhóm vào K^ord lần đầu
    ├── Steps tổng số lần gọi tool
    └── RAR   tỷ lệ lần gọi lặp lại cặp tool + tham số mà không thêm bằng chứng mới
```

**(1) Outcome Correctness**
- CA và FA tách riêng để biết agent sai do định vị nhầm component hay do nhầm cơ chế lỗi. JRA chỉ tính đúng khi đúng cả hai.
- Output thiếu field hoặc field không hợp lệ thì tính là sai ở metric tương ứng.
- JRA ≤ min(CA, FA).
- Cách tính: đây là tỷ lệ episode đúng, không phải trung bình nhiều lần chạy. Một episode là một lần agent chạy trên một case. Với mỗi model trên mỗi hệ thống, có N case thì có N episode, mỗi episode cho 0 hoặc 1, rồi chia cho N. Ví dụ JRA = số episode đúng cả component lẫn fault type / N.
- Kết quả theo độ khó (Fig. 3) thêm một bước: trong mỗi tổ hợp hệ thống × mức độ khó, tính metric cho từng model rồi lấy trung bình đều trên 10 model (§4.1).

Ví dụ (người đọc tự dựng, không phải số liệu của paper):

| Case | Đáp án R* | Agent trả lời | CA | FA | JRA |
|---|---|---|---|---|---|
| 1 | (checkout, ServiceSelectorMismatch) | (checkout, ServiceSelectorMismatch) | ✓ | ✓ | ✓ |
| 2 | (checkout, ServiceSelectorMismatch) | (checkout, ServicePortMappingMismatch) | ✓ | ✗ | ✗ |
| 3 | (cart, OOMKilled) | (redis, OOMKilled) | ✗ | ✓ | ✗ |
| 4 | (payment, IncorrectImageReference) | (frontend, CodeBusyLoop) | ✗ | ✗ | ✗ |

Kết quả: CA = 0,5, FA = 0,5, JRA = 0,25. Case 2 là định vị đúng nhưng nhầm cơ chế, case 3 là đúng cơ chế nhưng sai chỗ.

**(2) Process Grounding**
- Quét trajectory T theo thời gian. Lần gọi tool nào có response thỏa đủ các clause của một bundle thì milestone tương ứng được thiết lập (vào M^est). Nhóm hoàn thành khi có ít nhất một milestone được thiết lập. Các metric đếm theo nhóm, không theo milestone.
- MC: tỷ lệ nhóm hoàn thành, không quan tâm thứ tự.
- ECR: 0/1 theo case, bằng 1 khi và chỉ khi MC = 1.
- EOC: nhóm chỉ vào K^ord khi bằng chứng của nó được lấy (hoặc lấy lại, gọi là refresh) sau khi mọi nhóm tổ tiên trong ≺* đã vào K^ord. Một nhóm bị thiếu thì nhận 0 và chặn điểm EOC của mọi nhóm phụ thuộc nó.
- EOC ≤ MC.
- Báo cáo bằng macro average trên các case.
- Ba metric này không phụ thuộc kết luận cuối đúng hay sai, nên phân biệt được chẩn đoán có bằng chứng với đoán bừa (Gap 3).

Ví dụ (người đọc tự dựng) trên đồ thị của §3.3.3, gồm 5 nhóm, giả sử mỗi lần gọi tool thiết lập một milestone:

```
U → {M1} → {M2 ∨ M3} → {M4} → {M5}
                              └→ {M6}
```

| Agent | Thứ tự gọi | MC | ECR | EOC |
|---|---|---|---|---|
| A: bài bản | M1, M3, M4, M6, M5 | 1,0 | 1 | 1,0 |
| B: đi tắt | M1, M4, M5 | 0,6 | 0 | 0,2 |
| C: làm ngược | M4, M5, M6, M1, M2 | 1,0 | 1 | 0,4 |

- A lấy M3 thay M2 và làm M6 trước M5, đều hợp lệ.
- B thiếu {M2, M3}, nên M4 và M5 có bằng chứng nhưng không được tính EOC.
- C đủ bằng chứng nhưng M4, M5, M6 lấy trước các nhóm tiên quyết. Nếu C refresh lại M4, M5, M6 sau khi có M2 thì EOC lên 1,0, nhưng tốn thêm bước.

**(3) Diagnostic Efficiency**
- EE: tỷ lệ lần gọi tool góp clause vào bundle đã đưa một nhóm vào K^ord lần đầu. Với joint bundle, mọi lần gọi góp vào bundle đều được tính. Bằng chứng lấy thêm cho nhóm đã đủ thì không được tính.
- Steps: tổng số lần gọi tool.
- RAR: tỷ lệ lần gọi lặp lại cặp tool + tham số đã gọi mà không đem lại bằng chứng mới và không giúp nhóm mới nào tiến lên.
- Paper dặn đọc các metric efficiency cùng với MC và EOC, để không thưởng cho agent dừng sớm.

Ví dụ tính đủ các metric theo từng bước (người đọc tự dựng), cùng đồ thị 5 nhóm ở trên, agent gọi 4 lần:

| Bước | Lấy được | Vào K^est? | Vào K^ord? |
|---|---|---|---|
| 1 | M4 | có | không (M1 và {M2, M3} chưa có) |
| 2 | M1 | có | có |
| 3 | M2 | có | có (M1 đã nằm trong K^ord) |
| 4 | M5 | có | không (M4 chưa nằm trong K^ord) |

- MC = 4/5 = 0,8; EOC = 2/5 = 0,4; ECR = 0 (thiếu M6).
- EE = 2/4 = 0,5: chỉ bước 2 và 3 đưa nhóm vào K^ord.
- Nếu sau bước 3 agent gọi lại tool của bước 1 thì M4 được refresh và vào K^ord. Lần gọi này không bị tính là redundant vì có giúp một nhóm tiến lên.

**Nhận xét của người đọc (không phải của paper): số lần chạy và độ bất định**
- Đã tìm trong toàn bộ PDF (repeat, runs, trial, seed, variance, standard deviation, confidence): không thấy paper nói mỗi model × case chạy nhiều lần. Table 4 không có độ lệch chuẩn hay khoảng tin cậy. Nhiều khả năng mỗi tổ hợp chỉ chạy một lần, nhưng đây là suy ra từ việc không báo cáo, chưa có câu xác nhận rõ.
- §5.3 (Internal Validity) có thừa nhận "inference nondeterminism". Biện pháp được nêu là dùng chung framework, prompt, tool schema, step budget, temperature và snapshot, không phải chạy lặp.
- Temperature = 0 không bảo đảm kết quả lặp lại khi gọi qua API. Theo kiến thức nền (chưa kiểm chứng), reasoning model như GPT-5 có thể không cho chỉnh temperature, và paper không nói đã xử lý thế nào.
- Ước lượng do người đọc tự dựng: giả sử một hệ thống có khoảng 377 case (paper không cho số case theo từng hệ thống) và JRA ≈ 0,7 thì sai số chuẩn ≈ √(0,7 × 0,3 / 377) ≈ 0,024, khoảng tin cậy 95% vào cỡ ±0,05. Khi đó chênh lệch nhỏ như 0,70 với 0,68 chưa đủ để kết luận model nào hơn.
- Hàm ý cho đề tài: chạy lặp mỗi tổ hợp hoặc báo cáo khoảng tin cậy (ví dụ bootstrap trên các case).

### 4.2 RQ1: RCA Outcome Effectiveness (§4.2)

§4.2 so CA, FA, JRA giữa các model (Table 4), rồi phân tích kết quả theo 3 mức độ khó. Có 3 phát hiện chính.

**Phát hiện 1: triệu chứng thấy được ở Kubernetes không lộ trực tiếp root cause**
- Snapshot có nhiều bằng chứng ở mức Kubernetes (tên Pod, trạng thái Deployment, event, selector của Service, endpoint, log), nên agent thường tìm đúng object bị ảnh hưởng dù không suy ra được cơ chế lỗi.
- OnlineBoutique: CA luôn cao hơn FA và JRA. Ví dụ DeepSeek-V4-Flash có CA 0,88 nhưng FA 0,77, JRA 0,76; GPT-5 có CA 0,86 nhưng FA 0,69, JRA 0,68. Agent định vị đúng component nhưng nhầm giữa các cơ chế gần giống nhau, như image reference sai với registry fail, hoặc selector, port, protocol của Service.
- TrainTicket: quan hệ giữa CA và FA không một chiều, vì có nhiều service giống nhau nối qua gateway và database. Có lỗi lộ rõ loại lỗi nhưng lan qua nhiều service nên khó định vị; có lỗi định vị được service nhưng nguyên nhân cấu hình vẫn mơ hồ. Ví dụ GPT-5 có CA 0,70 và FA 0,71 gần bằng nhau; Qwen3.5-Plus có FA 0,79 cao hơn CA 0,67, tức nhận ra loại lỗi nhưng không luôn định vị được service.
- Kết luận của paper: benchmark tách được định vị triệu chứng ở mức object với quy nguyên nhân ở mức cơ chế, và JRA yêu cầu đúng cả hai.

**Phát hiện 2: model open-weight có thể cạnh tranh được**
- Open-weight là model công bố trọng số, tải về và tự host được. Proprietary chỉ gọi được qua API của hãng.
- OnlineBoutique: DeepSeek-V4-Flash đạt outcome cao nhất (CA 0,88, FA 0,77, JRA 0,76). Qwen3.5-27B (JRA 0,70) ngang hoặc hơn GPT-5 (0,68) và Gemini-2.5-Pro (0,67).
- Paper nói "cạnh tranh được", không phải "cao hơn": theo Table 4, Qwen3-8B chỉ có JRA 0,19, Qwen3-235B-A22B có 0,40, và trên TrainTicket JRA cao nhất là GPT-5 (0,68), một model proprietary.
- Lý do paper nêu: log, manifest, topology, event có thể nhạy cảm hoặc tốn kém khi gửi qua API bên ngoài, nên model open-weight cho thêm lựa chọn khi bị ràng buộc về chi phí, độ trễ hoặc quản trị dữ liệu.
- Nhận xét của người đọc: open-weight chỉ nói là có thể tự host. Phần đã đọc không nói 5 model open-weight được chạy tự host hay qua API, nên lợi thế này là về triển khai thực tế, không phải điều kiện thí nghiệm đã kiểm chứng.

**Phát hiện 3: độ khó do mức dễ quan sát triệu chứng và khoảng cách chẩn đoán quyết định**
- Độ khó là nhãn gán sẵn cho nhóm fault từ §3.2 (Table 2), không phải 3 fault type.

| Mức | Nhóm fault | Số case | Đặc điểm |
|---|---|---|---|
| Easy | Startup, Scheduling, Runtime | 391 | Triệu chứng lộ thẳng ở Kubernetes |
| Medium | Admission Control, Service Routing, Infrastructure | 189 | Phải nối nhiều object với nhau |
| Hard | Performance, Application Code Defect | 174 | Có tín hiệu bất thường nhưng gián tiếp |

- Easy: Pod unhealthy, image pull fail, Pod unschedulable, probe fail, hoặc lỗi runtime rõ ràng.
- Medium: phải liên kết nhiều object như deployment, service, endpoint, quota, node, thành phần control plane.
- Hard: vẫn có alert, metric, log bất thường nên bằng chứng không bị giấu. Nhưng tín hiệu chỉ cho biết hành vi hệ thống thay đổi ở đâu, không cho biết component hay cơ chế nào gây ra. Thứ còn thiếu là năng lực quy nguyên nhân từ telemetry (telemetry attribution) và phân tích source code, không phải lượng telemetry.
- JRA trung bình trên 10 model (Fig. 3) giảm rõ theo độ khó:
  - OnlineBoutique: 0,73 (Easy) → 0,51 (Medium) → 0,30 (Hard).
  - TrainTicket: 0,67 → 0,43 → 0,08.
- Paper dùng số này để khẳng định cách chia độ khó phản ánh khác biệt thật, không chỉ là nhãn bề mặt.
- Ở mức Hard, ECR vẫn khác 0 trong khi JRA rất thấp: agent vẫn thu được bằng chứng liên quan nhưng không quy được nguyên nhân từ đó.

### 4.3 RQ2: RCA Process Alignment (§4.3)

Ý chính: JRA cao không có nghĩa là quá trình điều tra đủ. Agent có thể đúng cả component lẫn fault type nhưng không hoàn thành đủ các nhóm milestone của D*, nên ECR thấp. Paper không chấm theo chuỗi tool (R3); điểm thấp là do đồ thị bằng chứng chưa được đóng. Có 4 phát hiện.

**Phát hiện 1: kết quả đúng phóng đại mức độ có căn cứ của chẩn đoán**
- JRA đo đúng cả component và fault type; ECR đo agent đã đóng được đồ thị bằng chứng hay chưa. Khoảng cách giữa hai metric cho thấy chỉ chấm kết quả cuối sẽ đánh giá quá cao độ tin cậy của agent.

| Hệ thống | Model | JRA | ECR |
|---|---|---|---|
| OnlineBoutique | DeepSeek-V4-Flash | 0,76 | 0,38 |
| OnlineBoutique | GPT-5 | 0,68 | 0,21 |
| OnlineBoutique | Qwen3.5-27B | 0,70 | 0,43 |
| TrainTicket | GPT-5 | 0,68 | 0,15 |
| TrainTicket | DeepSeek-V4-Flash | 0,63 | 0,24 |

- Cách paper giải thích: agent suy ra đúng cặp component–fault từ tín hiệu cục bộ mạnh (Pod status bất thường, alert, lỗi service) mà không dựng đủ chuỗi chẩn đoán để kết luận giải thích được.
- Paper gọi đây là ungrounded diagnosis: nhãn đúng nhưng bằng chứng hỗ trợ chưa đủ. Với SRE, đúng nhãn là chưa đủ, chẩn đoán cần cho thấy bằng chứng nào hỗ trợ quyết định can thiệp.

**Phát hiện 2: agent khám phá rộng nhưng nông (broad but shallow)**
- Agent hiếm khi đi lạc hoàn toàn: MC ở mức trung bình đến cao, tức là chạm được nhiều milestone và xem đúng object, log, cấu hình liên quan. Nhưng các phát hiện rời rạc thường không gộp được thành bộ bằng chứng đủ.
- OnlineBoutique: Qwen3.5-27B có MC 0,75 nhưng ECR 0,43; Gemini-2.5-Pro có MC 0,74 nhưng ECR 0,46; GPT-5 có MC 0,64 nhưng ECR 0,21.
- TrainTicket: Qwen3.5-Plus có MC 0,64 và DeepSeek-V4-Flash có MC 0,62, nhưng ECR chỉ 0,25 và 0,24.
- EOC thấp hơn MC một chút nhưng nhất quán: OnlineBoutique Qwen3.5-27B 0,75 → 0,70, GPT-5 0,64 → 0,55; TrainTicket Qwen3.5-Plus 0,64 → 0,58, DeepSeek-V4-Flash 0,62 → 0,56. Có bằng chứng được lấy trước khi nhóm tiên quyết được xác lập, nên paper gọi quá trình tìm kiếm là partly opportunistic.
- Khoảng cách MC → ECR lớn hơn nhiều so với MC → EOC. Hạn chế chính là không biến bằng chứng rải rác thành bộ bằng chứng đủ, không phải sai thứ tự.

**Phát hiện 3: tổng hợp RCA và hiệu quả điều tra là các năng lực tách rời**
- Kết quả đúng không kéo theo quá trình đủ. GPT-5 đạt JRA 0,68 trên cả hai hệ thống nhưng ECR chỉ 0,21 và 0,15. DeepSeek-V4-Flash đạt JRA 0,76 và 0,63 nhưng ECR 0,38 và 0,24. Model mạnh có thể tổng hợp đúng từ một phần tín hiệu nổi bật.
- Hiệu quả là một chiều riêng. OnlineBoutique: GPT-5 và Qwen3.5-Plus đạt EE 0,64 và 0,65 với chỉ 5,56 và 5,92 bước, tức lấy bằng chứng có chủ đích. Qwen3-8B dùng 16,01 bước nhưng EE chỉ 0,37, RAR 0,46.
- EE và Steps phân biệt được việc lấy bằng chứng hiệu quả với trajectory chỉ dài. Tổng hợp RCA, độ đủ của quá trình và hiệu quả chẩn đoán là ba năng lực khác nhau.

**Phát hiện 4: gọi tool lặp vô ích chủ yếu ở model yếu**
- Model mạnh (GPT-5, Qwen3.5-Plus, Gemini-2.5-Pro, DeepSeek-V4-Flash) có RAR gần 0 ở cả hai hệ thống. Lỗi của chúng nằm ở grounding bằng chứng, xác định target hoặc tổng hợp RCA, không ở việc gọi lặp.
- Model yếu lặp rõ rệt. OnlineBoutique: Qwen3-8B trung bình 16,01 bước, RAR 0,46, nhưng JRA 0,19, ECR 0,16; Qwen3-14B 14,58 bước, RAR 0,28, JRA 0,41.
- Trajectory dài không có nghĩa là chẩn đoán sâu; với model yếu, gọi thêm thường là truy vấn lặp hoặc khám phá ít giá trị.

**Nhận xét của người đọc (không phải của paper)**
- D* dựng từ toàn bộ chuỗi nhân quả nên ECR đòi đủ chuỗi giải thích (completeness), trong khi agent có thể chỉ cần vài tín hiệu nổi bật để xác định đúng lỗi (sufficiency). Paper quy toàn bộ khoảng cách JRA–ECR cho agent, không xét khả năng D* đòi nhiều hơn mức cần.
- Cần cân nhắc: JRA cao cũng có thể do đoán nhờ kiến thức nền; Fig. 3 có trường hợp ECR cao mà JRA thấp (Qwen3-235B-A22B ở TrainTicket mức Hard: JRA 0,09, ECR 0,52), tức có lỗi ở bước tổng hợp.
- Paper chỉ so hai tỷ lệ riêng, không báo cáo tỷ lệ case "đúng nhưng không đóng". Từ Table 4 chỉ suy ra chặn dưới, ví dụ GPT-5 ở OnlineBoutique có ít nhất 0,68 − 0,21 = 0,47 số case như vậy.

Chi tiết xem Finding 2 trong `finding/CloudOpsBench_FINDING.md`.

### 4.4 RQ3: Experience-Augmented RCA Agents (§4.4)

Ý chính: dùng lại kinh nghiệm chẩn đoán cũ có thể cải thiện cả outcome lẫn process, nhưng mức cải thiện không đều giữa hai hệ thống và phụ thuộc vào cách truy vấn kinh nghiệm (retrieval granularity).

**Động cơ:** trong vận hành thật, kỹ sư dựa nhiều vào kinh nghiệm tích lũy (trace sự cố cũ, ghi chú on-call, runbook) chứ không làm zero-shot.

**Setup**
- Với mỗi root cause, chia case thành tập train và test riêng biệt, tỷ lệ khoảng 1:1. Không có model nào được train; tập train chỉ là nguồn lấy kinh nghiệm, tập test dùng để chấm.
- Kho kinh nghiệm chỉ gồm trajectory thành công của GPT-5 trên tập train.
- Chỉ thử 3 model: Gemini-2.5-Flash, Qwen3.5-27B, DeepSeek-V4-Flash, vì cạnh tranh được mà chi phí và độ trễ thấp.

**Ba cấu hình so sánh**
- Base: agent ReAct ở §4.1 chạy trần, chỉ có U và tool, không có kinh nghiệm (zero-shot).
- Trajectory-as-ICL: lấy 3 trajectory thành công khớp nhất theo triệu chứng, dán nguyên vào prompt (tool call, observation, kết luận). Đưa ví dụ cụ thể.
- SOP (Standard Operating Procedure): chưng cất các thao tác và nhánh quyết định hay lặp lại từ trajectory thành công thành runbook theo nhóm fault. Đưa quy trình đã khái quát, không phải kho case để truy vấn.
- Cả ICL và SOP đều không dùng nhãn root cause để truy vấn, vì lúc chạy agent chưa biết đáp án.
- Case test là case mới nhưng loại lỗi cũ: chia theo từng root cause nên fault type nào có trong test thì cũng có case trong train.

**Kết quả (trung bình trên 3 model, Table 5)**

| | Base | ICL | SOP |
|---|---|---|---|
| OnlineBoutique JRA | 0,70 | 0,79 | 0,76 |
| OnlineBoutique ECR | 0,39 | 0,59 | 0,61 |
| TrainTicket JRA | 0,58 | 0,56 | 0,62 |
| TrainTicket ECR | 0,18 | 0,18 | 0,17 |

- OnlineBoutique: cả hai phương pháp cải thiện nhất quán cho cả 3 model.
- TrainTicket: không đều. SOP tăng JRA nhẹ, ICL còn giảm. MC tăng từ 0,55 lên 0,62 với cả hai, EOC từ 0,51 lên 0,56 (ICL) và 0,55 (SOP), nhưng ECR gần như không đổi.

**Cách paper giải thích (retrieval granularity)**
- Lúc chạy chưa biết root cause, nên phải truy vấn theo triệu chứng quan sát được.
- Một triệu chứng có thể ứng với nhiều root cause. ICL chỉ lấy 3 ví dụ, nên case lấy về có thể không cùng cơ chế với sự cố hiện tại.
- SOP gộp nhánh chẩn đoán ở mức nhóm fault, nên rộng hơn nhưng ít sát với từng case.
- Kết luận: kinh nghiệm vận hành là nguồn bổ trợ hữu ích, nhưng chất lượng truy vấn và mức trừu tượng hóa kiến thức quyết định lợi ích có chuyển được nhất quán giữa các hệ thống hay không.

**Nhận xét của người đọc (không phải của paper)**
- Dòng Base ở Table 5 trùng hoàn toàn với Table 4 (cả 3 model, cả 2 hệ thống, mọi metric). Paper không nói rõ Base ở Table 5 được tính trên tập nào. Nếu Table 4 tính trên toàn bộ case thì Base được chấm trên tập case khác với ICL/SOP (chỉ tập test). Vấn đề không phải Base được học gì (Base không học, chạy trên case train không gian lận), mà là so trên hai tập case khác nhau nên chênh lệch có thể một phần do khác tập case. Chi tiết xem Finding 3.
- Paper không đo độ chính xác truy vấn (ví dụ tỷ lệ case lấy về cùng root cause với case hiện tại); giải thích về granularity mới là diễn giải ("can be understood through").
- §4.4 không định nghĩa "successful trajectory" là đúng JRA hay đóng được ECR.
- Train và test có cùng tập root cause, nên thí nghiệm chỉ đo dùng lại kinh nghiệm cho loại lỗi đã gặp, chưa thử root cause chưa có trong kho.
- Chưa rõ: cách khớp triệu chứng (embedding hay từ khóa), SOP do LLM hay người chưng cất, và SOP được chọn theo nhóm fault thế nào khi nhóm fault là thông tin lúc dựng benchmark.

### 4.5 Failure Modes of Cloud RCA Agents (§4.5)

**Cách làm phân tích**
- Gom các case có JRA = 0 của cả 10 model thành failure pool.
- Từ pool, chọn có chủ đích (purposive sample) một số trajectory phủ đủ 2 hệ thống, 8 nhóm fault và các model mạnh, yếu khác nhau, rồi đọc thủ công (qualitative).
- Paper tự giới hạn: đây là phân tích khám phá, mô tả các hành vi tiêu biểu và có thể chồng lấn nhau. Không ước lượng tần suất, không phải taxonomy đầy đủ.

**4 kiểu đổ vỡ**

```
Failure modes
├── (1) Evidence-grounding   có bằng chứng nhưng hiểu sai hoặc xem nhẹ
├── (2) Search-control       điều khiển quá trình tìm kiếm kém
├── (3) Target-resolution    có bằng chứng nhưng quy sai đối tượng hoặc cơ chế
└── (4) Tool-grounding       gọi tool sai nên không lấy được hoặc lấy nhầm bằng chứng
```

**(1) Evidence-grounding: có bằng chứng nhưng hiểu sai**
- Bỏ qua bằng chứng rõ ràng: event startup đã báo `manifest unknown`, `403 Forbidden` hoặc thiếu Secret, nhưng agent vẫn kiểm tra các resource ngoài lề.
- Bám vào triệu chứng ồn nhất ở phía sau (frontend 503, latency cao, alert CPU nổi bật) và nhầm component ồn nhất là nguồn gây lỗi.
- Coi "không có gì" là "không có bằng chứng": endpoint rỗng, Pod không tồn tại, component lỗi không có log bị bỏ qua thay vì được xem là tín hiệu chẩn đoán.
- Hậu quả: cả hướng điều tra rơi vào sai họ lỗi, ví dụ code defect bị giải thích thành OOM, network delay hoặc lỗi cấu hình Service.

**(2) Search-control: không điều chỉnh tìm kiếm theo bằng chứng đã có**
- Chốt quá sớm: xem một Pod hoặc Service bất thường rồi kết luận, không kiểm tra giả thuyết cạnh tranh.
- Không đổi hướng khi hướng ban đầu yếu đi: đã xác nhận connectivity bình thường nhưng không chuyển sang kiểm tra routing ở gateway hoặc cấu hình.
- Ngược lại, không biết dừng: đã thấy bằng chứng quyết định (`replicas=0`, kube-proxy không chạy, lỗi truy cập DB rõ ràng) nhưng vẫn gọi truy vấn ít giá trị hoặc lặp lại.
- Paper tóm lại: agent điều khiển kém việc sửa giả thuyết, rẽ nhánh chẩn đoán và quyết định dừng.

**(3) Target-resolution: có bằng chứng nhưng chỉ sai chỗ hoặc sai cơ chế**
- Quy lỗi cho bên chịu ảnh hưởng thay vì bên gây ra: ở TrainTicket, lỗi DB mà các service ứng dụng thấy bị quy cho chính các service đó thay vì dependency dùng chung `tsdb-mysql`; lỗi routing ở gateway bị gán cho các business service bị ảnh hưởng.
- Nhầm các cơ chế gần nhau: image reference với registry DNS, port với protocol của probe, các subtype code defect gần nhau (khớp với khoảng cách CA > FA ở §4.2).
- Code defect cần nối alert, lỗi HTTP, metric bất thường với hành vi ở mức source code. Agent có thể đã xem đúng telemetry hoặc code nhưng vẫn giải thích busy loop, artificial delay hoặc đọc ghi file quá mức thành bão hòa tài nguyên hoặc lỗi performance.

**(4) Tool-grounding: lỗi ở chỗ nối giữa suy luận và thực thi**
- Tham số không hợp lệ, sai object hoặc scope, hoặc hành động không khớp với bước kiểm tra định làm, nên không lấy được bằng chứng cần thiết.
- Tinh vi hơn: truy vấn đúng cú pháp nhưng sai ý tạo ra bằng chứng gây hiểu nhầm. Ví dụ kiểm tra connectivity với sai port thì nhận về một connection failure thật, agent coi đó là triệu chứng của hệ thống và dùng để biện minh cho chẩn đoán sai.

**Kết luận của paper:** lỗi của agent thường hình thành trước dự đoán cuối, trong quá trình điều tra và suy luận dựa trên bằng chứng. Muốn cải thiện agent thì không chỉ cần dự đoán cuối tốt hơn mà còn cần trajectory chẩn đoán đáng tin và dễ giải thích hơn.

**Nhận xét của người đọc (không phải của paper)**
- Paper không cho cỡ mẫu, người phân loại hay cách đối chiếu giữa nhiều người. Paper đã tự nói không ước lượng tần suất, nên 4 kiểu lỗi chỉ là giả thuyết định tính, không kết luận được kiểu nào phổ biến nhất.
- Mẫu chỉ lấy từ case JRA = 0, nên không thấy các case đoán đúng nhưng quá trình hỏng (JRA = 1, ECR = 0, xem Finding 2), dù các case đó cũng có thể chứa search-control failure như chốt quá sớm.
- Liên quan đến selective RCA (cần kiểm tra, chưa phải gap đã chứng minh):
  - Kiểu (2) chốt quá sớm và không biết dừng: bài toán khi nào đủ bằng chứng để commit.
  - Kiểu (1) coi thiếu dữ liệu là không có bằng chứng: xử lý dữ liệu thiếu.
  - Kiểu (4) sai port tạo ra bằng chứng giả: cần kiểm tra bằng chứng trước khi dùng.
