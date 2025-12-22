"""
Tests for the analyze module.
"""

import pytest
from pathlib import Path
from pespr.analyze import ProjectAnalyzer, analyze_project


def test_project_analyzer_init_valid_path(tmp_path: Path) -> None:
    """Test ProjectAnalyzer initialization with valid path."""
    analyzer = ProjectAnalyzer(tmp_path)
    assert analyzer.project_path == tmp_path


def test_project_analyzer_init_invalid_path() -> None:
    """Test ProjectAnalyzer initialization with invalid path."""
    invalid_path = Path("/nonexistent/path")
    with pytest.raises(FileNotFoundError):
        ProjectAnalyzer(invalid_path)


def test_project_analyzer_analyze(tmp_path: Path) -> None:
    """Test basic project analysis."""
    analyzer = ProjectAnalyzer(tmp_path)
    results = analyzer.analyze()
    
    assert "exception_types" in results
    assert "error_locations" in results
    assert "type_errors" in results
    assert "project_path" in results
    assert results["project_path"] == str(tmp_path)


def test_analyze_project_function(tmp_path: Path) -> None:
    """Test analyze_project convenience function."""
    results = analyze_project(str(tmp_path))
    
    assert isinstance(results, dict)
    assert "exception_types" in results
    assert "error_locations" in results
    assert "type_errors" in results
