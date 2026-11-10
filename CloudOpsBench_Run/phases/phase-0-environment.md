# Phase 0 — Môi trường + dữ liệu benchmark

Plan: `../RUN_PLAN.md` · Repo: `/Users/trngnneee/CloudOpsBench/Cloud-OpsBench` @ `ec1d4f3`
Ngày chạy: 2026-11-10.

## Môi trường

- macOS (machine `NEWERA-NguyenDT-TECH`), repo clone:
  `/Users/trngnneee/CloudOpsBench/Cloud-OpsBench` @ `ec1d4f3`
- venv `.venv` tại root repo, **Python 3.14.6** (mới hơn mức docs yêu cầu ≥3.10;
  cả Phase 0 và Phase 1a chạy sạch, chưa thấy issue)
- Deps chính: `mcp 2.3.0`, `pydantic 2.14.3`, `openai 3.49.0`,
  `uvicorn 0.54.0`, `yaml 6.0.3`

## Kết quả: PASS

- Tạo `.venv` bằng `python3 -m venv .venv`, cài từ
  `agents/cloudops_agent/requirements.txt` + `cloudopsbench_mcp/requirements.txt`.
- `.venv/bin/python -c "import openai, pydantic, yaml, mcp, uvicorn"` không lỗi.

## Dữ liệu benchmark (đã kiểm tra trong repo)

- Đủ **754/754 case** ngay trong repo, không cần tải dataset HuggingFace:
  - boutique: 550 case (admission 58, scheduling 164, startup 62, runtime 45,
    service 54, performance 29, infrastructure 40, codedefect 98)
  - trainticket: 204 case (startup 24, runtime 96, service 37, performance 47)
- `process-label/` và `golden-trajectory/` phủ đủ 754 case.
- `benchmark/` chiếm ~3.6 GB. Số case khớp đúng bảng Fault Taxonomy trong
  README (57 fault types).
