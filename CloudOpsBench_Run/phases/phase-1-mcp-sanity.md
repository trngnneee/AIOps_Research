# Phase 1 — Sanity check MCP server (không LLM)

Plan: `../RUN_PLAN.md` · Repo: `/Users/trngnneee/CloudOpsBench/Cloud-OpsBench` @ `ec1d4f3`
Ngày chạy: 2026-11-10.

## 1a — Unit tests của MCP server (offline, không LLM)

**Lệnh (chạy từ repo root):**

```bash
.venv/bin/python -m unittest discover -s cloudopsbench_mcp/tests -v
```

**Kết quả: PASS — 12/12 tests OK trong 0.916s** (2026-11-10)

| Test | Nội dung kiểm tra (theo `cloudopsbench_mcp/tests/test_server.py`) | Kết quả |
|---|---|---|
| `test_exposes_exactly_the_backend_twelve_tools` | Boutique server expose đúng 12 tools, schema không lộ `case_path` | ok |
| `test_trainticket_uses_its_backend_and_exposes_ten_tools` | TrainTicket (case `service/25`) expose đúng 10 tools | ok |
| `test_catalog_preserves_backend_descriptions_and_schemas` | Catalog MCP giữ nguyên mô tả + schema argument của backend (mọi case, cả 2 system) | ok |
| `test_call_result_matches_existing_backend` | Kết quả `tools/call` qua MCP trùng kết quả gọi thẳng backend | ok |
| `test_resource_queries_match_both_backends` | Query resource khớp ở cả 2 backend | ok |
| `test_boutique_source_code_matches_backend` | Tool code inspection (boutique) khớp `tool_cache.json` | ok |
| `test_missing_required_arguments_return_recorded_error` | Thiếu argument bắt buộc → error được ghi, không crash | ok |
| `test_optional_limit_counts_invalid_requests_and_blocks_backend` | `CLOUDOPSBENCH_MAX_TOOL_CALLS`: request invalid vẫn tính vào hạn mức và chặn backend | ok |
| `test_rejects_hidden_case_arguments_and_records_call` | Client không tự chọn case (từ chối argument ẩn), call vẫn được ghi log | ok |
| `test_restricted_snapshot_needs_no_metadata_or_labels` | Server chạy được với snapshot chỉ gồm `tool_cache.json` + `raw_data/` (không cần `metadata.json`, `process-label/`) — khớp nguyên tắc "data boundary" trong MCP README | ok |
| `test_boutique_streamable_http_connection` | Kết nối Streamable HTTP loopback thật (boutique) | ok |
| `test_trainticket_streamable_http_connection` | Kết nối Streamable HTTP loopback thật (train-ticket) | ok |

**Raw output unittest (giữ nguyên):**

```text
test_boutique_source_code_matches_backend (test_server.CloudOpsMCPTests.test_boutique_source_code_matches_backend) ... ok
test_boutique_streamable_http_connection (test_server.CloudOpsMCPTests.test_boutique_streamable_http_connection) ... GetAlerts:{}
GetAlerts:{}
ok
test_call_result_matches_existing_backend (test_server.CloudOpsMCPTests.test_call_result_matches_existing_backend) ... GetAlerts:{}
GetAlerts:{}
ok
test_catalog_preserves_backend_descriptions_and_schemas (test_server.CloudOpsMCPTests.test_catalog_preserves_backend_descriptions_and_schemas) ... ok
test_exposes_exactly_the_backend_twelve_tools (test_server.CloudOpsMCPTests.test_exposes_exactly_the_backend_twelve_tools) ... ok
test_missing_required_arguments_return_recorded_error (test_server.CloudOpsMCPTests.test_missing_required_arguments_return_recorded_error) ... ok
test_optional_limit_counts_invalid_requests_and_blocks_backend (test_server.CloudOpsMCPTests.test_optional_limit_counts_invalid_requests_and_blocks_backend) ... GetAlerts:{}
ok
test_rejects_hidden_case_arguments_and_records_call (test_server.CloudOpsMCPTests.test_rejects_hidden_case_arguments_and_records_call) ... ok
test_resource_queries_match_both_backends (test_server.CloudOpsMCPTests.test_resource_queries_match_both_backends) ... ok
test_restricted_snapshot_needs_no_metadata_or_labels (test_server.CloudOpsMCPTests.test_restricted_snapshot_needs_no_metadata_or_labels) ... GetAlerts:{}
GetAlerts:{}
ok
test_trainticket_streamable_http_connection (test_server.CloudOpsMCPTests.test_trainticket_streamable_http_connection) ... GetAlerts:{}
GetAlerts:{}
ok
test_trainticket_uses_its_backend_and_exposes_ten_tools (test_server.CloudOpsMCPTests.test_trainticket_uses_its_backend_and_exposes_ten_tools) ... GetAlerts:{}
ok

----------------------------------------------------------------------
Ran 12 tests in 0.916s

OK
```

**Ghi nhận:** output có dòng `GetAlerts:{}` — đây là output của tool được test gọi trong quá trình test (case test không có alert hoặc alert rỗng), không phải lỗi; unittest vẫn kết luận `OK`.

## 1b — Start MCP server thật + gọi bằng client (Streamable HTTP)

**Lệnh (từ repo root):**

```bash
export CLOUDOPSBENCH_CASE_PATH="$PWD/benchmark/boutique/runtime/1"
export CLOUDOPSBENCH_SYSTEM="boutique"
export CLOUDOPSBENCH_FAULT_CATEGORY="runtime"
export CLOUDOPSBENCH_RUN_ID="smoke-boutique-runtime-1"
export CLOUDOPSBENCH_TRACE_PATH="$PWD/.runs/smoke-boutique-runtime-1/mcp.jsonl"
.venv/bin/python -m cloudopsbench_mcp
# -> Uvicorn running on http://127.0.0.1:8000
```

