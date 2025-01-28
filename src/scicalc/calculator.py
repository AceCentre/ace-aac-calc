import math
import re
import numpy as np

class Calculator:
    def __init__(self):
        self._memory = 0
        self._last_result = 0

    def evaluate(self, expression: str) -> float:
        # Clean and prepare the expression
        expression = self._prepare_expression(expression)
        
        try:
            # Create a safe dictionary of allowed functions
            safe_dict = {
                # Basic trig functions (wrapping to handle degrees)
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                
                # Inverse trig functions (converting result to degrees)
                'asin': lambda x: math.degrees(math.asin(x)),
                'acos': lambda x: math.degrees(math.acos(x)),
                'atan': lambda x: math.degrees(math.atan(x)),
                
                # Hyperbolic functions
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'asinh': math.asinh,
                'acosh': math.acosh,
                'atanh': math.atanh,
                
                # Powers and roots
                'sqrt': math.sqrt,
                'cbrt': lambda x: np.cbrt(x),
                'pow': pow,
                'exp': math.exp,
                
                # Logarithms
                'log': math.log10,
                'ln': math.log,
                'log2': math.log2,
                
                # Constants
                'pi': math.pi,
                'e': math.e,
                
                # Additional functions
                'abs': abs,
                'factorial': math.factorial,
                'rand': np.random.random,
                
                # Common operations
                'rad': math.radians,
                'deg': math.degrees
            }
            
            # Handle special cases
            expression = self._handle_special_cases(expression)
            
            # Debug the expression before evaluation
            # print(f"Evaluating: {expression}")
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            self._last_result = result
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")

    def _prepare_expression(self, expression: str) -> str:
        # First handle function calls to prevent interference
        def handle_function_call(match):
            func = match.group(1)
            args = match.group(2)
            # Special handling for log₂
            if func == 'log₂':
                return f'log2({args})'
            return f'{func}({args})'
            
        expression = re.sub(r'(\w+₂?)\s*\(([^)]+)\)', handle_function_call, expression)
        
        # Replace various multiplication symbols
        expression = expression.replace('x', '*')
        expression = expression.replace('×', '*')
        
        # Replace inverse trig functions
        expression = expression.replace('sin⁻¹', 'asin')
        expression = expression.replace('cos⁻¹', 'acos')
        expression = expression.replace('tan⁻¹', 'atan')
        expression = expression.replace('sinh⁻¹', 'asinh')
        expression = expression.replace('cosh⁻¹', 'acosh')
        expression = expression.replace('tanh⁻¹', 'atanh')
        
        # Handle exponents
        expression = expression.replace('^', '**')
        expression = re.sub(r'(\d+)²', r'\1**2', expression)
        expression = re.sub(r'(\d+)³', r'\1**3', expression)
        
        # Handle roots
        expression = expression.replace('∛', 'cbrt(')
        expression = expression.replace('√', 'sqrt(')
        
        # Handle special functions
        expression = expression.replace('EE', '*10**')
        
        # Handle constants with implicit multiplication
        expression = re.sub(r'(\d+)([πe])', r'\1*\2', expression)
        expression = expression.replace('π', 'pi')
        
        # Add missing closing brackets
        open_count = expression.count('(')
        close_count = expression.count(')')
        expression += ')' * (open_count - close_count)
        
        # Add implicit multiplication between parentheses
        expression = re.sub(r'\)\s*\(', ')*(', expression)
        
        # Add implicit multiplication for numbers next to parentheses
        expression = re.sub(r'(\d+)(?=\()', r'\1*', expression)
        expression = re.sub(r'\)(\d+)', r')*\1', expression)
        
        return expression

    def _handle_special_cases(self, expression: str) -> str:
        # Handle factorial
        if '!' in expression:
            expression = re.sub(r'(\d+)!', r'factorial(\1)', expression)
        
        # Handle percentage
        if '%' in expression:
            # First handle relative percentages (like 200+10%)
            def handle_relative_percent(match):
                base = float(match.group(1))
                op = match.group(2)
                percent = float(match.group(3))
                amount = base * percent / 100
                if op == '-':
                    amount = -amount
                return f"{base}{op}{amount}"
            
            # Handle patterns like "200+10%" or "200-10%"
            expression = re.sub(
                r'(\d+(?:\.\d+)?)\s*([+\-])\s*(\d+(?:\.\d+)?)\s*%',
                handle_relative_percent,
                expression
            )
            
            # Then handle any remaining standalone percentages (like 50%)
            def handle_standalone_percent(match):
                num = float(match.group(1))
                return str(num / 100)
            
            expression = re.sub(r'(\d+(?:\.\d+)?)\s*%', handle_standalone_percent, expression)
            
        return expression

    def memory_store(self):
        self._memory = self._last_result

    def memory_recall(self) -> float:
        return self._memory

    def memory_add(self):
        self._memory += self._last_result

    def memory_subtract(self):
        self._memory -= self._last_result 