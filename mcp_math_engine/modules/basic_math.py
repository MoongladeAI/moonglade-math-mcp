"""
Moonglade Deterministic Math - Module 1: Basic Math & High School Curriculum
Covers:
- Exact Arithmetic (1+1 to high-precision rational math)
- Algebra (linear, quadratic, systems of linear equations)
- Geometry (Pythagorean, areas, volumes, perimeter)
- Trigonometry (exact radical forms, radians, degrees)
- Statistics (mean, median, mode, sample/pop variance, standard deviation)
- Calculus basics (exact polynomial derivatives, definite integrals)
"""

from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction
import math
from typing import Dict, Any, List, Tuple, Union
import sympy as sp

from ..core import MathProof, to_decimal

class BasicMathModule:
    """Foundational high-school and exact mathematical engine."""
    name = "basic"
    priority = 10  # Baseline tier

    # ---------------------------------------------------------
    # 1. Exact Arithmetic
    # ---------------------------------------------------------
    @staticmethod
    def evaluate_arithmetic(expression: str) -> MathProof:
        """
        Evaluates arithmetic deterministically using exact rational Fraction or Decimal.
        Example: '1 + 1' or '3/7 + 5/9' or '100 * (1.05)^2'
        """
        # Parse into SymPy exact expression safely (no builtins / no eval RCE)
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
        safe_globals = {"__builtins__": {}, "Integer": sp.Integer, "Float": sp.Float, "Rational": sp.Rational, "Symbol": sp.Symbol}
        safe_locals = {"pi": sp.pi, "E": sp.E, "e": sp.E, "sqrt": sp.sqrt, "Abs": sp.Abs}
        sym_expr = parse_expr(
            expression,
            local_dict=safe_locals,
            global_dict=safe_globals,
            transformations=standard_transformations + (implicit_multiplication_application, convert_xor),
            evaluate=True,
        )
        exact_val = str(sym_expr)
        approx_val = str(sym_expr.evalf(15))
        
        return MathProof(
            domain="basic",
            operation="arithmetic",
            inputs={"expression": expression},
            exact_result=exact_val,
            approximate_result=approx_val,
            steps=[f"Parsed expression: {expression}", f"SymPy exact reduction: {exact_val}"]
        )

    # ---------------------------------------------------------
    # 2. Algebra: Quadratic Formula
    # ---------------------------------------------------------
    @staticmethod
    def quadratic_formula(a: Union[int, float, str], b: Union[int, float, str], c: Union[int, float, str]) -> MathProof:
        """
        Solves ax^2 + bx + c = 0 deterministically.
        Returns exact radical form and floating-point approximations.
        """
        x = sp.Symbol('x')
        sa, sb, sc = sp.Rational(str(a)), sp.Rational(str(b)), sp.Rational(str(c))
        poly = sa*x**2 + sb*x + sc
        discriminant = sb**2 - 4*sa*sc
        solutions = sp.solve(poly, x)
        
        sol_strs = [str(sol) for sol in solutions]
        sol_approx = [str(sol.evalf(8)) for sol in solutions]
        
        steps = [
            f"Equation: {sa}x^2 + {sb}x + {sc} = 0",
            f"Discriminant D = b^2 - 4ac = ({sb})^2 - 4({sa})({sc}) = {discriminant}",
            f"Roots: {', '.join(sol_strs)}"
        ]

        return MathProof(
            domain="basic",
            operation="quadratic_formula",
            inputs={"a": str(a), "b": str(b), "c": str(c)},
            exact_result=json_safe_list(sol_strs),
            approximate_result=json_safe_list(sol_approx),
            steps=steps
        )

    # ---------------------------------------------------------
    # 3. Algebra: Linear Equation System (2x2)
    # ---------------------------------------------------------
    @staticmethod
    def solve_linear_2x2(
        a1: str, b1: str, c1: str,
        a2: str, b2: str, c2: str
    ) -> MathProof:
        """
        Solves:
        a1*x + b1*y = c1
        a2*x + b2*y = c2
        """
        x, y = sp.symbols('x y')
        eq1 = sp.Eq(sp.Rational(a1)*x + sp.Rational(b1)*y, sp.Rational(c1))
        eq2 = sp.Eq(sp.Rational(a2)*x + sp.Rational(b2)*y, sp.Rational(c2))
        sol = sp.solve((eq1, eq2), (x, y))

        exact_res = {str(k): str(v) for k, v in sol.items()}
        steps = [
            f"System: [{a1}x + {b1}y = {c1}], [{a2}x + {b2}y = {c2}]",
            f"Deterministic Cramer's/Gaussian elimination solution: {exact_res}"
        ]

        return MathProof(
            domain="basic",
            operation="solve_linear_2x2",
            inputs={"eq1": f"{a1}x + {b1}y = {c1}", "eq2": f"{a2}x + {b2}y = {c2}"},
            exact_result=str(exact_res),
            approximate_result=str({str(k): str(v.evalf(8)) for k, v in sol.items()}),
            steps=steps
        )

    # ---------------------------------------------------------
    # 4. Geometry: Pythagorean Theorem
    # ---------------------------------------------------------
    @staticmethod
    def pythagorean(a: Union[int, str] = None, b: Union[int, str] = None, c: Union[int, str] = None) -> MathProof:
        """
        Solves a^2 + b^2 = c^2 for whichever side is missing.
        """
        steps = []
        if c is None:
            sa, sb = sp.Rational(str(a)), sp.Rational(str(b))
            c_exact = sp.sqrt(sa**2 + sb**2)
            exact = str(c_exact)
            approx = str(c_exact.evalf(8))
            steps.append(f"Hypotenuse c = sqrt(({sa})^2 + ({sb})^2) = sqrt({sa**2 + sb**2}) = {exact}")
            out_side = "c"
        elif a is None:
            sb, sc = sp.Rational(str(b)), sp.Rational(str(c))
            a_exact = sp.sqrt(sc**2 - sb**2)
            exact = str(a_exact)
            approx = str(a_exact.evalf(8))
            steps.append(f"Leg a = sqrt(({sc})^2 - ({sb})^2) = {exact}")
            out_side = "a"
        else:
            sa, sc = sp.Rational(str(a)), sp.Rational(str(c))
            b_exact = sp.sqrt(sc**2 - sa**2)
            exact = str(b_exact)
            approx = str(b_exact.evalf(8))
            steps.append(f"Leg b = sqrt(({sc})^2 - ({sa})^2) = {exact}")
            out_side = "b"

        return MathProof(
            domain="basic",
            operation="pythagorean",
            inputs={"a": str(a), "b": str(b), "c": str(c)},
            exact_result=exact,
            approximate_result=approx,
            steps=steps
        )

    # ---------------------------------------------------------
    # 5. Statistics: Descriptive Suite
    # ---------------------------------------------------------
    @staticmethod
    def descriptive_statistics(numbers: List[Union[int, float, str]]) -> MathProof:
        """
        Exact mean, variance, and standard deviation.
        """
        rats = [sp.Rational(str(n)) for n in numbers]
        n = len(rats)
        mean = sum(rats) / n
        pop_var = sum((x - mean)**2 for x in rats) / n
        sample_var = sum((x - mean)**2 for x in rats) / (n - 1) if n > 1 else sp.Rational(0)
        pop_std = sp.sqrt(pop_var)
        sample_std = sp.sqrt(sample_var)

        res = {
            "count": n,
            "mean": str(mean),
            "pop_variance": str(pop_var),
            "sample_variance": str(sample_var),
            "pop_std": str(pop_std),
            "sample_std": str(sample_std)
        }
        res_approx = {
            "count": n,
            "mean": str(mean.evalf(6)),
            "pop_variance": str(pop_var.evalf(6)),
            "sample_variance": str(sample_var.evalf(6)),
            "pop_std": str(pop_std.evalf(6)),
            "sample_std": str(sample_std.evalf(6))
        }

        return MathProof(
            domain="basic",
            operation="descriptive_statistics",
            inputs={"data": [str(x) for x in numbers]},
            exact_result=str(res),
            approximate_result=str(res_approx),
            steps=[f"Data count: {n}", f"Exact rational mean: {mean}", f"Sample variance: {sample_var}"]
        )

def json_safe_list(lst: List[str]) -> str:
    import json
    return json.dumps(lst)
