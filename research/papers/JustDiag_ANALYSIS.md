# JustDiag!: A Diagnostic Justification Engine for Accountable Root Cause Analysis

> **Đọc nhanh (30 giây):** Câu trả lời trôi chảy chưa đủ để chịu trách nhiệm trong vận hành. JustDiag bắt hệ RCA duy trì một **"hồ sơ lập luận"** tường minh: bằng chứng, giả thuyết cạnh tranh, mâu thuẫn, việc cần kiểm tiếp. Hệ được phép **không chốt** (*non-closure*) khi bằng chứng chưa đủ. Trên 66 sự cố thật, điểm outcome và process đều tăng so với bản không có cơ chế này; đổi lại số case "đóng" giảm từ 65/66 xuống 62/66.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2606.19407 **v1** (17/06/2026) |
| Tác giả | Tingzhu Bi, …, Meng Ma (Peking University; University of Edinburgh; BUPT) |
| Venue | Preprint |
| PDF | https://arxiv.org/pdf/2606.19407v1 |
| Mức độ đọc | Abstract, §1–§2, câu trả lời RQ1–RQ4 (§4), §5–§6; chưa đọc chi tiết appendix D/E |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Tiền lệ "được phép không chốt"; khác ở dữ liệu kín và chấm bằng LLM judge |

---

## 1. Paper giải quyết vấn đề gì?

- **[Paper §1]** Kỹ sư cần biết bằng chứng nào hỗ trợ chẩn đoán, đã xét những phương án nào, mâu thuẫn nào còn lại, và hệ đã thật sự giải quyết case hay đang giữ bất định. Đa số đánh giá chỉ chấm đáp án cuối.

**Ví dụ [Diễn giải]:** hồ sơ bệnh án tốt không chỉ ghi "viêm phổi", mà ghi "đã loại lao vì X-quang..., còn nghi ngờ nấm vì..., cần làm thêm xét nghiệm Y". Nếu chưa đủ căn cứ thì ghi "chưa kết luận, đề nghị theo dõi".

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input** | Telemetry metric đa biến của một sự cố |
| **Cơ chế** | Orchestrator điều phối các expert agent; tách giả thuyết thành các **claim** cần kiểm; phân xử mỗi claim là *supports / contradicts / insufficient* |
| **Output** | Trạng thái chẩn đoán có cấu trúc: giả thuyết tốt nhất hiện tại, phương án thay thế, mâu thuẫn, bất định còn lại; trạng thái kết thúc **resolved / provisionally_resolved / stalled / need_more_evidence** [Paper §1, §3] |

## 3. Môi trường thực nghiệm [Paper §4.1]

- **66 sự cố thật, proprietary**, từ một trung tâm dữ liệu hyperscale; mỗi case có metric đa biến và một bản tường thuật do SRE viết (*silver reference narrative*).
- Backbone chẩn đoán: **Gemini 3 Flash**; judge chấm: **GPT-5.4**.
- RQ1 dùng đủ 66 case; ablation và độ nhạy (RQ2–RQ3) chỉ dùng **10 case** để tiết kiệm chi phí; tác giả coi là kiểm tra định hướng.

## 4. RQ và câu trả lời [Paper §4]

| RQ | Trả lời |
|---|---|
| RQ1: Diagnostic justification có cải thiện outcome và process? | Có: Outcome 51,0 → 57,7; Process 44,0 → 50,5 so với bản không DJ. Bản không DJ đã hơn hai baseline ngoài |
| RQ2: Cơ chế nào quan trọng? | Evidence grounding và claim adjudication tạo chất lượng quá trình; hypothesis competition và coverage gate chủ yếu **chống chốt sớm** (10 case) |
| RQ3: Nhạy với tham số? | Siêu tham số tạo đánh đổi chất lượng–chi phí giải thích được |
| RQ4: Non-closure có trách nhiệm hơn? | Có, khi bằng chứng chưa đủ; case "stalled" vẫn xuất giả thuyết tốt nhất và phương án thay thế |

## 5. Hạn chế

**Paper tự nhận [§6]:** bị giới hạn bởi observability nhận được và chất lượng silver narrative; điểm judge chỉ là proxy, không phải ground truth.

**Người đọc nhận xét [Diễn giải]:**
- Dữ liệu kín, không tái lập được; chỉ metric.
- Đánh giá dựa trên **LLM judge + narrative bạc**, không có nhãn khách quan về "đáng lẽ nên chốt hay không".
- Không đo **ở cùng coverage**: giảm số case đóng có thể tự làm điểm trung bình đẹp hơn. Không có risk–coverage.
- Ablation trên 10 case là quá nhỏ để kết luận.

## 6. Nhóm khai thác được gì?

1. **Tiền lệ cần trích khi nói "agent được phép không chốt":** JustDiag đã làm non-closure trong RCA. Nhóm không được claim "lần đầu cho phép abstain".
2. **Khoảng cách phương pháp luận nhóm có thể lấp [Diễn giải]:** JustDiag thiếu (a) nhãn khách quan, (b) so sánh ở cùng coverage, (c) benchmark mở. Cloud-OpsBench cho nhãn khách quan R*, nên nhóm đo được "chốt sai" và "từ chối" bằng số đếm, không cần judge.
3. **Bộ trạng thái kết thúc:** gợi ý cho output schema của nhóm: `diagnosis` / `candidates` / `insufficient` (memo 07/11) tương ứng với resolved / provisionally_resolved / need_more_evidence.
4. **"Coverage gate" và "hypothesis competition"** là hai cơ chế chống chốt sớm có thể dùng làm baseline B (verifier-style) khi so với phương pháp gating của nhóm.

## 7. Thuật ngữ

- **Accountable RCA:** RCA mà người vận hành kiểm tra, phản biện được và biết khi nào nên hoãn.
- **Claim adjudication:** phân xử từng mệnh đề con (ủng hộ / mâu thuẫn / chưa đủ).
- **Non-closure:** chủ động không đóng case khi chưa đủ căn cứ.
- **Silver reference:** đáp án tham chiếu "bạc", do người viết nhưng không được kiểm chứng như nhãn vàng.
