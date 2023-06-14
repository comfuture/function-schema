"""
A small utility to generate JSON schemas for python functions.
"""
from .core import get_function_schema

__version__ = "0.1.0"
__all__ = (
    "get_function_schema",
    "__version__",
)
