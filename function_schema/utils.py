from typing import Annotated, Union
from .types import Doc


def is_support_uniontype():
    """Check if current python version supports UnionType or not"""
    try:
        from types import UnionType  # noqa
    except ImportError:
        return False
    return True


def unwrap_doc(
    obj: Annotated[
        Union[Doc, str], Doc(
            "The object to get the documentation string from.")
    ],
) -> Annotated[str, Doc("The documentation string.")]:
    """
    Get the documentation string from the given object.

    Example:
    >>> unwrap_doc(Doc("This is a documentation object"))
    'This is a documentation object'
    >>> unwrap_doc("This is a documentation string")
    'This is a documentation string'
    """
    if isinstance(obj, Doc):
        return obj.documentation
    return str(obj)
