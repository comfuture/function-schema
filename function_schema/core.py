import enum
import typing
import inspect


class SchemaFormat(str, enum.Enum):
    openai = "openai"
    claude = "claude"


def get_function_schema(
    func: typing.Annotated[typing.Callable, "The function to get the schema for"],
    format: typing.Annotated[
        typing.Optional[str], SchemaFormat, "The format of the schema to return"
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
        is_annotated = len(param_args) > 1

        enum_ = None
        default_value = inspect._empty

        if is_annotated:
            # first arg is type
            (T, *_) = param_args

            # find description in param_args tuple
            description = next(
                (arg for arg in param_args if isinstance(arg, str)),
                f"The {name} parameter",
            )

            # find enum in param_args tuple
            enum_ = next(
                (
                    arg
                    for arg in param_args
                    if isinstance(arg, type) and issubclass(arg, enum.Enum)
                ),
                None,
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
            schema["properties"][name]["enum"] = [t.name for t in enum_]

        if default_value is not inspect._empty:
            schema["properties"][name]["default"] = default_value

        if not isinstance(None, T) and default_value is inspect._empty:
            schema["required"].append(name)

    parms_key = "input_schema" if format == "claude" else "parameters"

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

    # hacking around typing modules, `typing.Union` and `types.UnitonType`
    union_types = typing.get_args(T)
    if len(union_types) > 1:
        _types = []
        for union_type in union_types:
            _types.append(guess_type(union_type))
        _types = [t for t in _types if t is not None]  # exclude None

        # number contains integer in JSON schema
        if "number" in _types and "integer" in _types:
            _types.remove("integer")

        if len(_types) == 1:
            return _types[0]
        return _types

    if not isinstance(T, type):
        return

    if T.__name__ == "NoneType":
        return

    if issubclass(T, str):
        return "string"
    if issubclass(T, bool):
        return "boolean"
    if issubclass(T, float):
        return "number"
    elif issubclass(T, int):
        return "integer"
    if T.__name__ == "list":
        return "array"
    if T.__name__ == "dict":
        return "object"
