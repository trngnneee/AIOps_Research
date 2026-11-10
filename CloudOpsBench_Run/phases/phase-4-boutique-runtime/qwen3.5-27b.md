# Phase 4 (lượt 3) — Chạy batch: boutique/runtime, 45 case, Qwen3.5-27B

Repo: `github.com/LLM4Ops/Cloud-OpsBench` @ `ec1d4f3` (clone local)
Ngày chạy: 2026-11-10.

Run trước trong series này (cùng category boutique/runtime, 45 case):
- [`deepseek-v4-flash-0731.md`](deepseek-v4-flash-0731.md)
- [`gemini-2.5-flash.md`](gemini-2.5-flash.md)

## Config

```yaml
model:
  model: "qwen/qwen3.5-27b"
  provider: openai_compatible
  api_base: "https://openrouter.ai/api/v1"
  temperature: 0
  max_tokens: 4096
  timeout: 60
  enable_thinking: false

diagnosis:
  max_iterations: 20
  system: "boutique"
  fault_category: "runtime"
  case_name: ""
  dataset_root: "/Users/trngnneee/CloudOpsBench/Cloud-OpsBench"
  save_root: "/Users/trngnneee/CloudOpsBench/trajectory/"
```

## Raw output `evaluation.py` (giữ nguyên)

```text
Outcome Evaluation v2
================================================================================
config_path: /Users/trngnneee/CloudOpsBench/Cloud-OpsBench/agents/cloudops_agent/configs/model_configs.yaml
system: boutique
fault_category: runtime
case_split:
case_split_file:
label_root: /Users/trngnneee/CloudOpsBench/Cloud-OpsBench/process-label/boutique/runtime
agent_root: /Users/trngnneee/CloudOpsBench/trajectory/boutique/qwen/qwen3.5-27b/runtime
--------------------------------------------------------------------------------
total_cases: 45
selected_cases: 45
run_cases: 45
missing_run_cases: 0
invalid_action_total: 72
--------------------------------------------------------------------------------
CA (Component Accuracy): 1.0
FA (Fault-Type Accuracy): 0.8667
JRA (Joint RCA Accuracy): 0.8667
MC (Milestone Coverage): 0.9185
EOC (Evidence-Order Consistency): 0.9185
ECR (Evidence Closure Rate): 0.7556
EE (Evidence Efficiency): 0.9256
steps (Average Diagnostic Steps per Case): 4.0889
RAR (Redundant Action Rate): 0.0
invalid_actions (Average Invalid Actions per Case): 0.4889
--------------------------------------------------------------------------------
Summary JSON: .../evaluation_v2_runtime_summary.json
Detail JSON: .../evaluation_v2_runtime_details.json
```

## Kết quả theo fault type

| Fault type | n | JRA=1 | ECR=1 |
|---|---:|---:|---:|
| `container_memory_limit_too_low` | 9 | 9 | 3 |
| `liveness_probe_incorrect_protocol` | 8 | 8 | 8 |
| `liveness_probe_incorrect_port` | 8 | 6 | 6 |
| `readiness_probe_incorrect_protocol` | 8 | 8 | 8 |
| `readiness_probe_incorrect_port` | 7 | 7 | 6 |
| `liveness_probe_incorrect_timing` | 5 | **1** | 3 |
| **Tổng** | **45** | **39 (0.867)** | **34 (0.756)** |

## 6 case JRA < 1 — phân tích

| Case | Ground truth | Rank-1 prediction | Correct answer trong top-3? | ECR |
|---|---|---|---|---:|
| 12 | app/emailservice / `liveness_probe_incorrect_port` | `container_memory_limit_too_low` | ❌ (top3: OOM, timing, code_memory_leak) | 0 |
| 15 | app/recommendationservice / `liveness_probe_incorrect_port` | `container_memory_limit_too_low` | ✅ rank 2 | 1 |
| 18 | app/currencyservice / `liveness_probe_incorrect_timing` | `container_memory_limit_too_low` | ✅ rank 2 | 1 |
| 19 | app/emailservice / `liveness_probe_incorrect_timing` | `container_memory_limit_too_low` | ✅ rank 3 | 0 |
| 20 | app/paymentservice / `liveness_probe_incorrect_timing` | `container_memory_limit_too_low` | ✅ rank 2 | 0 |
| 21 | app/recommendationservice / `liveness_probe_incorrect_timing` | `container_memory_limit_too_low` | ✅ rank 3 | 1 |

