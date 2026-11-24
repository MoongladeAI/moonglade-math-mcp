"""
Moonglade Deterministic Math - Module 3: Financial Math Adapter
Bridges the existing production `mcp_financial_math` engine into the
hierarchical cascading dispatch registry.

Specializations:
- Banker's Rounding (ROUND_HALF_EVEN, 2 decimal places for currency, 4 for ratios)
- Statutory banking covenants (GDSR, TDSR, LTV, Stress Test)
- Fixed-point 28-digit precision
- Cascades from / overrides basic arithmetic with statutory financial formulas.
"""

from decimal import Decimal, ROUND_HALF_EVEN
from typing import Dict, Any, List
import sys
import os

from ..core import MathProof, to_decimal

# Import existing production engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from mcp_financial_math.engine import BankingMathEngine as LegacyFinancialEngine
from mcp_financial_math.epoch_policy import get_policy

class FinancialMathModule:
    """Financial computation module (priority 80)."""
    name = "financial"
    priority = 80

    @staticmethod
    def calculate_mortgage_emi(
        principal: str,
        annual_rate: str,
        tenor_months: int,
        policy_id: str = "caribank-retail-credit-standard",
        epoch: str = "2026-Q4"
    ) -> MathProof:
        """
        Exact mortgage monthly installment (EMI) using 28-digit fixed-point math
        and statutory Banker's rounding.
        """
        engine_inst = LegacyFinancialEngine(policy_id=policy_id, epoch=epoch)
        p = _d(principal)
        r = _d(annual_rate)
        emi = engine_inst.calculate_equated_monthly_installment(p, r, tenor_months)
        total_payment = emi * _d(tenor_months)
        total_interest = total_payment - p

        return MathProof(
            domain="financial",
            operation="mortgage_emi",
            inputs={"principal": principal, "annual_rate": annual_rate, "tenor_months": tenor_months, "policy_id": policy_id, "epoch": epoch},
            exact_result=str(emi),
            approximate_result=str(emi),
            rounding_mode="ROUND_HALF_EVEN (0.01)",
            steps=[
                f"Statutory policy applied: {engine_inst.policy.jurisdiction} {engine_inst.policy.epoch}",
                f"Formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)",
                f"Computed exact EMI: {emi}",
                f"Total repayment: {total_payment}",
                f"Total interest: {total_interest}"
            ]
        )

    @staticmethod
    def compound_interest(
        principal: str,
        annual_rate: str,
        compounds_per_year: int,
        years: str
    ) -> MathProof:
        """
        Exact compound interest A = P(1 + r/n)^(nt) with Banker's rounding.
        """
        p = to_decimal(principal)
        r = to_decimal(annual_rate)
        n = Decimal(str(compounds_per_year))
        t = to_decimal(years)

        rate_per_period = r / n
        periods = n * t
        factor = (Decimal(1) + rate_per_period) ** periods
        amount = (p * factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        interest = amount - p

        return MathProof(
            domain="financial",
            operation="compound_interest",
            inputs={"principal": principal, "annual_rate": annual_rate, "compounds_per_year": compounds_per_year, "years": years},
            exact_result=str(amount),
            approximate_result=str(amount),
            rounding_mode="ROUND_HALF_EVEN (0.01)",
            steps=[
                f"Formula: A = P * (1 + r/n)^(n*t)",
                f"Total compounded amount: {amount}",
                f"Interest earned: {interest}"
            ]
        )

def _d(v: Any) -> Decimal:
    return Decimal(str(v))