Client smoke: `AiOps/CloudOpsBench_Run/mcp_smoke.py` (stdlib `urllib`, JSON-RPC
qua Streamable HTTP: `initialize` → `tools/list` → `tools/call`).

**Kết quả: PASS** (2026-11-10, ~20:46)

| Bước | Kết quả |
|---|---|
| `initialize` | `serverInfo: cloudopsbench 0.1.0`. **Server stateless — không phát `Mcp-Session-Id` header** (spec cho phép; client bỏ qua header session). |
| `tools/list` | Đúng **12 tools** (catalog boutique), description giữ nguyên từ backend: GetResources, DescribeResource, GetAppYAML, GetRecentLogs, GetErrorLogs, CheckServiceConnectivity, GetServiceDependencies, GetClusterConfiguration, GetAlerts, CheckNodeServiceStatus, ListCodeFiles, GetSourceCode |
| `GetAlerts {}` | `"No active metric anomalies detected at this time."` (`isError=false`) |
| `GetResources {namespace: boutique}` (thiếu `resource_type`) | `isError=true` + pydantic validation error — argument validation hoạt động, backend không chạy |
| `GetResources {resource_type: pods, namespace: boutique}` | List 11 pods; trong đó **`adservice-d6c9fcc6b-d4nlb  RESTARTS 2 (30s ago)`** |
| Trace `.runs/smoke-boutique-runtime-1/mcp.jsonl` | Ghi đủ 4 calls: `sequence`, `tool_name`, `is_error`, `duration_ms` (0.04–0.42 ms/call) |

**Raw output client (`mcp_smoke.py`, giữ nguyên):**

```text
[initialize] serverInfo: {'name': 'cloudopsbench', 'version': '0.1.0'}
[initialize] session: (không có — server stateless, bỏ qua header)
[tools/list] số tools: 12
  - GetResources: Simulates `kubectl get` to retrieve resource lists or current status details. IM
  - DescribeResource: Simulates `kubectl describe`. Retrieves detailed state, events, and conditions f
  - GetAppYAML: Retrieves the raw YAML configuration file for a specific service. Returns static
  - GetRecentLogs: Retrieves raw recent container logs for a specified Kubernetes service.
  - GetErrorLogs: Retrieves a statistical summary of application error logs grouped by error patte
  - CheckServiceConnectivity: Performs an active TCP connectivity check to the target service port from within
  - GetServiceDependencies: Retrieves the service network topology, showing upstream and downstream communic
  - GetClusterConfiguration: Retrieves a holistic health and configuration summary of all nodes in the cluste
  - GetAlerts: Retrieves active system alerts triggered by metric anomalies such as high latenc
  - CheckNodeServiceStatus: Checks the operating status of critical Kubernetes infrastructure components on
  - ListCodeFiles: Returns the business-code file list for a given microservice, including each fil
  - GetSourceCode: Returns the source code of one selected file.
[tools/call] GetAlerts arguments={}
[GetAlerts result] isError: False
No active metric anomalies detected at this time.

[tools/call] GetResources arguments={'namespace': 'boutique'}
[GetResources result] isError: True
Invalid tool arguments: 1 validation error for GetResourcesInput
resource_type
  Field required [type=missing, input_value={'namespace': 'boutique'}, input_type=dict]
    For further information see https://errors.pydantic.dev/2.14/v/missing.

SMOKE OK
```

Gọi lại `GetResources` đúng schema (`resource_type: "pods"`, `namespace:
"boutique"` — bằng curl, JSON-RPC id=5) trả về:

```text
NAME                                     READY   STATUS    RESTARTS      AGE
adservice-d6c9fcc6b-d4nlb                1/1     Running   2 (30s ago)   90s
cartservice-79b49f5555-fmgk7             1/1     Running   0             92s
checkoutservice-8445f8b6cb-kk958         1/1     Running   0             92s
currencyservice-75686c9564-bxbbm         1/1     Running   0             92s
emailservice-c86b9b8f6-c6lvl             1/1     Running   0             92s
frontend-657dd795f-tpqs6                  1/1     Running   0             92s
paymentservice-78c596648-4nr2p           1/1     Running   0             91s
productcatalogservice-ddb46fc86-z8p6c    1/1     Running   0             91s
recommendationservice-7bf5b7d9b8-2cfzn   1/1     Running   0             91s
redis-cart-6f966d9cc9-nwdl2              1/1     Running   0             91s
shippingservice-7ff54bf6b6-2gcm8         1/1     Running   0             91s
```

**Ghi nhận:**

- Case smoke là `boutique/runtime/1`: `query = "Service abnormal restart."`,
  `R* = {fault_object: app/adservice, root_cause: liveness_probe_incorrect_protocol}`.
  Observation từ `GetResources` (adservice restart 2 lần) khớp đúng triệu chứng —
  snapshot replay cho kết quả deterministic như thiết kế.
- `GetAlerts` trả rỗng ở case này là **đúng dữ liệu** (tool_cache key
  `GetAlerts:{}`), không phải bug — chính vì vậy dòng `GetAlerts:{}` trong
  unittest Phase 1a là của cùng case này. Liveness-probe fault ở đây phải tìm
  qua pod status/describe, không qua alert.
- Muốn đổi case: Ctrl-C server, đổi `CLOUDOPSBENCH_CASE_PATH`/run-id/trace, start lại
  (một instance = một case).
