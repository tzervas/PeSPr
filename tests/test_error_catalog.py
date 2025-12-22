"""
Tests for the error_catalog module.
"""

import pytest
from pespr.error_catalog import (
    ErrorCatalog,
    ErrorInfo,
    ErrorSeverity,
    ErrorCategory,
    get_error_catalog,
)


def test_error_info_creation() -> None:
    """Test ErrorInfo dataclass creation."""
    error = ErrorInfo(
        name="ValueError",
        category=ErrorCategory.RUNTIME,
        severity=ErrorSeverity.MEDIUM,
        description="Test error",
    )
    assert error.name == "ValueError"
    assert error.category == ErrorCategory.RUNTIME
    assert error.severity == ErrorSeverity.MEDIUM


def test_error_catalog_initialization() -> None:
    """Test ErrorCatalog initialization with default errors."""
    catalog = ErrorCatalog()
    errors = catalog.list_all_errors()
    
    assert len(errors) > 0
    assert any(error.name == "ValueError" for error in errors)
    assert any(error.name == "TypeError" for error in errors)


def test_error_catalog_register_error() -> None:
    """Test registering a new error in the catalog."""
    catalog = ErrorCatalog()
    
    custom_error = ErrorInfo(
        name="CustomError",
        category=ErrorCategory.CUSTOM,
        severity=ErrorSeverity.HIGH,
        description="A custom error type",
    )
    
    catalog.register_error(custom_error)
    retrieved = catalog.get_error("CustomError")
    
    assert retrieved is not None
    assert retrieved.name == "CustomError"
    assert retrieved.severity == ErrorSeverity.HIGH


def test_error_catalog_get_error() -> None:
    """Test retrieving an error from the catalog."""
    catalog = ErrorCatalog()
    error = catalog.get_error("ValueError")
    
    assert error is not None
    assert error.name == "ValueError"
    assert error.category == ErrorCategory.RUNTIME


def test_error_catalog_get_error_not_found() -> None:
    """Test retrieving a non-existent error."""
    catalog = ErrorCatalog()
    error = catalog.get_error("NonExistentError")
    
    assert error is None


def test_error_catalog_get_errors_by_category() -> None:
    """Test filtering errors by category."""
    catalog = ErrorCatalog()
    runtime_errors = catalog.get_errors_by_category(ErrorCategory.RUNTIME)
    
    assert len(runtime_errors) > 0
    assert all(error.category == ErrorCategory.RUNTIME for error in runtime_errors)


def test_error_catalog_get_errors_by_severity() -> None:
    """Test filtering errors by severity."""
    catalog = ErrorCatalog()
    medium_errors = catalog.get_errors_by_severity(ErrorSeverity.MEDIUM)
    
    assert len(medium_errors) > 0
    assert all(error.severity == ErrorSeverity.MEDIUM for error in medium_errors)


def test_get_error_catalog_singleton() -> None:
    """Test global error catalog singleton."""
    catalog1 = get_error_catalog()
    catalog2 = get_error_catalog()
    
    assert catalog1 is catalog2
