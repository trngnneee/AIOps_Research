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

