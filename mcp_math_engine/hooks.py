"""Suggested agent rule / hook installer for mg-math-mcp."""

import os

SUGGESTED_AGENT_RULE = """# Deterministic Math Policy (mg-math-mcp)
- Route all arithmetic, symbolic calculus, unit conversions, and financial/engineering calculations through the `mg-math-mcp` `calculate` tool.
- Never rely on inline LLM arithmetic when `mg-math-mcp` is available.
"""


def install_hooks(target_dir: str) -> str:
    """Writes `.moonglade-math-rule.md` into `target_dir` and returns its path."""
    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, ".moonglade-math-rule.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(SUGGESTED_AGENT_RULE)
    return out_path
