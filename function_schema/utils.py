from typing import Annotated, Any, Union
from .types import Doc


def is_support_uniontype():
    """Check if current python version supports UnionType or not"""
    try:
        from types import UnionType  # noqa
    except ImportError:
        return False
    return True


def is_doc_meta(
    obj: Annotated[Any, Doc("The object to be checked.")],
) -> Annotated[
    bool, Doc("True if the object is a documentation object, False otherwise.")
]:
    """
    Check if the given object is a documentation object.

    Example:
    >>> is_doc_meta(Doc("This is a documentation object"))
    True
    """
    return getattr(obj, "__class__") == Doc and hasattr(obj, "documentation")


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
    if is_doc_meta(obj):
        return obj.documentation
    return str(obj)
