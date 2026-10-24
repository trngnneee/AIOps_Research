---
name: paper-reading-notes
description: Quy trình đọc paper cho khóa luận AIOps trong thư mục AiOps. Dùng khi người dùng đọc một paper (Cloud-OpsBench, DiagGuard, ARBITER...) và nhờ tóm tắt, giải thích, đối chiếu cách hiểu của họ với bản gốc, ghi vào report, hoặc ghi một finding. Áp dụng cho các việc như "ghi vào report", "note lại", "tạo finding", "tóm tắt mục X trước khi đọc".
---

# Quy trình đọc paper cho khóa luận AIOps

Người dùng đọc paper theo từng mục, nói lại cách hiểu của họ, và nhờ kiểm tra rồi ghi vào report. Giao tiếp bằng tiếng Việt, giọng thân mật, ngắn gọn.

## Cấu trúc thư mục (gốc: `/Users/trngnneee/AiOps`)
- `paper/`: PDF của paper. Đọc bản PDF này trước, chỉ lên web khi PDF không có.
- `{PAPER}_reading_report.md`: report quá trình đọc, ví dụ `CloudOpsBench_reading_report.md`.
- `finding/{PAPER}_FINDING.md`: các finding (nhận xét, điểm yếu, hàm ý cho đề tài), ví dụ `finding/CloudOpsBench_FINDING.md`. `{PAPER}` là tên paper viết liền, cùng tiền tố với file report.

## Vòng làm việc cho mỗi mục
1. **Tóm tắt trước khi đọc** (khi người dùng yêu cầu): đi theo thứ tự của paper, giải thích ký hiệu bằng ví dụ, tránh dồn công thức.
2. **Người dùng nói cách hiểu** của họ. Mở PDF, đối chiếu với đúng đoạn nguyên văn rồi trả lời theo dạng: ý đúng, ý cần chỉnh, ý bị thiếu. Kèm số section hoặc số bảng.
3. **Chỉ ghi vào report sau khi người dùng xác nhận** ("oke ghi đi"). Không ghi trước.
4. Khi ghi: ghi theo ý của người dùng, đã gộp các chỉnh sửa đã thống nhất. Không thêm ý thừa. Nếu muốn thêm ý của paper mà họ chưa nhắc, ghi rõ khi báo lại để họ quyết định giữ hay bỏ.

## Trích dẫn và độ tin cậy
- Chỉ nói "paper nói" khi đã tìm thấy trong bản gốc. Tách rõ: điều paper nói, điều suy ra, điều chưa kiểm chứng.
- Phần suy ra từ tên hoặc kiến thức nền thì ghi chú rõ, mục chưa chắc đánh dấu `(?)`.
- Không bịa ví dụ rồi gắn vào paper. Ví dụ do mình dựng phải ghi "do mình dựng".
- Ý riêng của người dùng ghi dưới tiêu đề "Nhận xét của người đọc (không phải của paper)".
- Số liệu và định nghĩa quan trọng: báo người dùng tự mở lại để đối chiếu, vì công cụ tóm tắt tự động có thể sai.
- Nếu thấy mâu thuẫn giữa các nguồn (ví dụ số case khác nhau giữa hai phiên bản), ghi rõ version.

## Định dạng report
- Tiêu đề bám theo số mục của paper: `## 2. ...`, `### Gap 1 ...`, `#### 3.3.1 ...`, có ghi `(§x.y)`.
- Dùng bullet. Tránh bảng có ô dài và tránh bảng HTML (người dùng đọc file thô, không đọc được). Bảng Markdown chỉ dùng cho dữ liệu ngắn.
- Cấu trúc phân cấp thì vẽ cây chữ trong khối code (ký tự `├──`, `└──`).
- Viết ngắn gọn, đúng ý người dùng, không thêm đoạn bình luận dài.
- Khi người dùng sửa file trên đĩa, coi đó là trạng thái hiện tại, chỉ sửa đúng khối cần sửa, không ghi đè cả file.

## File finding
Mỗi finding gồm: vị trí trong paper, phần khách quan có căn cứ, phần chủ quan hoặc điểm yếu, biện pháp của paper, hàm ý cho đề tài, mục "Chưa kiểm chứng". Đánh dấu rõ là nhận xét của người đọc, chưa phải kết luận của paper.

## Ngữ cảnh đề tài
Khóa luận AIOps về Evidence-Adequacy-Aware Verification cho LLM agent trong Kubernetes incident management. Cloud-OpsBench là môi trường replay và cũng là công trình cần phân biệt novelty. Khi đọc paper mới, luôn để ý: họ verify cái gì, ở bước nào, theo từng claim hay cả case, có abstain hoặc request-evidence không, xử lý telemetry thiếu hoặc mâu thuẫn không, oracle lấy từ đâu và họ nói không làm gì.
