# RUN_PLAN — Chạy code Cloud-OpsBench

> Plan cá nhân (không thuộc upstream) để chạy code của repo này, đối chiếu với
> paper Cloud-OpsBench (arXiv 2603.00468).
> Repo: `github.com/LLM4Ops/Cloud-OpsBench` @ `ec1d4f3` (clone local).
> Ngày lập: 2026-11-10.

## 0. Bức tranh: có 4 thứ chạy được trong repo

| # | Thành phần | Nó làm gì | Cần LLM API key? |
|---|---|---|---|
| A | `interact.py` | Demo tương tác: tay gọi tool trên 1 case, xem ground truth | Không |
| B | `agents/cloudops_agent/` | ReAct agent baseline (skill-free) — chạy batch case | **Có** |
| C | `agents/cloudops_skill_agent/` | ReAct agent có Skill (SelectSymptom + Diagnostic Graph) | **Có** |
| D | `cloudopsbench_mcp/` | MCP server (Streamable HTTP, port 8000) để nối agent tự viết | Không (server) |

- B, C, D dùng chung backend tool snapshot ở `agents/cloudops_agent/tools/`.
- Không cần cluster, không cần deploy microservice: mọi thứ replay từ
  `benchmark/<system>/<category>/<case_id>/` (`metadata.json`, `tool_cache.json`, `raw_data/`, `code/`).
- Đối chiếu paper: mỗi lần chạy 1 case là 1 episode `Φ: ⟨U, S⟩ → ⟨T, R̂⟩`.
  - `U` = `query` trong `metadata.json`; `S` = snapshot của case.
  - `T` = file trace agent sinh ra (các cặp tool call + observation).
  - `R̂` = final answer của agent; evaluation so `R̂` với `R*` (`metadata.json → result`)
    và so `T` với `D*` (`process-label/.../milestone.json`).

## 1. Phase 0 — Môi trường (1 lần)

```bash
cd /Users/trngnneee/CloudOpsBench/Cloud-OpsBench
python3 -m venv .venv
.venv/bin/pip install -r agents/cloudops_agent/requirements.txt \
                       -r cloudopsbench_mcp/requirements.txt
```

- Python local hiện tại: **3.14.6** (MCP yêu cầu ≥ 3.10). Nếu pydantic/mcp lỗi
  trên 3.14 → cài Python 3.12 (`uv python install 3.12` hoặc pyenv) và tạo lại venv.
- Cho Phase 2 trở đi cần một **OpenAI-compatible API key** (OpenAI, OpenRouter,
  Gemini via LiteLLM proxy, vLLM local, v.v.).

**Checkpoint 0:** `.venv/bin/python -c "import openai, pydantic, yaml, mcp, uvicorn"` không lỗi.

## 2. Phase 1 — Sanity check không cần LLM (miễn phí)

### 2.1. Unit tests của MCP server (offline)

```bash
.venv/bin/python -m unittest discover -s cloudopsbench_mcp/tests -v
```

**Checkpoint 1a:** tất cả test PASS (kiểm tra tool catalog boutique=12,
train-ticket=10, backend-equivalent results, loopback HTTP).

### 2.2. Khởi động MCP server với 1 case

```bash
cd /Users/trngnneee/CloudOpsBench/Cloud-OpsBench
export CLOUDOPSBENCH_CASE_PATH="$PWD/benchmark/boutique/runtime/1"
export CLOUDOPSBENCH_SYSTEM="boutique"
export CLOUDOPSBENCH_FAULT_CATEGORY="runtime"
export CLOUDOPSBENCH_RUN_ID="smoke-boutique-runtime-1"
export CLOUDOPSBENCH_TRACE_PATH="$PWD/.runs/smoke-boutique-runtime-1/mcp.jsonl"
.venv/bin/python -m cloudopsbench_mcp
```

- Server chạy ở `http://127.0.0.1:8000/mcp` (Streamable HTTP). Ctrl-C để tắt.
- Một instance = một case; đổi case là khởi động lại server.
- Kiểm thử nhanh bằng client MCP bất kỳ (hoặc Phase 5), gọi `tools/list` →
  phải thấy 12 tools cho boutique.

**Checkpoint 1b:** server lên, `tools/list` trả 12 tools, gọi `GetAlerts`
trả về alert của case `boutique/runtime/1`.

### 2.3. (Tham khảo) `interact.py`

