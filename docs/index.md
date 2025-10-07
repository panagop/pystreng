# Welcome to pystreng

pystreng is a Python package for structural engineering calculations, focusing on Eurocode implementations.

## Features

- **Eurocode 2 Implementations**: 
    - Shear resistance calculations (VRdmax)
    - More features coming soon...

## Installation

```bash
pip install pystreng
```

## Quick Start

Here's a simple example calculating maximum shear resistance:

```python
from pystreng.codes.eurocodes.ec2.ch6.shear import VRdmax

# Calculate VRdmax (maximum shear resistance)
result = VRdmax(
    bw=300,    # web width in mm
    d=550,     # effective depth in mm
    fck=30,    # concrete strength in MPa
    fyk=500,   # reinforcement yield strength in MPa
    fywk=500,  # stirrup yield strength in MPa
    θ=0.4,     # strut angle in radians
    units='N-mm-rad'
)
print(f"VRdmax = {result:.2f} N")
```

## Documentation

- [API Reference](api.md): Detailed documentation of all functions and classes
- [Shear Calculations](codes/eurocode2/shear.md): Detailed explanation of shear resistance calculations

## Development

To contribute or run the documentation locally:

```bash
# Clone the repository
git clone https://github.com/panagop/pystreng
cd pystreng

# Install in development mode with docs extras
pip install -e ".[dev]"

# Build the documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```
