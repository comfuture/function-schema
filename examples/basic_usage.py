"""
Basic usage example for function-schema library.

This example demonstrates how to:
1. Define a function with type annotations and Doc metadata
2. Generate a JSON schema from the function
3. Use enum for parameter constraints
"""

from typing import Annotated, Optional, Literal
from function_schema import Doc, get_function_schema
import enum
import json


def get_weather(
    city: Annotated[str, Doc("The city to get the weather for")],
    unit: Annotated[
        Optional[str],
        Doc("The unit to return the temperature in"),
        enum.Enum("Unit", "celcius fahrenheit")
    ] = "celcius",
) -> str:
    """Returns the weather for the given city."""
    return f"Weather for {city} is 20°C"


def get_animal_with_enum(
    animal: Annotated[str, Doc("The animal to get"), 
                     enum.Enum("AnimalType", "dog cat")],
) -> str:
    """Returns the animal using enum."""
    return f"Animal is {animal}"


class AnimalType(enum.Enum):
    dog = enum.auto()
    cat = enum.auto()


def get_animal_with_class_enum(
    animal: Annotated[str, Doc("The animal to get"), AnimalType],
) -> str:
    """Returns the animal using class-based enum."""
    return f"Animal is {animal.value}"


def get_animal_with_literal(
    animal: Annotated[Literal["dog", "cat"], Doc("The animal to get")],
) -> str:
    """Returns the animal using Literal type."""
    return f"Animal is {animal}"


def get_weather_with_string_annotation(
    city: Annotated[str, "The city to get the weather for"],
    unit: Annotated[Optional[str], "The unit to return the temperature in"] = "celcius",
) -> str:
    """Returns the weather for the given city using plain string annotations."""
    return f"Weather for {city} is 20°C"


if __name__ == "__main__":
    # Generate schema for the main weather function
    schema = get_function_schema(get_weather)
    print("Basic weather function schema:")
    print(json.dumps(schema, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # Generate schema for Claude format
    claude_schema = get_function_schema(get_weather, "claude")
    print("Schema for Claude:")
    print(json.dumps(claude_schema, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # Generate schema for enum example
    enum_schema = get_function_schema(get_animal_with_enum)
    print("Animal enum schema:")
    print(json.dumps(enum_schema, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # Generate schema for Literal example
    literal_schema = get_function_schema(get_animal_with_literal)
    print("Animal literal schema:")
    print(json.dumps(literal_schema, indent=2))