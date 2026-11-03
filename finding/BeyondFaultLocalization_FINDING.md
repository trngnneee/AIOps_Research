# Finding: Beyond Fault Localization (DiagGuard)

**Paper:** *Beyond Fault Localization: A Trajectory-Level Study of LLM Agents for Microservice Root Cause Analysis* (Qisheng Lu, Aoyang Fang, Junjielong Xu, et al. - CUHK Shenzhen & Xi'an Jiaotong University)
**PDF:** `paper/Beyond Fault Localization.pdf` (23 trang)
**Quy ước đọc file này:** phần có nhãn **[Paper]** là điều paper nói (kèm § / Bảng). Phần có nhãn **[Diễn giải]** là nhận xét/đề xuất của reader, chưa phải kết luận của paper.

---

## 📌 CHEATSHEET (đọc lại trong 2 phút)

**Một câu:** Agent RCA đoán đúng tên service chưa chắc đã điều tra đúng. Paper chấm cả *quá trình* (trajectory), chỉ ra agent hay hỏng ở khâu xử lý bằng chứng, rồi thêm lớp bảo vệ **DiagGuard** để giảm lỗi đó.

**Quy mô thí nghiệm [Paper §1, §4]:** 5.000 trajectories · 9 framework (GoS, OpsAgent, mABC, OpenRCA, ThinkDepth.ai, Claude Code…) · 3 model (Qwen 3.5 Plus, Claude Sonnet 4.6, Doubao Seed 2.0).

**2 metric mới:**

| Metric | Đo cái gì |
| --- | --- |
| **Node F1** | Agent tìm đúng bao nhiêu service bị ảnh hưởng |
| **Edge F1** | Agent dựng lại đúng bao nhiêu mắt xích gọi RPC giữa service lỗi và service bị ảnh hưởng |

**5 phát hiện [Paper §5]:**

| # | Ý chính (1 dòng) |
| --- | --- |
| F1 | Agent linh hoạt (ReAct/deep research) thường tốt hơn agent bị ép workflow cứng. Ở nhóm đầu, **model nền** quyết định nhất |
| F2 | **Biết "ai lỗi" dễ hơn biết "lỗi lan thế nào"**: Edge F1 << Node F1; kể cả khi đoán đúng root cause, Edge F1 không vượt **0.67** |
| F3 | Nhiều round hơn **không** thông minh hơn: lượt thất bại tốn round/token hơn lượt thành công (lạc đường, spam tool) |
| F4 | Thành công = bám vùng ảnh hưởng và **dùng thật** bằng chứng vừa lấy. Thất bại = trôi ra ngoài hoặc lấy xong bỏ xó |
| F5 | Model mạnh (Sonnet) đổi ý định điều tra linh hoạt (log → metric → trace → tài nguyên). Model yếu (Qwen) lặp vòng nông |

**11 mã lỗi, 3 họ [Paper Bảng 3, §5.3]:**

| Họ | Nghĩa | Mã |
| --- | --- | --- |
| **OMIT** (bỏ sót) | Không đi kiểm tra bằng chứng cần thiết | OMIT1 baseline · OMIT2 cạnh chưa test · OMIT3 tài nguyên · OMIT4 xếp hạng đối chứng · OMIT5 độ phân giải (service vs pod) · OMIT6 mốc thời gian |
| **MIS** (đọc sai) | Có dữ liệu nhưng hiểu sai | MIS1 im lặng ≠ khỏe · MIS2 bắt nhầm nạn nhân (salience) · MIS3 nhầm caller/callee |
| **GEN** (suy luận) | Lập luận cố chấp hoặc bịa | GEN1 bám giả thuyết đầu · GEN2 bịa lỗi ngoài schema · GEN3 gặp lỗi tool là bỏ kênh dữ liệu |

Khác biệt giữa model: **Qwen** hay OMIT (OMIT1 51.9%, OMIT3 63.5%). **Sonnet** ít OMIT nhưng hay MIS3 (86.0%) và GEN2 (82.0%).

**DiagGuard [Paper §6.1, Hình 6a]:** vỏ bọc quanh agent, 3 điểm chạm, không cần biết đáp án:

1. **Grounder** (trước truy vấn đầu): đưa sẵn "bản đồ" hệ thống thật (bảng, metric, pod) → chặn OMIT3, OMIT5, GEN2.
2. **Verifier: Self-Audit** (trước khi điều tra): checklist nhắc baseline, timing…
3. **Verifier: Soundness Check** (trước khi chốt): "kết luận dựa trên bằng chứng nào? có mâu thuẫn không? đã test cạnh lan truyền chưa?"

**Kết quả [Paper §6.2-6.3, Bảng 4]:** Acc@1 tăng ở cả 14 cấu hình, trung vị **+10.5%**, cao nhất **+35.1%**. Ablation: chỉ Grounder +4.5% · chỉ Verifier +4.1% · đủ cả hai +9.0%.

**3 điểm mù [Diễn giải]:**

1. Giả định dữ liệu **luôn có sẵn**; telemetry thiếu hoặc cũ thì Verifier đòi bằng chứng cũng vô ích.
2. **Không cho phép abstain**: luôn bắt chốt 1 service.
3. Chỉ nhắc "hãy kiểm tra", không chỉ ra **query nào phân biệt được H1 vs H2**.

**Dùng cho luận văn [Diễn giải]:** (a) mượn taxonomy làm tiêu chí chấm lỗi · (b) báo cáo Node/Edge F1 cùng Acc@1 · (c) giữ Self-Audit + Soundness Check, thêm **Data Completeness/Freshness Check** và **Selective Gatekeeper (abstain)**.

---

## 1. Đọc nhanh: paper này nói gì?

### 1.1. Vấn đề
Các paper RCA trước chỉ chấm **kết quả cuối** (Acc@k, MRR, MAP): đoán trúng service lỗi là đạt [Paper §1, §2].

Ví dụ: một học sinh ghi đúng đáp số nhưng bài làm sai bước. Giáo viên chấm đáp số thì cho điểm tuyệt đối, nhưng không ai dám tin em đó làm được bài tương tự.

Kỹ sư SRE cũng vậy. Họ cần **chuỗi bằng chứng** và **đường lan truyền lỗi** (*fault propagation path*) mới dám hành động. Paper thấy nhiều agent đoán đúng nhờ may, ảo giác hoặc suy luận sai. Ví dụ: chưa từng đọc metric của service lỗi, hoặc dùng log *sau* khi sự cố kết thúc làm bằng chứng.

### 1.2. Cách làm
Thu 5.000 trajectories (toàn bộ các bước suy luận + tool call của agent), rồi chấm **quá trình**, không chỉ đáp án. Hai metric mới ở trên là công cụ chấm.

---

## 2. Năm phát hiện, giải thích kèm ý nghĩa [Paper §5]

**F1. Linh hoạt thắng cứng nhắc.**
Workflow cố định như "bước 1 đọc log, bước 2 đọc metric…" hay vướng khi sự cố không đi theo kịch bản. Agent kiểu ReAct tự chọn bước nên thích nghi tốt hơn. Trong nhóm top, khác biệt chính đến từ model nền.
→ *Ý nghĩa:* đừng đầu tư vào pipeline cứng; đầu tư vào chất lượng kiểm tra bằng chứng.

**F2. Biết ai lỗi dễ hơn biết lỗi lan thế nào.**
Edge F1 thấp hơn Node F1 nhiều (thường rớt 43-69% khi agent thất bại). Kể cả khi Acc@1 đúng, Edge F1 chưa bao giờ vượt **0.67**. Sự cố càng nhiều chặng (*causal depth* lớn), agent càng dễ gãy.
→ *Ý nghĩa:* "đoán trúng" không có nghĩa là "hiểu cơ chế".

**F3. Càng lúng túng càng tốn.**
Lượt thất bại tốn nhiều round và token hơn lượt thành công. Agent lạc đường thì spam tool call vô ích (*unproductive search*).
→ *Ý nghĩa:* tăng budget không cứu được agent đi sai hướng.

**F4. Kỷ luật quy trình quyết định thắng bại.**
Agent thắng làm hai việc: ở lại trong *fault-impact surface* (vùng bị ảnh hưởng) và dùng bằng chứng vừa thu cho bước kế tiếp. Agent thua trôi ra ngoài vùng lỗi, hoặc nhặt bằng chứng xong không dùng.

**F5. Vốn "ý định điều tra" (Intent Repertoire).**
Sonnet chuyển qua lại giữa đọc log, soi metric, theo trace, kiểm tra tài nguyên. Qwen kẹt trong vòng lặp nông (trace span mãi, hoặc soi một chỗ log).

---

## 3. Bảng mã lỗi chi tiết (Failure Taxonomy) [Paper Bảng 3, §5.3]

```text
Evidence-Handling Failures (3 họ, 11 mã)
├── OMIT: bỏ sót bằng chứng cần thiết
│   ├── OMIT1 Baseline gap    - không so với lúc bình thường (CPU 80% tưởng lỗi, ngày thường vẫn thế)
│   ├── OMIT2 Edge untested   - nói "A gọi B gây lỗi" nhưng không mở trace A→B ra xem
│   ├── OMIT3 Resource gap    - không kiểm tra metric/lifecycle của pod, node, disk cụ thể
│   ├── OMIT4 Ranking gap     - không so với pod cùng cấp: bất thường này riêng lẻ hay đại trà?
│   ├── OMIT5 Granularity gap - dừng ở cấp service, không đào xuống pod/container/endpoint
│   └── OMIT6 Timing gap      - dùng sự kiện 10:15 để giải thích lỗi lúc 10:00
├── MIS: có dữ liệu nhưng đọc sai
│   ├── MIS1 Silence-as-health - metric phẳng/log trống tưởng bình thường (thực ra service đã chết)
│   ├── MIS2 Salience bias     - đổ lỗi cho nạn nhân (Frontend đỏ vì nghẽn, thủ phạm là DB phía dưới)
│   └── MIS3 Semantics misread - lẫn chiều caller/callee, hoặc client error/server error
└── GEN: lập luận cố chấp hoặc bịa
    ├── GEN1 Anchor lock      - bám giả thuyết đầu dù bằng chứng sau bác bỏ
    ├── GEN2 Schema-out claim - bịa loại lỗi/trạng thái không tồn tại trong hệ thống
    └── GEN3 Friction stop    - tool lỗi hoặc trả rỗng một lần là bỏ luôn kênh dữ liệu đó
```

**So sánh model [Paper §5.3]:**
- **Qwen:** nặng OMIT, lười đào sâu (OMIT1 51.9%, OMIT3 63.5%).
- **Sonnet:** ít bỏ sót, nhưng hay đọc sai ngữ nghĩa MIS3 (86.0%) và bịa ngoài schema GEN2 (82.0%).

---

## 4. DiagGuard hoạt động thế nào [Paper §6.1, Hình 6a]

DiagGuard chặn ở 3 thời điểm và **không biết đáp án đúng** (*answer-agnostic*), nên không "chép đáp án" cho agent:

```text
[1] Trước truy vấn đầu tiên
        ↓
    GROUNDER: đưa Search Space Profile (bản đồ thật: bảng, metric, pod đang có)
    → chặn OMIT3, OMIT5; giảm GEN2 (bịa thứ không tồn tại)
        ↓
[2] Trước khi bắt đầu điều tra
        ↓
    VERIFIER - Self-Audit: checklist "đã so baseline (OMIT1) chưa? đã kiểm mốc thời gian (OMIT6) chưa?"
        ↓
    (agent điều tra bằng tools…)
        ↓
[3] Trước khi chốt kết luận
        ↓
    VERIFIER - Soundness Check: "dựa trên log/metric nào? mâu thuẫn với dữ liệu trước không?
                                 đã kiểm tra cạnh lan truyền (OMIT2) chưa?"
```

**Kết quả [Paper §6.2-6.3, Bảng 4]:**
- Acc@1 tăng trên cả **14 cấu hình**: trung vị **+10.5%**, cao nhất **+35.1%**.
- Ablation: chỉ Grounder **+4.5%** · chỉ Verifier **+4.1%** · đủ cả hai **+9.0%**.

---

## 5. Điểm mù của DiagGuard và gap cho luận văn [Diễn giải của reader]

> Đây là nhận xét khi đặt DiagGuard vào bài toán "Kubernetes RCA với telemetry thiếu/cũ". Paper không tuyên bố các điểm này. Cần kiểm tra thêm trước khi viết thành "research gap" (xem `aiops-research-question`).

| # | Điểm mù | Vì sao là vấn đề | Hướng mở |
| --- | --- | --- | --- |
| 1 | **Giả định dữ liệu đầy đủ** | Cơ chế nhắc ngầm hiểu "cứ query là có dữ liệu". Nếu collector nghẽn, log rớt, hoặc pod vừa restart/rollout thì Verifier đòi bằng chứng cũng không có gì để lấy | Kiểm tra **độ đầy đủ & độ tươi** của telemetry trước khi tin vào nó |
| 2 | **Không cho abstain** | Soundness Check xong vẫn bắt chốt 1 service. Khi H1 và H2 ngang nhau do thiếu dữ liệu, chốt = đoán mò có kiểm soát | **Selective RCA**: được trả "chưa đủ dữ liệu để kết luận duy nhất" |
| 3 | **Không chỉ ra query phân định** | Nhắc "hãy kiểm tra" nhưng không nói: đang phân vân H1/H2 thì query nào là *decisive test*? | **Hypothesis-driven differential query**: chọn đúng telemetry phân định thay vì spam query |

---

## 6. Việc cần làm cho luận văn [Diễn giải / đề xuất]

1. **Kế thừa taxonomy:** dùng Bảng 3 (hoặc bản rút gọn: OMIT1, OMIT3, OMIT6, MIS1, MIS2, GEN1) làm tiêu chí chấm lỗi cho thí nghiệm của nhóm.
2. **Kế thừa metric:** báo cáo Node F1 + Edge F1 cùng Acc@1, để chứng minh giải pháp hiểu đúng cơ chế lan truyền chứ không chỉ đoán trúng.
3. **Mở rộng Verifier:** giữ Self-Audit và Soundness Check, thêm 2 module:
   - **Data Completeness & Freshness Check:** telemetry lấy về có bị đứt, hoặc cũ hơn thời điểm rollout không?
   - **Selective Gatekeeper:** cho phép trả "Chưa đủ bằng chứng" khi telemetry suy giảm.
