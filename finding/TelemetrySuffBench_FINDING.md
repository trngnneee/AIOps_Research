# BÀI GIẢNG CHUYÊN SÂU: HIỂU TOÀN DIỆN VỀ TELEMETRYSUFFBENCH TỪ CON SỐ 0

> **Thông tin Paper gốc:**  
> - **Tên bài báo:** *TelemetrySuffBench: Is Agent Telemetry Sufficient for Failure-Origin Diagnosis?*  
> - **Tác giả:** Yuxuan Zhu, Peng Pu* (Đại học Sư phạm Hoa Đông - East China Normal University, Thượng Hải).  
> - **Mã lưu trữ:** arXiv:2608.07899v1 [cs.AI], công bố ngày 8 tháng 8 năm 2026.  
> - **Mã nguồn & Artifact:** `https://anonymous.4open.science/r/TelemetrySuffBench-E635/README.md`  
> - **Vị trí file PDF trong repo:** `paper/TelemetrySuffBench.pdf` (10 trang).  
> - **Mục tiêu tài liệu này:** Đóng vai trò như một **bài giảng sư phạm chi tiết**, giải thích cặn kẽ bản chất, cơ chế hoạt động, các thuật ngữ trừu tượng và toàn bộ phát hiện thực nghiệm của paper bằng ngôn ngữ trực quan, ví dụ thực tế đời sống và microservices; đồng thời chỉ rõ từng điểm cốt lõi để kế thừa cho Luận văn Tốt nghiệp về **Selective RCA trong Kubernetes**.

---

## MỤC LỤC BÀI GIẢNG

1. **Khái niệm mở đầu: Câu chuyện "Trinh thám phá án" & Nghịch lý Observability**
2. **Cơ chế lỗi "Quả bom nổ chậm" (Delayed-Binding Faults) hoạt động ra sao?**
3. **Chuỗi nhân quả 5 chặng: Tại sao người ta hay bắt nhầm "Nạn nhân" thay vì "Thủ phạm"?**
4. **Giải mã 7 Nhân tố ngữ nghĩa (7 Semantic Factors: I, D, P, R, S, V, T)**
5. **Kỹ thuật "Vụ án song sinh" (Exact-Equal Ambiguity) & Nghệ thuật biết nói "Tôi không biết" (Safe Abstention)**
6. **Mổ xẻ 3 Câu hỏi nghiên cứu (RQ1, RQ2, RQ3) & Những con số giật mình**
7. **Đánh giá phản biện: Điểm sáng chói & Điểm mù của bài báo**
8. **Kim chỉ nam cho Luận văn: Đưa toàn bộ tư tưởng bài báo vào Kubernetes**

---

## PHẦN 1: CÂU CHUYỆN "TRINH THÁM PHÁ ÁN" & NGHỊCH LÝ OBSERVABILITY

Để hiểu được bài báo này từ con số 0, hãy bắt đầu bằng một câu chuyện thực tế về công việc của kỹ sư vận hành (SRE) hoặc một AI Agent chẩn đoán sự cố:

### 1.1. Thuật ngữ nền tảng: Observability và Telemetry là gì?
- **Telemetry (Dữ liệu viễn trắc/vận hành):** Là toàn bộ các dấu vết kỹ thuật mà một phần mềm để lại khi nó chạy. Nó gồm:
  - *Logs:* Nhật ký ghi lại sự kiện ("Lúc 10:00:01 bắt đầu chạy hàm A...").
  - *Metrics:* Các con số đo lường (CPU dùng bao nhiêu %, RAM bao nhiêu MB, số request/giây).
  - *Traces (Spans):* Bản ghi hành trình của một yêu cầu, từ lúc người dùng bấm nút, qua Service 1, sang Service 2, gọi cơ sở dữ liệu (Database).
- **Observability (Khả năng quan sát):** Là việc hệ thống của bạn được cài cắm đầy đủ công cụ (như OpenTelemetry, Prometheus, Datadog) để thu thập được toàn bộ đống telemetry ở trên. Khi có lỗi, bạn mở bảng điều khiển ra xem được mọi ngóc ngách.

### 1.2. Nghịch lý lớn: "Thấy hết mọi thứ" liệu có đồng nghĩa với "Biết ai làm sai"?
Mọi người trong ngành thường nghĩ: *Cứ log thật nhiều, trace thật chi tiết theo chuẩn xịn xò (như OpenTelemetry hay OpenInference) thì khi có lỗi, AI Agent chỉ cần đọc trace là tìm ra nguyên nhân gốc ngay!*

**Bài báo này tát một gáo nước lạnh vào quan niệm đó:**
> **"Observability alone does not establish diagnostic adequacy"** (§I, trang 1)  
> *(Khả năng quan sát được không đồng nghĩa với tính đầy đủ để chẩn đoán!)*

**Ví dụ trực quan do mình dựng:**
> Bạn là quản đốc một nhà máy may. Đến khâu kiểm tra chất lượng cuối cùng (Terminal Verifier), bảo vệ phát hiện: "Áo này bị đơm nhầm cúc màu đen, trong khi đơn hàng yêu cầu cúc màu trắng!".
> - Khâu kiểm tra này la lên báo động $\rightarrow$ Bạn biết chắc chắn $100\%$ là có lỗi (**Failure Detection** cực kỳ dễ).
> - Bạn kiểm tra camera khâu đơm cúc (Downstream Symptom), thấy đúng là máy đơm cúc vừa đơm cái cúc đen lên áo.
> - **Nếu bạn vội vàng kết luận:** "Máy đơm cúc bị hỏng!" $\rightarrow$ **Bạn đã sai hoàn toàn!**
> - Chiếc máy đơm cúc chỉ làm đúng chức năng của nó: Nó lấy cúc từ chiếc hộp ghi nhãn "Cúc A" do kho phát cho. Kẻ gây ra lỗi thực sự là **ông nhân viên thủ kho ở khâu đầu tiên** (Origin Event) đã dán nhầm nhãn "Cúc A" lên chiếc hộp chứa cúc đen!

