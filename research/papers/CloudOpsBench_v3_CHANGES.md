# Cloud-OpsBench: thay đổi từ v2 sang v3 (ảnh hưởng tới ghi chú cũ của nhóm)

> **Vì sao cần file này:** `CloudOpsBench_reading_report.md`, `finding/CloudOpsBench_FINDING.md` và `research/research-question-memo.md` đều trích **v2**. arXiv đã có **v3 (06/11/2026)**, đổi nhiều số liệu và sửa đúng một điểm nhóm từng nghi ngờ. File này **không sửa** các ghi chú cũ; nó liệt kê chỗ cần cập nhật khi nhóm trích dẫn.

| Mục | Thông tin |
|---|---|
| Bản mới | arXiv:2603.00468 **v3** (06/11/2026), 28 trang: https://arxiv.org/abs/2603.00468v3 |
| Repo | https://github.com/LLM4Ops/Cloud-OpsBench, MIT; commit mới nhất thấy được `ec1d4f38b952…` (03/11/2026) |
| Paper đi kèm | *Freezing the Crime Scene: A State Snapshot Paradigm for Reproducible Agentic SRE Evaluation*, FSE 2026 (companion), trang 1733–1737 (theo phần Citation trong README) |
| Mức độ đọc | Abstract, §1, §4.1, §4.4–§4.6, §5 của v3; Table 5–7 |
| Ngày đọc | 09/11/2026 |

---

## 1. Những gì giữ nguyên

- Quy mô dữ liệu: **754 case, 57 fault type, 8 nhóm, 2 hệ thống** (OnlineBoutique 550, TrainTicket 204) [v3 Abstract, §1].
- Ý tưởng snapshot replay, 12 tool (OnlineBoutique; TrainTicket 10 tool qua MCP), nhãn R* và D* (milestone graph), bộ metric CA/FA/JRA/MC/EOC/ECR/EE/Steps/RAR.
- Agent ReAct, temperature 0, tối đa 20 bước cho RQ1–RQ3.

## 2. Những gì thay đổi

| Nội dung | v2 (ghi chú cũ) | v3 |
|---|---|---|
| Số model | 10 | **11** (thêm **GLM-5.1**) |
| Số RQ | 3 (outcome, process, experience) | **4**: thêm **RQ4 Agent Architectures and Harnesses** |
| Bảng kết quả chính | Table 4 | **Table 5** (đánh số lại) |
| Bảng experience reuse | Table 5 | **Table 6** |
| JRA cao nhất OnlineBoutique | 0,76 (DeepSeek-V4-Flash) | **0,78 (GLM-5.1)** |
| GPT-5 OnlineBoutique MC / ECR | 0,64 / 0,21 | **0,70 / 0,39** |
| DeepSeek-V4-Flash OB JRA / ECR | 0,76 / 0,38 | **0,73 / 0,57** |
| Claude-Sonnet-4 OB JRA / ECR | 0,52 / 0,44 | **0,66 / 0,64** |
| Qwen3.5-27B OB JRA / ECR | 0,70 / 0,43 | **0,72 / 0,64** |
| GPT-5 TrainTicket JRA / ECR | 0,68 / 0,15 | **0,68 / 0,40** |
| Bảng chéo "đúng nhưng thiếu bằng chứng" | không báo | **Có (Figure 6):** GPT-5 đúng mà thiếu bằng chứng ở **33,1%** case OB và **29,4%** TT; chiều ngược (đủ bằng chứng nhưng sai) 3,9% và 1,5%. Qwen3-14B ngược lại: đủ bằng chứng nhưng sai 21,7% / 18,1% |
| RQ3: tập chấm của Base | Không nói rõ (Finding 3 của nhóm nghi Base chấm trên tập khác) | **"Base, ICL, and SOP are evaluated on the same held-out test cases"** [v3 §4.4]; số Base ở Table 6 giờ **khác** Table 5 |
| RQ3 kết quả OB (trung bình 3 model) | JRA 0,70 → 0,79 (ICL); ECR 0,39 → 0,59 | JRA 0,70 → **0,79** (ICL), ECR 0,62 → **0,75**; SOP 0,71 / 0,64 |
| Phân tích trajectory | §4.5 failure modes | **§4.6**: failure modes (4 loại như cũ) + **§4.6.2 case study 3 chẩn đoán đúng nhưng ECR = 0** |

