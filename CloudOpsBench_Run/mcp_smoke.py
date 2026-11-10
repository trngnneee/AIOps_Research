"""MCP smoke client for Cloud-OpsBench (stdlib only).

Chạy khi server `python -m cloudopsbench_mcp` đang listen ở 127.0.0.1:8000.
Làm: initialize -> tools/list -> tools/call GetAlerts -> tools/call GetResources.
"""
from __future__ import annotations

import json
import sys
import urllib.request

URL = "http://127.0.0.1:8000/mcp"
BASE_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def post(payload: dict, session: str | None = None):
    headers = dict(BASE_HEADERS)
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.headers, resp.read().decode("utf-8")


def parse(body: str) -> dict | None:
    body = body.strip()
    if not body:
        return None
    if body.startswith("{"):
        return json.loads(body)
    for line in body.splitlines():
        if line.startswith("data:"):
            return json.loads(line[5:].strip())
    raise ValueError(f"Unparseable response: {body[:500]}")


def main() -> int:
    headers, body = post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "mcp-smoke", "version": "0.1"},
            },
        }
    )
    init = parse(body)
    print("[initialize] serverInfo:", init["result"].get("serverInfo"))
    session = headers.get("Mcp-Session-Id")
    print("[initialize] session:", session or "(không có — server stateless, bỏ qua header)")

    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, session=session)

    _, body = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, session=session)
    tools = parse(body)["result"]["tools"]
    print(f"[tools/list] số tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {(tool.get('description') or '').splitlines()[0][:80]}")

    case = "GetAlerts"
    print(f"[tools/call] {case} arguments={{}}")
    _, body = post(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": case, "arguments": {}},
        },
        session=session,
    )
    result = parse(body)["result"]
    print("[GetAlerts result] isError:", result.get("isError", False))
    text = result["content"][0]["text"]
    print(text[:2000])
    print("... (cắt bớt)" if len(text) > 2000 else "")

    print(f"[tools/call] GetResources arguments={{'namespace': 'boutique'}}")
    _, body = post(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "GetResources",
                "arguments": {"namespace": "boutique"},
            },
        },
        session=session,
    )
    result = parse(body)["result"]
    print("[GetResources result] isError:", result.get("isError", False))
    text = result["content"][0]["text"]
    print(text[:2000])
    print("... (cắt bớt)" if len(text) > 2000 else "")

    print("SMOKE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