Trong các hệ thống AI Agent nhiều bước (Agentic Workflows), điều này xảy ra liên tục:
- **Phát hiện lỗi (Detection):** Rất dễ, nhìn mã lỗi 500 hoặc verifier báo sai là biết.
- **Tìm nguyên nhân gốc (Origin Localization):** Cực kỳ khó, vì kẻ gây lỗi ở tít đầu nguồn, còn chỗ phát hiện lỗi lại nằm ở cuối nguồn!
- Nếu dữ liệu telemetry chỉ ghi chép chung chung theo chuẩn thông thường (như "Bước 1 thành công", "Bước 2 thành công", "Bước 3 lỗi"), thì dù trace có dài 1.000 dòng, bạn vẫn **hoàn toàn thiếu bằng chứng** để chỉ ra ông nhân viên thủ kho ở Bước 1!

---

## PHẦN 2: CƠ CHẾ LỖI "QUẢ BOM NỔ CHẬM" (DELAYED-BINDING FAULTS)

Làm sao để các nhà khoa học kiểm tra xem một mô hình AI chẩn đoán thông minh thật hay chỉ "đoán mò vào triệu chứng"? Họ tạo ra một cơ chế tiêm lỗi kinh điển: **Delayed-Binding Faults** (Lỗi liên kết trễ - §III-B, Hình 1).

### 2.1. Phân biệt: "Lỗi chết ngay" vs "Lỗi ngấm ngầm"
- **Lỗi chết ngay (Immediate Failure):** Một con agent gõ sai cú pháp lệnh SQL hoặc chia cho số 0. Chương trình crash ngay lập tức tại đúng dòng code đó. Bắt lỗi này quá tầm thường, không cần benchmark phức tạp.
- **Lỗi ngấm ngầm (Delayed-Binding / Quả bom nổ chậm):** 
  - Tại bước đầu tiên, con agent không hề làm sập chương trình.
  - Nó chỉ chọn **sai một cái tên tham chiếu (Symbolic Reference)**.
  - Các bước tiếp theo vẫn nhận tham chiếu đó và chạy trơn tru, không có một exception nào văng ra.
  - Cho đến nhiều bước sau, khi tham chiếu đó được đem ra "kích hoạt" (activation) và thực thi cập nhật vào dữ liệu thật, quả bom mới phát nổ!

### 2.2. Đi sâu vào mô hình của Paper (Hình 1, trang 4)
Hãy tưởng tượng hệ thống có một **Sổ đăng ký tham chiếu (Reference Registry)**:
- `ref_A`: Mã trỏ đến Hồ sơ A (Record A - Đúng nhiệm vụ cần cập nhật).
- `ref_B`: Mã trỏ đến Hồ sơ B (Record B - Một hồ sơ hợp lệ khác trong hệ thống, nhưng không phải mục tiêu của nhiệm vụ này).

```text
[NHIỆM VỤ GIAO CHO AGENT]: Hãy cập nhật số dư cho Record A!

1. ORIGIN COMPONENT (Thủ phạm thật sự):
   - Thay vì chọn ref_A, nó lại chọn nhầm ref_B* (nhưng vẫn nghĩ là mình đang xử lý A).
   - Lỗi được gieo mầm tại đây! Không có lỗi cú pháp nào xảy ra.
        ↓
2. INTERMEDIATE SPANS (Các bước trung gian):
   - Dữ liệu ref_B* được truyền qua Module Lập kế hoạch (Planner) → Bộ nhớ (Memory) → Phân quyền (Guardrail).
   - Tất cả các module này chạy bình thường, log trả về status: "SUCCESS".
        ↓
3. ACTIVATION & RESOLVER (Ngòi nổ kích hoạt):
   - Bộ giải mã (Resolver) đọc mã ref_B*, tra vào Sổ đăng ký → Thấy ref_B* trỏ đến Record B.
   - Đây là điểm "Xung đột ngầm đầu tiên" (First Visible Deviation).
        ↓
4. DOWNSTREAM UPDATE TOOL (Triệu chứng thực thi):
   - Công cụ ghi đè (Update Tool) thực hiện lệnh: Ghi đè trạng thái mới lên Record B.
   - Lệnh ghi đè chạy THÀNH CÔNG RỰC RỠ (Status 200 OK)! Record B bị sửa oan.
        ↓
5. TERMINAL VERIFIER (Phát hiện lỗi cuối cùng):
   - Trình kiểm tra mở Record A ra đối soát: "Ủa, sao Record A vẫn chưa được sửa?".
   - Verifier ném ra ngoại lệ: FAILED (Final state mismatch)!
```

### 2.3. Sáu "Toán tử" tiêm lỗi (6 Operators - §III-B)
Paper không chỉ tiêm một kiểu, mà mô phỏng 6 cách thức mà phần mềm hay gán nhầm tham chiếu:
1. **Alias binding:** Nhầm bí danh (tưởng `ref_B` là bí danh của A).
2. **Version binding:** Lấy nhầm phiên bản cũ/mới (gây ra loại lỗi `stale_reference_state`).
3. **Namespace handoff:** Bàn giao nhầm không gian tên giữa các component.
4. **Schema binding:** Ràng buộc nhầm lược đồ dữ liệu.
5. **Evidence binding:** Dẫn chứng nhầm bằng chứng từ tài liệu khác.
6. **Retry-token binding:** Dùng lại token của lượt thử trước đó (gây ra loại lỗi `stale_reference_state`).

