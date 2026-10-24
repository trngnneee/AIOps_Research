# Báo cáo quá trình đọc paper: Cloud-OpsBench

**Paper:** Cloud-OpsBench: A Reproducible Benchmark for Agentic Root Cause Analysis in Cloud Systems (arXiv 2603.00468, preprint)

**Tiến độ:** đang đọc §2 (Motivation), phần các gap trong quá trình đánh giá mô hình.

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

