import math
import re
import numpy as np
import pyperclip
import time

class Calculator:
    def __init__(self):
        self._memory = 0
        self._last_result = 0
        self._last_expression = None
        self._last_pasteboard = None

    # Dictionary of function name mappings (case-insensitive)
    FUNCTION_ALIASES = {
        'cos': 'cos', 'COS': 'cos', 'Cos': 'cos',
        'sin': 'sin', 'SIN': 'sin', 'Sin': 'sin',
        'tan': 'tan', 'TAN': 'tan', 'Tan': 'tan',
        'acos': 'acos', 'ACOS': 'acos', 'Acos': 'acos',
        'asin': 'asin', 'ASIN': 'asin', 'Asin': 'asin',
        'atan': 'atan', 'ATAN': 'atan', 'Atan': 'atan',
        'sqrt': 'sqrt', 'SQRT': 'sqrt', 'Sqrt': 'sqrt', '√': 'sqrt',
        'log': 'log', 'LOG': 'log', 'Log': 'log',
        'ln': 'ln', 'LN': 'ln', 'Ln': 'ln',
        'exp': 'exp', 'EXP': 'exp', 'Exp': 'exp',
        'pi': 'pi', 'PI': 'pi', 'Pi': 'pi', 'π': 'pi',
    }

    def clean_expression(self, expression):
        """Clean and normalize the input expression."""
        if not expression:
            return expression
        
        # Replace function names with their canonical forms
        cleaned = expression
        for alias, canonical in self.FUNCTION_ALIASES.items():
            # Use word boundaries to avoid partial replacements
            cleaned = re.sub(rf'\b{alias}\b', canonical, cleaned)
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        # Replace common symbols
        cleaned = cleaned.replace('×', '*')
        cleaned = cleaned.replace('÷', '/')
        cleaned = cleaned.replace('−', '-')
        cleaned = cleaned.replace('^', '**')
        
        return cleaned

    def evaluate(self, expression: str) -> float:
        # Store the original expression
        self._last_expression = expression
        
        # Clean and prepare the expression
        expression = self.clean_expression(expression)
        
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

    def format_output(self, result: float, return_format: str = "answer") -> str:
        """Format the output based on the requested format."""
        if return_format == "answer":
            return f"{result}"
        elif return_format == "answer,calc":
            if self._last_expression:
                return f"{result}\n{self._last_expression} = {result}"
            return f"{result}"
        else:  # full
            if self._last_expression:
                return f"{self._last_expression} = {result}"
            return f"{result}"

    def watch_pasteboard(self, callback=None):
        """
        Watch the pasteboard for changes and evaluate the last line of any new content.
        
        Args:
            callback: Optional function to call with results
        """
        print("Watching pasteboard for calculations... Press Ctrl+C to stop.")
        try:
            while True:
                current_content = pyperclip.paste()
                
                # Check if pasteboard has changed
                if current_content != self._last_pasteboard:
                    lines = current_content.strip().split('\n')
                    last_line = lines[-1].strip()
                    
                    try:
                        # Try to evaluate the last line
                        result = self.evaluate(last_line)
                        
                        # Update the last line with the result
                        lines[-1] = f"{last_line} = {result}"
                        new_content = '\n'.join(lines)
                        
                        # Update pasteboard
                        pyperclip.copy(new_content)
                        
                        # Store current state
                        self._last_pasteboard = new_content
                        
                        # Call callback if provided
                        if callback:
                            callback(result, last_line)
                            
                    except ValueError:
                        # Not a valid calculation, just update last content
                        self._last_pasteboard = current_content
                
                time.sleep(0.5)  # Check every half second
                
        except KeyboardInterrupt:
            print("\nStopped watching pasteboard.")

    def output_to_pasteboard(self, result: float, format: str = "answer"):
        """Output the result to the pasteboard in the specified format."""
        output = self.format_output(result, format)
        pyperclip.copy(output)

    def memory_store(self):
        self._memory = self._last_result

    def memory_recall(self) -> float:
        return self._memory

    def memory_add(self):
        self._memory += self._last_result

    def memory_subtract(self):
        self._memory -= self._last_result 