---

## PHẦN 3: CHUỖI NHÂN QUẢ 5 CHẶNG (CAUSAL STAGES)

Để đánh giá công bằng, paper vạch ra **5 chặng nhân quả** dọc theo chiều thời gian (§III-B, §III-G):

```text
Trục thời gian:  (1) ---------> (2) ---------> (3) ---------> (4) ---------> (5)
                Origin      Intermediate   Activation      Symptom        Terminal
              [Nguồn gốc]   [Trung gian]  [Kích hoạt]   [Triệu chứng]   [Báo động]
```

### Chi tiết 5 chặng:
1. **Stage 1: Origin Event (Gốc rễ):** Sự kiện đầu tiên gán sai tham chiếu. Đây là câu trả lời DUY NHẤT đúng cho câu hỏi: *"Lỗi bắt nguồn từ đâu?"*.
2. **Stage 2: Intermediate Spans (Lưu chuyển):** Các sự kiện chuyển tiếp tham chiếu, hệ thống vẫn xanh lè, không có dấu hiệu bất thường.
3. **Stage 3: Activation & First Visible Deviation (Hiển lộ đầu tiên):** Sự kiện mà giá trị sai lần đầu tiên xuất hiện trong logic nghiệp vụ (Resolver dịch mã sai ra đối tượng sai).
4. **Stage 4: Symptom Event (Triệu chứng hạ nguồn):** Hành động gây hậu quả trực tiếp (Tool cập nhật nhầm vào Record B).
5. **Stage 5: Terminal Event (Điểm kết thúc):** Trình kiểm tra Verifier phát hiện ra trạng thái cuối cùng không khớp và gióng chuông báo động.

### Hiện tượng "Sụp đổ chặng nhân quả" (Causal Stage Collapse):
Paper đưa ra một phát hiện châm biếm: Nếu một mô hình AI hay một kỹ sư chỉ chăm chăm nhìn vào log của công cụ cập nhật (Stage 4) hay log của trình báo động (Stage 5) rồi kết luận đó là nguyên nhân gốc, thì độ chính xác định vị nguyên nhân thực tế (**Origin-Step Top-1 Accuracy**) sẽ là **$0.0\%$ tròn trĩnh** (§IV, Bảng II)!

---

## PHẦN 4: GIẢI MÃ 7 NHÂN TỐ NGỮ NGHĨA (7 SEMANTIC FACTORS)

Đây là phần mang tính phương pháp luận cốt lõi của paper (RQ2 - §III-E, Bảng I). Thay vì để nguyên một đống log hỗn độn, các tác giả đã phân rã toàn bộ dữ liệu telemetry thành **7 nhân tố độc lập**:

```text
                  CẤU TRÚC 7 NHÂN TỐ CỦA MỘT DÒNG TELEMETRY
┌───┬───────────────────────────────────┬──────────────────────────────────────────┐
│Ký │ Tên nhân tố (Semantic Factor)     │ Giải thích nôm na (Bản chất đời thường)   │
│hiệu│                                   │                                          │
├───┼───────────────────────────────────┼──────────────────────────────────────────┤
│ I │ Identity & Event Semantics        │ "AI LÀM?": Tên role, tên component,     │
│   │                                   │ danh tính actor, loại sự kiện, tên tool. │
├───┼───────────────────────────────────┼──────────────────────────────────────────┤
│ D │ Decision Content                  │ "QUYẾT ĐỊNH CÁI GÌ?": Giá trị tham chiếu  │
│   │                                   │ tượng trưng (symbolic ref) đã được chọn. │
├───┼───────────────────────────────────┼──────────────────────────────────────────┤
│ P │ Provenance & Registry Mappings    │ "NGUỒN GỐC TỪ ĐÂU?": Bản đồ tra cứu      │
│   │                                   │ registry, tài liệu gốc được trích xuất.  │
├───┼───────────────────────────────────┼──────────────────────────────────────────┤
│ R │ Propagation Relations             │ "GỌI NHAU THẾ NÀO?": Cạnh quan hệ cha-con│
│   │                                   │ (parent-child), sự kiện nguồn bộ nhớ.   │
├───┼───────────────────────────────────┼──────────────────────────────────────────┤
│ S │ Tool Inputs & State Transitions   │ "CÔNG CỤ CHẠY RA SAO?": Tham số gọi tool,│
│   │                                   │ kết quả trả về, truy vấn retrieval.      │
├───┼───────────────────────────────────┼──────────────────────────────────────────┤
│ V │ Verifier Evidence                 │ "ĐỐI CHIẾU THẾ NÀO?": Giá trị kỳ vọng vs │
│   │                                   │ giá trị thực tế của mục tiêu.            │
├───┼───────────────────────────────────┼──────────────────────────────────────────┤
│ T │ Terminal Status                   │ "KẾT CỤC RA SAO?": Mã lỗi kết thúc,      │
│   │                                   │ chuỗi thông báo exception văng ra.       │
└───┴───────────────────────────────────┴──────────────────────────────────────────┘
```

