"""Backward-compatible alias re-exporting plugins.banking_adjudication as mcp_financial_math."""
from plugins.banking_adjudication.epoch_policy import EpochPolicy, get_policy, register_epoch
from plugins.banking_adjudication.engine import BankingMathEngine, ComputationProof

__version__ = "1.0.0"
__all__ = ["EpochPolicy", "get_policy", "register_epoch", "BankingMathEngine", "ComputationProof"]
