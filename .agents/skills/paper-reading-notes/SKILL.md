---
name: paper-reading-notes
description: Giải thích từng phần paper AIOps, đối chiếu cách hiểu với bản gốc và ghi reading report hoặc finding có dẫn chứng. Dùng khi đọc một paper, hỏi về công thức/phương pháp, nói lại cách hiểu, yêu cầu ghi note; dùng aiops-literature-review cho khảo sát nhiều paper.
---

# Quy trình đọc paper cho khóa luận AIOps

Người dùng đọc paper theo từng mục, nói lại cách hiểu của họ, và nhờ kiểm tra rồi ghi vào report. Giao tiếp bằng tiếng Việt, giọng thân mật, ngắn gọn.

## Cấu trúc thư mục (tính từ gốc repository)
- Đọc `AGENTS.md` và `roadmap/AIOps_Thesis_Research_Guide.md` để biết quy ước và hướng đang kiểm chứng; không coi roadmap là bằng chứng novelty.
- `paper/`: PDF của paper. Đọc bản local trước, kiểm tra title/version. Lên nguồn gốc khi thiếu PDF, cần kiểm tra phiên bản mới hoặc đối chiếu artifact.
- `{PAPER}_reading_report.md`: report quá trình đọc, ví dụ `CloudOpsBench_reading_report.md`.
- `finding/{PAPER}_FINDING.md`: các finding (nhận xét, điểm yếu, hàm ý cho đề tài), ví dụ `finding/CloudOpsBench_FINDING.md`. `{PAPER}` là tên paper viết liền, cùng tiền tố với file report.

## Vòng làm việc cho mỗi mục
1. **Tóm tắt trước khi đọc** (khi người dùng yêu cầu): đi theo thứ tự của paper, giải thích ký hiệu bằng ví dụ, tránh dồn công thức.
2. **Người dùng nói cách hiểu** của họ. Mở PDF, đối chiếu với đúng đoạn nguyên văn rồi trả lời theo dạng: ý đúng, ý cần chỉnh, ý bị thiếu. Kèm số section hoặc số bảng.
3. **Ghi khi đã được yêu cầu** ("ghi vào report", "oke ghi đi"). Yêu cầu ghi trực tiếp đã là sự cho phép, không hỏi lại. Nếu chỉ đang trao đổi cách hiểu thì trả lời, chưa sửa file.
4. Khi ghi: ghi theo ý của người dùng, đã gộp các chỉnh sửa đã thống nhất. Không thêm ý thừa. Nếu muốn thêm ý của paper mà họ chưa nhắc, ghi rõ khi báo lại để họ quyết định giữ hay bỏ.

## Trích dẫn và độ tin cậy
- Chỉ nói "paper nói" khi đã tìm thấy trong bản gốc. Tách rõ: điều paper nói, điều suy ra, điều chưa kiểm chứng.
- Phần suy ra từ tên hoặc kiến thức nền thì ghi chú rõ, mục chưa chắc đánh dấu `(?)`.
- Không bịa ví dụ rồi gắn vào paper. Ví dụ do mình dựng phải ghi "do mình dựng".
- Ý riêng của người dùng ghi dưới tiêu đề "Nhận xét của người đọc (không phải của paper)".
- Số liệu và định nghĩa quan trọng: tự đối chiếu với nguồn và kèm vị trí để người dùng kiểm tra. Nếu chưa truy cập được đoạn gốc, nói rõ giới hạn; không giả vờ đã đọc.
- Dùng `pdftotext -layout` nếu có; xem trực quan trang gốc khi bảng, hình hoặc công thức bị trích xuất sai. OCR chỉ là bản nháp cần kiểm tra. Không sửa PDF gốc, không cài thêm thư viện nếu công cụ sẵn có đã đủ.
- Với công thức: giải thích biến, giả định, một ví dụ nhỏ và điều công thức không đo được. Ví dụ tự dựng phải ghi rõ và không được biến thành số liệu paper.
- Không suy từ abstract rằng paper không làm một việc. Phân biệt chưa đọc, không được báo cáo trong phần đã kiểm tra, và bằng chứng paper loại trừ rõ ràng.
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
Lấy ngữ cảnh hiện tại từ roadmap, không khóa hướng nghiên cứu vào tên phương pháp cũ. Với hướng selective RCA hiện tại, chú ý: verify cái gì và ở bước nào; theo claim hay cả case; có abstain hoặc request-evidence không; xử lý dữ liệu thiếu/lỗi thời/mâu thuẫn ra sao; oracle và metadata từ đâu; baseline có cùng ngân sách không. Các câu chưa trả lời được là câu cần kiểm tra, không phải gap đã được chứng minh.