### Các tác giả làm thí nghiệm gì với 7 nhân tố này?
Họ tạo ra các **"Mặt nạ" (Masks)**:
- **`Full`:** Giữ nguyên toàn bộ 7 nhân tố.
- **Thí nghiệm "Bỏ bớt 1 đứa" (Leave-one-factor-out):**
  - `Full-I`: Che mất tên người làm (`I`), giữ 6 đứa còn lại.
  - `Full-D`: Che mất quyết định tham chiếu (`D`), giữ 6 đứa còn lại.
  - `Full-P`: Che mất nguồn gốc registry (`P`), giữ 6 đứa còn lại.
  - ... tương tự cho `Full-R`, `Full-S`, `Full-V`, `Full-T`.
- **Thí nghiệm "Tập hợp mục tiêu" (Targeted Subsets):**
  - `I+D+P+V`: Bộ tứ thượng nguồn (Danh tính + Quyết định + Nguồn gốc + Kỳ vọng).
  - `D+P+V`: Giống trên nhưng bỏ danh tính `I`.
  - `S+V+T`: Bộ ba hạ nguồn (Chỉ có tham số tool + Đối chiếu + Lỗi văng ra).

Mục đích: Tìm xem **nhân tố nào mới thực sự là "linh hồn" giúp AI tìm đúng nguyên nhân gốc?**

---

## PHẦN 5: KỸ THUẬT "VỤ ÁN SONG SINH" (EXACT-EQUAL AMBIGUITY) & NGHỆ THUẬT BIẾT NÓI "TÔI KHÔNG BIẾT"

Đây là phần thông minh nhất và có giá trị khoa học cao nhất của bài báo (RQ3 - §III-F).

### 5.1. Căn bệnh "Ảo tưởng tự tin" của Large Language Models
Khi bạn đưa cho ChatGPT, Claude hay DeepSeek một đống log và hỏi: *"Cái gì gây ra lỗi này?"*, bản chất của LLM là luôn cố gắng đưa ra một câu trả lời nghe có vẻ thuyết phục. Nó hiếm khi dám nói: *"Thưa bạn, với đống log này thì Sherlock Holmes cũng không thể biết ai làm sai!"*.
Trong kỹ thuật, hành vi này gọi là **Unsupported Guessing (Đoán mò vô căn cứ)**. Trong vận hành đám mây, đoán mò là thảm họa, vì kỹ sư sẽ đi sửa nhầm service đang chạy tốt!

### 5.2. Kỹ thuật "Vụ án song sinh" (Exact-Equal Ambiguous Origin Pairs)
Làm sao chứng minh được bằng toán học rằng mô hình đang đoán mò? Các tác giả đã nghĩ ra một phương pháp cực kỳ chặt chẽ:
1. Tạo ra **Vụ án A:** Thủ phạm thực sự được tiêm vào component **`Planning`** ($\omega_a = Planning$).
2. Tạo ra **Vụ án B:** Thủ phạm thực sự được tiêm vào component **`Memory`** ($\omega_b = Memory$).
3. Tuy nhiên, họ áp dụng một mặt nạ telemetry $m$ sao cho: **Đoạn log mà mô hình nhìn thấy ở Vụ án A và Vụ án B giống hệt nhau từng dấu chấm, dấu phẩy, bằng nhau tuyệt đối từng byte (Byte-stable equality - Công thức 2, §III-F)!**

$$P_m(\tau_a) = P_m(\tau_b) \quad \text{nhưng} \quad \omega_a \neq \omega_b$$

### 5.3. Tiêu chuẩn đánh giá: Chỉ có MỘT đáp án đúng duy nhất!
Đặt mình vào vị trí của mô hình: Bạn cầm trên tay một bản hồ sơ giống hệt nhau ở cả 2 vụ án.
- Nếu bạn kết luận: *"Thủ phạm là Planning!"* $\rightarrow$ Ở vụ án B, bạn sai bét! Thậm chí ở vụ án A, dù bạn trúng tên `Planning`, bạn vẫn bị chấm điểm là **Đoán mò vô căn cứ (Unsupported Unique-Origin Answer)**, vì trong tay bạn làm gì có bằng chứng nào để loại trừ `Memory`?
- **Lựa chọn khoa học và đạo đức duy nhất:** Mô hình bắt buộc phải trả lời:
  > **`INSUFFICIENT_EVIDENCE`** *(Bằng chứng không đủ để chỉ ra duy nhất một thủ phạm! Tôi từ chối kết luận bừa bãi!)*

### 5.4. Các chỉ số đo lường độ trung thực (Metrics):
- **FAR (False-Answer Rate - Tỷ lệ đoán bừa):** Tỷ lệ mô hình vẫn cố chấp chỉ định 1 thủ phạm trên tập hồ sơ nhập nhằng (*Ambiguous*). **Càng thấp càng tốt, 100% nghĩa là đoán bừa toàn bộ!**
- **UAR (Unnecessary-Abstention Rate - Tỷ lệ từ chối oan):** Tỷ lệ mô hình nói "tôi không biết" trên những hồ sơ vốn dĩ đã có đầy đủ bằng chứng rõ ràng (*Answerable*). **Càng thấp càng tốt!**
- **Safe Accuracy:** Điểm số toàn diện: Vừa đoán đúng khi đủ tin, vừa biết từ chối khi thiếu tin.

---

## PHẦN 6: MỔ XẺ 3 CÂU HỎI NGHIÊN CỨU & NHỮNG CON SỐ GIẬT MÌNH

Năm "anh tài" AI mạnh nhất được mang ra thử nghiệm: **GPT-5.5, GPT-5.6 Sol, DeepSeek-V4-Pro, Claude Opus 5, Qwen 3.7 Max**.

