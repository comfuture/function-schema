# Function schema

[![CI](https://github.com/comfuture/function-schema/actions/workflows/ci.yml/badge.svg)](https://github.com/comfuture/function-schema/actions/workflows/ci.yml)
[![Release](https://github.com/comfuture/function-schema/actions/workflows/python-publish.yml/badge.svg)](https://github.com/comfuture/function-schema/actions/workflows/python-publish.yml)
[![PyPI version](https://badge.fury.io/py/function-schema.svg)](https://badge.fury.io/py/function-schema)

This is a small utility to generate JSON schemas for python functions.
With power of type annotations, it is possible to generate a schema for a function without describing it twice.

At this moment, extracting schema from a function is useful for [OpenAI Assistant Tool Calling](https://platform.openai.com/docs/assistants/tools/function-calling), [OpenAI API function-call](https://platform.openai.com/docs/guides/function-calling), and [Anthropic Claude Tool calling](https://docs.anthropic.com/claude/docs/tool-use) feature.
And it can be used for other purposes for example to generate documentation in the future.

## Installation

```sh
pip install function-schema
```

## Usage

```python
from typing import Annotated, Optional
from function_schema import Doc
import enum

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
```

Function description is taken from the docstring.
Type hinting with `typing.Annotated` for annotate additional information about the parameters and return type.

Then you can generate a schema for this function:
```python
import json
from function_schema import get_function_schema

schema = get_function_schema(get_weather)
print(json.dumps(schema, indent=2))
```

Will output:

```json
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
        "enum": [
          "celcius",
          "fahrenheit"
        ],
        "default": "celcius"
      }
    },
  }
  "required": [
    "city"
  ]
}
```

For claude, you should pass 2nd argument as SchemaFormat.claude or `claude`:

```python
from function_schema import get_function_schema

schema = get_function_schema(get_weather, "claude")
```

Please refer to the [Claude tool use](https://docs.anthropic.com/claude/docs/tool-use) documentation for more information.

You can use any type hinting supported by python for the first argument of `Annotated`. including:
`typing.Literal`, `typing.Optional`, `typing.Union`, and `T | None` for python 3.10+.  
`Doc` class or plain string in `Annotated` is used for describe the parameter.

Enumeratable candidates can be defined with `enum.Enum` in the argument of `Annotated`.
In shorthand, you can use `typing.Literal` as the type will do the same thing:

```python
from typing import Annotated, Literal

def get_animal(
    animal: Annotated[Literal["dog", "cat"], Doc("The animal to get")],
) -> str:
    """Returns the animal."""
    return f"Animal is {animal}"
```

### CLI usage

```sh
function_schema mymodule.py my_function | jq
```

### More Examples

For comprehensive usage examples with different AI platforms, see the [examples directory](./examples/):

- **[Basic Usage](./examples/basic_usage.py)** - Core features and function definition patterns
- **[OpenAI Integration](./examples/openai_example.py)** - Assistant API and Chat Completion examples  
- **[Claude Integration](./examples/claude_example.py)** - Anthropic Claude tool calling examples
- **[MCP Integration](./examples/mcp_example.py)** - Model Context Protocol examples
- **[CLI Usage](./examples/cli_example.py)** - Command-line interface examples

## License
MIT License
