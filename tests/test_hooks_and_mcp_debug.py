import json
import os
import shutil
import tempfile
from mcp_math_engine.hooks import install_hooks
from mcp_math_engine.server import handle_request


def test_hooks_and_mcp_debug():
    tmp = tempfile.mkdtemp(prefix="mg_math_hooks_")
    telem_path = os.path.join(tmp, "telemetry.jsonl")
    os.environ["MOONGLADE_MATH_TELEMETRY_PATH"] = telem_path
    try:
        rule_path = install_hooks(tmp)
        with open(rule_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "mg-math-mcp" in content
        print(f"\n[DEBUG] Installed hook rule at: {rule_path}")

        init_resp = handle_request({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        assert init_resp["result"]["protocolVersion"] == "2024-11-05"
        print("[DEBUG] initialize:", json.dumps(init_resp))

        req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "calculate", "arguments": {"operation": "arithmetic", "args": {"expression": "1 + 1"}}}
        }
        calc_resp1 = handle_request(req)
        payload1 = json.loads(calc_resp1["result"]["content"][0]["text"])
        calc_resp2 = handle_request(req)
        payload2 = json.loads(calc_resp2["result"]["content"][0]["text"])
        assert payload1["exact_result"] == "2"
        assert payload1["proof_hash"] == payload2["proof_hash"]

        with open(telem_path, "r", encoding="utf-8") as f:
            lines = [json.loads(l) for l in f if l.strip()]
        assert len(lines) == 2
        assert lines[0]["cache_hit"] is False
        assert lines[1]["cache_hit"] is True
        print("[DEBUG] telemetry:", json.dumps(lines))
    finally:
        os.environ.pop("MOONGLADE_MATH_TELEMETRY_PATH", None)
        shutil.rmtree(tmp, ignore_errors=True)
