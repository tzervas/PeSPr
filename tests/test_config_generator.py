"""
Tests for the config_generator module.
"""

import pytest
from pathlib import Path
import yaml
from pespr.config_generator import ConfigGenerator, generate_config


def test_config_generator_init() -> None:
    """Test ConfigGenerator initialization."""
    analysis_results = {
        "exception_types": ["ValueError", "TypeError"],
        "project_path": "/test/path",
    }
    generator = ConfigGenerator(analysis_results)
    assert generator.analysis_results == analysis_results


def test_config_generator_generate() -> None:
    """Test configuration generation."""
    analysis_results = {
        "exception_types": ["ValueError", "TypeError"],
        "project_path": "/test/path",
    }
    generator = ConfigGenerator(analysis_results)
    config = generator.generate()
    
    assert config["version"] == "1.0"
    assert config["project"] == "/test/path"
    assert "error_handling" in config
    assert "logging" in config


def test_config_generator_generate_with_output(tmp_path: Path) -> None:
    """Test configuration generation with file output."""
    output_file = tmp_path / "test_config.yaml"
    analysis_results = {
        "exception_types": ["ValueError"],
        "project_path": "/test/path",
    }
    
    generator = ConfigGenerator(analysis_results)
    config = generator.generate(output_file)
    
    assert output_file.exists()
    
    # Verify file contents
    with open(output_file, "r") as f:
        loaded_config = yaml.safe_load(f)
    
    assert loaded_config["version"] == "1.0"
    assert loaded_config["project"] == "/test/path"


def test_generate_config_function(tmp_path: Path) -> None:
    """Test generate_config convenience function."""
    output_file = tmp_path / "dynel_config.yaml"
    
    # Create a test project directory
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    config = generate_config(str(project_dir), str(output_file))
    
    assert isinstance(config, dict)
    assert "version" in config
    assert output_file.exists()
