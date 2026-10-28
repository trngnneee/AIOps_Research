# Skills nghiên cứu AIOps

Nguồn duy nhất: `.agents/skills/`. Quy ước dùng chung nằm ở `AGENTS.md`; `CLAUDE.md` nhập file này. Hướng nghiên cứu lấy từ roadmap, chưa coi là gap đã chứng minh.

| Skill | Ví dụ yêu cầu |
| --- | --- |
| `paper-reading-notes` | “Giải thích §3 Cloud-OpsBench rồi kiểm tra cách hiểu của tui.” |
| `aiops-literature-review` | “Tìm bài gần nhất về RCA khi telemetry thiếu; lưu search log và related-work matrix.” |
| `scientific-critical-thinking` | “Phản biện claim này: baseline và oracle có đủ để kết luận không?” |
| `aiops-research-question` | “Từ các paper đã đọc, đề xuất RQ và bằng chứng có thể bác bỏ từng hướng.” |
| `aiops-experiment-design` | “Thiết kế pilot kiểm tra RQ2 với baseline, budget và incident split công bằng.” |
| `aiops-research-writing` | “Viết related work từ nguồn đã kiểm tra, đánh dấu claim chưa có bằng chứng.” |

Có thể gọi `$tên-skill` ở client hỗ trợ; tự chọn skill được bật mặc định. Client có thể cần lượt mới hoặc mở lại session để quét skills. Không có lệnh đăng ký dùng chung bảo đảm discovery cho mọi client; khi chưa được liệt kê, yêu cầu agent đọc đường dẫn `SKILL.md` tương ứng.

## Nguồn và phụ thuộc

- `paper-reading-notes`: kế thừa skill của repo, giữ quy trình học/ghi chú; sửa đường dẫn máy cũ, quyền ghi và hướng đề tài đang kiểm chứng.
- Bốn skills `aiops-*`: viết riêng cho roadmap và quy trình nghiên cứu trong repo.
- `scientific-critical-thinking`: nhập chọn lọc từ K-Dense, MIT, có [commit và điều chỉnh](skills/scientific-critical-thinking/SOURCE.md), license và references. Không tự động cập nhật.
- Đã tham khảo https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/literature-review cho search provenance và kiểm tra citation; không nhập bộ scripts hay tích hợp dịch vụ của skill đó.
- Không cần tài khoản/API trả phí. Python dùng để validate; `pdftotext` đang có sẵn cho PDF. Không cài gói toàn hệ thống. Web vẫn cần khi tìm bài mới; không có mạng thì công bố giới hạn.

## Liên kết Claude trên Windows

Từ repo root, chạy `powershell -NoProfile -File .agents/scripts/link-claude-skills.ps1`. Script không thay thế một thư mục skills thật hoặc link trỏ sai. Di chuyển/đối chiếu nội dung cũ trước nếu gặp trường hợp đó.

Ưu tiên symlink tương đối `../.agents/skills`; Windows có thể cần Developer Mode/quyền tạo symlink. Nếu không được, dùng junction cục bộ. Junction không phải symlink portable trong Git: tạo lại bằng script sau khi clone/chuyển máy và không stage nội dung xuyên junction. Trên hệ thống hỗ trợ symlink, Git cần `core.symlinks=true` khi checkout link đã commit. Không dùng bản sao để đồng bộ skills.

Kiểm tra bằng `Get-Item .claude/skills | Format-List LinkType,Target` và so sánh file qua cả hai đường dẫn. `.agents/skills` luôn là nơi sửa nội dung.

Trạng thái máy hiện tại: symlink không tạo được, đã dùng junction; `.claude/.gitignore` bỏ qua junction. Đường dẫn skill cũ trong `.claude` được bỏ khỏi Git index để commit không giữ bản trùng, nội dung chuyển sang `.agents`. Nếu sau này chuyển sang symlink được Git theo dõi, bỏ quy tắc ignore `/skills/` và thay junction bằng symlink trước khi stage.

## Kiểm chứng khi thay đổi

Chạy `skill-creator/scripts/quick_validate.py` với từng thư mục skill trong môi trường có PyYAML; kiểm tra thêm các link Markdown cục bộ và license/commit của nội dung nhập. Validator chỉ kiểm tra cấu trúc, không chứng minh chất lượng suy luận.

Các tình huống cần thử bằng yêu cầu thực tế:

1. Chỉ thảo luận cách hiểu paper: sửa cách hiểu và dẫn nguồn, không tự ghi report.
2. Yêu cầu ghi note trực tiếp: sửa đúng mục, không hỏi lại và không ghi đè note khác.
3. Chỉ có abstract: không kết luận thiếu phương pháp hoặc có novelty.
4. Chưa có pilot/baseline: đề xuất RQ có điều kiện và phép thử khả thi, không nhận gap đã xác lập.
5. Không có lịch sử telemetry thật: thu hẹp claim stale hoặc gọi đúng là perturbation nhân tạo.
6. Agent abstain mọi case: coverage bằng 0, selective error không xác định; không kết luận phương pháp hoàn hảo.
