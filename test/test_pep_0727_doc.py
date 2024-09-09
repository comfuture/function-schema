from typing import Annotated
from enum import Enum
from function_schema.core import get_function_schema, Doc


def test_docs_in_annotation():
    """Test a function with annotations with Doc"""
    def func1(a: Annotated[int, Doc("An integer parameter")]):
        """My function"""
        ...

    schema = get_function_schema(func1)
    assert schema["name"] == "func1", "Function name should be func1"
    assert schema["description"] == "My function", "Function description should be there"
    assert schema["parameters"]["properties"]["a"]["type"] == "number", "parameter a should be an integer"
    assert schema["parameters"]["properties"]["a"]["description"] == "An integer parameter", "parameter a should have a description"
    assert schema["parameters"]["required"] == [
        "a"], "parameter a should be required"


def test_doc_in_nth_args():
    """Test a function with annotations with Doc in nth args"""
    def func1(a: Annotated[str, Enum("Candidates", "a b c"), Doc("A string parameter")]):
        """My function"""
        ...

    schema = get_function_schema(func1)
    assert schema["name"] == "func1", "Function name should be func1"
    assert schema["description"] == "My function", "Function description should be there"
    assert schema["parameters"]["properties"]["a"]["type"] == "string", "parameter a should be an string"
    assert schema["parameters"]["properties"]["a"]["description"] == "A string parameter", "parameter a should have a description"
    assert schema["parameters"]["properties"]["a"]["enum"] == [
        "a", "b", "c"], "parameter a should have enum values"


def test_multiple_docs_in_annotation():
    """Test a function with annotations with multiple Doc"""
    def func1(a: Annotated[int, Doc("An integer parameter"), Doc("A number")]):
        """My function"""
        ...

    schema = get_function_schema(func1)
    assert schema["name"] == "func1", "Function name should be func1"
    assert schema["description"] == "My function", "Function description should be there"
    assert schema["parameters"]["properties"]["a"]["type"] == "number", "parameter a should be an integer"
    assert schema["parameters"]["properties"]["a"]["description"] == "An integer parameter", "first description should be used"


def test_mixed_docs_in_annotation():
    """Test a function with annotations with mixed Doc and strings"""
    def func1(a: Annotated[int, "An integer parameter", Doc("A number")]):
        """My function"""
        ...

    schema = get_function_schema(func1)
    assert schema["name"] == "func1", "Function name should be func1"
    assert schema["description"] == "My function", "Function description should be there"
    assert schema["parameters"]["properties"]["a"]["type"] == "number", "parameter a should be an integer"
    assert schema["parameters"]["properties"]["a"]["description"] == "A number", "`Doc` should be used rather than string"
