# Phase 4 (lượt 2) — Chạy batch: boutique/runtime, 45 case, google/gemini-2.5-flash (OpenRouter)

Plan: `../../RUN_PLAN.md` · Repo: `/Users/trngnneee/CloudOpsBench/Cloud-OpsBench` @ `ec1d4f3`
Ngày chạy: 2026-11-10. Run trước cùng category (deepseek-v4-flash-0731):
[`deepseek-v4-flash-0731.md`](deepseek-v4-flash-0731.md).

## Raw output `evaluation.py` (giữ nguyên)

```text
selected_cases: 45
run_cases: 45
missing_run_cases: 0
invalid_action_total: 4
--------------------------------------------------------------------------------
CA (Component Accuracy): 1.0
FA (Fault-Type Accuracy): 0.8889
JRA (Joint RCA Accuracy): 0.8889
MC (Milestone Coverage): 0.8222
EOC (Evidence-Order Consistency): 0.8074
ECR (Evidence Closure Rate): 0.4667
EE (Evidence Efficiency): 0.9262
steps (Average Diagnostic Steps per Case): 3.9111
RAR (Redundant Action Rate): 0.0
invalid_actions (Average Invalid Actions per Case): 0.0889
--------------------------------------------------------------------------------
```

Toàn 45 case `stop_reason=submit` (0 max_steps). Steps/case: `{3: 18, 4: 18,
5: 7, 7: 1, 8: 1}`, min 3, max 8. Invalid actions (4): 2 lần API error thoáng
qua (self-recovered bước sau) + 2 lần JSON action input sai format.
Token: 962.5k input + 41.1k output ≈ **$0.39** (giá OpenRouter 2.5 Flash:
$0.30/M in, $2.50/M out).

## Metrics theo fault type

| Fault type | n | JRA=1 | ECR=1 | (deepseek: JRA=1 / ECR=1) |
|---|---:|---:|---:|---|
| `container_memory_limit_too_low` | 9 | 9 | 0 | 9 / 0 |
| `liveness_probe_incorrect_protocol` | 8 | 8 | 2 | 8 / 0 |
| `liveness_probe_incorrect_port` | 8 | 8 | 7 | 8 / 1 |
| `readiness_probe_incorrect_protocol` | 8 | 8 | 4 | 8 / 2 |
| `readiness_probe_incorrect_port` | 7 | 7 | 5 | 7 / 4 |
| `liveness_probe_incorrect_timing` | 5 | **0** | 3 | **5** / 5 |
| **Tổng** | **45** | **40 (0.889)** | **21 (0.467)** | 45 / 12 |

## 5 case sai (cùng 1 pattern)

| Case | Component (đúng?) | Rank-1 dự đoán | Đúng label có trong top-3? | ECR |
|---|---|---|---|---:|
| 17 | adservice ✓ | `container_memory_limit_too_low` | rank 3 ✓ | **1** |
| 18 | currencyservice ✓ | `container_memory_limit_too_low` | ❌ (top3: OOM, code_memory_leak, pod_cpu_overload) | 0 |
| 19 | emailservice ✓ | `container_memory_limit_too_low` | rank 2 ✓ | **1** |
| 20 | paymentservice ✓ | `container_memory_limit_too_low` | rank 3 ✓ | **1** |
| 21 | recommendationservice ✓ | `container_memory_limit_too_low` | ❌→ rank 3 ✓ | 0 |

(GT cả 5: `liveness_probe_incorrect_timing`; deepseek đúng cả 5, ECR 5/5.)

→ Gemini **nhầm lẫn hệ thống** fault "probe timing quá nhạy (gây restart liên tục)"
thành "OOM"
(cả 5/5 case, component luôn đúng). Triệu chứng telemetry của timing fault
(restart lặp, có thể kèm tín hiệu memory) gần giống OOM — đúng kiểu
"nhầm các cơ chế gần nhau" (failure mode (3) target-resolution, §4.5 paper)
và khoảng cách CA > FA (§4.2: CA 0.82 > FA 0.67 với Gemini-2.5-Flash).

## So 2 model trên cùng 45 case

