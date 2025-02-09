import pytest
from scicalc.calculator import Calculator
import math
import unittest

class TestCalculator(unittest.TestCase):
    def test_basic_arithmetic(self):
        calc = Calculator()
        assert calc.evaluate("2+2") == 4
        assert calc.evaluate("3*4") == 12
        assert calc.evaluate("10/2") == 5
        assert calc.evaluate("5-3") == 2

    def test_auto_complete_brackets(self):
        calc = Calculator()
        # Test with missing closing bracket
        result = calc.evaluate("sin(30")
        assert result == pytest.approx(0.5, abs=1e-2)  # sin(30°) = 0.5
        
        # Test nested brackets
        result = calc.evaluate("sin(cos(30")
        # Calculator uses degrees for both sin and cos
        expected = math.sin(math.radians(math.cos(math.radians(30))))
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        assert result == pytest.approx(expected, rel=1e-2)
        
    def test_implicit_multiplication(self):
        calc = Calculator()
        calc.evaluate("1")  # Set x to 1
        assert calc.evaluate("2x3") == 6
        assert calc.evaluate("2×3") == 6
        assert calc.evaluate("2*3") == 6
        assert calc.evaluate("2(3+4)") == 14  # This should work - implicit multiplication
        # Test invalid implicit multiplication
        with pytest.raises(ValueError):
            calc.evaluate("(2)(3)")  # This should still fail - ambiguous

    def test_memory_operations(self):
        calc = Calculator()
        calc.evaluate("5")
        calc.memory_store()  # M+
        assert calc.memory_recall() == 5  # MR
        calc.evaluate("3")
        calc.memory_add()    # M+
        assert calc.memory_recall() == 8
        calc.memory_subtract()  # M-
        assert calc.memory_recall() == 5

    def test_scientific_functions(self):
        calc = Calculator()
        # Using degrees for trig functions
        assert calc.evaluate("sin(90)") == pytest.approx(1.0, rel=1e-2)  # sin 90°
        assert calc.evaluate("cos(0)") == pytest.approx(1.0, rel=1e-2)   # cos 0°
        assert calc.evaluate("tan(45)") == pytest.approx(1.0, rel=1e-2)  # tan 45°
        assert calc.evaluate("sqrt(16)") == 4

    def test_advanced_scientific_functions(self):
        calc = Calculator()
        # Inverse trig functions (results in degrees)
        assert calc.evaluate("asin(0.5)") == pytest.approx(30.0, rel=1e-5)
        assert calc.evaluate("acos(0)") == pytest.approx(90.0, rel=1e-5)
        
        # Hyperbolic functions
        assert calc.evaluate("sinh(1)") == pytest.approx(1.1752, rel=1e-4)
        assert calc.evaluate("cosh(0)") == pytest.approx(1.0, rel=1e-4)
        
        # Powers and special numbers
        assert calc.evaluate("2²") == 4
        assert calc.evaluate("2³") == 8
        assert calc.evaluate("cbrt(27)") == 3  # Use explicit function name
        assert calc.evaluate("√16") == 4
        assert calc.evaluate("∜16") == 2  # Fourth root
        assert calc.evaluate("3ʸ√27") == 3  # Cube root using nth root
        assert calc.evaluate("2ˣ3") == 8  # 2 to the power of 3
        
        # Logarithms
        assert calc.evaluate("log(100)") == 2
        assert calc.evaluate("ln(e)") == pytest.approx(1.0, rel=1e-4)
        assert calc.evaluate("log₂(8)") == 3
        assert calc.evaluate("logbase(8, 2)") == 3  # Log base 2 of 8

    def test_special_operations(self):
        calc = Calculator()
        # Factorial
        assert calc.evaluate("5!") == 120
        
        # Percentage
        assert calc.evaluate("50%") == 0.5
        assert calc.evaluate("200+10%") == 220.0
        
        # Scientific notation
        assert calc.evaluate("2e3") == 2000.0
        
        # Degree/Radian conversion
        assert calc.evaluate("rad(180)") == pytest.approx(math.pi, rel=1e-4)
        assert calc.evaluate("deg(pi)") == pytest.approx(180.0, rel=1e-4)

    def test_implicit_multiplication_advanced(self):
        calc = Calculator()
        assert calc.evaluate("2*pi") == pytest.approx(2 * math.pi, rel=1e-4)
        assert calc.evaluate("2*e") == pytest.approx(2 * math.e, rel=1e-4)
        assert calc.evaluate("2*3") == 6

    def test_error_handling(self):
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.evaluate("invalid")
        with pytest.raises(ValueError):
            calc.evaluate("1/0")
        with pytest.raises(ValueError):
            calc.evaluate("sin()")

    def test_complex_expressions(self):
        calc = Calculator()
        assert calc.evaluate("2+3*4") == 14
        assert calc.evaluate("(2+3)*4") == 20
        assert calc.evaluate("2^3") == 8
        assert calc.evaluate("sin(45)+cos(45)") == pytest.approx(1.414, rel=1e-3)

    def test_memory_chain(self):
        calc = Calculator()
        calc.evaluate("5")
        calc.memory_store()
        calc.evaluate("3")
        calc.memory_add()
        calc.evaluate("2")
        calc.memory_subtract()
        assert calc.memory_recall() == 6

    def test_percentage_variations(self):
        calc = Calculator()
        assert calc.evaluate("50%") == 0.5
        assert calc.evaluate("200+10%") == 220
        assert calc.evaluate("200-10%") == 180.0
        assert calc.evaluate("50% + 50%") == 1.0

    def test_scientific_notation(self):
        calc = Calculator()
        assert calc.evaluate("2e3") == 2000.0
        assert calc.evaluate("1.5e2") == 150.0

    def test_mixed_functions(self):
        calc = Calculator()
        assert calc.evaluate("sin(45)**2 + cos(45)**2") == pytest.approx(1.0, rel=1e-10)
        assert calc.evaluate("log(sqrt(100))") == 1
        assert calc.evaluate("2*pi") == pytest.approx(2 * math.pi, rel=1e-10)

    def test_invalid_expression(self):
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.evaluate("invalid")

    def test_case_insensitive_functions(self):
        calc = Calculator()
        assert calc.evaluate("Sin(0)") == 0
        assert calc.evaluate("COS(0)") == 1
        assert calc.evaluate("SQRT(16)") == 4
        assert calc.evaluate("PI") == math.pi

    def test_symbol_replacement(self):
        calc = Calculator()
        assert calc.evaluate("2×3") == 6
        assert calc.evaluate("6÷2") == 3
        assert calc.evaluate("2**3") == 8
        assert calc.evaluate("5−2") == 3
        assert calc.evaluate("sqrt(16)") == 4

    def test_whitespace_handling(self):
        calc = Calculator()
        assert calc.evaluate("2 + 2") == calc.evaluate("2+2")
        assert calc.evaluate(" sin(0) ") == 0
        assert calc.evaluate("2 * sin(0)") == 0 

    def test_evaluate_expression_with_equals(self):
        calc = Calculator()
        # Test basic equation with equals
        assert calc.evaluate("28^2 = 784/2") == 392
        # Test multiple equals signs
        assert calc.evaluate("28^2 = 784 = 784/2") == 392
        # Test with spaces around equals
        assert calc.evaluate("100 = 50 = 25 = 5*5") == 25 

    def test_reciprocal_and_fractions(self):
        calc = Calculator()
        assert calc.evaluate("1/2") == 0.5
        assert calc.evaluate("1⁄2") == 0.5  # Unicode fraction slash
        assert calc.evaluate("reciprocal(2)") == 0.5
        # Test reciprocal with previous result
        calc.evaluate("2")  # Set last result
        assert calc.evaluate("1/x") == 0.5  # Should use last result

    def test_unicode_operators(self):
        calc = Calculator()
        # Multiplication variants
        assert calc.evaluate("2×3") == 6
        assert calc.evaluate("2∗3") == 6
        assert calc.evaluate("2∙3") == 6
        
        # Division variants
        assert calc.evaluate("6÷2") == 3
        assert calc.evaluate("6∕2") == 3
        
        # Minus variants
        assert calc.evaluate("5−2") == 3
        assert calc.evaluate("5⁻2") == 3
        
        # Plus/equals variants
        assert calc.evaluate("2⁺2") == 4
        assert calc.evaluate("2⁼2") == 0  # This becomes comparison

    def test_unicode_constants(self):
        calc = Calculator()
        assert calc.evaluate("π") == pytest.approx(math.pi)
        assert calc.evaluate("2π") == pytest.approx(2 * math.pi)
        assert calc.evaluate("e") == pytest.approx(math.e)
        assert calc.evaluate("2e") == pytest.approx(2 * math.e)
        assert calc.evaluate("∞") == float('inf')
        assert calc.evaluate("ϕ") == pytest.approx((1 + math.sqrt(5)) / 2)  # Golden ratio

    def test_degree_and_radian(self):
        calc = Calculator()
        assert calc.evaluate("90°") == pytest.approx(math.pi/2)  # 90 degrees in radians
        assert calc.evaluate("rad(180)") == pytest.approx(math.pi)
        assert calc.evaluate("deg(π)") == pytest.approx(180.0)

    def test_prime_notation(self):
        calc = Calculator()
        assert calc.evaluate("5′") == 5
        assert calc.evaluate("5″") == 25  # Double prime = square
        assert calc.evaluate("5‴") == 125  # Triple prime = cube

    def test_plus_minus(self):
        calc = Calculator()
        result = calc.evaluate("±5")
        assert isinstance(result, list)
        assert result[0] == 5
        assert result[1] == -5

    def test_superscript_numbers(self):
        calc = Calculator()
        assert calc.evaluate("2⁰") == 1
        assert calc.evaluate("2¹") == 2
        assert calc.evaluate("2²") == 4
        assert calc.evaluate("2³") == 8
        assert calc.evaluate("2⁴") == 16

    def test_subscript_numbers(self):
        calc = Calculator()
        assert calc.evaluate("log₂(8)") == 3
        assert calc.evaluate("log₁₀(100)") == 2 

    def test_calculator_init(self):
        calc = Calculator()
        self.assertEqual(calc._memory, 0)
        self.assertEqual(calc._last_result, 0)
        self.assertIsNone(calc._last_expression)
        self.assertIsNone(calc._decimal_places)
    
    def test_calculator_init_with_decimal_places(self):
        calc = Calculator(decimal_places=2)
        self.assertEqual(calc._decimal_places, 2)

    def test_decimal_places_formatting(self):
        # Test with 2 decimal places
        calc = Calculator(decimal_places=2)
        self.assertEqual(calc.format_output(3.14159, "answer"), "3.14")
        self.assertEqual(calc.format_output(2.0, "answer"), "2.0")
        
        # Test with 4 decimal places
        calc = Calculator(decimal_places=4)
        self.assertEqual(calc.format_output(3.14159, "answer"), "3.1416")
        
        # Test with no decimal places limit
        calc = Calculator()
        self.assertEqual(calc.format_output(3.14159, "answer"), "3.14159")
    
    def test_decimal_places_in_calculations(self):
        calc = Calculator(decimal_places=2)
        self.assertEqual(calc.evaluate("22/7"), 3.14)  # Should round to 2 places
        
        calc = Calculator(decimal_places=4)
        self.assertEqual(calc.evaluate("22/7"), 3.1429)  # Should round to 4 places
        
        calc = Calculator()  # No decimal limit
        result = calc.evaluate("22/7")
        self.assertGreater(len(str(result).split('.')[1]), 4)  # Should have more decimals 