---

### 6.1. RQ1: Telemetry phát hiện lỗi có đủ để tìm nguồn gốc lỗi không? (§V-A, Bảng II, Hình 2)

Các tác giả cho 5 mô hình đọc 6 định dạng log khác nhau. Kết quả thu được tạo nên một cú sốc lớn:

```text
                  SO SÁNH GIỮA PHÁT HIỆN LỖI VÀ TÌM NGUỒN GỐC
100% ┌─────────────────────────────────────────────────────────────┐
     │ Detection F1 (Phát hiện lỗi): 99.5% - 100% ở MỌI định dạng! │
     └─────────────────────────────────────────────────────────────┘
  0% ┌─────────────────────────────────────────────────────────────┐
     │ Origin-Step Acc (Tìm đúng gốc): <= 0.5% ở OTel / Metadata! │
     └─────────────────────────────────────────────────────────────┘
```

#### Số liệu thực tế trong paper (Bảng II & Hình 2):
1. **Khi có đầy đủ thông tin (`Full`):**
   - Cả 5 mô hình đều phát hiện lỗi gần như hoàn hảo (Detection F1 từ $99.3\%$ đến $100.0\%$).
   - Về việc tìm đúng sự kiện gốc: **GPT-5.6 Sol** và **Claude Opus 5** xuất sắc đạt **$97.2\%$**, GPT-5.5 đạt $90.3\%$, DeepSeek-V4-Pro đạt $84.7\%$, còn Qwen 3.7 Max chỉ đạt $33.8\%$.
2. **Khi chuyển sang chuẩn công nghiệp (`Metadata`, `OpenTelemetry`, `OpenInference`):**
   - **Phát hiện lỗi:** Vẫn cực kỳ cao ($99.5\% - 100.0\%$). Hệ thống vẫn biết là có lỗi xảy ra.
   - **Tìm nguồn gốc lỗi:** **RƠI THẲNG XUỐNG DƯỚI $0.5\%$ (gần như bằng 0 tròn trĩnh)!**
   - Độ chính xác tìm component chỉ quanh quẩn $9.7\% - 11.1\%$ (đúng bằng xác suất nhắm mắt chọn bừa 1 trong 9 component).
3. **Mô hình đã nhìn vào đâu khi bị che bớt log?**
   - Dữ liệu causal stage chỉ ra: **$97.9\%$ dự đoán ở Metadata, $99.0\%$ ở OTel và $98.7\%$ ở OpenInference đều đổ dồn vào Downstream Symptom (sự kiện cập nhật sai)**!
   - Mô hình hoàn toàn bị "dắt mũi" bởi các triệu chứng hiển hiện ở hạ nguồn.

> 📢 **KẾT LUẬN RQ1:** Chuẩn OpenTelemetry hay OpenInference hiện nay rất tốt để làm còi báo động (Alerting), nhưng **không đủ bằng chứng ngữ nghĩa** để AI tìm ra ngọn nguồn sự cố!

---

### 6.2. RQ2: Bóc tách 7 nhân tố - Nhân tố nào là "Sinh mệnh" của chẩn đoán? (§V-B, Bảng III, Hình 3)

Thí nghiệm bóc tách từng nhân tố đã phơi bày cấu trúc nội tâm của quá trình suy luận RCA:

#### 1. Cú sập thế kỷ khi bỏ nhân tố `D` (Decision Content - Quyết định tham chiếu):
- Khi rút `D` ra khỏi bộ log (`Full-D`), độ chính xác định vị sự kiện gốc của **TOÀN BỘ 5 MÔ HÌNH RỚT THẲNG VỀ $0.0\%$!**
- Không một mô hình nào sống sót. Độ chính xác component rơi về đúng $11.1\%$ (ngẫu nhiên).
- Trong khi đó, khả năng phân loại loại lỗi (`Fault-type Macro-F1`) vẫn đạt $40\% - 88\%$. Nghĩa là mô hình vẫn biết đây là lỗi gì, nhưng hoàn toàn mù tịt về việc ai đã gây ra nó.
- **$98.1\%$ dự đoán của mô hình bị nhảy sang sự kiện Activation (nơi resolver tiêu thụ tham chiếu)**.

#### 2. Vai trò sống còn của `P` (Provenance - Nguồn gốc tra cứu):
- Bỏ `P` (`Full-P`), độ chính xác rớt từ $19.4$ đến $79.9$ điểm phần trăm. DeepSeek mất tới $79.9\%$ độ chính xác, Claude mất $68.8\%$.
- $66.7\%$ dự đoán bị trôi dạt về sự kiện Activation.

#### 3. Bộ ba bất khả xâm phạm: `I + D + P`
- Gom 4 nhân tố `I+D+P+V`: Cả 5 mô hình lấy lại phong độ xuất sắc, đạt độ chính xác từ **$86.1\%$ đến $100.0\%$**.
- Nhưng nếu vứt `I` đi (chỉ còn `D+P+V`): Độ chính xác lập tức sập xuống **$5.6\% - 61.8\%$** (mất từ $38.2$ đến $93.8$ điểm phần trăm!).
- *Giải thích đời thường:* Có quyết định sai (`D`), có sổ tra cứu (`P`), nhưng không có tên tuổi (`I`) thì AI biết gán tội cho ai?