| Metric | deepseek-v4-flash-0731 | gemini-2.5-flash (OpenRouter) |
|---|---:|---:|
| CA | 1.00 | 1.00 |
| FA / JRA | **1.00** | 0.889 |
| MC | 0.756 | **0.822** |
| EOC | 0.748 | **0.807** |
| ECR | 0.267 (12/45) | **0.467 (21/45)** |
| EE | 0.801 | **0.926** |
| Steps | 4.04 | 3.91 |
| invalid/case | 0.489 | 0.089 |
| Chi phí | ~$0.08 | ~$0.39 |

22/45 case có khác biệt JRA hoặc ECR giữa 2 model:
- **17 case ECR 0→1** (gemini đóng milestone đầy đủ hơn — đặc biệt
  `liveness/readiness_probe_incorrect_port` và các case OOM... không: OOM
  cả 2 model đều ECR=0).
- **5 case ECR 1→0** (deepseek đóng, gemini bỏ sót milestone).
- **5 case JRA 1→0** (chính nhóm timing ở trên).

## So với bảng paper (caveats)

⚠️ Không phải reproduce: checkpoint qua OpenRouter (không verify được là
snapshot nào), chỉ 1 category Easy (45/550 case), harness commit `ec1d4f3`.

| Metric | Paper: Gemini-2.5-Flash (Boutique, 550) | Run này (runtime, 45) |
|---|---:|---:|
| CA / FA / JRA | 0.82 / 0.67 / 0.65 | 1.00 / 0.89 / 0.89 |
| MC / EOC / ECR | 0.71 / 0.67 / 0.37 | 0.82 / 0.81 / 0.47 |
| EE / Steps / RAR | 0.58 / 6.49 / 0.01 | 0.93 / 3.91 / 0.00 |

Cùng chiều: JRA–ECR gap vẫn hiện rõ (0.89 vs 0.47; paper: 0.65 vs 0.37),
CA > FA (nhóm fault type gần nhau gây nhầm lẫn).

## Quan sát chính

1. **JRA–ECR gap tồn tại ở cả 2 model, 2 hướng:**
   - deepseek: JRA 1.00 nhưng ECR 0.27 — đúng nghĩa "ungrounded diagnosis"
     (Finding 2): đoán đúng từ tín hiệu cục bộ, không thu đủ evidence.
   - gemini case 17/19/20: **ECR=1 mà JRA=0** — hình chiếu ngược: agent đi
     đủ toàn bộ milestone (kể cả xem cấu hình probe) nhưng **vẫn kết luận
     sai label**. Quá trình "đóng" theo D* không bảo đảm kết luận đúng —
     D* được gán cho đúng fault, còn agent thiết lập các milestone trong
     khung giải thích OOM của nó. Đây là ví dụ cụ thể cho giới hạn của
     milestone-based process eval (liên quan Finding 1 & 2).
2. **Nhầm lẫn hệ thống theo fault type** (5/5 timing→OOM) cho thấy lỗi không
   ngẫu nhiên: cùng một confound telemetry, model nhất quán sai — thuận lợi
   cho việc nghiên cứu failure mode (dùng được làm pilot "confound
   probe-timing vs OOM").
3. **Chi phí/thời gian không phải nút chai**: $0.39/45 case, ~30 phút;
   0 case kẹt budget; RAR=0.

## Việc tiếp theo

- [ ] (Optional) Reproduce confound: chạy lại 5 case timing (17–21) với
      deepseek + gemini, đọc prompt/trace chi tiết so sánh bước nào phân kỳ.
- [ ] (Optional) Chạy category Hard (`boutique/performance`, 29 case) với 1
      model để xem JRA–ECR gap ở nơi tín hiệu yếu hơn.
- [ ] (Optional) Skill agent trên 45 case này (save_root riêng) — kiểm tra
      giả thuyết "skill giúp đóng milestone OOM/protocol (ECR 0→cao hơn)".
- [ ] Khi viết luận văn: trích cặp số deepseek/gemini với caveat "2 model,
      45 case Easy, checkpoint không verify" — dùng làm evidence định tính
      cho JRA–ECR gap, không dùng làm reproduce bảng paper.
