# Perihelion Signal Processor (PeSPr)

🚀 **Project Status**: In active development. All components subject to change. Contributions and feedback welcome.

🎯 **Intent**: Enhance and automate error handling, recovery, propagation management, and logging in Python projects by integrating static and dynamic analysis with tools like DynEL.

🛠️ **Goals**:
- Automate error handling and logging configuration
- Improve error propagation and control flow
- Integrate with CI/CD pipelines and IDEs
- Optimize performance for scalability

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Basic Example](#basic-example)
   - [Advanced Usage](#advanced-usage)
4. [Features](#features)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Development Setup](#development-setup)
8. [Proposed Implementation](#proposed-implementation)
   - [Proof of Concept (POC)](#proof-of-concept-poc)
   - [Minimum Viable Product (MVP)](#minimum-viable-product-mvp)
9. [Security Best Practices](#security-best-practices)
10. [Contribution](#contribution)
11. [License](#license)
12. [Contact](#contact)
13. [Troubleshooting](#troubleshooting)
14. [Acknowledgments](#acknowledgments)
15. [References](#references)

## Description

PeSPr (Perihelion Signal Processor) is a sister project to [DynEL (Dynamic Error Logging)](https://gitlab.com/DynEL/DynEL), designed to automate the generation of DynEL configuration files. It leverages static analysis tools (Mypy, Astroid) and dynamic analysis (pytest) to extract exception types, error-prone code segments, and runtime behaviors, creating a robust error handling and logging framework for Python projects.

## Installation

Install PeSPr via pip:

```bash
pip install pespr
```

For development, use [UV](https://docs.astral.sh/uv/) to manage dependencies. See [Development Setup](#development-setup).

## Usage

### Basic Example

Analyze a project to generate a `dynel_config.yaml`:

```bash
pespr analyze /path/to/your/project
```

### Advanced Usage

Generate or update configurations with additional options:

```bash
pespr generate-config /path/to/your/project --output dynel_config.yaml
pespr update-config /path/to/your/project
```

## Features

- **Static Analysis**: Extracts exception data using Mypy and Astroid
- **Dynamic Analysis**: Integrates runtime data with pytest
- **Error Catalog**: Comprehensive registry of error types
- **Logging**: Advanced formatting and outputs via Loguru
- **CI/CD Integration**: Automates config generation in pipelines
- **Extensibility**: Supports custom error handlers and plugins

## Configuration

Configure PeSPr with a `pespr_config.yaml` file:

```yaml
analysis:
  ignore_dirs: ['tests', 'docs']
  max_depth: 5
logging:
  level: INFO
  output: ['file', 'console']
ci_integration:
  enabled: true
  report_format: json
```

See the [Configuration Guide](docs/configuration.md) for details.

## Testing

Run tests with pytest:

```bash
pytest
```

Install development dependencies first (see [Development Setup](#development-setup)).

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tzervas/pespr.git
   ```
2. Navigate to the directory:
   ```bash
   cd pespr
   ```
3. Install dependencies with UV:
   ```bash
   uv sync
   ```
4. Configure via `pespr_config.yaml` or environment variables.
5. Run the application:
   ```bash
   python main.py
   ```

## Proposed Implementation

### Proof of Concept (POC)

Basic static analysis and config generation:

```python
from pespr import analyze_project

config = analyze_project('/path/to/project')
config.save('dynel_config.yaml')
```

### Minimum Viable Product (MVP)

Configurable integration with DynEL:

```python
from pespr import PeSPrConfig, generate_config

config = PeSPrConfig()
config.load('pespr_config.yaml')
generate_config('/path/to/project', config)
```

## Security Best Practices

🔒
- Validate all inputs to prevent injection or errors
- Use structured error handling to avoid crashes
- Secure logging to prevent sensitive data leaks
- Keep dependencies updated to address vulnerabilities

## Contribution

See the [Developer Guide](docs/devel-docs/developer_guide.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution details.

## License

MIT License. See [LICENSE](LICENSE) for more information.

## Contact

- **Author**: Tyler Zervas
- **GitHub**: [tzervas](https://github.com/tzervas)
- **X**: [@vec_wt_tech](https://x.com/vec_wt_tech)

## Troubleshooting

Check the [issue tracker](https://github.com/tzervas/pespr/issues) for common problems or contact the author.

## Acknowledgments

Thanks to the teams behind [Mypy](https://github.com/python/mypy), [Astroid](https://github.com/PyCQA/astroid), [Loguru](https://github.com/Delgan/loguru), and [pytest](https://github.com/pytest-dev/pytest).

## References

- [DynEL Documentation](https://gitlab.com/DynEL/DynEL)
- [UV Documentation](https://docs.astral.sh/uv/)