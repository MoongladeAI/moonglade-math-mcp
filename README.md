# Moonglade Deterministic Math MCP (`moonglade-math-mcp`)

Zero-hallucination symbolic and fixed-point mathematical execution engine exposed via the **Model Context Protocol (MCP)**. Every calculation traverses a deterministic priority hierarchy (`Plugin Submodule → Domain → Basic Math`) and emits a cryptographic `MathProof` receipt containing the exact result, step-by-step execution trace, rounding mode (`ROUND_HALF_EVEN`), and SHA-256 verification digest.

## Repository Architecture

```text
moonglade-math-mcp/
├── pyproject.toml
├── README.md
├── mcp_math_engine/          # Core Hierarchical Engine & MCP JSON-RPC Server
│   ├── core.py               # MathProof receipt & 35-digit Decimal context
│   ├── registry.py           # Priority-cascading namespace dispatcher
│   ├── server.py             # Stdio MCP server (calculate & list_math_hierarchy)
│   └── modules/              # Built-in foundational tiers
│       ├── basic_math.py     # Rational arithmetic, algebra, geometry, statistics
│       ├── scientific_math.py# Symbolic calculus (SymPy), matrices, SI constants
│       └── financial_math.py # Fixed-point TVM, compound interest, base EMI
├── plugins/                  # Auto-discovered Domain Extension Plugins
│   ├── __init__.py           # Dynamic plugin loader (discover_and_register_plugins)
│   ├── banking_adjudication/ # Epoch-governed retail mortgage & covenant underwriting
│   ├── building_energy/      # Municipal energy consumption & BIM budget rates
│   ├── energy_grid/          # Grid load, storage & renewable dispatch
│   ├── municipal_spatial/    # Spatial density & parcel calculations
│   └── transit_mobility/     # Fleet headway, capacity & mobility metrics
└── tests/                    # Automated Verification Suite
```

## Creating a Domain Extension Plugin

Drop a new folder inside `plugins/<your_plugin>/` with a `pack.py` (or `plugin.py`) defining `register_pack(registry: MathRegistry)`:

```python
from mcp_math_engine.core import MathProof, to_decimal
from mcp_math_engine.registry import MathRegistry

def register_pack(registry: MathRegistry):
    registry.register_module("custom.domain", priority=100, parent="basic", description="Custom domain formulas")
    registry.register_operation("my_formula", "custom.domain", my_handler)
```

All plugins in `plugins/` are automatically discovered and registered on engine startup.
