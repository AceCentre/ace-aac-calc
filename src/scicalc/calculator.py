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

    # Dictionary of mathematical symbols and their Python equivalents
    MATH_SYMBOLS = {
        # Basic operators
        '×': '*', '∗': '*', '∙': '*',  # Multiplication variants
        '÷': '/', '∕': '/',  # Division variants
        '−': '-', '₋': '-', '⁻': '-',  # Minus variants
        '⁺': '+', '₊': '+',  # Plus variants
        '⁼': '=', '₌': '=',  # Equals variants
        '^': '**', '⁽': '(', '⁾': ')',  # Power and parentheses
        '⁄': '/',  # Fraction slash
        
        # Variables
        'x': 'x',  # Variable x
        
        # Roots
        '√': 'sqrt',  # Square root
        '∛': 'cbrt',  # Cube root
        '∜': 'root4',  # Fourth root
        'ʸ√': 'nthroot',  # nth root
        
        # Powers
        'ʸ': '**',  # General power
        'ˣ': '**',  # Power of x
        
        # Greek letters commonly used in math
        'π': 'pi',    # Pi
        'ϕ': 'phi',   # Phi
        'θ': 'theta', # Theta
        'ϑ': 'theta', # Theta variant
        'ϵ': 'epsilon', # Epsilon
        'ϱ': 'rho',   # Rho
        
        # Other mathematical symbols
        '∞': 'inf',   # Infinity
        '°': 'deg',   # Degree
        '′': 'prime', # Prime
        '″': 'prime2', # Double prime
        '‴': 'prime3', # Triple prime
        '±': 'pm',    # Plus-minus
    }

    def clean_expression(self, expression):
        """Clean and normalize the input expression."""
        if not expression:
            return expression
        
        # Debug print for bracket handling
        print(f"Input: {expression}")
        
        # First handle root functions before other replacements
        cleaned = expression
        cleaned = re.sub(r'∜\s*(\d+|\([^)]+\))', r'root4(\1)', cleaned)  # Fourth root
        cleaned = re.sub(r'∛\s*(\d+|\([^)]+\))', r'cbrt(\1)', cleaned)  # Cube root
        cleaned = re.sub(r'√\s*(\d+|\([^)]+\))', r'sqrt(\1)', cleaned)  # Square root
        
        # Handle superscript numbers first
        superscript_map = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
        def replace_superscript(match):
            return f"**{match.group(0).translate(superscript_map)}"
        cleaned = re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', replace_superscript, cleaned)
        
        # Handle subscript numbers in logarithms
        subscript_map = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
        def replace_subscript(match):
            base = match.group(1).translate(subscript_map)
            return f"logbase({match.group(2)}, {base})"
        cleaned = re.sub(r'log([₀₁₂₃₄₅₆₇₈₉]+)\((.+?)\)', replace_subscript, cleaned)
        
        # Handle scientific notation before other replacements
        def handle_scientific(match):
            num, exp = match.groups()
            return f"{num}*10**{exp}"
        cleaned = re.sub(r'(\d+)e(\d+)', handle_scientific, cleaned)
        
        # First balance any unclosed parentheses
        open_count = cleaned.count('(')
        close_count = cleaned.count(')')
        if open_count > close_count:
            # Simply add missing closing parentheses at the end
            cleaned += ')' * (open_count - close_count)
            print(f"After bracket completion: {cleaned}")
        
        # Handle special cases first before any other processing
        if cleaned.strip() == '1/x':
            return 'reciprocal(x)'  # Use reciprocal function
        
        # Handle plus-minus
        if cleaned.startswith('±'):
            return f'pm({cleaned[1:]})'
        
        # Replace mathematical symbols with their Python equivalents
        for symbol, replacement in self.MATH_SYMBOLS.items():
            cleaned = cleaned.replace(symbol, replacement)
        
        # Replace function names with their canonical forms first
        for alias, canonical in self.FUNCTION_ALIASES.items():
            # Use word boundaries to avoid partial replacements
            cleaned = re.sub(rf'\b{alias}\b', canonical, cleaned)
        
        # Handle implicit multiplication with constants
        cleaned = re.sub(r'(\d+)([πe])', r'\1*\2', cleaned)  # Numbers with constants
        # Handle all forms of implicit multiplication
        cleaned = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', cleaned)  # Number followed by variable (2x)
        cleaned = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', cleaned)  # Variable followed by number (x2)
        cleaned = re.sub(r'(\d+)\(', r'\1*(', cleaned)  # Number followed by parenthesis
        cleaned = re.sub(r'(\d+)([√∛∜])', r'\1*\2', cleaned)  # Number followed by root
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        # Handle special functions
        cleaned = re.sub(r'(\w+)⁻¹\(', r'a\1(', cleaned)  # sin⁻¹(x) becomes asin(x)
        
        # Handle degrees with proper multiplication
        cleaned = re.sub(r'(\d+)°', r'rad(\1)', cleaned)  # Use rad function
        
        # Handle prime notation
        cleaned = re.sub(r'(\d+)′', r'prime(\1)', cleaned)  # Single prime
        cleaned = re.sub(r'(\d+)″', r'prime2(\1)', cleaned)  # Double prime
        cleaned = re.sub(r'(\d+)‴', r'prime3(\1)', cleaned)  # Triple prime
        
        return cleaned

    def evaluate(self, expression: str) -> float:
        # Store the original expression
        self._last_expression = expression
        
        # Initialize x variable with last result
        if not hasattr(self, '_last_result'):
            self._last_result = 0
        
        # If expression contains equals sign, take the part after the last equals
        if '=' in expression:
            expression = expression.split('=')[-1].strip()
        
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
                'root4': lambda x: x ** (1/4),
                'root': lambda x, n: x ** (1/n),  # General root function
                'nthroot': lambda x, n: x ** (1/n),  # nth root
                'pow': pow,
                'exp': math.exp,
                'reciprocal': lambda x: 1/x,  # 1/x function
                
                # Logarithms
                'log': math.log10,
                'ln': math.log,
                'log2': math.log2,
                'logbase': lambda x, base: math.log(x, base),  # Log with arbitrary base
                
                # Unicode operators need explicit functions
                '×': lambda x, y: x * y,
                '∗': lambda x, y: x * y,
                '∙': lambda x, y: x * y,
                '÷': lambda x, y: x / y,
                '∕': lambda x, y: x / y,
                '−': lambda x, y: x - y,
                '⁻': lambda x, y: x - y,
                '⁺': lambda x, y: x + y,
                
                # Constants
                'pi': math.pi,
                'e': math.e,
                'inf': float('inf'),
                'phi': (1 + math.sqrt(5)) / 2,  # Golden ratio
                'theta': math.pi,  # Common use of theta is pi
                'epsilon': np.finfo(float).eps,  # Machine epsilon
                'rho': math.pi,  # Sometimes used as alternative to pi
                
                # Additional functions
                'abs': abs,
                'factorial': math.factorial,
                'rand': np.random.random,
                'pm': lambda x: [x, -x],  # Plus-minus returns both values
                'prime': lambda x: x,      # For now, just return the number
                'prime2': lambda x: x**2,  # Square
                'prime3': lambda x: x**3,  # Cube
                
                # Common operations
                'rad': math.radians,
                'deg': math.degrees,
                
                # Add x variable for calculations
                'x': self._last_result,  # x is always initialized now
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
        # First clean the expression
        expression = self.clean_expression(expression)
        
        # First handle function calls to prevent interference
        def handle_function_call(match):
            func = match.group(1)
            args = match.group(2)
            # Special handling for log₂
            if func == 'log₂':
                return f'log2({args})'
            return f'{func}({args})'
        
        # Handle function calls with proper parentheses
        expression = re.sub(r'(\w+₂?)\s*\(([^)]*)\)?', r'\1(\2)', expression)
        
        # Replace various multiplication symbols
        expression = expression.replace('x', '*')
        expression = expression.replace('×', '*')
        
        # Handle special functions and roots
        expression = re.sub(r'∛(\d+)', r'cbrt(\1)', expression)
        expression = re.sub(r'√(\d+)', r'sqrt(\1)', expression)
        
        # Handle superscript numbers
        expression = re.sub(r'(\d+)²', r'\1**2', expression)
        expression = re.sub(r'(\d+)³', r'\1**3', expression)
        
        # Add missing closing brackets, but preserve the original count for each opening
        stack = []
        result = []
        for char in expression:
            if char == '(':
                stack.append(len(result))
            elif char == ')':
                if stack:
                    stack.pop()
            result.append(char)
        
        # Add missing closing brackets in reverse order
        while stack:
            pos = stack.pop()
            result.append(')')
        
        expression = ''.join(result)
        
        # Add implicit multiplication
        # Between number and parenthesis
        expression = re.sub(r'(\d+)(?=\()', r'\1*', expression)
        # Between closing and opening parentheses
        expression = re.sub(r'\)\(', ')*(', expression)
        # Between number and constant
        expression = re.sub(r'(\d+)([πe])', r'\1*\2', expression)
        # Between parentheses groups
        expression = re.sub(r'\)\s*(\d+)', r')*\1', expression)
        
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