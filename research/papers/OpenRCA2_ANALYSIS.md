# OpenRCA 2.0: From Outcome Labels to Causal Process Supervision

> **Đọc nhanh (30 giây):** Các benchmark RCA cũ chỉ chấm "đoán đúng service lỗi chưa". OpenRCA 2.0 gán thêm nhãn **đường lan truyền lỗi** (service A làm hỏng B, B làm hỏng C…) và cho thấy agent thường **đoán trúng thủ phạm nhưng giải thích sai đường đi**. Tác giả gọi hiện tượng này là *ungrounded diagnosis*.

| Mục | Thông tin |
|---|---|
| Mã / phiên bản | arXiv:2606.27154 **v2** (30/06/2026), ghi chú "work in progress" |
| Tác giả | Aoyang Fang, …, Pinjia He (CUHK Shenzhen); cùng nhóm với DiagGuard và 2510.04711 |
| Venue | Preprint |
| Dữ liệu | 500 instance; trạng thái công bố artifact **[Chưa kiểm]** (bản v2 viết "after public release…", Appendix A) |
| PDF | https://arxiv.org/pdf/2606.27154v2 |
| Mức độ đọc | Full text phần chính (§1–§6) và Appendix A, F; chưa đọc kỹ Appendix B–E, G–H |
| Ngày đọc | 09/11/2026 |
| Độ gần với đề tài | ★★☆ Benchmark tham chiếu; tự nêu "information availability" là future work |

**Quy ước:** **[Paper]** = điều paper nói (kèm vị trí). **[Diễn giải]** = nhận xét, ví dụ của người viết. **[Chưa kiểm]** = chưa xác minh.

---

## 1. Paper giải quyết vấn đề gì?

**Giải thích cho người mới [Diễn giải]:** hãy tưởng tượng một dây chuyền 4 người chuyền tay nhau một cái hộp: Seat → Travel → Order → Gateway. Seat làm rơi hộp. Gateway là người đứng cuối nên la lên "hộp hỏng!". Benchmark cũ chỉ hỏi "ai làm rơi?". Agent trả lời "Seat" là được điểm tối đa, kể cả khi nó bảo "Seat đưa thẳng cho Order" (bỏ qua Travel). OpenRCA 2.0 chấm thêm phần "hộp đã đi qua những ai".

- **[Paper, Abstract, §1]** Các benchmark RCA hiện có chỉ gán nhãn root cause, không gán nhãn đường lan truyền tới triệu chứng, nên task bị đơn giản hóa thành "pattern matching".
- **[Paper, §1, Figure 1]** *Ungrounded diagnosis* = agent nêu đúng service gốc nhưng không có đường lan truyền đã kiểm chứng nối nó với triệu chứng quan sát được.

## 2. Input → Output

| | Nội dung |
|---|---|
| **Input của agent** | Telemetry đa phương thức (traces, metrics, logs) dạng parquet của một lần inject lỗi. Agent **không** được cho dependency graph [Paper §3.1] |
| **Công cụ của agent** | Truy vấn SQL (DuckDB) trên file parquet, liệt kê bảng, xem schema, `think_tool` [Paper Appendix F] |
| **Output của agent** | JSON gồm tập root cause (service, fault_kind) + các cạnh lan truyền; mỗi claim kèm câu SQL chạy lại được làm bằng chứng [Paper §3.1, Appendix F] |
| **Nhãn chuẩn** | Đồ thị lan truyền G* được PAVE kiểm chứng (trung bình 7,5 cạnh/instance) [Paper Abstract, Table 1] |

## 3. Môi trường thực nghiệm [Paper §3.1, Table 1]

- 3 hệ microservice: **TrainTicket** (320 instance), **Hotel Reservation** của DeathStarBench (142), **OpenTelemetry Demo** (38).
- 27 loại lỗi (chaos primary kinds): ứng dụng, tài nguyên, mạng, pod.
- Nguồn: pool lớn của Fang et al. (8.137 lần inject, xem 2510.04711) + campaign mới. Lọc bỏ *silent injection* (lần inject không để lại dấu vết), rồi chọn phân tầng còn 500.
- Agent: kiến trúc ReAct lấy từ Deep Research agent; ngân sách khoảng 50 tool call, trần 100 [Paper Appendix F].
- 11 LLM: Claude Opus 4.7, Gemini 3.1 Pro, Claude Sonnet 4.6, MiMo 2.5 Pro, GLM 5.1, Kimi K2.6, DeepSeek V4 Pro, Qwen3.6-Max, Hy 3.0 Preview, Seed 2.0 Pro, MiniMax M2.7.

## 4. Cách làm (process)

```text
Fault injection (biết trước do(v_root): thành phần, loại lỗi, thời điểm)
   │
   ├─ Bước 1: Structural Pruning   → liệt kê các đường lan truyền khả dĩ theo topology + luật lan truyền
   ├─ Bước 2: Causal Verification  → chỉ giữ đường thỏa CẢ 3 điều kiện:
   │        (a) cấu trúc: phù hợp cơ chế lan truyền đã biết
   │        (b) thống kê: lệch có ý nghĩa so với baseline trước khi inject
   │        (c) thời gian: thượng nguồn bất thường trước hạ nguồn
   └─ Kết quả: đồ thị G* làm "đáp án quá trình"
```

