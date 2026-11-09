# Nhật ký tìm kiếm tài liệu (09/11/2026)

File này ghi **nguồn gốc** của các paper trong `research/papers/` và báo cáo `research/research-direction-report.md`: tìm bằng gì, lúc nào, lọc ra sao, cái gì không truy cập được. Nhóm không cần đọc file này để hiểu báo cáo; dùng khi cần kiểm chứng hoặc khi hội đồng hỏi "tìm tài liệu thế nào".

## 1. Phạm vi và tiêu chí

- **Loại review:** scoping review có trọng tâm (không phải systematic review).
- **Câu hỏi định hướng:** (1) bức tranh LLM agent cho RCA/AIOps 2025–2026; (2) bằng chứng về độ tin cậy, abstention, uncertainty của agent; (3) các hướng thay thế khả thi cho nhóm 2 sinh viên trong 6 tháng.
- **Đưa vào:** paper/preprint 2023–11/2026 về LLM agent cho RCA, SRE, incident; benchmark AIOps có tương tác; phương pháp uncertainty/calibration/selective prediction cho agent dùng tool; audit benchmark RCA.
- **Không dùng làm bằng chứng:** blog doanh nghiệp, trang tổng hợp AI (emergentmind, themoonlight, papers.cool…). Chỉ dùng để phát hiện paper, sau đó đọc bản gốc trên arXiv.
- **Mốc thời gian:** tìm kiếm ngày 09/11/2026.

## 2. Công cụ

| Công cụ | Dùng để |
|---|---|
| WebSearch (standard / extended) | Phát hiện paper |
| arXiv API (`export.arxiv.org/api/query`) | Xác minh ID, tiêu đề, phiên bản mới nhất, ngày cập nhật của 41 ID |
| `curl` + `pdftotext` (bản 4.00) | Tải PDF phiên bản mới nhất và trích văn bản để đọc |
| GitHub API | Kiểm tra cấu trúc repo Cloud-OpsBench, commit, README, mã agent |
| OpenAlex API | Lấy abstract của paper IEEE Access (ResearchGate chặn truy cập) |

## 3. Truy vấn đã chạy

