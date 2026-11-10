# Phase 4 (lượt 1) — Chạy batch: boutique/runtime, 45 case, deepseek-v4-flash-0731

Plan: `../../RUN_PLAN.md` · Repo: `/Users/trngnneee/CloudOpsBench/Cloud-OpsBench` @ `ec1d4f3`
Ngày chạy: 2026-11-10.

## Thiết lập

- Config: `system: boutique`, `fault_category: runtime`, `case_name: ""` (cả
  category = 45 case), `max_iterations: 20`, `temperature: 0`,
  model `deepseek/deepseek-v4-flash-0731` qua OpenRouter.
- Lệnh: `.venv/bin/python agents/cloudops_agent/run.py` rồi
  `.venv/bin/python agents/cloudops_agent/evaluation.py`.
- Case 1 (đã chạy ở Phase 2) được resume logic `[SKIP]`, chạy mới 44 case.
- **Không có case nào `stop_reason=max_steps`** — cả 45 case đều `submit`
  trong budget.

## Raw output `evaluation.py` (giữ nguyên)

```text
Outcome Evaluation v2
================================================================================
total_cases: 45
selected_cases: 45
run_cases: 45
missing_run_cases: 0
invalid_action_total: 22
--------------------------------------------------------------------------------
CA (Component Accuracy): 1.0
FA (Fault-Type Accuracy): 1.0
JRA (Joint RCA Accuracy): 1.0
MC (Milestone Coverage): 0.7556
EOC (Evidence-Order Consistency): 0.7481
ECR (Evidence Closure Rate): 0.2667
EE (Evidence Efficiency): 0.8007
steps (Average Diagnostic Steps per Case): 4.0444
RAR (Redundant Action Rate): 0.0
invalid_actions (Average Invalid Actions per Case): 0.4889
--------------------------------------------------------------------------------
Summary JSON: .../evaluation_v2_runtime_summary.json
Detail JSON: .../evaluation_v2_runtime_details.json
```

(ECR = 0.2667 tức 12/45 case đạt evidence closure đầy đủ.)

## Metrics theo fault type

Category runtime (boutique) chứa 6 fault type trong 45 case này:

| Fault type | n | JRA=1 | ECR=1 |
|---|---:|---:|---:|
| `container_memory_limit_too_low` | 9 | 9 | 0 |
| `liveness_probe_incorrect_protocol` | 8 | 8 | 0 |
| `liveness_probe_incorrect_port` | 8 | 8 | 1 |
| `readiness_probe_incorrect_protocol` | 8 | 8 | 2 |
| `readiness_probe_incorrect_port` | 7 | 7 | 4 |
| `liveness_probe_incorrect_timing` | 5 | 5 | 5 |
| **Tổng** | **45** | **45 (100%)** | **12 (26.7%)** |

Steps/case: `{3: 16, 4: 19, 5: 5, 6: 2, 7: 3}` — trung bình 4.04, max 7.
Invalid actions (22 total, 0.49/case) **đều là `invalid_model_output`**
(lỗi format text: "Expected exactly one Action and Action Input block",
"Action Input must be one JSON object with no trailing text") — harness bỏ
qua step đó và bước kế tiếp model tự sửa; không có tool error.

Chi phí token: 1.07M input + 112k output ≈ **$0.08 cho cả 45 case**
($0.0018/case theo giá OpenRouter deepseek-v4-flash-0731).

## So với bảng paper (caveats trước)

⚠️ **Không phải reproduce** — checkpoint model không verify được
(`0731` là snapshot 31/07/2026, paper không ghi snapshot đã dùng), inference
qua OpenRouter thay vì API vendor, và đây chỉ là **1 category (difficulty
Easy)** chứ không phải cả system. Đọc chỉ như "cùng họ model, cùng harness,
tập con data".

| Metric | Paper: DeepSeek-V4-Flash (Boutique, 550 case) | Run này (runtime, 45 case) |
|---|---:|---:|
| CA | 0.88 | **1.00** |
| FA | 0.77 | **1.00** |
| JRA | 0.76 | **1.00** |
| MC | 0.74 | 0.76 |
| EOC | 0.64 | 0.75 |
| ECR | 0.38 | 0.27 |
| EE | 0.62 | 0.80 |
| Steps | 6.45 | 4.04 |
| RAR | 0.00 | 0.00 |

Outcome cao hơn paper là hợp lý: runtime là nhóm Easy, triệu chứng cục bộ
mạnh (pod restart, probe failure, OOM) — model flash suy ra đúng cặp
component–fault gần như mọi case. MC/EOC/EE ở cùng vùng paper, steps thấp hơn.

## Quan sát chính (liên kết với findings)

1. **JRA–ECR gap tái hiện ở quy mô batch: 1.00 vs 0.27.** 33/45 case
   (73.3%) trả đúng rank-1 mà **không** đóng đủ milestone — chính xác
   "ungrounded diagnosis" (paper §4.3) và Finding 2 trong
   `AiOps/finding/CloudOpsBench_FINDING.md`: khoảng cách này không đơn thuần
   là "điều tra nông" — model dựa vào tín hiệu cục bộ mạnh + kiến thức tiên
   nghiệm mà bỏ qua bước xác nhận cấu hình (vd M3 trong case 1).
2. **ECR phân hoá theo fault type:** `liveness_probe_incorrect_timing`
   (5/5 closure) vs `container_memory_limit_too_low` (0/9) và
   `liveness_probe_incorrect_protocol` (0/8). Với OOM: model nhìn
   RESTARTS/OOMKilled là đủ để đoán đúng, nhưng milestone đòi thêm bằng
   chứng về memory limit/config → closure thiếu. Với protocol: cần đối chiếu
   YAML (probe http vs service gRPC) mà model không làm. → Hướng nghiên cứu
   khả thi: milestone nào là "cần thiết thực sự" vs "quy ước gán nhãn"
   (Finding 1: nhãn chủ quan).
3. **Hiệu suất vận hành:** không case nào kẹt (0 max_steps), RAR=0, chi phí
   ~$0.08/45 case, ~15–30 phút chạy → benchmark này **rẻ và nhanh** để chạy
   thử nghiệm agent/modification; nút chai không phải hạ tầng hay chi phí
   LLM.
4. **Invalid actions ~0.49/case** đều do format output (model đôi khi viết
   2 block Action hoặc JSON có trailing text) — đây là lỗi "tool-grounding
   mức syntax" (failure mode (4) trong §4.5 paper), ở mức nhẹ, tự phục hồi
   bước sau.

## Việc tiếp theo

- [ ] (Optional) Chạy category khó hơn (vd boutique/performance 29 case,
      difficulty Hard) để xem JRA còn bao nhiêu % và ECR thay đổi thế nào —
      test dự đoán "tín hiệu cục bộ yếu → ungrounded diagnosis tăng".
- [ ] (Optional) Chạy `cloudops_skill_agent` cùng 45 case (save_root riêng)
      để so ECR: skill có giúp đóng milestone M3 nhiều hơn không?
- [ ] Khi viết luận văn: trích số 45 case này với đúng caveat "cùng họ
      model, tập con, không verify checkpoint" — không ghi là reproduce paper.