#### 4. Nghịch lý dữ liệu hạ nguồn: "Nhiều log chưa chắc đã thông minh hơn!"
- Gom toàn bộ dữ liệu hạ nguồn `S+V+T` (Tool state + Verifier + Exception): **Tất cả các model đều đạt $0.0\%$ accuracy!**
- Ngược lại, khi bỏ `S` ra khỏi Full (`Full-S`): Độ chính xác của 4/5 mô hình **thậm chí còn tăng lên** (GPT-5.5 tăng từ $93.1\%$ lên thẳng $100.0\%$)!
- *Giải thích đời thường:* Dữ liệu tool chi tiết ở hạ nguồn đóng vai trò như **vật cản gây nhiễu (distractor)**, làm mô hình hoa mắt và kéo sự chú ý của nó về hiện trường vụ nổ thay vì kẻ đặt bom.

---

### 6.3. RQ3: AI có dám thừa nhận "Tôi không biết" khi dữ liệu mập mờ? (§V-D, Bảng IV)

Khi đưa cho các mô hình các cặp hồ sơ "Vụ án song sinh" (Rich-Ambiguous) dưới 4 chiến lược câu lệnh (prompt):

```text
               TỶ LỆ ĐOÁN MÒ (FAR) TRÊN HỒ SƠ NHẬP NHẰNG DƯỚI PROMPT P0
DeepSeek-V4-Pro : ████████████████████ 100.0% (Đoán bừa 100% số ca!)
Qwen 3.7 Max    : ████████████████████ 100.0% (Đoán bừa 100% số ca!)
GPT-5.5         : █████████████████▍   87.5%
GPT-5.6 Sol     : ████████▉            44.4%
Claude Opus 5   : ██▌                  12.5% (Cẩn trọng nhất!)
```

#### Những phát hiện chấn động từ Bảng IV:
1. **Khi dữ liệu sơ sài (Sparse-Ambiguous):** Cả 5 mô hình đều đạt **$0\%$ FAR** (đều ngoan ngoãn trả lời `INSUFFICIENT_EVIDENCE`).
2. **Cạm bẫy "Hồ sơ dày cộp" (Rich-Ambiguous):**
   - Khi hồ sơ nhìn bề ngoài có vẻ chi tiết, đầy đủ spans và metrics, **DeepSeek-V4-Pro và Qwen 3.7 Max nhắm mắt đoán bừa $100.0\%$ các ca!** Dù prompt P0 đã viết hoa cảnh báo rõ ràng.
   - GPT-5.5 cũng đoán bừa tới $87.5\%$.
   - Duy nhất **Claude Opus 5** thể hiện bản lĩnh chẩn đoán đáng tin cậy với FAR chỉ $12.5\%$.
3. **Hiệu lực thần kỳ của Prompt P3 (Contrastive Elimination - Loại trừ đối chứng):**
   - Khi đổi prompt sang P3 (bắt buộc mô hình: *"Phải tìm bằng chứng loại trừ các giả thuyết khác trước khi chốt"*):
     - **GPT-5.5:** Tỷ lệ đoán bừa giảm ngoạn mục từ $87.5\%$ xuống còn **$38.9\%$** (giảm $48.6\%$).
     - **GPT-5.6 Sol:** Giảm từ $44.4\%$ xuống còn **$13.9\%$** (giảm $30.6\%$).
     - **Claude Opus 5:** Giảm thẳng từ $12.5\%$ về **$0.0\%$ tuyệt đối** (không còn một ca đoán bừa nào)!
   - **Tuy nhiên, với DeepSeek và Qwen:** Prompt P3 **HOÀN TOÀN BẤT LỰC** (vẫn lì lợm đoán bừa $100.0\%$).
4. **Cái giá phải trả (Safety–Utility Trade-off):**
   - Ép mô hình cẩn trọng hơn bằng P3 khiến nó trở nên "đa nghi" hơn, làm tăng tỷ lệ từ chối oan trên các ca vốn dĩ giải được (UAR của GPT-5.6 Sol tăng từ $24.3\%$ lên $34.0\%$).

---

## PHẦN 7: ĐÁNH GIÁ PHẢN BIỆN (CRITICAL APPRAISAL)

Để ứng dụng một bài báo vào luận văn thạc sĩ/tốt nghiệp, ta không thể khen một chiều mà phải nhìn rõ cả điểm mạnh lẫn điểm yếu của nó:

### 7.1. Điểm xuất sắc vượt bậc (Strengths)
1. **Tính hợp lệ nội tại tuyệt đối (Strict Internal Validity):** Cùng một lần chạy, tác giả chỉ đổi "kính lọc" (deterministic projections), loại bỏ hoàn toàn sự hên xui do môi trường ngẫu nhiên.
2. **Chuẩn vàng khách quan cho bài toán từ chối (Exact Ambiguity):** Việc ép hai kịch bản lỗi khác nhau có cùng biểu diễn byte JSON tạo ra một phép thử toán học không thể cãi cãi. Không cần dựa vào cảm tính hay dùng LLM Judge để chấm điểm.
3. **Kỷ luật khoa học mẫu mực:** Có tập kiểm chứng mù đóng băng (frozen blind holdout), bootstrap 10.000 lần, phạt 0 điểm cho mọi output lỗi cú pháp JSON.

### 7.2. Điểm hạn chế & Điểm mù (Limitations)
1. **Miền bài toán hẹp và nhân tạo (Synthetic Setup):** Lỗi hầu như xoay quanh việc gán nhầm tham chiếu symbolic reference trên ứng dụng xử lý đơn hàng/vé giả lập. Hệ thống microservices thực tế phức tạp hơn nhiều (tràn bộ nhớ, nghẽn mạng, race condition...).
2. **Quan sát tĩnh (Passive Traces) thay vì Tương tác (Interactive Debugging):**
   - TelemetrySuffBench vứt cho mô hình một tệp trace tĩnh rồi bắt đoán.
   - Ngoài đời, một kỹ sư SRE giỏi khi thấy thiếu thông tin sẽ **gõ thêm lệnh** (`kubectl logs`, `kubectl describe`) để lấy thêm dữ liệu. Paper chưa đo lường được khả năng "chủ động truy vấn để giải quyết mâu thuẫn" (*active disambiguation*).
