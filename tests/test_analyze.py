"""
Tests for the analyze module.
"""

import pytest
from pathlib import Path
from pespr.analyze import ProjectAnalyzer, analyze_project, ExceptionExtractor


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
    assert "files_analyzed" in results
    assert results["project_path"] == str(tmp_path)


def test_analyze_project_function(tmp_path: Path) -> None:
    """Test analyze_project convenience function."""
    results = analyze_project(str(tmp_path))
    
    assert isinstance(results, dict)
    assert "exception_types" in results
    assert "error_locations" in results
    assert "type_errors" in results


def test_exception_extraction_raise_statement(tmp_path: Path) -> None:
    """Test extraction of exceptions from raise statements."""
    # Create a test Python file with raise statements
    test_file = tmp_path / "test_raises.py"
    test_file.write_text("""
def example_function():
    raise ValueError("Invalid value")
    raise TypeError("Wrong type")
    raise RuntimeError("Runtime error")
""")
    
    analyzer = ProjectAnalyzer(tmp_path)
    results = analyzer.analyze()
    
    assert "ValueError" in results["exception_types"]
    assert "TypeError" in results["exception_types"]
    assert "RuntimeError" in results["exception_types"]
    assert len(results["error_locations"]) >= 3


def test_exception_extraction_except_clause(tmp_path: Path) -> None:
    """Test extraction of exceptions from except clauses."""
    test_file = tmp_path / "test_except.py"
    test_file.write_text("""
def example_function():
    try:
        risky_operation()
    except ValueError as e:
        handle_error(e)
    except KeyError as e:
        handle_key_error(e)
""")
    
    analyzer = ProjectAnalyzer(tmp_path)
    results = analyzer.analyze()
    
    assert "ValueError" in results["exception_types"]
    assert "KeyError" in results["exception_types"]


def test_exception_extraction_multiple_exceptions(tmp_path: Path) -> None:
    """Test extraction of multiple exceptions in one except clause."""
    test_file = tmp_path / "test_multiple.py"
    test_file.write_text("""
def example_function():
    try:
        risky_operation()
    except (ValueError, TypeError, KeyError) as e:
        handle_error(e)
""")
    
    analyzer = ProjectAnalyzer(tmp_path)
    results = analyzer.analyze()
    
    # Should extract all exception types from the tuple
    assert "ValueError" in results["exception_types"]
    assert "TypeError" in results["exception_types"]
    assert "KeyError" in results["exception_types"]


def test_exception_extraction_custom_exceptions(tmp_path: Path) -> None:
    """Test extraction of custom exception classes."""
    test_file = tmp_path / "test_custom.py"
    test_file.write_text("""
class CustomError(Exception):
    pass

class AnotherError(RuntimeError):
    pass

def example_function():
    raise CustomError("Custom error")
    raise AnotherError("Another error")
""")
    
    analyzer = ProjectAnalyzer(tmp_path)
    results = analyzer.analyze()
    
    assert "CustomError" in results["exception_types"]
    assert "AnotherError" in results["exception_types"]


def test_find_python_files_directory(tmp_path: Path) -> None:
    """Test finding Python files in a directory."""
    # Create some Python files
    (tmp_path / "file1.py").write_text("# file 1")
    (tmp_path / "file2.py").write_text("# file 2")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file3.py").write_text("# file 3")
    
    analyzer = ProjectAnalyzer(tmp_path)
    python_files = analyzer._find_python_files()
    
    assert len(python_files) == 3
    assert all(f.suffix == ".py" for f in python_files)


def test_find_python_files_single_file(tmp_path: Path) -> None:
    """Test finding a single Python file."""
    test_file = tmp_path / "single.py"
    test_file.write_text("# single file")
    
    analyzer = ProjectAnalyzer(test_file)
    python_files = analyzer._find_python_files()
    
    assert len(python_files) == 1
    assert python_files[0] == test_file


def test_analyze_with_syntax_error(tmp_path: Path) -> None:
    """Test that analysis handles syntax errors gracefully."""
    test_file = tmp_path / "syntax_error.py"
    test_file.write_text("def broken( syntax error here")
    
    analyzer = ProjectAnalyzer(tmp_path)
    results = analyzer.analyze()
    
    # Should not crash, just log warning
    assert isinstance(results, dict)
    assert "exception_types" in results


def test_exception_extractor_direct() -> None:
    """Test ExceptionExtractor directly."""
    extractor = ExceptionExtractor()
    assert len(extractor.exception_types) == 0
    assert len(extractor.error_locations) == 0


def test_error_location_structure(tmp_path: Path) -> None:
    """Test that error locations have the correct structure."""
    test_file = tmp_path / "test_location.py"
    test_file.write_text("""
def example():
    raise ValueError("test")
""")
    
    analyzer = ProjectAnalyzer(tmp_path)
    results = analyzer.analyze()
    
    assert len(results["error_locations"]) > 0
    location = results["error_locations"][0]
    
    assert "file" in location
    assert "line" in location
    assert "type" in location
    assert "exception" in location
    assert location["type"] in ["raise", "except"]
