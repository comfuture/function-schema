"""
A small utility to generate JSON schemas for python functions.
"""
from .core import get_function_schema, guess_type, Doc, Annotated

__version__ = "0.4.5"
__all__ = (
    "__version__",
    "get_function_schema",
    "guess_type",
    "Doc",
    "Annotated",
)
