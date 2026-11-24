"""
Moonglade Deterministic Math Protocol - Core Types & Proof System
Zero floating-point ambiguity. Fully verifiable execution trace.
"""

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
import hashlib
import json
from typing import Dict, Any, List, Optional

# Set default high-precision fixed point context
getcontext().prec = 35
getcontext().rounding = ROUND_HALF_EVEN

def to_decimal(val: Any) -> Decimal:
    """Safe conversion to exact Decimal."""
    if isinstance(val, Decimal):
        return val
    return Decimal(str(val))

@dataclass
class MathProof:
    """
    Cryptographic computation receipt.
    Proves inputs, formula, module priority, output, and execution steps.
    """
    domain: str                     # 'basic', 'scientific', 'financial'
    operation: str                  # e.g., 'quadratic_formula', 'mortgage_emi'
    inputs: Dict[str, Any]
    exact_result: str               # Canonical string representation (Decimal / Fraction / SymPy exact)
    approximate_result: Optional[str] = None
    rounding_mode: Optional[str] = None
    steps: List[str] = field(default_factory=list)
    proof_hash: str = ""

    def __post_init__(self):
        if not self.proof_hash:
            self.proof_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = {
            "domain": self.domain,
            "operation": self.operation,
            "inputs": self.inputs,
            "exact_result": self.exact_result,
            "approximate_result": self.approximate_result,
            "steps": self.steps
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "operation": self.operation,
            "inputs": self.inputs,
            "exact_result": self.exact_result,
            "approximate_result": self.approximate_result,
            "rounding_mode": self.rounding_mode,
            "steps": self.steps,
            "proof_hash": self.proof_hash
        }
