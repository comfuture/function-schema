import typing

import pytest

from function_schema.core import guess_type
from function_schema.utils import is_py310_atleast


def test_primitive():
    """Test primitive types"""
    assert guess_type(int) == "number"
    assert guess_type(str) == "string"
    assert guess_type(float) == "number"
    assert guess_type(bool) == "boolean"


def test_typings():
    """Test typing module types"""
    assert guess_type(typing.Any) == {}
    assert guess_type(typing.List) == "array"
    assert guess_type(typing.Dict) == "object"
    assert guess_type(typing.Tuple) == "array"

    assert guess_type(typing.List[int]) == "array"
    assert guess_type(typing.List[str]) == "array"
    assert guess_type(typing.List[float]) == "array"
    assert guess_type(typing.List[bool]) == "array"

    assert guess_type(typing.Dict[str, int]) == "object"
    assert guess_type(typing.Dict[str, str]) == "object"


def test_optional():
    """Test optional types"""
    assert guess_type(typing.Optional[int]) == "number"
    assert guess_type(typing.Optional[str]) == "string"
    assert guess_type(typing.Optional[float]) == "number"
    assert guess_type(typing.Optional[bool]) == "boolean"


def test_union_null():
    """Test union types with null"""
    assert guess_type(typing.Union[int, None]) == "number"
    assert guess_type(typing.Union[str, None]) == "string"
    assert guess_type(typing.Union[float, None]) == "number"
    assert guess_type(typing.Union[bool, None]) == "boolean"


def test_union():
    """Test union types"""
    assert set(guess_type(typing.Union[int, str])) == {"number", "string"}
    assert guess_type(typing.Union[int, float]) == "number"
    assert set(guess_type(typing.Union[int, bool])) == {"number", "boolean"}
    assert set(guess_type(typing.Union[bool, int])) == {"boolean", "number"}
    assert set(guess_type(typing.Union[str, float])) == {"string", "number"}
    assert set(guess_type(typing.Union[str, bool])) == {"string", "boolean"}
    assert set(guess_type(typing.Union[float, bool])) == {"number", "boolean"}
    assert set(guess_type(typing.Union[str, float, bool])) == {
        "string",
        "number",
        "boolean",
    }
    assert set(guess_type(typing.Union[str, float, bool, None])) == {
        "string",
        "number",
        "boolean",
    }


@pytest.mark.skipif(
    not is_py310_atleast(), reason="Union type is only available in Python 3.10+"
)
def test_union_type():
    """Test union types in Python 3.10+"""

    assert set(guess_type(int | str)) == {"number", "string"}
    assert guess_type(int | float) == "number"
    assert set(guess_type(int | bool)) == {"number", "boolean"}
    assert set(guess_type(str | float)) == {"string", "number"}
    assert set(guess_type(str | bool)) == {"string", "boolean"}
    assert set(guess_type(float | bool)) == {"number", "boolean"}
    assert set(guess_type(str | float | bool)) == {
        "string",
        "number",
        "boolean",
    }
    assert set(guess_type(str | float | bool | None)) == {
        "string",
        "number",
        "boolean",
    }


def test_literal_type():
    """Test literal type"""
    assert guess_type(typing.Literal["a"]) == "string", "should be string"
    assert guess_type(typing.Literal[1]) == "number", "should be number"
    assert guess_type(typing.Literal[1.0]) == "number", "should be number"

    assert set(guess_type(typing.Literal["a", 1, None])) == {
        "string",
        "number",
    }, "should be string or integer, omit None"

    assert set(guess_type(typing.Literal["a", 1])) == {"string", "number"}
    assert set(guess_type(typing.Literal["a", 1.0])) == {"string", "number"}
    assert set(guess_type(typing.Literal["a", 1.1])) == {"string", "number"}
    assert set(guess_type(typing.Literal["a", 1, 1.0])) == {
        "string",
        "number",
    }, "should omit integer if number is present"

    assert set(guess_type(typing.Literal["a", 1, 1.0, None])) == {"string", "number"}
