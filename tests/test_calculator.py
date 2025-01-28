import pytest
from scicalc.calculator import Calculator
import math

def test_basic_arithmetic():
    calc = Calculator()
    assert calc.evaluate("2+2") == 4
    assert calc.evaluate("3*4") == 12
    assert calc.evaluate("10/2") == 5
    assert calc.evaluate("5-3") == 2

def test_auto_complete_brackets():
    calc = Calculator()
    result = calc.evaluate("sin(30")
    assert result == pytest.approx(0.5, rel=1e-2)
    
def test_implicit_multiplication():
    calc = Calculator()
    assert calc.evaluate("2(3)") == 6
    assert calc.evaluate("2x3") == 6
    assert calc.evaluate("2(3+4)") == 14

def test_memory_operations():
    calc = Calculator()
    calc.evaluate("5")
    calc.memory_store()  # M+
    assert calc.memory_recall() == 5  # MR
    calc.evaluate("3")
    calc.memory_add()    # M+
    assert calc.memory_recall() == 8
    calc.memory_subtract()  # M-
    assert calc.memory_recall() == 5

def test_scientific_functions():
    calc = Calculator()
    # Using degrees for trig functions
    assert calc.evaluate("sin(90)") == pytest.approx(1.0, rel=1e-2)  # sin 90°
    assert calc.evaluate("cos(0)") == pytest.approx(1.0, rel=1e-2)   # cos 0°
    assert calc.evaluate("tan(45)") == pytest.approx(1.0, rel=1e-2)  # tan 45°
    assert calc.evaluate("sqrt(16)") == 4

def test_advanced_scientific_functions():
    calc = Calculator()
    # Inverse trig functions (results in degrees)
    assert calc.evaluate("sin⁻¹(0.5)") == pytest.approx(30.0, rel=1e-5)  # arcsin 0.5 = 30°
    assert calc.evaluate("cos⁻¹(0)") == pytest.approx(90.0, rel=1e-5)    # arccos 0 = 90°
    
    # Hyperbolic functions
    assert calc.evaluate("sinh(1)") == pytest.approx(1.1752, rel=1e-4)
    assert calc.evaluate("cosh(0)") == pytest.approx(1.0, rel=1e-4)
    
    # Powers and special numbers
    assert calc.evaluate("2²") == 4
    assert calc.evaluate("2³") == 8
    assert calc.evaluate("∛27") == 3
    assert calc.evaluate("√16") == 4
    
    # Logarithms
    assert calc.evaluate("log(100)") == 2
    assert calc.evaluate("ln(e)") == pytest.approx(1.0, rel=1e-4)
    assert calc.evaluate("log₂(8)") == 3

def test_special_operations():
    calc = Calculator()
    # Factorial
    assert calc.evaluate("5!") == 120
    
    # Percentage
    assert calc.evaluate("50%") == 0.5
    assert calc.evaluate("200+10%") == 220
    
    # Scientific notation
    assert calc.evaluate("2EE3") == 2000
    
    # Degree/Radian conversion
    assert calc.evaluate("rad(180)") == pytest.approx(math.pi, rel=1e-4)
    assert calc.evaluate("deg(pi)") == pytest.approx(180.0, rel=1e-4)

def test_implicit_multiplication_advanced():
    calc = Calculator()
    assert calc.evaluate("2π") == pytest.approx(2 * math.pi, rel=1e-4)
    assert calc.evaluate("2e") == pytest.approx(2 * math.e, rel=1e-4)
    assert calc.evaluate("(2)(3)") == 6

def test_error_handling():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.evaluate("invalid")
    with pytest.raises(ValueError):
        calc.evaluate("1/0")
    with pytest.raises(ValueError):
        calc.evaluate("sin()")

def test_complex_expressions():
    calc = Calculator()
    assert calc.evaluate("2+3*4") == 14
    assert calc.evaluate("(2+3)*4") == 20
    assert calc.evaluate("2^3") == 8
    assert calc.evaluate("sin(45)+cos(45)") == pytest.approx(1.414, rel=1e-3)

def test_memory_chain():
    calc = Calculator()
    calc.evaluate("5")
    calc.memory_store()
    calc.evaluate("3")
    calc.memory_add()
    calc.evaluate("2")
    calc.memory_subtract()
    assert calc.memory_recall() == 6

def test_percentage_variations():
    calc = Calculator()
    assert calc.evaluate("50%") == 0.5
    assert calc.evaluate("200+10%") == 220
    assert calc.evaluate("200-10%") == 180
    assert calc.evaluate("50% + 50%") == 1.0

def test_scientific_notation():
    calc = Calculator()
    assert calc.evaluate("2EE3") == 2000
    assert calc.evaluate("1.5EE2") == 150

def test_mixed_functions():
    calc = Calculator()
    assert calc.evaluate("sin(45)^2 + cos(45)^2") == pytest.approx(1.0, rel=1e-10)
    assert calc.evaluate("log(sqrt(100))") == 1
    assert calc.evaluate("2π") == pytest.approx(2 * math.pi, rel=1e-10) 