3. **Chưa giải quyết bài toán dữ liệu cũ/lỗi thời (Stale Telemetry):** Paper có nhãn `stale_reference_state` nhưng bản chất vẫn là tham chiếu sai logic, chưa phải hiện tượng log bị trễ hay metric bị cache trong hạ tầng mạng.

---

## PHẦN 8: KIM CHỈ NAM CHO LUẬN VĂN: ĐƯA TOÀN BỘ TƯ TƯỞNG BÀI BÁO VÀO KUBERNETES

> **Đề tài Luận văn của nhóm bạn:**  
> **Selective Root Cause Analysis under Incomplete Telemetry in Kubernetes**  
> *(Chẩn đoán nguyên nhân gốc có chọn lọc trong môi trường Kubernetes khi dữ liệu vận hành bị thiếu hụt)*

Đây là phần quan trọng nhất: Làm sao "xào nấu" tinh hoa của TelemetrySuffBench vào đề tài Kubernetes của bạn để đạt điểm tối đa trước hội đồng?

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   TAM GIÁC VÀNG CHO ĐỀ TÀI LUẬN VĂN CỦA BẠN                            │
├───────────────────────────────┬────────────────────────────────────────────────────────┤
│ NGUỒN HỌC HỎI                 │ BẠN LẤY ĐƯỢC GÌ CHO LUẬN VĂN?                          │
├───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. TelemetrySuffBench         │ • Nền tảng lý thuyết: Tại sao thiếu dữ liệu thì        │
│    (Paper hiện tại)           │   BẮT BUỘC phải Abstain (từ chối kết luận)?            │
│                               │ • Kỹ thuật tạo benchmark: Exact-Equal Ambiguity.       │
│                               │ • Bộ thước đo: FAR, UAR, Safe Accuracy, Coverage.      │
│                               │ • Chiến thuật Prompt P3 (Contrastive Elimination).     │
├───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 2. Cloud-OpsBench             │ • Môi trường thực tế: Hệ thống Microservices chạy      │
│    (Môi trường K8s)           │   trên cụm Kubernetes thật.                            │
│                               │ • Vòng lặp Agent tương tác gõ lệnh bằng Read-only tools│
├───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 3. DiagGuard                  │ • Bộ phân loại lỗi suy luận (Taxonomy: OMIT, MIS, GEN).│
│    (Kiến trúc Verifier)       │ • Cơ chế gác cổng (Guard / Verifier) trước khi commit. │
└───────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

### 8.1. Bài học 1: Ánh xạ chuỗi nhân quả 5 chặng sang sự cố Kubernetes

Khi thuyết trình luận văn, hãy chiếu sơ đồ này để chứng minh bạn hiểu sâu bản chất nhân quả:

```text
[CHẶNG 1: ORIGIN (Gốc rễ sự cố)]
   └── Kỹ sư cấu hình sai trong YAML: Viết nhầm Service selector `app: payment-v2` 
       thành `app: payment-v1` (tương đương nhân tố Decision `D` bị sai).
           ↓
[CHẶNG 2: INTERMEDIATE (K8s Control Plane Reconcile)]
   └── Kube-controller-manager cập nhật trạng thái Service. Service được tạo thành công,
       không hề có lỗi cú pháp văng ra.
           ↓
[CHẶNG 3: ACTIVATION & DEVIATION (Lỗi hiển lộ ngầm)]
   └── EndpointSlice của Service bị rỗng (`endpoints: []`) vì không có Pod nào khớp nhãn.
           ↓
[CHẶNG 4: SYMPTOM (Triệu chứng thực thi)]
   └── Ingress Nginx nhận request gửi tới `/pay`, tìm Service không thấy Endpoint nào,
       ném ra lỗi `HTTP 503 Service Temporarily Unavailable`.
           ↓
[CHẶNG 5: TERMINAL (Cảnh báo kết thúc)]
   └── Prometheus phát hiện tỷ lệ 5xx vượt ngưỡng, Alertmanager bắn tin nhắn lên Slack.
```

> 💡 **Điểm mấu chốt để bảo vệ luận văn:**  
> Nếu Agent RCA của bạn chỉ đọc log Nginx (Chặng 4) và Prometheus alert (Chặng 5) - tức là chỉ có dữ liệu hạ nguồn `S+V+T`, thì theo TelemetrySuffBench, **khả năng Agent đoán đúng nguyên nhân gốc là $0\%$!** Agent bắt buộc phải có tool chạy `kubectl get endpoints` (Chặng 3) và `kubectl describe svc` (Chặng 1).

---

### 8.2. Bài học 2: Cách tạo Benchmark "Incomplete Telemetry" chuẩn chỉnh bằng kỹ thuật "Vụ án song sinh"

Trong nghiên cứu khoa học, nếu bạn tự tạo ra một ca lỗi rồi tự phán: *"Ca này tôi thấy thiếu dữ liệu nên Agent phải trả lời không biết"*, hội đồng sẽ phản biện: *"Đó là do bạn nghĩ thế, biết đâu mô hình khác nó vẫn suy luận ra được!"*.

