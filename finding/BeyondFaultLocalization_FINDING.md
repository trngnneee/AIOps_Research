# Finding: Beyond Fault Localization (DiagGuard)

**Paper gốc:** *Beyond Fault Localization: A Trajectory-Level Study of LLM Agents for Microservice Root Cause Analysis* (Qisheng Lu, Aoyang Fang, Junjielong Xu, et al. - CUHK Shenzhen & Xi'an Jiaotong University).  
**Vị trí file PDF:** `paper/Beyond Fault Localization.pdf` (23 trang).  
**Trạng thái:** Nhận xét, phân tích chuyên sâu và đối chiếu trực tiếp với bản gốc PDF của người đọc.

---

## 1. Bài toán cốt lõi & Động lực nghiên cứu (§1, §2)

### 1.1. Lỗ hổng của cách đánh giá cũ (Outcome-Level)
- Các nghiên cứu RCA (Root Cause Analysis) trước đây hầu như chỉ chấm điểm ở đầu ra cuối cùng: $Acc@k$, $MRR$, $MAP$ (tức là xem Agent có đoán trúng tên Service bị lỗi không).
- **Thực tế nguy hiểm:** Kỹ sư vận hành (SRE) không thể tin cậy một chẩn đoán nếu chỉ có mỗi cái nhãn. Họ cần chuỗi bằng chứng (evidence) và đường dẫn lan truyền lỗi (*fault propagation path*). 
- Phân tích của paper chỉ ra: **Rất nhiều Agent đoán đúng chỉ do ăn may, ảo giác hoặc suy luận sai bét** (ví dụ: chưa từng đọc metric của service bị lỗi, hoặc lấy log sau khi sự cố kết thúc để làm bằng chứng).

### 1.2. Hướng tiếp cận của Paper: Trajectory-Level Study
- Thu thập và giải phẫu **5.000 quỹ đạo suy luận (reasoning trajectories)** của **9 framework** (cả agent chuyên RCA như *GoS, OpsAgent, mABC, OpenRCA* lẫn agent lập trình/nghiên cứu tổng quát như *ThinkDepth.ai, Claude Code*) chạy trên 3 mô hình nền tảng (*Qwen 3.5 Plus, Claude Sonnet 4.6, Doubao Seed 2.0*).
- Đưa ra 2 metric mới đo lường khả năng dựng lại hiện trường sự cố:
  - **Node F1:** Đo tỷ lệ nhận diện đúng các service nằm trong diện bị ảnh hưởng trên chuỗi sự cố.
  - **Edge F1:** Đo tỷ lệ dựng lại đúng các mắt xích/quan hệ gọi RPC trực tiếp giữa service gây lỗi và service bị ảnh hưởng.

---

## 2. 5 Phát hiện thực nghiệm quan trọng (Core Findings §5)

Đây là những hiểu biết sâu sắc (insights) rút ra từ 5.000 trajectories mà bất kỳ ai làm Agent RCA cũng cần nắm:

- **Finding 1 (Kiến trúc linh hoạt ăn đứt quy trình cứng nhắc):** Các framework linh hoạt, ít ràng buộc (như agent dạng ReAct/deep research) lại chẩn đoán tốt hơn các agent bị ép theo workflow quá chặt chẽ. Ở nhóm top đầu, **năng lực của mô hình nền tảng (Backbone Model) mới là yếu tố quyết định nhất**.
- **Finding 2 (Biết ai lỗi dễ hơn biết tại sao lỗi lan truyền):** Điểm $Edge\ F1$ luôn thấp hơn $Node\ F1$ rất nhiều (thường rớt 43–69% khi Agent thất bại). Ngay cả khi Agent đoán trúng Root Cause ($Acc@1$ đúng), $Edge\ F1$ thực tế chưa bao giờ vượt quá **0.67**. Tức là Agent gần như **không bao giờ dựng lại được đầy đủ chuỗi lan truyền lỗi**. Càng sự cố nhiều chặng (*causal depth* lớn), Agent càng dễ gãy.
- **Finding 3 (Càng lúng túng càng tốn tiền - "Unproductive Search"):** Nhiều round truy vấn hơn **không hề** giúp Agent thông minh hơn. Các lượt chạy thất bại tiêu tốn số round và token cao hơn hẳn lượt thành công, vì Agent bị lạc đường, spam tool calls vô nghĩa và đốt budget.
- **Finding 4 (Kỷ luật quy trình quyết định thắng bại):** Agent thành công là Agent biết bám chặt vào vùng ảnh hưởng (*fault-impact surface*) và **thực sự sử dụng bằng chứng vừa lấy được** cho bước tiếp theo. Agent thất bại thường bị trôi dạt ra ngoài vùng lỗi hoặc nhặt bằng chứng xong vứt xó.
- **Finding 5 (Vốn từ vựng chẩn đoán - Intent Repertoire):** Agent mạnh (như Claude Sonnet) có bộ ý định đa dạng (chuyển đổi linh hoạt giữa đọc log, soi metric, theo vết trace, kiểm tra tài nguyên). Agent yếu hơn (như Qwen) bị kẹt trong các vòng lặp nông (ví dụ lặp đi lặp lại việc trace span hoặc soi log một chỗ).

---

## 3. Bảng mã lỗi xử lý bằng chứng (Failure Taxonomy - Bảng 3, §5.3)

Paper hệ thống hóa toàn bộ các cú vấp ngã của Agent thành **3 họ lỗi lớn gồm 11 mã lỗi cụ thể**:

```text
Evidence-Handling Failures (11 Failure Modes)
├── 1. Protocol Omissions (OMIT) - Lười & Bỏ qua bằng chứng sống còn
│   ├── OMIT1 (Baseline gap): Không so sánh với lúc bình thường (thấy CPU 80% tưởng lỗi, dù ngày thường vẫn thế).
│   ├── OMIT2 (Edge untested): Khẳng định Service A gọi Service B gây lỗi nhưng không hề mở trace span giữa A và B ra xem.
│   ├── OMIT3 (Resource gap): Không kiểm tra metric/lifecycle của tài nguyên cụ thể (tên pod, node, disk).
│   ├── OMIT4 (Ranking gap): Không xếp hạng đối chứng với các pod đồng cấp xem bất thường này là cá biệt hay đại trà.
│   ├── OMIT5 (Granularity gap): Chỉ dừng ở cấp Service, lười đào sâu xuống Pod/Container/Endpoint cụ thể.
│   └── OMIT6 (Timing gap): Sai mốc thời gian (lấy sự kiện lúc 10:15 để giải thích cho lỗi xảy ra lúc 10:00).
├── 2. Semantic Misreads (MIS) - Có dữ liệu nhưng đọc hiểu sai
│   ├── MIS1 (Silence-as-health): Thấy metric phẳng lặng hoặc log trống thì tưởng bình thường (thực ra service đã chết đứng).
│   ├── MIS2 (Salience bias): Bắt nhầm "nạn nhân" (thấy Frontend đỏ lòm vì nghẽn thì đổ tội, dù thủ phạm là DB bên dưới).
│   └── MIS3 (Semantics misread): Đọc lộn chiều gọi caller vs callee, hoặc nhầm lẫn client error vs server error.
└── 3. General Reasoning (GEN) - Suy luận bịa đặt hoặc bảo thủ
    ├── GEN1 (Anchor lock): Cố chấp bám chặt giả thuyết ban đầu dù bằng chứng các bước sau đã bác bỏ nó.
    ├── GEN2 (Schema-out claim): Tự bịa ra một loại lỗi/trạng thái không hề có trong hệ thống.
    └── GEN3 (Friction stop): Hơi tí gặp lỗi tool query hoặc trả về rỗng là bỏ cuộc, ngắt luôn kênh dữ liệu đó.
```

> **So sánh thú vị giữa các Model (§5.3):**  
> - **Qwen:** Mắc bệnh **OMIT** nặng nhất (lười đào sâu, hay chạy vòng tròn lặp lại: OMIT1 chiếm 51.9%, OMIT3 chiếm 63.5%).
> - **Sonnet:** Ít khi bỏ sót bằng chứng, nhưng lại cực kỳ hay mắc **MIS3** (86.0% đọc hiểu sai ngữ nghĩa caller-callee) và **GEN2** (82.0% ảo giác bịa ra lỗi ngoài schema do liên tưởng quá đà).

---

## 4. Giải pháp DiagGuard: Cơ chế phòng vệ 2 lớp (§6.1, Hình 6a)

DiagGuard được thiết kế như một lớp vỏ bọc bảo vệ (Guard) xung quanh Agent chẩn đoán (*Diagnostician*) tại **3 thời điểm quan trọng**, hoàn toàn độc lập với câu trả lời (*answer-agnostic*):

```text
       [1. Trước khi truy vấn lần đầu]
                     ↓
          GROUNDER: Cung cấp Search Space Profile
          (Đưa sẵn bản đồ thực tế của hệ thống: các bảng, metrics, pods hiện có 
           → Chặn lỗi OMIT3, OMIT5 và ngăn ảo giác GEN2)
                     ↓
       [2. Trước khi bắt đầu bước điều tra]
                     ↓
          VERIFIER: Diagnostic Self-Audit
          (Checklist nhắc nhở: "Đã so sánh baseline OMIT1 chưa? Đã kiểm tra mốc thời gian OMIT6 chưa?")
                     ↓
           [Agent thực hiện điều tra qua Tools...]
                     ↓
       [3. Trước khi chốt kết luận cuối cùng (Pre-commitment)]
                     ↓
          VERIFIER: Soundness Check
          (Hạch hỏi bằng chứng: "Kết luận này dựa trên log/metric nào? Có mâu thuẫn 
           với dữ liệu nào trước đó không? Đã kiểm tra cạnh lan truyền OMIT2 chưa?")
```

### Kết quả can thiệp (§6.2, §6.3 - Bảng 4):
- Giúp cải thiện độ chính xác $Acc@1$ trên toàn bộ 14 cấu hình thử nghiệm, mức tăng trung vị là **+10.5%** (có trường hợp tăng tới **+35.1%**).
- **Ablation test (Bóc tách thành phần):** 
  - Chỉ dùng Grounder: Tăng $+4.5\%$.
  - Chỉ dùng Verifier: Tăng $+4.1\%$.
  - Kết hợp cả hai (Full DiagGuard): Tăng $+9.0\%$.

---

## 5. Điểm mù của DiagGuard & Research Gap cho Luận văn (Khai thác chuyên sâu)

Khi đặt DiagGuard vào bài toán thực tế của luận văn (Kubernetes RCA với dữ liệu thiếu hoặc cũ), DiagGuard bộc lộ **3 điểm mù rất lớn**:

### Điểm mù 1: Giả định môi trường "hoàn hảo" (Đầy đủ Telemetry)
- Toàn bộ cơ chế nhắc nhở của DiagGuard giả định rằng: *Nếu Agent chịu khó query thì dữ liệu luôn nằm sẵn trong cơ sở dữ liệu để đọc.*
- **Thực tế đề tài nhóm:** Khi telemetry bị **thiếu khách quan (Incomplete/Missing)** do agent collector bị nghẽn, log bị rớt hoặc mạng chập chờn; hoặc **dữ liệu bị lỗi thời (Stale)** do Pod vừa bị restart/rollout. Lúc này Verifier đòi hỏi bằng chứng thì Agent cũng **không thể lấy đâu ra dữ liệu**! DiagGuard hoàn toàn bất lực trước kịch bản này.

### Điểm mù 2: Thiếu cơ chế "Dừng lại / Từ chối kết luận" (Abstention / Selective RCA)
- DiagGuard ép Agent phải trải qua *Soundness Check*, nhưng cuối cùng **vẫn bắt Agent phải chốt 1 con service chịu tội**.
- Khi telemetry bị thiếu làm cho 2 giả thuyết H1 và H2 ngang cơ nhau, việc bắt buộc chốt đáp án sẽ biến thành **đoán mò có kiểm soát**. 
- **Cơ hội cho đề tài:** Thiết kế một cơ chế Selective RCA: Khi Verifier thấy bằng chứng bị thiếu hụt không thể phân biệt nguyên nhân, Agent được quyền trả về: **"Chưa đủ dữ liệu để kết luận duy nhất (Abstain)"**.

### Điểm mù 3: Chưa có cơ chế truy vấn phân biệt nguyên nhân (Hypothesis-Driven Differential Query)
- DiagGuard nhắc Agent *"hãy kiểm tra đi"*, nhưng không chỉ ra *"nếu đang phân vân giữa H1 và H2 thì câu query nào là phép thử mang tính quyết định (decisive test)?"*.
- Đây là nhánh mở rộng cực kỳ giá trị cho đề tài: Định hướng Agent tìm đúng telemetry mang tính phân định thay vì spam query tốn kém.

---

## 6. Kế hoạch hành động cụ thể cho Nhóm

1. **Kế thừa bộ Failure Taxonomy:** Sử dụng nguyên vẹn hoặc rút gọn bộ mã lỗi **Table 3** (nhất là `OMIT1` baseline, `OMIT3` resource, `OMIT6` timing, `MIS1` silence, `MIS2` salience, `GEN1` anchor) làm tiêu chí chấm điểm và phân tích lỗi cho các thí nghiệm của nhóm.
2. **Kế thừa Metric:** Sử dụng $Node\ F1$ và $Edge\ F1$ bên cạnh $Acc@1$ để chứng minh giải pháp của nhóm không chỉ đoán trúng rùa mà còn hiểu đúng quy trình lan truyền lỗi.
3. **Mở rộng kiến trúc Verifier:** Giữ lại tư tưởng *Self-Audit* và *Soundness Check* của DiagGuard, nhưng trang bị thêm 2 module mới:
   - **Data Completeness & Freshness Check:** Kiểm tra xem telemetry lấy về có bị đứt gãy hoặc cũ hơn thời điểm rollout không.
   - **Selective Gatekeeper:** Cho phép Agent đưa ra phán quyết *"Chưa đủ bằng chứng"* để tránh đoán bừa khi telemetry bị suy giảm.
