"""
Moonglade Deterministic Math - Module 2: Scientific & Advanced Math
Overrides / extends basic math with:
- Exact Scientific Constants (speed of light, Planck, gravitational, Avogadro, Boltzmann)
- Differential & Integral Calculus (arbitrary order symbolic derivatives, definite/indefinite integration)
- Linear Algebra (matrix determinant, eigenvalues, matrix multiplication, inversion)
- Vector Calculus (dot product, cross product, magnitude)
- Complex Analysis (Euler's identity, polar decomposition)
"""

from typing import Dict, Any, List, Union
import sympy as sp

from ..core import MathProof

# Exact CODATA 2018 / 2022 Physical Constants (SI)
SCIENTIFIC_CONSTANTS = {
    "c": {"symbol": "c", "value": "299792458", "unit": "m/s", "desc": "Speed of light in vacuum"},
    "h": {"symbol": "h", "value": "6.62607015e-34", "unit": "J*s", "desc": "Planck constant"},
    "hbar": {"symbol": "hbar", "value": "1.054571817e-34", "unit": "J*s", "desc": "Reduced Planck constant"},
    "e": {"symbol": "e", "value": "1.602176634e-19", "unit": "C", "desc": "Elementary charge"},
    "k_B": {"symbol": "k_B", "value": "1.380649e-23", "unit": "J/K", "desc": "Boltzmann constant"},
    "N_A": {"symbol": "N_A", "value": "6.02214076e23", "unit": "1/mol", "desc": "Avogadro constant"},
    "G": {"symbol": "G", "value": "6.67430e-11", "unit": "m^3/(kg*s^2)", "desc": "Newtonian constant of gravitation"},
    "g_0": {"symbol": "g_0", "value": "9.80665", "unit": "m/s^2", "desc": "Standard gravity acceleration"}
}

class ScientificMathModule:
    """Scientific computation module (priority 50)."""
    name = "scientific"
    priority = 50

    @staticmethod
    def get_constant(symbol: str) -> MathProof:
        """Retrieves exact statutory SI constant."""
        if symbol not in SCIENTIFIC_CONSTANTS:
            raise ValueError(f"Unknown constant: {symbol}. Available: {list(SCIENTIFIC_CONSTANTS.keys())}")
        const_info = SCIENTIFIC_CONSTANTS[symbol]
        return MathProof(
            domain="scientific",
            operation="constant_lookup",
            inputs={"symbol": symbol},
            exact_result=const_info["value"],
            approximate_result=const_info["value"],
            steps=[f"SI standard constant definition: {const_info['desc']} ({const_info['unit']})"]
        )

    @staticmethod
    def _safe_parse(expression: str, variable: str = "x"):
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
        var = sp.Symbol(variable)
        safe_locals = {
            variable: var,
            "pi": sp.pi, "E": sp.E, "e": sp.E, "oo": sp.oo,
            "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
            "exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt, "Abs": sp.Abs,
        }
        safe_globals = {"__builtins__": {}, "Integer": sp.Integer, "Float": sp.Float, "Rational": sp.Rational, "Symbol": sp.Symbol}
        return parse_expr(
            expression,
            local_dict=safe_locals,
            global_dict=safe_globals,
            transformations=standard_transformations + (implicit_multiplication_application, convert_xor),
            evaluate=True,
        )

    @classmethod
    def symbolic_derivative(cls, expression: str, variable: str = "x", order: int = 1) -> MathProof:
        """Computes exact nth-order symbolic derivative."""
        var = sp.Symbol(variable)
        expr = cls._safe_parse(expression, variable)
        deriv = sp.diff(expr, var, order)
        
        return MathProof(
            domain="scientific",
            operation="symbolic_derivative",
            inputs={"expression": expression, "variable": variable, "order": order},
            exact_result=str(deriv),
            steps=[
                f"Function f({variable}) = {expr}",
                f"Order {order} derivative d^{order}f/d{variable}^{order} = {deriv}"
            ]
        )

    @classmethod
    def symbolic_integral(
        cls,
        expression: str,
        variable: str = "x",
        lower_bound: Union[str, None] = None,
        upper_bound: Union[str, None] = None
    ) -> MathProof:
        """Computes exact definite or indefinite integral."""
        var = sp.Symbol(variable)
        expr = cls._safe_parse(expression, variable)
        
        if lower_bound is not None and upper_bound is not None:
            a = cls._safe_parse(lower_bound, variable)
            b = cls._safe_parse(upper_bound, variable)
            integral_val = sp.integrate(expr, (var, a, b))
            exact_res = str(integral_val)
            approx_res = str(integral_val.evalf(8))
            step = f"Definite integral of {expr} from {a} to {b} = {exact_res}"
        else:
            integral_val = sp.integrate(expr, var)
            exact_res = f"{integral_val} + C"
            approx_res = None
            step = f"Indefinite integral of {expr} with respect to {var} = {exact_res}"

        return MathProof(
            domain="scientific",
            operation="symbolic_integral",
            inputs={"expression": expression, "variable": variable, "lower": lower_bound, "upper": upper_bound},
            exact_result=exact_res,
            approximate_result=approx_res,
            steps=[step]
        )

    @staticmethod
    def matrix_operations(matrix_a: List[List[Union[int, float, str]]], operation: str = "determinant") -> MathProof:
        """
        Matrix operations: 'determinant', 'inverse', 'eigenvalues'.
        """
        M = sp.Matrix(matrix_a)
        steps = [f"Matrix dimensions: {M.shape}"]

        if operation == "determinant":
            det = M.det()
            exact = str(det)
            approx = str(det.evalf(8))
            steps.append(f"Exact determinant: {exact}")
        elif operation == "inverse":
            inv = M.inv()
            exact = str(inv.tolist())
            approx = str([[str(val.evalf(6)) for val in row] for row in inv.tolist()])
            steps.append(f"Matrix inverse calculated.")
        elif operation == "eigenvalues":
            eigs = M.eigenvals()
            exact = str({str(k): v for k, v in eigs.items()})
            approx = str({str(k.evalf(6)): v for k, v in eigs.items()})
            steps.append(f"Eigenvalues with multiplicities: {exact}")
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        return MathProof(
            domain="scientific",
            operation=f"matrix_{operation}",
            inputs={"matrix": matrix_a, "operation": operation},
            exact_result=exact,
            approximate_result=approx,
            steps=steps
        )
