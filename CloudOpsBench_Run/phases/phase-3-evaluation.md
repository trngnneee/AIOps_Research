# Phase 3 — Evaluation (case boutique/runtime/1, deepseek-v4-flash-0731)

Plan: `../RUN_PLAN.md` · Repo: `/Users/trngnneee/CloudOpsBench/Cloud-OpsBench` @ `ec1d4f3`
Ngày chạy: 2026-11-10.

## Lệnh

```bash
.venv/bin/python agents/cloudops_agent/evaluation.py
```

(Offline, không cần LLM/API key: đọc `configs/model_configs.yaml` để định vị
`<save_root>/boutique/deepseek/deepseek-v4-flash-0731/runtime/` + so với
`process-label/boutique/runtime/`.)

## Raw output (giữ nguyên)

```text
Outcome Evaluation v2
================================================================================
config_path: /Users/trngnneee/CloudOpsBench/Cloud-OpsBench/agents/cloudops_agent/configs/model_configs.yaml
system: boutique
fault_category: runtime
case_split:
case_split_file:
label_root: /Users/trngnneee/CloudOpsBench/Cloud-OpsBench/process-label/boutique/runtime
agent_root: /Users/trngnneee/CloudOpsBench/trajectory/boutique/deepseek/deepseek-v4-flash-0731/runtime
--------------------------------------------------------------------------------
total_cases: 45
selected_cases: 1
run_cases: 1
missing_run_cases: 0
invalid_action_total: 0
--------------------------------------------------------------------------------
CA (Component Accuracy): 1.0
FA (Fault-Type Accuracy): 1.0
JRA (Joint RCA Accuracy): 1.0
MC (Milestone Coverage): 0.6667
EOC (Evidence-Order Consistency): 0.6667
ECR (Evidence Closure Rate): 0.0
EE (Evidence Efficiency): 1.0
steps (Average Diagnostic Steps per Case): 3.0
RAR (Redundant Action Rate): 0.0
invalid_actions (Average Invalid Actions per Case): 0.0
--------------------------------------------------------------------------------
Summary JSON: /Users/trngnneee/CloudOpsBench/trajectory/boutique/deepseek/deepseek-v4-flash-0731/evaluation_v2_runtime_summary.json
Detail JSON: /Users/trngnneee/CloudOpsBench/trajectory/boutique/deepseek/deepseek-v4-flash-0731/evaluation_v2_runtime_details.json
```

Pipeline evaluation hoạt động: tìm đúng trace, đúng milestone, không crash,
`missing_run_cases: 0`.

## Phân tích: outcome đúng, process chưa đóng

### Outcome (rank 1)

| Metric | Giá trị | Nghĩa |
|---|---|---|
| CA | 1.0 | Component đúng: `app/adservice` = `R*.fault_object` |
| FA | 1.0 | Fault type đúng: `liveness_probe_incorrect_protocol` = `R*.root_cause` |
| JRA | 1.0 | Cả hai đúng cùng lúc |

### Process — so trace với milestone graph (`process-label/boutique/runtime/1/milestone.json`)

Graph `D*` của case này có 3 milestone group, dependency M1 → M2 → M3,
`completion_formula: all [M1, M2, M3]`:

| Milestone | Role | Bằng chứng được phép (tóm tắt) | Agent có đạt không? |
|---|---|---|---|
| M1 | `first_level_liveness_symptom` | `GetResources(pods, boutique)` mà observation chứa "adservice" + RESTARTS/CrashLoop | ✅ Step 1: `GetResources(pods, output_wide)` — pod adservice RESTARTS=2 |
| M2 | `probe_failure_evidence` | `DescribeResource(pod adservice-d6c9fcc6b-d4nlb)` | ✅ Step 2: đúng pod, đúng tool — events liveness probe fail |
| M3 | `root_cause_probe_configuration` | `GetAppYAML(adservice)` hoăc `DescribeResource(deployment/replicaset adservice)` — xem cấu hình probe (http vs grpc, port 9555) | ❌ **Không đạt** — agent Submit ngay sau step 2, chưa bao giờ xem YAML/Deployment để xác nhận probe được khai báo sai protocol |

→ `MC = 2/3 = 0.6667`, `EOC = 0.6667` (M1→M2 đúng thứ tự nhân quả; M3 thiếu),
`ECR = 0` (binary: chưa đủ "all"), `EE = 1.0` (cả 2 tool call đều đóng góp
milestone hợp lệ), `RAR = 0`, `invalid_actions = 0`.

### Đọc kết quả

- Agent suy ra đúng root cause **chỉ từ pod describe** (events probe failure
  "malformed HTTP status code" + knowledge rằng adservice là gRPC service) —
  mà không cần bước xác nhận cấu hình M3. Đúng nghĩa "ungrounded diagnosis":
  rank-1 đúng, nhưng bằng chứng chưa đóng vòng.
- Đây chính là pattern **khoảng cách JRA–ECR** (paper §4.3, Table 4) được ghi
  trong `AiOps/finding/CloudOpsBench_FINDING.md` (Finding 2) — quan sát ở quy
  mô 1 case, 1 model.
- Góc nhìn Finding 1 (nhãn chủ quan): M3 đòi agent phải *xem lại* cấu hình
  probe dù evidence ở M2 đã gần đủ để kết luận — "đủ bằng chứng" là phán đoán
  của người gán nhãn, không phải của cơ chế fault.
- **Lưu ý:** mới 1 case → các metric trung bình (MC, EOC, EE, steps, RAR...)
  chưa có ý nghĩa thống kê; mục đích lượt này là verify pipeline Phase 3.