**Hãy dùng chiêu thức Exact-Equal Ambiguity của TelemetrySuffBench để phản biện lại:**
Xây dựng một cặp sự cố trong Kubernetes có **biểu hiện quan sát giống hệt nhau khi bị thiếu công cụ**:

- **Sự cố 1:** Service trỏ sai `targetPort` (Port 8080 thay vì 80).
- **Sự cố 2:** Ứng dụng bên trong Container bị deadlock, không lắng nghe trên Port 80.
- **Tạo môi trường Incomplete:** Bạn cố tình vô hiệu hóa tool `kubectl exec` và tool xem cấu hình runtime, chỉ cho Agent xem log của Ingress Gateway và trạng thái Pod.
  - Cả 2 sự cố đều cho ra cùng một biểu hiện: *Ingress báo HTTP 502/503, Pod status vẫn `Running 1/1`*.
  - Lúc này, về mặt toán học: $P(\text{Sự cố 1}) = P(\text{Sự cố 2})$.
  - **Nhãn chuẩn khách quan:** Bất kỳ Agent nào vội vàng kết luận là do targetPort hay do treo app đều bị tính là **Đoán mò vô căn cứ (Unsupported Commit - FAR)**. Agent thông minh bắt buộc phải trả về: **`INSUFFICIENT_EVIDENCE` (Abstain)**!

---

### 8.3. Bài học 3: Kế thừa Bộ chỉ số đánh giá (Evaluation Metrics)

Trong bài báo luận văn, hãy dùng chính xác bảng chỉ số này để nghiệm thu kết quả:
1. **Coverage (Độ phủ):** Tỷ lệ ca mà Agent dám đưa ra kết luận (không từ chối):
   $$\text{Coverage} = \frac{\text{Số ca kết luận}}{\text{Tổng số ca}}$$
2. **Selective Error:** Tỷ lệ đoán sai **trong số những ca mà Agent đã dám kết luận** (đo lường độ an toàn khi đã mở miệng nói).
3. **FAR (False-Answer Rate):** Tỷ lệ đoán bừa trên tập hồ sơ thiếu bằng chứng (càng thấp càng tốt).
4. **UAR (Unnecessary-Abstention Rate):** Tỷ lệ từ chối oan trên tập hồ sơ đầy đủ bằng chứng (càng thấp càng tốt).
5. **Safe Accuracy:** Điểm số an toàn toàn diện:
   $$\text{Safe Accuracy} = \frac{\text{Số ca đoán đúng trên tập Đủ} + \text{Số ca từ chối đúng trên tập Thiếu}}{\text{Tổng số ca thử nghiệm}}$$

---

### 8.4. Bài học 4: Thiết kế Prompt P3 & Cơ chế Gác cổng (Verifier Gatekeeper)

Dựa trên phát hiện về Prompt P3, bạn hãy tích hợp quy tắc này vào prompt hệ thống của Agent chẩn đoán:

```markdown
### QUY TẮC PHẢN BIỆN LOẠI TRỪ (CONTRASTIVE ELIMINATION PROTOCOL):
Trước khi đưa ra kết luận cuối cùng về Root Cause, bạn BẮT BUỘC phải thực hiện 3 bước:
1. Liệt kê ít nhất 2 giả thuyết nguyên nhân khác nhau có thể dẫn tới triệu chứng này.
2. Với mỗi giả thuyết, chỉ ra bằng chứng cụ thể (log, metric, cấu hình) bạn ĐÃ THU THẬP ĐƯỢC 
   chứng minh hoặc bác bỏ nó.
3. NẾU dữ liệu hiện có không thể loại trừ dứt điểm một trong các giả thuyết, hoặc thiếu bằng chứng 
   trực tiếp từ cấu hình/trạng thái K8s:
   --> BẠN BẮT BUỘC PHẢI TRẢ VỀ: "INSUFFICIENT_EVIDENCE" (Abstain).
   --> TUYỆT ĐỐI KHÔNG ĐƯỢC ĐOÁN MÒ MỘT NGUYÊN NHÂN DUY NHẤT!
```

---

## TỔNG KẾT BÀI HỌC CỐT LÕI (TAKEAWAY GHI NHỚ)

1. **Có log không có nghĩa là có thể chẩn đoán (Observability $\neq$ Diagnostic Adequacy).** Đừng bị đánh lừa bởi những bản trace dài hàng nghìn dòng.
2. **Kẻ gây lỗi (Origin) luôn khác với nơi chịu hậu quả (Symptom/Terminal).** Nếu telemetry không ghi lại được quyết định thượng nguồn (`D`) và nguồn gốc tra cứu (`P`), độ chính xác định vị nguyên nhân gốc sẽ là **$0\%$**.
3. **Đừng nhồi nhét quá nhiều log hạ nguồn (`S+V+T`).** Chúng chỉ làm Agent hoa mắt và đổ tội cho các thành phần vô tội.
4. **Khi dữ liệu thiếu hụt hoặc nhập nhằng, LLM có xu hướng đoán mò cực kỳ nguy hiểm.** Biện pháp cứu cánh là ép mô hình phải **phản biện loại trừ (Prompt P3)** và trang bị cơ chế **từ chối an toàn (Safe Abstention)**.
5. **Áp dụng vào Luận văn:** Dùng kỹ thuật *Exact-Equal Ambiguity* để tạo benchmark khách quan, đo lường bằng *Risk–Coverage / FAR / UAR*, và xây dựng Agent biết dừng lại đúng lúc khi dữ liệu Kubernetes bị suy giảm!