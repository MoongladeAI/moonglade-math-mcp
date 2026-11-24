"""
Moonglade Deterministic Math MCP Server
Standard Model Context Protocol JSON-RPC / stdio server.
Exposes the hierarchical math registry to any AI agent, IDE, or bank client.
"""

import sys
import json
import os
import time
import hashlib
import datetime
from typing import Dict, Any

_RESULT_CACHE: Dict[str, Dict[str, Any]] = {}


def _cache_key(op: str, args: Dict[str, Any]) -> str:
    canonical = json.dumps({"operation": op, "args": args}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _log_telemetry(entry: Dict[str, Any]) -> None:
    path = os.environ.get(
        "MOONGLADE_MATH_TELEMETRY_PATH",
        os.path.join(os.path.expanduser("~"), ".moonglade", "math_mcp_telemetry.jsonl"),
    )
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

# Ensure package is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp_math_engine import engine, MathProof

def handle_request(req: dict) -> dict:
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "mg-math-mcp",
                    "version": "1.0.0"
                }
            }
        }

    elif method == "notifications/initialized":
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate",
                        "description": "Execute deterministic calculation through hierarchical registry (submodule -> domain -> basic)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "operation": {
                                    "type": "string",
                                    "description": "Operation name (e.g. arithmetic, quadratic_formula, mortgage_emi, derivative, integral, constant)"
                                },
                                "args": {
                                    "type": "object",
                                    "description": "Keyword arguments specific to the operation"
                                }
                            },
                            "required": ["operation"]
                        }
                    },
                    {
                        "name": "list_hierarchy",
                        "description": "List all registered mathematical namespaces, operations, and priority dispatch tree",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "calculate":
            op = arguments.get("operation")
            args = arguments.get("args", {})
            t0 = time.perf_counter()
            try:
                key = _cache_key(op, args)
                if key in _RESULT_CACHE:
                    payload = _RESULT_CACHE[key]
                    cache_hit = True
                else:
                    proof = engine.execute(op, **args)
                    payload = proof.to_dict()
                    _RESULT_CACHE[key] = payload
                    cache_hit = False
                _log_telemetry({
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "operation": op,
                    "domain": payload.get("domain"),
                    "duration_ms": round((time.perf_counter() - t0) * 1000, 3),
                    "cache_hit": cache_hit,
                    "is_error": False,
                    "proof_hash": payload.get("proof_hash"),
                })
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(payload, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                _log_telemetry({
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "operation": op,
                    "domain": None,
                    "duration_ms": round((time.perf_counter() - t0) * 1000, 3),
                    "cache_hit": False,
                    "is_error": True,
                    "error": str(e),
                })
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32000,
                        "message": str(e)
                    }
                }

        elif tool_name == "list_hierarchy":
            hierarchy = engine.list_hierarchy()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(hierarchy, indent=2)
                        }
                    ]
                }
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {tool_name}"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"}
    }

def main():
    """Stdio JSON-RPC loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
