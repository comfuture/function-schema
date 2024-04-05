from typing import Annotated
import enum
from function_schema.core import get_function_schema


def test_function_schema_type():
    """Test a function schema for claude"""

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
    assert (
        schema["parameters"]["properties"]["animal"]["type"] == "string"
    ), "parameter animal should be a string"
    assert schema["parameters"]["properties"]["animal"]["enum"] == [
        "Cat",
        "Dog",
    ], "parameter animal should have an enum"

    schema2 = get_function_schema(func1, format="claude")
    assert (
        schema2["input_schema"]["properties"]["animal"]["type"] == "string"
    ), "parameter animal should be a string"
    assert schema2["input_schema"]["properties"]["animal"]["enum"] == [
        "Cat",
        "Dog",
    ], "parameter animal should have an enum"
