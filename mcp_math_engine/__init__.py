"""
Moonglade Deterministic Math Engine - Bootstrapper & Public API
Wires standard hierarchy:
- Base Tier: 'basic' (Priority 10)
- Domain Tier: 'scientific' (Priority 50), 'financial' (Priority 80)
- Extension Hooks: Arbitrary nested submodules (Priority 100+) cascade backwards.
"""

from .registry import MathRegistry, engine
from .core import MathProof
from .modules.basic_math import BasicMathModule
from .modules.scientific_math import ScientificMathModule
from .modules.financial_math import FinancialMathModule

def initialize_default_engine() -> MathRegistry:
    """Bootstraps default hierarchy and registers foundational operations."""
    
    # 1. Register Modules in Hierarchy
    engine.register_module(
        namespace="basic",
        priority=10,
        parent=None,
        description="Standard high school curriculum, arithmetic, algebra, geometry, statistics"
    )
    engine.register_module(
        namespace="scientific",
        priority=50,
        parent="basic",
        description="Advanced calculus, linear algebra, statutory physical constants"
    )
    engine.register_module(
        namespace="financial",
        priority=80,
        parent="basic",
        description="Statutory banking covenants, fixed-point rounding, compounding"
    )

    # 2. Register Basic Operations
    engine.register_operation(
        operation="arithmetic",
        namespace="basic",
        handler=BasicMathModule.evaluate_arithmetic,
        description="Exact arithmetic reduction using rational fractions and high-precision fixed point"
    )
    engine.register_operation(
        operation="quadratic_formula",
        namespace="basic",
        handler=BasicMathModule.quadratic_formula,
        description="Solves ax^2 + bx + c = 0 in exact radical form"
    )
    engine.register_operation(
        operation="solve_linear_2x2",
        namespace="basic",
        handler=BasicMathModule.solve_linear_2x2,
        description="Exact 2x2 linear system solver"
    )
    engine.register_operation(
        operation="pythagorean",
        namespace="basic",
        handler=BasicMathModule.pythagorean,
        description="Pythagorean theorem for missing triangle side"
    )
    engine.register_operation(
        operation="statistics",
        namespace="basic",
        handler=BasicMathModule.descriptive_statistics,
        description="Mean, variance, and standard deviation"
    )

    # 3. Register Scientific Operations
    engine.register_operation(
        operation="constant",
        namespace="scientific",
        handler=ScientificMathModule.get_constant,
        description="Statutory SI/CODATA physical constants"
    )
    engine.register_operation(
        operation="derivative",
        namespace="scientific",
        handler=ScientificMathModule.symbolic_derivative,
        description="Symbolic nth-order derivative"
    )
    engine.register_operation(
        operation="integral",
        namespace="scientific",
        handler=ScientificMathModule.symbolic_integral,
        description="Definite or indefinite symbolic integral"
    )
    engine.register_operation(
        operation="matrix",
        namespace="scientific",
        handler=ScientificMathModule.matrix_operations,
        description="Matrix operations (determinant, inverse, eigenvalues)"
    )

    # 4. Register Financial Operations
    engine.register_operation(
        operation="mortgage_emi",
        namespace="financial",
        handler=FinancialMathModule.calculate_mortgage_emi,
        description="Exact fixed-point statutory mortgage EMI"
    )
    engine.register_operation(
        operation="compound_interest",
        namespace="financial",
        handler=FinancialMathModule.compound_interest,
        description="Fixed-point compound interest with Banker's rounding"
    )

    # 5. Auto-discover and register domain plugins from plugins/
    try:
        from plugins import discover_and_register_plugins
        discover_and_register_plugins(engine)
    except ImportError:
        pass

    return engine

# Auto-initialize global instance
initialize_default_engine()

__all__ = ["engine", "MathRegistry", "MathProof", "initialize_default_engine"]
