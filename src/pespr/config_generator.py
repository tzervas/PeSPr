"""
Configuration generator module for PeSPr.

This module generates DynEL configuration files based on project analysis.
PeSPr analyzes Python projects and creates configuration files for DynEL
(Dynamic Error Logging) to automate error handling and logging setup.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from loguru import logger


class ConfigGenerator:
    """Generates DynEL configuration files from analysis results."""

    def __init__(self, analysis_results: Dict[str, Any]) -> None:
        """
        Initialize the ConfigGenerator.

        Args:
            analysis_results: Results from project analysis
        """
        self.analysis_results = analysis_results
        logger.info("Initialized ConfigGenerator")

    def generate(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Generate a DynEL configuration from analysis results.

        Args:
            output_path: Optional path to save the configuration file

        Returns:
            Dictionary containing the generated configuration
        """
        logger.info("Generating DynEL configuration")
        
        config: Dict[str, Any] = {
            "version": "1.0",
            "project": self.analysis_results.get("project_path", ""),
            "error_handling": {
                "exceptions": self.analysis_results.get("exception_types", []),
                "handlers": [],
            },
            "logging": {
                "level": "INFO",
                "format": "json",
                "outputs": ["file", "console"],
            },
        }
        
        if output_path:
            self._save_config(config, output_path)
        
        logger.info("Configuration generation complete")
        return config

    def _save_config(self, config: Dict[str, Any], output_path: Path) -> None:
        """
        Save configuration to a YAML file.

        Args:
            config: Configuration dictionary to save
            output_path: Path where the configuration will be saved
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        logger.info(f"Configuration saved to {output_path}")


def generate_config(
    project_path: str,
    output_path: str = "dynel_config.yaml"
) -> Dict[str, Any]:
    """
    Generate a DynEL configuration file for a project.

    Args:
        project_path: Path to the Python project to analyze
        output_path: Path where the configuration will be saved

    Returns:
        Dictionary containing the generated configuration

    Example:
        >>> config = generate_config('/path/to/project')
        >>> print(config['version'])
    """
    from pespr.analyze import analyze_project
    
    logger.info(f"Generating config for {project_path}")
    analysis_results = analyze_project(project_path)
    
    generator = ConfigGenerator(analysis_results)
    return generator.generate(Path(output_path))
