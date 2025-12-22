"""
Perihelion Signal Processor (PeSPr)

A Python package for automating error handling and logging configuration
by integrating static and dynamic analysis with tools like DynEL.
"""

__version__ = "0.1.0"
__author__ = "Tyler Zervas"

from pespr.analyze import analyze_project
from pespr.config_generator import generate_config

__all__ = [
    "analyze_project",
    "generate_config",
    "__version__",
]
