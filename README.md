# Scientific Calculator CLI

A command-line scientific calculator designed specifically for AAC (Augmentative and Alternative Communication) users. This calculator provides advanced mathematical functions with an accessible interface that can be easily integrated with AAC software.

## Features

- Basic arithmetic operations (+, -, *, /)
- Scientific functions:
  - Trigonometric functions (sin, cos, tan)
  - Inverse trigonometric functions (sin⁻¹, cos⁻¹, tan⁻¹)
  - Hyperbolic functions (sinh, cosh, tanh)
  - Logarithms (log₂, log₁₀, ln)
  - Powers and roots (√, ∛, x², x³)
- Special operations:
  - Percentages (50%, 200+10%)
  - Factorial (5!)
  - Scientific notation (2EE3 = 2×10³)
- Memory functions (store, recall, add to memory, subtract from memory)
- Automatic bracket completion
- Implicit multiplication (2π = 2*π)

## Installation

### Windows Installer
Download the latest installer from the [Releases](https://github.com/yourusername/scicalccli/releases) page.

### From Source

```bash
uv pip install git+https://github.com/yourusername/scicalccli.git
```

## Usage

To use the calculator, simply run the `scicalc` command in your terminal.

### Basic Usage

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