Lý do số process thay đổi: README ghi ngày 16/07/2026 *"Released milestone-based process annotations and updated the evaluation metrics"*. **[Diễn giải]** Nhiều khả năng v3 dùng bộ nhãn milestone mới. Bảng kết quả trong README GitHub vẫn là **số cũ (v2)**.

## 3. RQ4 mới: kiến trúc và harness [v3 §4.5, Table 7]

Cố định model **GLM-5.1**, ngân sách 50 tool call, so 5 cách tổ chức điều tra:

| Cách | OB JRA | OB ECR | OB Tokens (K) | TT JRA | TT ECR | TT Tokens (K) |
|---|---|---|---|---|---|---|
| ReAct | 0,81 | 0,68 | 55,13 | 0,55 | 0,38 | 129,46 |
| Plan-and-Execute | 0,76 | 0,64 | 60,47 | 0,62 | 0,50 | 126,77 |
| Reflection | 0,84 | 0,68 | 76,82 | 0,57 | 0,36 | 230,78 |
| Codex (qua MCP) | **0,86** | **0,83** | 126,29 | **0,67** | **0,81** | 205,17 |
| OpenCode (qua MCP) | 0,84 | 0,81 | 105,85 | 0,63 | 0,71 | 361,27 |

Số liệu đã đối chiếu bằng trích xuất `pdftotext -raw` trang 19 và khớp với câu chữ ở §4.5 (ví dụ Plan-and-Execute TT JRA 0,62 / ECR 0,50; Codex 126,29K token ≈ 2,29 lần ReAct 55,13K).

Kết luận của paper: cùng JRA có thể đi kèm ECR rất khác; tốn token hơn không bảo đảm tốt hơn.

## 4. Ảnh hưởng tới ghi chú cũ của nhóm

| Ghi chú cũ | Cần làm gì |
|---|---|
| Finding 2 ("paper không báo tỷ lệ JRA đúng nhưng ECR = 0") | **v3 đã báo** (Figure 6). Cập nhật: chỉ đúng với v2 |
| Finding 3 ("Base ở RQ3 có thể không cùng tập case") | **v3 đã sửa**: ghi rõ cùng held-out test. Nhận xét của nhóm đúng với v2 và tác giả đã xử lý |
| Finding 1 (không thấy inter-annotator agreement) | Vẫn đúng ở v3: tìm "inter-annotator / Cohen / kappa / agreement rate" trong v3 không thấy kết quả |
| Nhận xét "không chạy lặp, không khoảng tin cậy" | Vẫn đúng ở phần đã đọc của v3 |
| Memo 07/11: "GPT-5 OnlineBoutique JRA 0,68 nhưng ECR 0,21" | Đổi thành **0,68 / 0,39 (v3)**, hoặc ghi rõ "theo v2" |

## 5. Ý nghĩa cho hướng nghiên cứu [Diễn giải]

1. **Hiện tượng "đúng mà thiếu bằng chứng" vẫn đứng vững ở v3** (33,1% với GPT-5 trên OB). Động lực cho việc cần đánh giá độ tin cậy không đổi.
2. **Harness ảnh hưởng mạnh** (ReAct → Codex: ECR 0,68 → 0,83 với cùng model). Nhóm phải cố định harness khi so sánh và ghi rõ phiên bản.
3. **ECR của model mạnh tăng nhiều ở v3**, nên luận điểm "agent điều tra nông" yếu đi một phần. Hướng chốt không dựa vào ECR thấp, mà dựa vào việc agent **vẫn sai 20–45%** và cần biết lúc nào sai.
4. Repo có **MCP server**, nên có thể dùng agent bên ngoài (Codex, OpenCode) nếu cần, nhưng ReAct mặc định rẻ nhất (khoảng 55K token mỗi case OB với GLM-5.1).
