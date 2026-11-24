"""
Moonglade Hierarchical Deterministic Math Engine
Resolves calculations by traversing a tree of nested modules:
Most Specialized First (Highest Priority / Leaf Submodule) -> Domain -> Basic Math.

Key Concepts:
- Pure Functional Registry: Modules and submodules register their formulas/operations.
- Hierarchical Namespaces: e.g. "scientific.physics.acoustics" or "financial.mortgage.barbados"
- Priority Invariants: Specialized child formulas take precedence over parent generalizations.
- Fallback Cascade: If a specialized formula doesn't handle an operation, it cascades down to parent.
- Proof Receipts: Every calculation yields a cryptographic MathProof with execution trace.
"""

from typing import Dict, Any, List, Optional, Callable
import importlib
from .core import MathProof

class MathRegistry:
    """
    Hierarchical registry and cascading dispatcher.
    Orders modules from most specialized (deepest / highest priority) to basic.
    """
    def __init__(self):
        # Maps namespace (e.g. "basic", "scientific", "financial") to module metadata
        self._modules: Dict[str, Dict[str, Any]] = {}
        # Maps operation_name -> list of candidate handlers sorted by priority desc
        self._operations: Dict[str, List[Dict[str, Any]]] = {}

    def register_module(
        self,
        namespace: str,
        priority: int,
        parent: Optional[str] = None,
        description: str = ""
    ):
        """Registers a module or submodule in the hierarchy."""
        self._modules[namespace] = {
            "namespace": namespace,
            "priority": priority,
            "parent": parent,
            "description": description
        }

    def register_operation(
        self,
        operation: str,
        namespace: str,
        handler: Callable[..., MathProof],
        priority_override: Optional[int] = None,
        description: str = ""
    ):
        """
        Registers an operation within a namespace.
        Higher priority handlers shadow/override broader ones.
        """
        mod_info = self._modules.get(namespace, {"priority": 0})
        effective_priority = priority_override if priority_override is not None else mod_info.get("priority", 0)

        entry = {
            "operation": operation,
            "namespace": namespace,
            "handler": handler,
            "priority": effective_priority,
            "description": description
        }

        if operation not in self._operations:
            self._operations[operation] = []

        self._operations[operation].append(entry)
        # Keep sorted by priority descending: most specialized first!
        self._operations[operation].sort(key=lambda x: x["priority"], reverse=True)

    def execute(self, operation: str, **kwargs) -> MathProof:
        """
        Executes an operation using the highest priority available implementation,
        cascading down if specific constraints aren't met.
        """
        if operation not in self._operations or not self._operations[operation]:
            raise ValueError(
                f"Unknown operation: '{operation}'. "
                f"Available operations: {list(self._operations.keys())}"
            )

        candidates = self._operations[operation]
        last_error = None

        # Cascade down from most specialized to general
        for candidate in candidates:
            try:
                proof = candidate["handler"](**kwargs)
                # Annotate proof with resolution hierarchy metadata
                proof.domain = candidate["namespace"]
                return proof
            except TypeError as te:
                # Signature mismatch or missing specialized parameters -> cascade down
                last_error = te
                continue
            except Exception as e:
                # If explicit failure, cascade or raise based on logic
                last_error = e
                continue

        raise RuntimeError(
            f"Failed to execute operation '{operation}' across registered hierarchy. "
            f"Tried namespaces: {[c['namespace'] for c in candidates]}. Last error: {last_error}"
        )

    def list_hierarchy(self) -> List[Dict[str, Any]]:
        """Returns the registered hierarchy tree and operation dispatch table."""
        return [
            {
                "operation": op,
                "handlers": [
                    {
                        "namespace": h["namespace"],
                        "priority": h["priority"],
                        "description": h["description"]
                    }
                    for h in handlers
                ]
            }
            for op, handlers in self._operations.items()
        ]

# Global Singleton Engine Instance
engine = MathRegistry()
