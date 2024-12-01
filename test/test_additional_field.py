from typing import Annotated, Optional
from function_schema.core import get_function_schema, FieldInfo


def test_fieldinfo_type():
    """Test if FieldInfo type overrides the guessed type"""
    def func(a: Annotated[int, FieldInfo(type="integer")]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["type"] == "integer"


def test_fieldinfo_description():
    """Test if FieldInfo description is added to the schema"""
    def func(a: Annotated[int, FieldInfo(description="An integer parameter")]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["description"] == "An integer parameter"


def test_fieldinfo_enum():
    """Test if FieldInfo enum is added to the schema"""
    def func(a: Annotated[str, FieldInfo(enum=["red", "green", "blue"])]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["enum"] == [
        "red", "green", "blue"]


def test_fieldinfo_required():
    """Test if FieldInfo required is added to the schema"""
    def func(a: Annotated[Optional[int], FieldInfo(required=True)]):
        ...

    schema = get_function_schema(func)
    assert "required" in schema["parameters"]
    assert "a" in schema["parameters"]["required"]


def test_fieldinfo_min_max():
    def func(a: Annotated[int, FieldInfo(minimum=1, maximum=100)]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["minimum"] == 1
    assert schema["parameters"]["properties"]["a"]["maximum"] == 100


def test_fieldinfo_exclusive_min_max():
    def func(a: Annotated[int, FieldInfo(exclusive_minimum=0, exclusive_maximum=10)]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["exclusiveMinimum"] == 0
    assert schema["parameters"]["properties"]["a"]["exclusiveMaximum"] == 10


def test_fieldinfo_length():
    def func(a: Annotated[str, FieldInfo(min_length=5, max_length=10)]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["minLength"] == 5
    assert schema["parameters"]["properties"]["a"]["maxLength"] == 10


def test_fieldinfo_pattern():
    def func(a: Annotated[str, FieldInfo(pattern="^[a-zA-Z0-9]+$")]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["pattern"] == "^[a-zA-Z0-9]+$"


def test_more_than_one_fieldinfo():
    def func(a: Annotated[int, FieldInfo(minimum=1, maximum=100), FieldInfo(pattern="^[0-9]+$")]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["minimum"] == 1
    assert schema["parameters"]["properties"]["a"]["maximum"] == 100
    assert schema["parameters"]["properties"]["a"]["pattern"] == "^[0-9]+$"


def test_fieldinfo_expression():
    def func(a: Annotated[int, FieldInfo() >= 1]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["minimum"] == 1


def test_fieldinfo_expression_chain():
    F = FieldInfo()

    def func(a: Annotated[int, 1 <= F < 2]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["minimum"] == 1
    assert schema["parameters"]["properties"]["a"]["exclusiveMaximum"] == 2


def test_fieldinfo_expression_combo():
    def func(a: Annotated[int, 1 <= FieldInfo(description="The number") <= 42]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["minimum"] == 1
    assert schema["parameters"]["properties"]["a"]["maximum"] == 42
    assert schema["parameters"]["properties"]["a"]["description"] == "The number"


def test_dict_as_additional_field():
    def func(a: Annotated[int, {"minimum": 10}]):
        ...

    schema = get_function_schema(func)
    assert schema["parameters"]["properties"]["a"]["minimum"] == 10