- **Ý tưởng cốt lõi [Paper §1, §2.1]:** *information asymmetry*. Agent phải suy ngược từ triệu chứng (khó). Người gán nhãn biết sẵn can thiệp nên chỉ cần **kiểm chứng xuôi** từ nguyên nhân ra hậu quả (dễ hơn nhiều). Paper gọi đây là *forward verification*.
- **Kiểm tra nhãn [Paper §3.4]:** 2 tác giả audit độc lập 100 instance ngẫu nhiên, đồng ý 94/100. Cả 6 bất đồng đều theo hướng "nhãn thiếu cạnh yếu", không có cạnh sai được đưa vào.

## 5. Câu hỏi nghiên cứu và câu trả lời

Paper không đặt RQ đánh số mà trình bày 3 Finding [Paper §3.2]:

| Finding | Nội dung |
|---|---|
| F1 | Điểm outcome đã thấp, nhưng còn che giấu lỗi: đúng ít nhất 1 service (AnySvc) 76,0%, nhưng có đường lan truyền kiểm chứng (PR) chỉ 61,5% |
| F2 | Edge F1 trung bình 43,4% luôn thấp hơn Node F1 62,2% (kém 18,8 điểm) ở **mọi** model |
| F3 | Không model nào thắng mọi cột; xếp hạng phụ thuộc chi phí kiểm chứng phía sau |

## 6. Kết quả chính [Paper Abstract, Table 2, §3.3]

- Khớp chính xác tập root cause (EM) trung bình **20,7%**; cao nhất Gemini 3.1 Pro 29,4%, Claude Opus 4.7 27,6%.
- **3 kiểu lỗi lặp lại** khi đọc trajectory (§3.3):
  1. *Premature commitment*: thấy một nguyên nhân hợp lý là dừng, bỏ sót lỗi thứ hai tinh vi hơn.
  2. *Presence bias*: coi "im lặng" là "khỏe". Ví dụ pod bị kill không còn sinh span; agent kết luận "service này không có lỗi" và đổ cho caller.
  3. *Salience capture*: bị hút vào tín hiệu ồn nhất (service hub nhiều traffic, dòng log SEVERE) dù đó chỉ là khuếch đại hạ nguồn.

## 7. Hạn chế

**Paper tự nhận [§5 Assumptions and Threats to Validity]:**
- Cần can thiệp thật (fault injection), dependency graph đủ đầy, lỗi phải để lại dấu vết trong telemetry, baseline sạch. Nếu thiếu, số liệu chỉ là cận trên.
- Bộ luật lan truyền có thể âm thầm bỏ sót cơ chế ngoài từ vựng hiện tại.

**Người đọc nhận xét [Diễn giải]:**
- Benchmark **tĩnh**: agent chỉ query file parquet, không tương tác hệ thống như `kubectl`. Khác Cloud-OpsBench.
- Chỉ giữ case **có** dấu vết telemetry, nên accuracy đo trên tập "dữ liệu lý tưởng" (giống Cloud-OpsBench lọc case).
- Mỗi model chạy một lần trên mỗi case; chưa thấy chạy lặp hay khoảng tin cậy trong phần đã đọc **[Chưa kiểm ở appendix]**.
- Người audit là tác giả; chưa có người gán nhãn độc lập bên ngoài.
- Không đo agent **có biết mình chưa chắc** hay không; mọi agent luôn phải trả lời.

## 8. Nhóm khai thác được gì?

1. **Bằng chứng động lực cho đề tài:** câu nguyên văn ở §5, ngay trước §6: telemetry hạn chế (subsampled traces, missing modalities, truncated windows) là *"a controllable evaluation axis that we leave to future work"*. Đây là bằng chứng tác giả tự nhận chỗ trống, dùng được trong phần Motivation. Trích đúng câu, không phóng đại thành "chưa ai làm".
2. **Ungrounded diagnosis = "đúng nhưng không đáng tin":** củng cố luận điểm của nhóm rằng accuracy cao chưa đủ để tin agent. Đây là lý do cần cơ chế **ước lượng độ tin cậy** cho từng chẩn đoán (hướng chốt trong báo cáo tổng hợp).
3. **3 kiểu lỗi** (premature commitment, presence bias, salience capture) gần với taxonomy của DiagGuard (MIS1, MIS2, GEN1) và Cloud-OpsBench §4.6. Có thể dùng làm **đặc trưng (feature)** để dự đoán agent sai. Ví dụ: agent dừng sau rất ít truy vấn, chỉ xem service có tín hiệu mạnh nhất.
4. **Ý tưởng forward verification:** người gán nhãn có lợi thế thông tin so với agent. Nhóm có thể dùng ý này khi xây nhãn trên Cloud-OpsBench: fault plan biết trước, nên kiểm xuôi xem tool nào còn chứa dấu vết.
5. **Không nên chọn làm môi trường chính:** dữ liệu tĩnh, cần hạ tầng DuckDB/parquet khá lớn, artifact chưa chắc đã công bố. Cloud-OpsBench phù hợp hơn cho nhóm.

## 9. Thuật ngữ

- **Fault injection:** cố tình gây lỗi (giảm CPU, chặn mạng, kill pod) để có "đáp án" biết trước.
- **Propagation path:** chuỗi service bị ảnh hưởng dây chuyền từ gốc tới chỗ người dùng thấy lỗi.
- **Node F1 / Edge F1:** đo trùng khớp tập service (node) và tập cạnh lan truyền (edge) giữa dự đoán và nhãn.
- **EM (Exact Match):** tập root cause dự đoán trùng khít tập đáp án.
- **Silent injection:** inject lỗi nhưng hệ thống không có biểu hiện đo được, nên bị loại khỏi benchmark.
