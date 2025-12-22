"""
Error catalog and registry module for PeSPr.

This module provides a comprehensive error catalog system for managing
and categorizing different types of errors and exceptions.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class ErrorSeverity(Enum):
    """Severity levels for errors."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorCategory(Enum):
    """Categories for error types."""
    
    RUNTIME = "runtime"
    TYPE = "type"
    SYNTAX = "syntax"
    LOGIC = "logic"
    RESOURCE = "resource"
    NETWORK = "network"
    SECURITY = "security"
    CUSTOM = "custom"


@dataclass
class ErrorInfo:
    """Information about a specific error type."""
    
    name: str
    category: ErrorCategory
    severity: ErrorSeverity
    description: str = ""
    exceptions: List[str] = field(default_factory=list)
    handlers: List[str] = field(default_factory=list)
    
    def __hash__(self) -> int:
        return hash(self.name)


class ErrorCatalog:
    """Comprehensive catalog of error types and patterns."""

    def __init__(self) -> None:
        """Initialize the ErrorCatalog with default error types."""
        self._catalog: Dict[str, ErrorInfo] = {}
        self._initialize_default_errors()
        logger.info("Initialized ErrorCatalog")

    def _initialize_default_errors(self) -> None:
        """Initialize catalog with common Python exception types."""
        default_errors = [
            ErrorInfo(
                name="ValueError",
                category=ErrorCategory.RUNTIME,
                severity=ErrorSeverity.MEDIUM,
                description="Raised when an operation receives an argument with the right type but inappropriate value",
                exceptions=["ValueError"],
            ),
            ErrorInfo(
                name="TypeError",
                category=ErrorCategory.TYPE,
                severity=ErrorSeverity.MEDIUM,
                description="Raised when an operation is applied to an object of inappropriate type",
                exceptions=["TypeError"],
            ),
            ErrorInfo(
                name="FileNotFoundError",
                category=ErrorCategory.RESOURCE,
                severity=ErrorSeverity.HIGH,
                description="Raised when a file or directory is requested but doesn't exist",
                exceptions=["FileNotFoundError"],
            ),
            ErrorInfo(
                name="KeyError",
                category=ErrorCategory.RUNTIME,
                severity=ErrorSeverity.MEDIUM,
                description="Raised when a dictionary key is not found",
                exceptions=["KeyError"],
            ),
            ErrorInfo(
                name="AttributeError",
                category=ErrorCategory.RUNTIME,
                severity=ErrorSeverity.MEDIUM,
                description="Raised when an attribute reference or assignment fails",
                exceptions=["AttributeError"],
            ),
        ]
        
        for error in default_errors:
            self._catalog[error.name] = error

    def register_error(self, error_info: ErrorInfo) -> None:
        """
        Register a new error type in the catalog.

        Args:
            error_info: Information about the error to register
        """
        self._catalog[error_info.name] = error_info
        logger.debug(f"Registered error: {error_info.name}")

    def get_error(self, name: str) -> Optional[ErrorInfo]:
        """
        Retrieve error information by name.

        Args:
            name: Name of the error to retrieve

        Returns:
            ErrorInfo if found, None otherwise
        """
        return self._catalog.get(name)

    def get_errors_by_category(self, category: ErrorCategory) -> List[ErrorInfo]:
        """
        Get all errors in a specific category.

        Args:
            category: Category to filter by

        Returns:
            List of ErrorInfo objects in the category
        """
        return [
            error for error in self._catalog.values()
            if error.category == category
        ]

    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[ErrorInfo]:
        """
        Get all errors with a specific severity.

        Args:
            severity: Severity level to filter by

        Returns:
            List of ErrorInfo objects with the severity
        """
        return [
            error for error in self._catalog.values()
            if error.severity == severity
        ]

    def list_all_errors(self) -> List[ErrorInfo]:
        """
        Get all registered errors.

        Returns:
            List of all ErrorInfo objects in the catalog
        """
        return list(self._catalog.values())


# Global error catalog instance
_global_catalog: Optional[ErrorCatalog] = None


def get_error_catalog() -> ErrorCatalog:
    """
    Get the global error catalog instance.

    Returns:
        The global ErrorCatalog instance
    """
    global _global_catalog
    if _global_catalog is None:
        _global_catalog = ErrorCatalog()
    return _global_catalog
