import enum
import typing
import inspect

def get_function_schema(
    func: typing.Annotated[typing.Callable, "The function to get the schema for"]
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
    >>> get_function_schema(get_weather)
    {
        "name": "get_weather",
        "description": "Returns the weather for the given city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get the weather for"
                },
                "unit": {
                    "type": "string",
                    "description": "The unit to return the temperature in",
                    "enum": ["celcius", "fahrenheit"],
                    "default": "celcius"
                }
            },
            "required": ["city"]
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
        is_annotated = len(param_args) > 1

        enum_ = None
        default_value = inspect._empty

        if is_annotated:
            # first arg is type
            (T, _) = param_args

            # find description in param_args tuple
            description = next(
                (arg for arg in param_args if isinstance(arg, str)),
                f"The {name} parameter",
            )

            # find enum in param_args tuple
            enum_ = next(
                (arg for arg in param_args if isinstance(arg, enum.Enum)), None
            )
        else:
            T = param.annotation
            description = f"The {name} parameter"

        # find default value for param
        if param.default is not inspect._empty:
            default_value = param.default

        schema["properties"][name] = {
            "type": guess_type(T),
            "description": description,  # type: ignore
        }

        if enum_ is not None:
            schema["properties"][name]["enum"] = enum_.values

        if default_value is not inspect._empty:
            schema["properties"][name]["default"] = default_value

        if not isinstance(None, T):
            schema["required"].append(name)
    return {
        "name": func.__qualname__,
        "description": inspect.getdoc(func),
        "parameters": schema,
    }


def guess_type(
    T: typing.Annotated[type, "The type to guess the JSON schema type for"]
) -> typing.Annotated[
    typing.Union[str, list[str]], "str | list of str that representing JSON schema type"
]:
    """Guesses the JSON schema type for the given python type."""
    _types = []

    # hacking around typing modules, `typing.Union` and `types.UnitonType`
    if isinstance(1, T):
        _types.append("integer")
    elif isinstance(1.1, T):
        _types.append("number")

    if isinstance("", T):
        _types.append("string")
    if not isinstance(1, T) and isinstance(True, T):
        _types.append("boolean")
    if isinstance([], T):
        _types.append("array")
    if isinstance({}, T):
        return "object"

    if len(_types) == 0:
        return "object"

    if len(_types) == 1:
        return _types[0]

    return _types
