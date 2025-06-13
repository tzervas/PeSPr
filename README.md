# Perihelion Signal Processor (PeSPr)

## Overview

PeSPr (Perihelion Signal Processor) is a sister project to [DynEL (Dynamic Error Logging)](https://gitlab.com/DynEL/DynEL), aimed at enhancing and automating the error handling, recovery, propagation management, and logging processes in Python projects. By leveraging static code analysis and integrating with existing open-source tools, PeSPr extracts crucial information from target projects to generate accurate and dynamic DynEL configuration files.

This is an early development project, and all contents are subject to change.

## Key Features

- **Automated Static Analysis**: Utilizes Mypy and Astroid to extract exception types, locations, and error-prone code segments.
- **Dynamic Configuration Generation**: Automatically creates and updates DynEL config files based on extracted project information.
- **Error Catalog and Registry**: Maintains a comprehensive database of error types and handling strategies.
- **Enhanced Logging**: Integrates with Loguru for sophisticated log formatting and flexible output options.
- **CI/CD Integration**: Extends CLI functionality for seamless integration with CI/CD pipelines.
- **Performance Optimization**: Implements caching and optimizes error handling operations.

## Installation

```bash
pip install pespr
```

## Quick Start

1. Install PeSPr in your project:
   ```bash
   pip install pespr
   ```

2. Run the initial analysis:
   ```bash
   pespr analyze /path/to/your/project
   ```

3. PeSPr will generate a `dynel_config.yaml` file in your project root.

4. Import and initialize DynEL with the generated config in your main script:
   ```python
   from dynel import DynelConfig, configure_logging
   
   config = DynelConfig()
   config.load_exception_config()
   configure_logging(config)
   ```

## Usage

### Basic Static Analysis

```bash
pespr analyze /path/to/your/project
```

### Generating DynEL Config

```bash
pespr generate-config /path/to/your/project
```

### Updating Existing Config

```bash
pespr update-config /path/to/your/project
```

## Configuration

PeSPr can be configured using a `pespr_config.yaml` file in your project root. Example:

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

## Contributing

Please fork the repository and use a feature branch. Pull requests are welcome.

## Roadmap

- [ ] Implement machine learning component for suggesting optimal exception handling strategies
- [ ] Develop real-time config optimization based on runtime error patterns
- [ ] Create a visual editor for DynEL config files
- [ ] Integrate natural language processing for generating human-readable error descriptions
- [ ] Expand third-party tool integrations

## License

PeSPr is MIT licensed. See [LICENSE](LICENSE) for more details.

## Contact

- **Author**: Tyler Zervas
- **GitLab**: [https://github.com/tzervas]
- **X**: [https://x.com/vec_wt_tech]

## Acknowledgments

PeSPr builds upon several excellent open-source projects:
- [Mypy](https://github.com/python/mypy)
- [Astroid](https://github.com/PyCQA/astroid)
- [Loguru](https://github.com/Delgan/loguru)
- [pytest](https://github.com/pytest-dev/pytest)

I'm grateful to the maintainers and contributors of these projects for their fantastic work.