| # | Truy vấn | Chế độ | Kết quả đáng chú ý |
|---|---|---|---|
| 1 | LLM agent root cause analysis Kubernetes benchmark arXiv 2026 | standard | Cloud-OpsBench, Auditable Graph-Guided RCA, 2607.13548 |
| 2 | agentic root cause analysis microservices evidence verification hallucination arXiv 2026 | standard | TopoEvo, STAR, OpenRCA 2.0, Stalled-Biased-Confused, ORCA-bench, KRCA |
| 3 | LLM root cause analysis abstention insufficient evidence uncertainty calibration incident | standard | PACE-LM, LM-PACE (FSE 2024), Roy et al. 2403.04123 |
| 4 | survey LLM agents AIOps incident management root cause analysis 2026 | standard | Survey 2406.11213 / 2507.12472 (CSUR), LLM4Log 2604.16359, AgentOps 2508.02121 |
| 5 | SRE agent benchmark Kubernetes incident mitigation remediation LLM 2026 | standard | ITBench-AA, SREGym, SRE-World (NeurIPS 2026) |
| 6 | LLM agent RCA missing telemetry observability gaps robustness degraded logs | standard | Kim et al. 2602.09937; chủ yếu blog doanh nghiệp |
| 7 | small language model fine-tuning agent trajectories root cause analysis cloud incidents 2026 | standard | AOI 2603.03378, *Small LMs as Autonomous Operational Agents* (NeurIPS 2026), eARCO |
| 8 | LLM cascade escalation human handoff incident diagnosis cost accuracy tradeoff SRE agent | standard | Chỉ blog; không thấy paper học thuật về cascade cho RCA |
| 9 | benchmark shortcut leakage root cause analysis LLM agent fault injection artifacts audit | standard | HackDetect 2607.22368 và audit benchmark agent nói chung |
| 10 | STAR stage-attributed triage repair RCA agents microservices arXiv 2605.15581 | standard | Xác nhận STAR |
| 11 | Kubernetes misconfiguration detection repair LLM manifest benchmark 2026 | standard | GenKubeSec, LLMSecConfig, 2609.27030 |
| 12 | "root cause analysis" LLM agent token cost efficiency early stopping tool calls budget 2026 | standard | BAGEN (qua blog), không đọc |
| 13 | confidence estimation LLM agent root cause analysis trajectory signals predict failure escalate | **extended** | HTC (Agentic Confidence Calibration), CURA, AgentDebug |
| 14 | uncertainty quantification tool-using LLM agents trajectory-level failure prediction selective abstention 2026 | standard | 2608.11552, TRACER, ACL 2026 SRW thesis proposal |
| 15 | partial observability information availability agentic root cause analysis benchmark telemetry loss 2026 arXiv | **extended** | CTBench, ORCA-bench Finding #4, 2609.13463 |
| 16 | "Stalled, Biased, and Confused" LLM root cause analysis reasoning failures | standard | Xác nhận FORGE 2026 |
| 17 | uncertainty calibration "root cause analysis" LLM agent selective prediction coverage risk microservice 2026 | **extended** | 2609.07395, UCCI, DiscoUQ, GALA, LATS-RCA; **không thấy** paper áp dụng calibrated confidence / selective prediction cho RCA microservice |
| 18 | Holistic Trajectory Calibration LLM agents … arXiv | standard | Xác nhận 2601.15778 |
| 19 | root cause analysis LLM agent Kubernetes October 2026 arXiv new benchmark incident diagnosis | **extended** | ARGUS 2608.23084, TriFleetRCA, SynergyRCA |
| 20 | RCA agent abstain OR defer OR escalate human on-call "Cloud-OpsBench" OR "ITBench" OR "OpenRCA" confidence threshold | **extended** | **Không thấy** benchmark nào kiểm abstain/defer/escalate theo ngưỡng confidence trên ba benchmark này; slurm-rca-bench (HPC) có Brier; CHAP (giao thức) |
| 21 | CTBench telecom troubleshooting AI agents observability levels … | standard | Xác nhận CTBench |
| 22 | OpenRCA 2.0 PAVE ungrounded diagnosis … | standard | Xác nhận OpenRCA 2.0 |
| 23 | UCCI calibrated uncertainty cost-optimal LLM cascade routing … | standard | Xác nhận UCCI |
| 24 | "confidence" OR "uncertainty" LLM agent "root cause analysis" Kubernetes escalate human selective trust 2026 arXiv benchmark Cloud-OpsBench | **extended** | Süerkan et al. (IEEE Access 2026), TraceBench 2608.27182; không có paper gộp đủ các yếu tố |
| 25 | "The Confidence Dichotomy" miscalibration tool-use agents ACL 2026 Xuan | standard | ACL 2026 long 520, arXiv 2601.07264 |
| 26 | SRE-World NeurIPS 2026 benchmark … | standard | SRE-World, *Passing Without Repairing* (NeurIPS 2026) |
| 27 | "Evaluating Self-Reflective LLM Agents for Autonomous Kubernetes Troubleshooting" | **extended** | IEEE Access 2026 (Süerkan, Kugu, Emekci), KubeLLM, OperAID |
| 28 | "Passing Without Repairing" verifier blind spots live SRE agent benchmark NeurIPS 2026 | standard | Mô tả trên trang NeurIPS |

Kết quả web search là danh sách xếp hạng; không ghi "số hit" vì công cụ không trả số đó.

## 4. Paper đã tải và đọc full text (phiên bản mới nhất ngày 09/11/2026)

| ID | Phiên bản | Trang | File phân tích |
|---|---|---|---|
| 2603.00468 | v3 (06/11/2026) | 28 | `papers/CloudOpsBench_v3_CHANGES.md` |
| 2606.27154 | v2 | 30 | `papers/OpenRCA2_ANALYSIS.md` |
| 2607.28545 | v3 | 42 | `papers/ORCABench_ANALYSIS.md` |
| 2607.13548 | v2 | 29 | `papers/HowFarRCA_ANALYSIS.md` |
| 2602.09937 | v2 | 6 | `papers/WhyAgentsFailRCA_ANALYSIS.md` |
| 2601.22208 | v1 | 19 | `papers/StalledBiasedConfused_ANALYSIS.md` |
| 2601.15778 | v1 | 37 | `papers/AgenticConfidenceCalibration_ANALYSIS.md` |
| 2602.11409 | v1 | 10 | `papers/TRACER_ANALYSIS.md` |
| 2608.11552 | v1 | 24 | `papers/TrajectoryUQ_ANALYSIS.md` |
| 2309.05833 | v3 | 21 | `papers/PACELM_ANALYSIS.md` |
| 2605.18796 | v1 | 9 | `papers/UCCI_ANALYSIS.md` |
| 2606.19407 | v1 | 23 | `papers/JustDiag_ANALYSIS.md` |
| 2605.15581 | v1 | 11 | `papers/STAR_ANALYSIS.md` |
| 2609.19825 | v1 | 12 | `papers/EviRCA_ANALYSIS.md` |
| 2609.23766 | v1 | 8 | `papers/TriFleetRCA_ANALYSIS.md` |
| 2606.08590 | v1 | 8 | `papers/AuditableGraphRCA_ANALYSIS.md` |
| 2608.12002 | v2 | 32 | `papers/CTBench_ANALYSIS.md` |
| 2605.07161 | v3 | 26 | `papers/SREGym_ANALYSIS.md` |
| 2603.03378 | v4 | 37 | `papers/AOI_ANALYSIS.md` |
| 2606.29159 | v2 | 21 | `papers/PooledLeaderboardAudit_ANALYSIS.md` |
| 2609.07395 | v1 | 119 | `papers/UQAgentsTaxonomy_ANALYSIS.md` |

