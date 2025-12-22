# Perihelion Signal Processor (PeSPr) Developer Guide

## Introduction

PeSPr automates error handling and logging configuration for Python projects by integrating static and dynamic analysis. This guide provides instructions for setting up a development environment and contributing to the project.

## Setting Up the Development Environment

### Prerequisites

- Python 3.11+
- UV (recommended for dependency management)
- Git
- Mojo SDK (optional, for high-performance operations)

### Cloning the Repository

```bash
git clone https://github.com/tzervas/pespr.git
```

### Installing Dependencies

```bash
cd pespr
uv sync
```

Or use pip:

```bash
pip install -r requirements.txt
```

### Installing Mojo (Optional)

For high-performance model operations, install the Mojo SDK:

```bash
# Install Modular CLI
curl -s https://get.modular.com | sh -

# Install Mojo SDK
modular install mojo

# Verify installation
mojo --version
```

See the [Mojo Integration Guide](mojo_integration.md) for detailed setup and usage.

### Configuring the Environment

Edit `pespr_config.yaml` or set environment variables. See [Configuration Guide](docs/configuration.md).

## Project Structure

- **`src/`**: Core source code
  - **`pespr/`**: Python modules
  - **`pespr_mojo/`**: Mojo performance modules (optional)
- **`tests/`**: Unit and integration tests
- **`docs/`**: Documentation
- **`config/`**: Configuration files

### Key Modules

- **`analyze.py`**: Static analysis logic (with optional Mojo acceleration)
- **`config_generator.py`**: DynEL config generation
- **`error_catalog.py`**: Error registry management
- **Mojo modules** (optional):
  - **`ast_analyzer.mojo`**: High-performance AST analysis
  - **`type_checker.mojo`**: Accelerated type checking
  - **`pattern_matcher.mojo`**: Fast pattern matching

## Development Workflow

### Branching Strategy

- Feature branches: `feature/<description>`
- Bugfix branches: `bugfix/<description>`
- Target `main` for PRs

### Coding Standards

- Adhere to PEP8
- Use type hints
- Validate inputs and secure error handling

### Testing Requirements

- Write unit and integration tests with pytest
- Run tests:
  ```bash
  pytest
  ```

### Documentation Standards

- Use Google-style docstrings
- Update docs for changes

## Building and Running

### Running Locally

```bash
python main.py
```

### Running Tests

```bash
pytest
```

## Debugging and Troubleshooting

- **Dependency Issues**: Run `uv sync`
- **Config Errors**: Validate `pespr_config.yaml`
- Use `pdb` for debugging:
  ```bash
  python -m pdb main.py
  ```

## Advanced Topics

### Performance Optimization

Profile with `cProfile`:

```bash
python -m cProfile main.py
```

Optimize analysis with caching and parallelism.

### Extending the Framework

- Add tools to `analyze.py`
- Extend `error_catalog.py` for custom handlers
- Implement performance-critical operations in Mojo (see [Mojo Integration Guide](mojo_integration.md))

## Working with Mojo

### When to Use Mojo
- Performance-critical AST operations
- Large-scale static analysis
- Type inference bottlenecks
- Pattern matching hot paths

### Mojo Development Workflow
1. Profile Python code to identify bottlenecks
2. Implement critical path in Mojo
3. Create Python bindings
4. Add tests and benchmarks
5. Validate performance improvements

### Example: Migrating a Function to Mojo

Python version:
```python
def count_exceptions(file_path: str) -> int:
    # Slow Python implementation
    pass
```

Mojo version:
```mojo
fn count_exceptions(file_path: String) -> Int:
    # Fast Mojo implementation with SIMD
    pass
```

See [Mojo Integration Guide](mojo_integration.md) for comprehensive examples.