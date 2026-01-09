# AAC Based Scientific Calculator

<img src="./resources/logo.png" width="50" alt="AAC Calculator">

A scientific calculator project with multiple implementations - all with the aim to work with AAC Software:

1. [Vanilla HTML Calculator](#vanilla-html-calculator). This is the current main way we recommend to use this. Its offline, works in the browser and as such as a webview in a AAC software system such as the Grid. Try it [here](https://raw.githack.com/AceCentre/ace-aac-calc/main/vanilla-html/calcstandalone.html)
2. [Python CLI Calculator](#python-cli-version). This is a command line calculator that can be used in any system that can execute Python scripts. It requires either a pythoon interpreter or a comppiled version. We build this together with a web server that can be used to serve the calculator. **IF you want/must have a calculator with minimal screen space eg. in the message bar you need this**
3. [React Version](#react-version). This is a modern React implementation of the calculator. It is a work in progress and does not yet have all the features of the other implementations.



https://github.com/user-attachments/assets/b5c1cbdd-1850-4be5-aa9d-2be025a8bceb



## Vanilla HTML Calculator
Located in `/vanilla-html/`

See a demo of this in action [here](https://raw.githack.com/AceCentre/ace-aac-calc/main/vanilla-html/calcstandalone.html)

- Single HTML file calculator that runs in any browser
- No dependencies or installation required
- Supports keyboard shortcuts and memory operations
- Windows installer available for Grid 3 integration

### Features
- Basic arithmetic operations (+, -, *, /)
- Scientific functions (sin, cos, tan, log, etc.)
- Memory operations
- Expression history with recall
- Adjustable decimal places (0-15)
- Radians/Degrees toggle
- Unicode math symbol support
- Algebraic expressions
- Random number generation
- Bracket completion preview

### Input Methods

The calculator accepts both text and Unicode math symbols:

| Text Input | Symbol Input | Description |
|------------|-------------|-------------|
| `sqrt(x)`  | `√x`        | Square root |
| `pi`       | `π`         | Pi constant |
| `*`        | `×`         | Multiplication |
| `/`        | `÷`         | Division |
| `^2`       | `²`         | Square |
| `^3`       | `³`         | Cube |
| `e`        | `ℯ`         | Euler's number |

### Example Expressions

#### Basic Math
```
2 + 2 = 4
1/2 × 20 = 10
√16 = 4
π × 2 = 6.283185307
```

#### Scientific Functions
```
sin(45) = 0.7071067812
log(100) = 2
√(π) = 1.7724538509
```

#### Random Numbers
```
rand() = 0.7324846372         # Random number between 0-1
floor(rand() * 6) + 1 = 4    # Roll a die (1-6)
floor(rand() * 100) + 1 = 42 # Random number 1-100
```

#### Algebraic Expressions
```
x^2 + 2x + 1                 # Quadratic expression
2x + 2y                      # Linear expression with variables
```

#### Memory Operations
- Store current result: Ctrl/⌘ + P (M+)
- Subtract from memory: Ctrl/⌘ + M (M-)
- Recall memory: Ctrl/⌘ + R (MR)

### Line References with @

Maybe slightly easier that using M+,M- etc you can reference previous results using the @ symbol followed by the line number. Each line in the history is numbered for easy reference.

```
1. 10 + 5 = 15
2. 20 + 12.5 = 32.5
3. @2−@1 → (32.5)−(15) = 17.5
```

#### Examples
- `@1` references the result from line 1
- `1000 - @3` subtracts line 3's result from 1000
- `@2 * @1` multiplies results from lines 2 and 1
- `floor(@1 * 6)` uses line 1's result in a function

The calculator will show both your expression with @ references and the expanded calculation with actual values.


### Keyboard Shortcuts
- `Enter` or `=` - Evaluate expression
- `Escape` - Clear workpad
- `↑` - Previous expression
- `↓` - Next expression
- `Alt/⌘ + D` - Toggle Degrees/Radians
- `Ctrl + (0-9)` - Set decimal places
- `Ctrl/⌘ + C` - Copy highlighted expression
- `Ctrl/⌘ + Shift + L` - Copy full expression

### Tips
- Brackets are automatically completed as you type
- History is scrollable and expressions can be recalled
- Click the DP button or use Ctrl + number to set decimal places
- Toggle between degrees/radians for trigonometry
- Unicode symbols can be typed directly or using text equivalents

### Installation
Download the latest installer from the [Releases](https://github.com/AceCentre/ScientificCalculator/releases) page.

## Python CLI Version
Located in `/python-cli/`
- Command-line interface calculator
- Python implementation with web server option
- Clipboard integration
- Designed for AAC software integration

### Features
- Command-line operation
- Clipboard monitoring mode
- Web server interface
- Full mathematical function support


### Examples

```bash
scicalc "2+2"              # Basic arithmetic
scicalc "sin(30)"          # Trigonometry (degrees)
scicalc "log₂(8)"         # Logarithms
scicalc "√16"             # Square root
scicalc "5!"              # Factorial
scicalc "200+10%"         # Percentages
scicalc "2π"              # Implicit multiplication
scicalc "2EE3"            # Scientific notation
```

### Output Formats

You can control how results are displayed using the `--return` option:

```bash
scicalc --return answer "2+2"        # Only shows the result: "4"
scicalc --return answer,calc "2+2"   # Shows both: "4\n2+2 = 4"
scicalc --return full "2+2"          # Shows full: "2+2 = 4" (default)
```

### Clipboard Integration

The calculator can interact with the system clipboard in two ways:

#### Watch Mode
```bash
scicalc --readpasteboard
```
This mode continuously monitors your clipboard. When you copy a mathematical expression, 
it automatically calculates the result and updates the clipboard with both the expression 
and its result. Great for doing a series of calculations!

#### Output to Clipboard
```bash
scicalc --output-to-pasteboard "2+2"
```
This copies the result directly to your clipboard instead of displaying it.
Can be combined with --return options:
```bash
scicalc --output-to-pasteboard --return answer "2+2"  # Only copies the number
```

Note: You cannot use --output-to-pasteboard with --readpasteboard

## Integration with AAC Software

This calculator is designed to work seamlessly with AAC software. The command-line interface makes it easy to:
- Call from any AAC software that can execute commands
- Copy results to clipboard for pasting
- Use with keyboard shortcuts or switch access

### Example AAC Integration

1. **Basic Calculation**: Set up a button that runs:
   ```bash
   scicalc --return answer "YOUR_EXPRESSION"
   ```

2. **Clipboard Watch Mode**: Create a button for continuous calculation:
   ```bash
   scicalc --readpasteboard
   ```
   Then users can copy expressions and get results automatically.

3. **Direct to Clipboard**: For AAC systems that work better with clipboard:
   ```bash
   scicalc --output-to-pasteboard --return answer "YOUR_EXPRESSION"
   ```

## Development

### Requirements
- Python 3.8 or higher
- Dependencies listed in pyproject.toml
- uv (Python package installer)

### Setup Development Environment

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/yourusername/scicalccli.git
cd scicalccli
uv pip install -e ".[test]"
```

### Running Tests

```bash
uv run pytest
```

### Input Methods

The calculator accepts both text and Unicode math symbols:

| Text Input | Symbol Input | Description |
|------------|-------------|-------------|
| `sqrt(x)`  | `√x`        | Square root |
| `pi`       | `π`         | Pi constant |
| `*`        | `×`         | Multiplication |
| `/`        | `÷`         | Division |
| `^2`       | `²`         | Square |
| `^3`       | `³`         | Cube |
| `e`        | `ℯ`         | Euler's number |

Examples:
- `2×π` or `2*pi` → `6.283185...`
- `√25` or `sqrt(25)` → `5`
- `3²` or `3^2` → `9`

Both notation styles work interchangeably, so you can mix and match based on your preference.


## React Version
Located in `/react/`
- Modern React implementation
- Component-based architecture
- Enhanced UI/UX
- Work in progress


(NB: this was the precursor to the vanilla html version. We are not actively developing it further. I ❤️ old skool html)

## Development
Each implementation has its own development setup. Its pretty obvious. Read the code.

## License
[GPL-3.0](LICENSE)


## Credits

- Will Wade @ [AceCentre](https://www.acecentre.org.uk)
- Marion & Katie Stanton @ [Candle](https://candleaac.com) for nudging me towards how to do this
- [Desmos](https://www.desmos.com/) for the math rendering engine inspiration (its still good and free! but there is no clear shortcut and its not easy to run offline)

## User Testing / Inspiration

- Patrick McCabe and Failbroome Academy for the initial idea and testing
