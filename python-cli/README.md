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

### From Source
```bash
uv pip install git+https://github.com/AceCentre/AAC-SciCalc.git
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
```bash
scicalc --return answer "2+2"        # Only shows the result: "4"
scicalc --return answer,calc "2+2"   # Shows both: "4\n2+2 = 4"
scicalc --return full "2+2"          # Shows full: "2+2 = 4" (default)
```

### Clipboard Integration

#### Watch Mode
```bash
scicalc --readpasteboard
```
Monitors clipboard for expressions and automatically calculates results.

#### Output to Clipboard
```bash
scicalc --output-to-pasteboard "2+2"
```
Copies result to clipboard. Can be combined with --return options:
```bash
scicalc --output-to-pasteboard --return answer "2+2"
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
git clone https://github.com/AceCentre/AAC-SciCalc.git
cd AAC-SciCalc/python-cli
uv pip install -e ".[test]"
```

### Running Tests
```bash
uv run pytest
``` 