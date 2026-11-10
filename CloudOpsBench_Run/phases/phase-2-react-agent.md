# Phase 2 — Chạy 1 case bằng baseline ReAct agent

Plan: `../RUN_PLAN.md` · Repo: `/Users/trngnneee/CloudOpsBench/Cloud-OpsBench` @ `ec1d4f3`
Ngày chạy: 2026-11-10.

## Thiết lập

- Lệnh: `.venv/bin/python agents/cloudops_agent/run.py` (từ repo root)
- Config (`agents/cloudops_agent/configs/model_configs.yaml`):
  - `model: "deepseek/deepseek-v4-flash-0731"` qua OpenRouter
    (`api_base: https://openrouter.ai/api/v1`), `temperature: 0`, `max_tokens: 4096`
  - `system: boutique`, `fault_category: runtime`, `case_name: "1"`,
    `max_iterations: 20`
  - `dataset_root: /Users/trngnneee/CloudOpsBench/Cloud-OpsBench`,
    `save_root: /Users/trngnneee/CloudOpsBench/trajectory/`
  - API key: điền local khi chạy, xóa sau khi chạy xong (config không giữ key).

## Kết quả: PASS — agent chẩn đoán đúng rank 1, submit sau 3 steps

```text
[PLAN] system=boutique category=runtime cases=1 model=deepseek/deepseek-v4-flash-0731 ...
[RUN] 1/1 case=1
[DONE] case=boutique/runtime/1 finished=True steps=3
```

`result_raw.json`: `finished=true`, `stop_reason=submit`, `steps_used=3`.

### Chuỗi steps (từ trace `1.json`)

| Step | Action (input) | Input/Output tokens | Latency |
|---|---|---|---|
| 1 | `GetResources {"resource_type": "pods", "namespace": "boutique", "output_wide": true}` | 4 078 / 57 | 2.1s |
| 2 | `DescribeResource {"resource_type": "pod", "name": "adservice-d6c9fcc6b-d4nlb", "namespace": "boutique"}` | 4 647 / 201 | 5.4s |
| 3 | `Submit {top_3_predictions, key_evidence_summary}` | 5 880 / 582 | 12.4s |

Không có step nào `invalid`, không có tool error.

### So `R̂` với `R*`

Case `boutique/runtime/1`: `query = "Service abnormal restart."`,
`R* = {fault_object: app/adservice, root_cause: liveness_probe_incorrect_protocol}`.

| Rank | `R̂` (fault_object / root_cause) | So với `R*` |
|---|---|---|
| 1 | `app/adservice` / `liveness_probe_incorrect_protocol` | **KHỚP CẢ HAI TRƯỜNG** |
| 2 | `app/adservice` / `liveness_probe_incorrect_port` | đúng component, subtype gần |
| 3 | `app/adservice` / `readiness_probe_incorrect_protocol` | đúng component, probe khác |

→ Manual check: `CA = 1`, `FA = 1`, `JRA = 1` (rank 1).

### Key evidence (agent tự tổng hợp)

> adservice pod has RESTARTS=2 while all other pods have 0. Pod describe shows
> liveness probe is http-get on port 9555, but adservice is a gRPC service.
> Liveness probe failures show malformed HTTP status code from the gRPC response,
> causing the container to be killed and restarted.

Logic nhân quả đúng cơ chế fault: probe sai protocol (HTTP thay vì gRPC trên
9555) → probe fail → kubelet kill/restart → "Service abnormal restart".

## Ghi nhận

- Chi phí lượt này: ~14.6k input + ~0.8k output tokens (3 calls OpenRouter) —
  vài phần nghìn USD với deepseek-v4-flash.
- 3 steps cho case difficulty `easy` — thấp hơn mức trung bình
  `DeepSeek-V4-Flash` trên Boutique trong README (~6.45 steps).
- Trace + `result_raw.json` ghi đúng layout `<save_root>/<system>/<model>/
  <category>/<case>/`; resume logic (SKIP nếu `stop_reason ∈ {submit, max_steps}`)
  đã được quan sát hoạt động ở lượt trước — muốn chạy lại cùng case/cùng model
  phải xóa trace trước.
