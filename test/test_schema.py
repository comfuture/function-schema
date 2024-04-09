import enum
from typing import Annotated, Literal
from function_schema.core import get_function_schema


def test_simple_function():
    """Test a simple function"""

    def func1():
        """My function"""
        ...

    schema = get_function_schema(func1)

    assert schema["name"] == "func1", "Function name should be func1"
    assert (
        schema["description"] == "My function"
    ), "Function description should be My function"
    assert (
        schema["parameters"]["properties"] == {}
    ), "Function parameters should be empty"
    assert schema["parameters"]["required"] == [], "required parameters should be empty"


def test_function_with_args():
    """Test a function with args"""

    def func1(a: int, b: str, c: float = 1.0):
        """My function"""
        ...

    schema = get_function_schema(func1)

    assert schema["name"] == "func1", "Function name should be func1"
    assert (
        schema["description"] == "My function"
    ), "Function description should be there"
    assert (
        schema["parameters"]["properties"]["a"]["type"] == "integer"
    ), "parameter a should be an integer"
    assert (
        schema["parameters"]["properties"]["b"]["type"] == "string"
    ), "parameter b should be a string"
    assert (
        schema["parameters"]["properties"]["c"]["type"] == "number"
    ), "parameter c should be a number"
    assert (
        schema["parameters"]["properties"]["c"]["default"] == 1.0
    ), "c should have a default value of 1.0"
    assert schema["parameters"]["required"] == [
        "a",
        "b",
    ], "parameters with no default value should be required"


def test_annotated_function():
    """Test a function with annotations"""

    def func1(
        a: Annotated[int, "An integer parameter"],
        b: Annotated[str, "A string parameter"],
    ):
        """My function"""
        ...

    schema = get_function_schema(func1)

    assert (
        schema["parameters"]["properties"]["a"]["type"] == "integer"
    ), "parameter a should be an integer"
    assert (
        schema["parameters"]["properties"]["a"]["description"] == "An integer parameter"
    ), "parameter a should have a description"
    assert (
        schema["parameters"]["properties"]["b"]["type"] == "string"
    ), "parameter b should be a string"
    assert (
        schema["parameters"]["properties"]["b"]["description"] == "A string parameter"
    ), "parameter b should have a description"

    assert schema["parameters"]["required"] == [
        "a",
        "b",
    ], "parameters with no default value should be required"


def test_annotated_function_with_enum():
    """Test a function with annotations and enum"""

    def func1(
        animal: Annotated[
            str,
            "The animal you want to pet",
            enum.Enum("Animal", "Cat Dog"),
        ],
    ):
        """My function"""
        ...

    schema = get_function_schema(func1)
    print(schema)
    assert (
        schema["parameters"]["properties"]["animal"]["type"] == "string"
    ), "parameter animal should be a string"
    assert schema["parameters"]["properties"]["animal"]["enum"] == [
        "Cat",
        "Dog",
    ], "parameter animal should have an enum"


def test_literal_type():
    """Test literal type"""

    def func1(animal: Annotated[Literal["Cat", "Dog"], "The animal you want to pet"]):
        """My function"""
        ...

    schema = get_function_schema(func1)
    print(schema)
    assert (
        schema["parameters"]["properties"]["animal"]["type"] == "string"
    ), "parameter animal should be a string"
    assert schema["parameters"]["properties"]["animal"]["enum"] == [
        "Cat",
        "Dog",
    ], "parameter animal should have an enum"

    def func2(animal: Literal["Cat", "Dog"]):
        """My function"""
        ...

    schema = get_function_schema(func2)
    assert (
        schema["parameters"]["properties"]["animal"]["type"] == "string"
    ), "parameter animal should be a string"

    assert schema["parameters"]["properties"]["animal"]["enum"] == [
        "Cat",
        "Dog",
    ], "parameter animal should have an enum"
