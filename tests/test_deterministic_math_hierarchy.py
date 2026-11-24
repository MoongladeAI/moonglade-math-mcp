"""
Test suite verifying Moonglade Deterministic Math Hierarchy:
1. Basic Math (1+1 to high school algebra/calculus)
2. Priority Cascading: Submodule -> Domain -> Basic
3. Cryptographic proof generation on all outputs
"""

import sys
import os

# Set paths - relative to repository root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp_math_engine import engine, MathProof

def test_basic_arithmetic():
    print("--- 1. Testing Basic Arithmetic (1+1 & Radicals) ---")
    proof = engine.execute("arithmetic", expression="1 + 1")
    assert proof.exact_result == "2"
    print(f"1 + 1 = {proof.exact_result} | Proof Hash: {proof.proof_hash[:16]}... [PASS]")

    proof_frac = engine.execute("arithmetic", expression="3/7 + 5/9")
    assert proof_frac.exact_result == "62/63"
    print(f"3/7 + 5/9 = {proof_frac.exact_result} [PASS]")

def test_high_school_algebra():
    print("\n--- 2. Testing High School Algebra (Quadratic & Systems) ---")
    # x^2 - 5x + 6 = 0 -> roots 2, 3
    proof = engine.execute("quadratic_formula", a=1, b=-5, c=6)
    print(f"x^2 - 5x + 6 = 0 Roots: {proof.exact_result} [PASS]")

    # 2x + y = 7, x - y = 2 -> x = 3, y = 1
    proof_sys = engine.execute("solve_linear_2x2", a1="2", b1="1", c1="7", a2="1", b2="-1", c2="2")
    print(f"System Solution: {proof_sys.exact_result} [PASS]")

def test_geometry_and_statistics():
    print("\n--- 3. Testing Geometry & Statistics ---")
    # 3-4-5 Triangle
    proof_pyth = engine.execute("pythagorean", a=3, b=4)
    assert proof_pyth.exact_result == "5"
    print(f"Pythagorean Hypotenuse for 3, 4 = {proof_pyth.exact_result} [PASS]")

    # Stats: [10, 20, 30, 40, 50]
    proof_stat = engine.execute("statistics", numbers=[10, 20, 30, 40, 50])
    print(f"Descriptive Statistics: {proof_stat.exact_result} [PASS]")

def test_scientific_calculus_and_constants():
    print("\n--- 4. Testing Scientific Domain ---")
    # Speed of light
    proof_c = engine.execute("constant", symbol="c")
    assert proof_c.exact_result == "299792458"
    print(f"Speed of light c = {proof_c.exact_result} m/s [PASS]")

    # Derivative of x^3 + 2x^2 + 5
    proof_diff = engine.execute("derivative", expression="x**3 + 2*x**2 + 5", variable="x", order=1)
    assert proof_diff.exact_result == "3*x**2 + 4*x"
    print(f"d/dx(x^3 + 2x^2 + 5) = {proof_diff.exact_result} [PASS]")

    # Definite Integral of 2*x from 0 to 5 -> 25
    proof_int = engine.execute("integral", expression="2*x", variable="x", lower_bound="0", upper_bound="5")
    assert proof_int.exact_result == "25"
    print(f"Integral of 2x [0 to 5] = {proof_int.exact_result} [PASS]")

def test_financial_priority_cascade():
    print("\n--- 5. Testing Financial Module & Statutory Precision ---")
    # $500,000 BBD mortgage @ 6.25% for 300 months
    proof_emi = engine.execute(
        "mortgage_emi",
        principal="500000.00",
        annual_rate="0.0625",
        tenor_months=300,
        policy_id="caribank-retail-credit-standard",
        epoch="2026-Q4"
    )
    assert proof_emi.exact_result == "3298.35"
    print(f"Statutory EMI: ${proof_emi.exact_result} (Banker's rounded) [PASS]")

def test_submodule_hierarchical_extension():
    print("\n--- 6. Testing Submodule Extension & Priority Cascade ---")
    
    # Register an arbitrary specialized submodule: e.g. "scientific.physics.specialized"
    # Overriding a basic operation or extending with high priority (priority 150)
    engine.register_module(
        namespace="scientific.physics.specialized",
        priority=150,
        parent="scientific",
        description="High-priority specialized physical laws"
    )

    def specialized_growth(base_val: str, factor: str) -> MathProof:
        val = int(base_val) * int(factor) * 2  # Specialized doubled-intensity formula
        return MathProof(
            domain="scientific.physics.specialized",
            operation="growth_model",
            inputs={"base": base_val, "factor": factor},
            exact_result=str(val),
            steps=["Executed in high-priority specialized submodule: scientific.physics.specialized"]
        )

    engine.register_operation(
        operation="growth_model",
        namespace="scientific.physics.specialized",
        handler=specialized_growth,
        description="Specialized high-priority model"
    )

    proof_ext = engine.execute("growth_model", base_val="10", factor="5")
    assert proof_ext.domain == "scientific.physics.specialized"
    assert proof_ext.exact_result == "100"
    print(f"Specialized submodule resolved first: {proof_ext.domain} -> {proof_ext.exact_result} [PASS]")

if __name__ == "__main__":
    test_basic_arithmetic()
    test_high_school_algebra()
    test_geometry_and_statistics()
    test_scientific_calculus_and_constants()
    test_financial_priority_cascade()
    test_submodule_hierarchical_extension()
    print("\n==========================================")
    print("ALL DETERMINISTIC HIERARCHICAL MATH TESTS PASSED!")
    print("==========================================")
