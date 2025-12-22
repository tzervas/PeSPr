"""
Static and dynamic analysis module for PeSPr.

This module provides functionality to analyze Python projects for:
- Exception types and locations
- Error-prone code segments
- Type checking with Mypy
- AST analysis with Astroid
"""

import ast
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from loguru import logger
import astroid
from astroid import nodes


class ExceptionExtractor:
    """Extracts exception information from Python AST."""

    def __init__(self) -> None:
        """Initialize the exception extractor."""
        self.exception_types: Set[str] = set()
        self.error_locations: List[Dict[str, Any]] = []

    def extract_from_file(self, file_path: Path) -> None:
        """
        Extract exception information from a Python file.

        Args:
            file_path: Path to the Python file to analyze
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse with astroid for better analysis
            module = astroid.parse(content, path=str(file_path))
            self._visit_node(module, file_path)

        except (SyntaxError, astroid.AstroidSyntaxError) as e:
            logger.warning(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")

    def _visit_node(self, node: nodes.NodeNG, file_path: Path) -> None:
        """
        Recursively visit AST nodes to extract exception information.

        Args:
            node: Astroid AST node to visit
            file_path: Path to the file being analyzed
        """
        # Extract raise statements
        if isinstance(node, nodes.Raise):
            self._handle_raise(node, file_path)

        # Extract exception handlers (except clauses)
        if isinstance(node, nodes.ExceptHandler):
            self._handle_except(node, file_path)

        # Extract function definitions that may raise
        if isinstance(node, nodes.FunctionDef):
            self._handle_function_def(node, file_path)

        # Recursively visit child nodes
        for child in node.get_children():
            self._visit_node(child, file_path)

    def _handle_raise(self, node: nodes.Raise, file_path: Path) -> None:
        """
        Handle a raise statement node.

        Args:
            node: Raise statement node
            file_path: Path to the file being analyzed
        """
        if node.exc:
            exception_type = self._get_exception_type(node.exc)
            if exception_type:
                self.exception_types.add(exception_type)
                self.error_locations.append({
                    "file": str(file_path),
                    "line": node.lineno,
                    "type": "raise",
                    "exception": exception_type,
                })

    def _handle_except(self, node: nodes.ExceptHandler, file_path: Path) -> None:
        """
        Handle an exception handler (except clause) node.

        Args:
            node: ExceptHandler node
            file_path: Path to the file being analyzed
        """
        if node.type:
            exception_type = self._get_exception_type(node.type)
            if exception_type:
                self.exception_types.add(exception_type)
                self.error_locations.append({
                    "file": str(file_path),
                    "line": node.lineno,
                    "type": "except",
                    "exception": exception_type,
                })

    def _handle_function_def(self, node: nodes.FunctionDef, file_path: Path) -> None:
        """
        Handle a function definition node to extract raises annotations.

        Args:
            node: FunctionDef node
            file_path: Path to the file being analyzed
        """
        # Check for raises in docstring
        if node.doc_node:
            doc = node.doc_node.value
            if "raises" in doc.lower() or "raise" in doc.lower():
                # Simple heuristic - could be improved with more sophisticated parsing
                logger.debug(f"Function {node.name} at {file_path}:{node.lineno} may raise exceptions (from docstring)")

    def _get_exception_type(self, node: nodes.NodeNG) -> Optional[str]:
        """
        Extract exception type name from a node.

        Args:
            node: AST node representing an exception

        Returns:
            Exception type name or None
        """
        try:
            if isinstance(node, nodes.Name):
                return node.name
            elif isinstance(node, nodes.Attribute):
                # Handle module.Exception format
                return node.as_string()
            elif isinstance(node, nodes.Call):
                # Handle Exception() format
                if isinstance(node.func, nodes.Name):
                    return node.func.name
                elif isinstance(node.func, nodes.Attribute):
                    return node.func.as_string()
            elif isinstance(node, nodes.Tuple):
                # Handle multiple exceptions in except clause
                types = []
                for elt in node.elts:
                    exc_type = self._get_exception_type(elt)
                    if exc_type:
                        types.append(exc_type)
                return ", ".join(types) if types else None
        except Exception as e:
            logger.debug(f"Error extracting exception type: {e}")
        return None


class ProjectAnalyzer:
    """Analyzes Python projects for error handling patterns."""

    def __init__(self, project_path: Path) -> None:
        """
        Initialize the ProjectAnalyzer.

        Args:
            project_path: Path to the Python project to analyze
        """
        self.project_path = Path(project_path)
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")
        logger.info(f"Initialized ProjectAnalyzer for {project_path}")

    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the project and extract error handling information.

        Returns:
            Dictionary containing analysis results including:
            - exception_types: List of exception types found
            - error_locations: List of code locations that raise exceptions
            - type_errors: List of type checking issues from Mypy
            - files_analyzed: Number of Python files analyzed
        """
        logger.info(f"Starting analysis of {self.project_path}")
        
        # Extract exceptions from Python files
        extractor = ExceptionExtractor()
        python_files = self._find_python_files()
        
        for file_path in python_files:
            logger.debug(f"Analyzing {file_path}")
            extractor.extract_from_file(file_path)
        
        results: Dict[str, Any] = {
            "exception_types": sorted(list(extractor.exception_types)),
            "error_locations": extractor.error_locations,
            "type_errors": [],  # TODO: Implement Mypy integration
            "project_path": str(self.project_path),
            "files_analyzed": len(python_files),
        }
        
        logger.info(f"Analysis complete: {len(extractor.exception_types)} exception types, "
                   f"{len(extractor.error_locations)} locations, "
                   f"{len(python_files)} files")
        return results

    def _find_python_files(self) -> List[Path]:
        """
        Find all Python files in the project.

        Returns:
            List of paths to Python files
        """
        python_files = []
        
        if self.project_path.is_file() and self.project_path.suffix == ".py":
            # Single file
            python_files.append(self.project_path)
        elif self.project_path.is_dir():
            # Directory - recursively find Python files
            python_files = list(self.project_path.rglob("*.py"))
            # Filter out common directories to skip
            python_files = [
                f for f in python_files
                if not any(part.startswith(".") or part in ["__pycache__", "venv", "env", ".venv"]
                          for part in f.parts)
            ]
        
        return python_files


def analyze_project(project_path: str) -> Dict[str, Any]:
    """
    Analyze a Python project for error handling patterns.

    Args:
        project_path: Path to the Python project to analyze

    Returns:
        Dictionary containing analysis results

    Example:
        >>> results = analyze_project('/path/to/project')
        >>> print(results['exception_types'])
    """
    analyzer = ProjectAnalyzer(Path(project_path))
    return analyzer.analyze()
