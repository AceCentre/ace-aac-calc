# AAC Based Scientific Calculator

A scientific calculator project with multiple implementations - all with the aim to work with AAC Software:

## Vanilla HTML Calculator
Located in `/vanilla-html/`
- Single HTML file calculator that runs in any browser
- No dependencies or installation required
- Supports keyboard shortcuts and memory operations
- Windows installer available for Grid 3 integration

### Features
- Basic arithmetic operations (+, -, *, /)
- Scientific functions (sin, cos, tan, log, etc.)
- Memory operations
- Expression history with recall
- Adjustable decimal places
- Radians/Degrees toggle

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

## React Version
Located in `/react/`
- Modern React implementation
- Component-based architecture
- Enhanced UI/UX
- Work in progress

## Documentation
See individual README files in each project directory for specific documentation:
- [Vanilla HTML Documentation](vanilla-html/README.md)
- [Python CLI Documentation](python-cli/README.md)
- [React Documentation](react/README.md)

## Development
Each implementation has its own development setup. See the respective README files for details.

## License
[GPL-3.0](LICENSE)

## Key Features

- Basic arithmetic operations (+, -, *, /)
- Scientific functions (sin, cos, tan, log, etc.)
- Memory operations
- Expression history with recall
- Adjustable decimal places
- Radians/Degrees toggle

## Keyboard Shortcuts

- `Enter` or `=` - Evaluate expression
- `Escape` - Clear workpad
- `↑` - Previous expression
- `↓` - Next expression
- `Alt/⌘ + D` - Toggle Degrees/Radians
- `Ctrl + (0-9)` - Set decimal places

## Memory Operations

- `Ctrl/⌘ + P` - Memory Plus (M+)
- `Ctrl/⌘ + M` - Memory Minus (M-)
- `Ctrl/⌘ + R` - Memory Recall (MR)

## Common Operations

### Random Numbers
- Generate random number (0-1): `rand()`
- Roll a die (1-6): `floor(rand() * 6) + 1`
- Random number (1-100): `floor(rand() * 100) + 1`

### Mathematical Functions
- Square root: `sqrt(25)`
- Power: `2^3` or `pow(2,3)`
- Absolute value: `abs(-5)`
- Floor: `floor(3.7)`
- Ceiling: `ceil(3.2)`
- Round: `round(3.5)`

### Trigonometry
- Sine: `sin(45)` 
- Cosine: `cos(45)`
- Tangent: `tan(45)`
- Arc sine: `asin(0.5)`
- Arc cosine: `acos(0.5)`
- Arc tangent: `atan(0.5)`

### Constants
- Pi: `pi`
- Euler's number: `e`

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
