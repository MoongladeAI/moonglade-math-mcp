# Changelog

## 1.0.1 (2026-11-24)
- Replaced raw `sp.sympify()` with restricted `parse_expr()` in `basic_math.py` and `scientific_math.py` (no builtins / no `eval` RCE).
- Added strict input validation in `plugins/banking_adjudication/engine.py` rejecting non-positive loan, property value, tenor, or income inputs and negative rates/taxes/debts.
- Added root `MIT` `LICENSE`.
- Verified `9/9` pytest suite passing.