```bash
.venv/bin/python interact.py boutique runtime
```

⚠️ **Dự kiến FAIL** ở commit hiện tại — xem "Known issues" (mục 6).
Nếu muốn dùng, sửa hoặc bỏ qua và dùng MCP server (2.2) thay thế.

## 3. Phase 2 — Chạy 1 case bằng ReAct agent baseline (B)

### 3.1. Sửa config

File: `agents/cloudops_agent/configs/model_configs.yaml`

```yaml
model:
  model: "<model-name>"            # vd: "gpt-5", "deepseek-v4-flash", ...
  provider: openai_compatible
  api_base: "<your-api-base>"
  api_key: "<your-api-key>"        # ⚠️ file này bị git track — KHÔNG commit key
  temperature: 0
  max_tokens: 4096
  timeout: 60
  # Qwen: uncomment nếu cần
  # enable_thinking: false

diagnosis:
  max_iterations: 20
  system: "boutique"               # ["boutique", "trainticket"]
  fault_category: "runtime"        # ["admission","scheduling","startup","runtime",
                                   #  "service","performance","infrastructure","codedefect" (boutique)]
  case_name: "1"                   # 1 case duy nhất; để "" = chạy cả category
  dataset_root: "/Users/trngnneee/CloudOpsBench/Cloud-OpsBench"
  save_root: "/Users/trngnneee/CloudOpsBench/trajectory/"
```

Lưu ý:
- `fault_category` hợp lệ phụ thuộc system: trainticket chỉ có
  `startup, runtime, service, performance`; boutique có đủ 8 (kể cả `codedefect`).
- `dataset_root` mặc định trong repo là `/root/Cloud-OpsBench` (path Linux) — **phải đổi**.
- `save_root` trong `agents/cloudops_agent/.gitignore` có pattern `trajectory/`
  nhưng save_root nằm ngoài repo (ở `/Users/trngnneee/CloudOpsBench/trajectory/`) nên an toàn.

### 3.2. Chạy

```bash
cd /Users/trngnneee/CloudOpsBench/Cloud-OpsBench
.venv/bin/python agents/cloudops_agent/run.py
```

- Không cần CLI args; mọi thứ đọc từ config.
- Có resume: case nào đã có trace `stop_reason ∈ {submit, max_steps}` sẽ bị SKIP.

### 3.3. Kiểm tra output

```
<save_root>/boutique/<model>/runtime/1/
├── 1.json            # T: full trace — mỗi step: thought, action, action_input,
│                     #   observation, tokens, latency
└── result_raw.json   # R̂: final answer (top-3 predictions) + stop_reason + steps_used
```

Đối chiếu tay: mở `benchmark/boutique/runtime/1/metadata.json` → field `result`
là `R*`. So component + fault type của `R̂` (rank 1) với `R*`.

**Checkpoint 2:** trace `1.json` có đầy đủ steps, `result_raw.json` có
`top_3_predictions`, agent không crash trong 20 iterations.

## 4. Phase 3 — Evaluation

```bash
cd /Users/trngnneee/CloudOpsBench/Cloud-OpsBench
.venv/bin/python agents/cloudops_agent/evaluation.py
```

- Đọc **cùng một** `configs/model_configs.yaml`, tự tìm benchmark cases +
  outputs tương ứng dưới `save_root`.
- Báo cáo: `CA, FA, JRA` (outcome) + `MC, EOC, ECR, EE, steps, RAR,
  invalid_actions` (process — so trace với `process-label/.../milestone.json`).
- Với 1 case: outcome metrics là 0/1 của đúng case đó; giá trị trung bình chỉ
  có ý nghĩa khi chạy nhiều case (Phase 4).

**Checkpoint 3:** `evaluation.py` in ra bảng metrics (không crash, tìm thấy
trace + milestone cho case đã chạy).

## 5. Phase 4 — Mở rộng (có chi phí, làm có chủ đích)

1. **Chạy cả 1 category:** xóa `case_name` (để `""`) rồi `run.py`.
   - boutique/runtime = ~141 case? (xem `ls benchmark/boutique/runtime | wc -l`
     trước khi chạy) — mỗi case tối đa `max_iterations`=20 lần gọi LLM,
     trung bình ~6–16 steps theo bảng paper.
   - **Ước lượng chi phí:** ~500–800 lần gọi LLM cho 1 category.
     Chạy smoke bằng model rẻ/flash trước, model mạnh chạy sau.
