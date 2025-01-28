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

## Integration with AAC Software

This calculator is designed to work seamlessly with AAC software. The command-line interface makes it easy to:
- Call from any AAC software that can execute commands
- Copy results to clipboard for pasting
- Use with keyboard shortcuts or switch access

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
