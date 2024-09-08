import enum
import typing
import inspect
import platform
import packaging.version

current_version = packaging.version.parse(platform.python_version())
py_310 = packaging.version.parse("3.10")

if current_version >= py_310:
    from types import UnionType
else:
    UnionType = typing.Union  # type: ignore

try:
    from typing import Doc
except ImportError:
    try:
        from typing_extensions import Doc
    except ImportError:
        class Doc:
            def __init__(self, documentation: str, /):
                self.documentation = documentation

__all__ = ("get_function_schema", "guess_type", "Doc")

def is_doc_meta(obj):
    """
    Check if the given object is a documentation object.
    Parameters:
        obj (object): The object to be checked.
    Returns:
        bool: True if the object is a documentation object, False otherwise.

    Example:
    >>> is_doc_meta(Doc("This is a documentation object"))
    True
    """
    return getattr(obj, '__class__') == Doc and hasattr(obj, 'documentation')

def unwrap_doc(obj: typing.Union[Doc, str]):
    """
    Get the documentation string from the given object.
    Parameters:
        obj (Doc | str): The object to get the documentation string from.
    Returns:
        str: The documentation string.

    Example:
    >>> unwrap_doc(Doc("This is a documentation object"))
    'This is a documentation object'
    >>> unwrap_doc("This is a documentation string")
    'This is a documentation string'
    """
    if is_doc_meta(obj):
        return obj.documentation
    return str(obj)


def get_function_schema(
    func: typing.Annotated[typing.Callable, "The function to get the schema for"],
    format: typing.Annotated[
        typing.Optional[typing.Literal["openai", "claude"]],
        "The format of the schema to return",
    ] = "openai",
) -> typing.Annotated[dict[str, typing.Any], "The JSON schema for the given function"]:
    """
    Returns a JSON schema for the given function.

    You can annotate your function parameters with the special Annotated type.
    Then get the schema for the function without writing the schema by hand.

    Especially useful for OpenAI API function-call.

    Example:
    >>> from typing import Annotated, Optional
    >>> import enum
    >>> def get_weather(
    ...     city: Annotated[str, "The city to get the weather for"],
    ...     unit: Annotated[
    ...         Optional[str],
    ...         "The unit to return the temperature in",
    ...         enum.Enum("Unit", "celcius fahrenheit")
    ...     ] = "celcius",
    ... ) -> str:
    ...     \"\"\"Returns the weather for the given city.\"\"\"
    ...     return f"Hello {name}, you are {age} years old."
    >>> get_function_schema(get_weather) # doctest: +SKIP
    {
        'name': 'get_weather',
        'description': 'Returns the weather for the given city.',
        'parameters': {
            'type': 'object',
            'properties': {
                'city': {
                    'type': 'string',
                    'description': 'The city to get the weather for'
                },
                'unit': {
                    'type': 'string',
                    'description': 'The unit to return the temperature in',
                    'enum': ['celcius', 'fahrenheit'],
                    'default': 'celcius'
                }
            },
            'required': ['city']
        }
    }
    """
    sig = inspect.signature(func)
    params = sig.parameters
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    for name, param in params.items():
        param_args = typing.get_args(param.annotation)
        is_annotated = typing.get_origin(param.annotation) is typing.Annotated

        enum_ = None
        default_value = inspect._empty

        if is_annotated:
            # first arg is type
            (T, *_) = param_args

            # find description in param_args tuple
            description = next(
                (unwrap_doc(arg) for arg in param_args if isinstance(arg, (Doc, str))),
                f"The {name} parameter",
            )

            # find enum in param_args tuple
            enum_ = next(
                (
                    [e.name for e in arg]
                    for arg in param_args
                    if isinstance(arg, type) and issubclass(arg, enum.Enum)
                ),
                # use typing.Literal as enum if no enum found
                typing.get_origin(T) is typing.Literal and typing.get_args(T) or None,
            )
        else:
            T = param.annotation
            description = f"The {name} parameter"
            if typing.get_origin(T) is typing.Literal:
                enum_ = typing.get_args(T)

        # find default value for param
        if param.default is not inspect._empty:
            default_value = param.default

        schema["properties"][name] = {
            "type": guess_type(T),
            "description": description,  # type: ignore
        }

        if enum_ is not None:
            schema["properties"][name]["enum"] = [t for t in enum_ if t is not None]

        if default_value is not inspect._empty:
            schema["properties"][name]["default"] = default_value

        if (
            typing.get_origin(T) is not typing.Literal
            and not isinstance(None, T)
            and default_value is inspect._empty
        ):
            schema["required"].append(name)

        if typing.get_origin(T) is typing.Literal:
            if all(typing.get_args(T)):
                schema["required"].append(name)

    parms_key = "input_schema" if format == "claude" else "parameters"

    schema["required"] = list(set(schema["required"]))

    return {
        "name": func.__name__,
        "description": inspect.getdoc(func),
        parms_key: schema,
    }


def guess_type(
    T: typing.Annotated[type, "The type to guess the JSON schema type for"],
) -> typing.Annotated[
    typing.Union[str, list[str]], "str | list of str that representing JSON schema type"
]:
    """Guesses the JSON schema type for the given python type."""

    # special case
    if T is typing.Any:
        return {}

    origin = typing.get_origin(T)

    if origin is typing.Annotated:
        return guess_type(typing.get_args(T)[0])

    # hacking around typing modules, `typing.Union` and `types.UnitonType`
    if origin in [typing.Union, UnionType]:
        union_types = [t for t in typing.get_args(T) if t is not type(None)]
        _types = [
            guess_type(union_type)
            for union_type in union_types
            if guess_type(union_type) is not None
        ]

        # number contains integer in JSON schema
        # deduplicate
        _types = list(set(_types))

        if len(_types) == 1:
            return _types[0]
        return _types

    if origin is typing.Literal:
        type_args = typing.Union[tuple(type(arg) for arg in typing.get_args(T))]
        return guess_type(type_args)
    elif origin is list or origin is tuple:
        return "array"
    elif origin is dict:
        return "object"

    if not isinstance(T, type):
        return

    if T.__name__ == "NoneType":
        return

    if issubclass(T, str):
        return "string"
    if issubclass(T, bool):
        return "boolean"
    if issubclass(T, (float, int)):
        return "number"
    # elif issubclass(T, int):
    #     return "integer"
    if T.__name__ == "list":
        return "array"
    if T.__name__ == "dict":
        return "object"
