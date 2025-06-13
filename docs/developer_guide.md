# Perihelion Signal Processor (PeSPr) Developer Guide

## Introduction

PeSPr automates error handling and logging configuration for Python projects by integrating static and dynamic analysis. This guide provides instructions for setting up a development environment and contributing to the project.

## Setting Up the Development Environment

### Prerequisites

- Python 3.11+
- UV (recommended for dependency management)
- Git

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

### Configuring the Environment

Edit `pespr_config.yaml` or set environment variables. See [Configuration Guide](docs/configuration.md).

## Project Structure

- **`src/`**: Core source code
- **`tests/`**: Unit and integration tests
- **`docs/`**: Documentation
- **`config/`**: Configuration files

### Key Modules

- **`analyze.py`**: Static analysis logic
- **`config_generator.py`**: DynEL config generation
- **`error_catalog.py`**: Error registry management

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