"Đọc full text" ở đây là **đọc có chọn lọc trên toàn văn**: abstract, giới thiệu, thiết lập, câu trả lời RQ, kết luận, hạn chế, và các bảng cần thiết. Mức đọc cụ thể ghi ở đầu từng file phân tích. Appendix phần lớn chưa đọc.

## 5. Chỉ biết qua abstract / trang hội nghị / kết quả tìm kiếm (chưa đọc full text)

| Paper | Nguồn đã xem | Ghi chú |
|---|---|---|
| ITBench (2502.05352, ICML 2025), ITBench-AA (05/2026) | arXiv API, trang Artificial Analysis | Benchmark SRE/IT automation |
| AIOpsLab (2501.06706, MLSys 2025) | arXiv API | Benchmark live |
| STRATUS (2506.02009, NeurIPS 2025) | arXiv API | Agent SRE có undo |
| SRE-World (NeurIPS 2026) | Trang NeurIPS 173084 | 44 task live, GPT 5.6 đạt 29% pass@1 |
| Passing Without Repairing (NeurIPS 2026) | Trang NeurIPS 173080 | Oracle mitigation chấp nhận cả hệ chưa sửa |
| Süerkan et al., IEEE Access 2026, DOI 10.1109/access.2026.3743626 | Abstract qua OpenAlex | Reflexion cho remediation K8s; **ResearchGate chặn (HTTP 403)** |
| The Confidence Dichotomy (ACL 2026, arXiv 2601.07264) | ACL Anthology, kết quả tìm kiếm | Tool lấy bằng chứng làm agent quá tự tin |
| Oh et al. 2026 (ACL) – UQ in LLM agents | Trích trong 2608.11552 | Nền tảng UQ cho agent |
| CURA (2608.27808), Towards Risk-free AI Agent Deployment (2608.16411), CHAP (2606.09751) | arXiv API | Giám sát/escalation cho agent nói chung |
| ARGUS (2608.23084), GALA (2608.08968, ASE'26), LATS-RCA (2605.03505, SEAA'26), TopoEvo (2605.15611), KRCA (2607.01788) | arXiv API | Phương pháp RCA mới; chưa đọc |
| ARBITER (2607.19182), Can LLMs Really Recover Microservice Failures? (2607.04623) | arXiv API | Remediation |
| 2510.04711 (FSE'26) *Rethinking the Evaluation of Microservice RCA with a Fault Propagation-Aware Benchmark* | arXiv API | Memo cũ ghi tên khác; tên đúng ở v2 là tên này |
| RCAEval (2412.17015), GenKubeSec (2405.19954), 2609.27030, Roy et al. (2403.04123) | arXiv API | Tham khảo |

## 6. Truy cập thất bại

- ResearchGate (paper Süerkan et al.): HTTP 403. Đã lấy abstract qua OpenAlex; full text phải mở thủ công.
- Semantic Scholar API: HTTP 429 (giới hạn tốc độ); thay bằng OpenAlex.

## 7. Giới hạn của lần tìm kiếm này

- Không tìm có hệ thống trên ACM DL, IEEE Xplore, Google Scholar; không làm citation chaining đầy đủ.
- Không tìm thấy paper **không có nghĩa là không tồn tại**. Mọi nhận định "chưa thấy" trong báo cáo là **tạm thời** và phải kiểm lại trước khi viết proposal.
- Một số paper rất mới (10–11/2026) có thể chưa được công cụ tìm kiếm lập chỉ mục.