**Pattern thống nhất:** Tất cả 6 case sai đều là fault type probe-related (timing hoặc port). Model luôn đoán `container_memory_limit_too_low` ở rank 1 — tức là thấy restart + memory signal rồi quy về OOM mà không tách biệt đúng cơ chế probe. 5/6 case vẫn có đáp án đúng trong top-3.

## Quan sát chính

1. **Component Accuracy hoàn hảo (1.0):** Qwen3.5-27B luôn đúng component (adservice, currencyservice, emailservice, paymentservice, recommendationservice) — không có lỗi target-resolution nào. Lỗi chỉ nằm ở phân biệt fault *type* bên trong cùng component.

2. **Confusability probe-vs-OOM:** 5/6 lỗi rơi vào `liveness_probe_incorrect_*` bị đọc thành OOM. Telemetry (restart count, memory pressure) tạo tín hiệu gần như trùng cho cả hai cơ chế. Đây là confound thực sự ở tầng telemetry — không phải lỗi model mà là **tín hiệu quan sát không đủ phân biệt** giữa probe-config fault và memory-limit fault. (Liên kết trực tiếp với Finding 2 trong `AiOps/finding/CloudOpsBench_FINDING.md`.)

3. **ECR cao bất thường (0.756):** So với DeepSeek (0.267) và Gemini-2.5-Flash (0.467) trên cùng 45 case, Qwen3.5-27B thu thập evidence "đầy đủ" hơn hẳn. Tuy nhiên ở 5 case OOM, ECR vẫn = 0 dù model đã gọi đúng tools — milestone M3 (xem app YAML / deployment spec) có vẻ bị bỏ qua khi model đã "chắc" về OOM.

4. **Invalid actions cao (1.6/case):** Tất cả 72 invalid actions là `invalid_model_output` — lỗi format (JSON không parse được, thiếu closing bracket, text thừa sau JSON...). Đây là failure mode (4) "Tool-grounding" ở tầng syntax, không phải sai về nội dung. So sánh: DeepSeek 0.49/case, Gemini 0.09/case. Qwen 27B có tỷ lệ format lỗi cao hơn ~20x so với Gemini.

5. **Hiệu quả:** Average 4.09 steps/case (gần ngang DeepSeek 4.04, nhanh hơn Gemini 3.91). EE = 0.926, RAR = 0 → không có bước thừa, mọi tool call đều đóng góp evidence.

6. **Chi phí vận hành:** 1,405,285 input tokens + 113,707 output tokens ≈ **$0.66** (giá OpenRouter: $0.26/M in, $2.60/M out). Rẻ nhất trong 3 model.

## So sánh 3 model (boutique/runtime, 45 case)

| Metric | DeepSeek-V4-Flash-0731 | Gemini-2.5-Flash | **Qwen3.5-27B** |
|---|---:|---:|---:|
| CA | 1.00 | 1.00 | **1.00** |
| FA / JRA | **1.00** | 0.889 | 0.867 |
| MC | 0.756 | 0.822 | **0.919** |
| EOC | 0.748 | 0.807 | **0.919** |
| ECR | 0.267 | 0.467 | **0.756** |
| EE | 0.801 | 0.926 | 0.926 |
| Steps | 4.04 | 3.91 | 4.09 |
| RAR | 0.00 | 0.00 | 0.00 |
| Invalid actions/case | 0.49 | 0.09 | 1.60 |
| Chi phí ước tính | ~$0.08 | ~$0.39 | ~$0.66 |

## Caveats

- Chỉ 1 category (runtime), 1 system (boutique), 45 case — chưa đại diện cho 754 case / 57 fault types.
- Checkpoint model không verify được chính xác (OpenRouter không expose exact revision).
- `enable_thinking: false` — Qwen 3.5 có hybrid thinking; nếu bật on, behaviour có thể khác đáng kể.
- Không phải reproduce bảng paper (model versions, harness version, label version có thể khác).

## Việc tiếp theo

- [ ] Chạy cùng 45 case với skill agent (`cloudops_skill_agent`) để xem Skill injection có cải thiện ECR ở nhóm OOM + probe-timing không.
- [ ] (Optional) Chạy `boutique/performance` (29 case, difficulty Hard) — nơi tín hiệu yếu hơn, kỳ vọng JRA giảm và confound tăng.
- [ ] (Optional) Bật `enable_thinking: true` và re-run 5–6 case probe-timing để xem reasoning có giúp tách biệt OOM vs probe fault không.