2. **Chạy cả system:** lặp cho từng `fault_category`, giữ `system` cố định.
   - Boutique 550 case, Train-Ticket 204 case → đây là quy mô 1 hàng trong
     bảng Experimental Results của paper (1 model × 1 system).
3. **Agent có Skill (C):** làm y hệt Phase 2–3 nhưng trong
   `agents/cloudops_skill_agent/`, **`save_root` riêng** (vd
   `trajectory/skill/`) để không trộn trajectories khi so sánh B vs C.
4. **Reproduce bảng paper:** mỗi hàng = 1 model × 1 system (toàn bộ case).
   So `CA/FA/JRA/MC/EOC/ECR/EE/Steps/RAR` của mình với bảng README.

## 6. Known issues (tại commit `ec1d4f3`, cần kiểm tra khi chạy)

1. **`interact.py` đã stale so với layout hiện tại.** Nó trỏ
   `AGENT_ROOT = ./cloudops_agent` (thiếu prefix `agents/`) và import
   `tools.adapters` / `tools.definition` — các module này không còn tồn tại
   (tools giờ ở `agents/cloudops_agent/tools/{cloudops,snapshot}.py`).
   → "Easy Demo" trong README dự kiến broken. Fix nhanh: sửa
   `AGENT_ROOT` thành `agents/cloudops_agent` và import
   `from tools.cloudops import create_k8s_tools` + viết lại phần gọi tool
   (hàm `call_tool` cũ không còn). Chưa fix — chờ Phase 1 chạy xong mới quyết.
2. **Config mặc định dùng path Linux** (`/root/...`) — đổi theo Phase 2.
3. **`configs/model_configs.yaml` bị git track** (không nằm trong .gitignore).
   Khi điền API key, file sẽ hiện trong `git status` — **không commit**.
   Có thể thêm vào `.gitignore` local hoặc giữ diff riêng.
4. **Python 3.14** chưa được repo test chính thức (docs nói ≥3.10). Fallback:
   Python 3.12.

## 7. Phase 5 (optional) — Nối agent tự viết qua MCP (D)

Phục vụ nghiên cứu: thay vì dùng ReAct agent có sẵn, viết/điều khiển agent
riêng (vd chính opencode) và để MCP server cung cấp tools.

1. Start server như Phase 2.2 (mỗi case một instance, port/run-id/trace riêng).
2. Config client — có sẵn example cho **opencode**
   (`cloudopsbench_mcp/examples/opencode/opencode.json`):

   ```json
   {
     "mcp": {
       "cloudopsbench": {
         "type": "remote",
         "url": "http://127.0.0.1:8000/mcp",
         "enabled": true,
         "oauth": false
       }
     }
   }
   ```

   Merge vào config của **một workspace riêng**, ngoài repo benchmark.
3. Task prompt cho agent: lấy `query` + `namespace` từ `metadata.json` của case:

   ```text
   Diagnose the reported incident in namespace <namespace>.
   Incident report: <query>
   Use the cloudopsbench MCP tools to collect incident evidence.
   Identify the faulty component and root cause, and explain the supporting evidence.
   ```

   ⚠️ Giữ field `result` (ground truth) **xa agent** — chỉ dùng khi chấm.
4. Server ghi mọi tool call vào `CLOUDOPSBENCH_TRACE_PATH` (JSONL).
   ⚠️ **Trace JSONL của MCP KHÔNG phải input format của `evaluation.py`**
   (evaluator đọc trace format của ReAct agent). Muốn chấm agent tự viết bằng
   metrics chính thức cần viết converter trace → format
   `evaluation_utils` (nghiên cứu thêm, ghi ở đây khi làm).

## 8. Checklist tổng

- [ ] Phase 0: venv + deps import được
- [ ] Phase 1: MCP unittest xanh; server lên, 12 tools (boutique)
- [ ] Phase 2: 1 case chạy xong, trace + result_raw tồn tại, so tay với `R*`
- [ ] Phase 3: `evaluation.py` ra bảng metrics
- [ ] Phase 4: (optional) 1 category đầy đủ; agent skill so sánh
- [ ] Phase 5: (optional) agent tự viết qua MCP + converter trace
- [ ] Không commit API key; không push gì lên remote nếu chưa được yêu cầu
