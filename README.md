# Function schema

[![CI](https://github.com/comfuture/function-schema/actions/workflows/ci.yml/badge.svg)](https://github.com/comfuture/function-schema/actions/workflows/ci.yml)
[![Release](https://github.com/comfuture/function-schema/actions/workflows/python-publish.yml/badge.svg)](https://github.com/comfuture/function-schema/actions/workflows/python-publish.yml)
[![PyPI version](https://badge.fury.io/py/function-schema.svg)](https://badge.fury.io/py/function-schema)

This is a small utility to generate JSON schemas for python functions.
With power of type annotations, it is possible to generate a schema for a function without describing it twice.

At this moment, extracting schema from a function is useful for [OpenAI Assistant Toll Calling](https://platform.openai.com/docs/assistants/tools/function-calling), [OpenAI API function-call](https://platform.openai.com/docs/guides/function-calling), and [Anthropic Claude Toll calling](https://docs.anthropic.com/claude/docs/tool-use) feature.
And it can be used for other purposes for example to generate documentation in the future.

## Installation

```sh
pip install function-schema
```

## Usage

```python
from typing import Annotated, Optional
import enum

def get_weather(
    city: Annotated[str, "The city to get the weather for"],
    unit: Annotated[
        Optional[str],
        "The unit to return the temperature in",
        enum.Enum("Unit", "celcius fahrenheit")
    ] = "celcius",
) -> str:
    """Returns the weather for the given city."""
    return f"Weather for {city} is 20°C"
```

Function description is taken from the docstring.
Type hinting with `typing.Annotated` for annotate additional information about the parameters and return type.

- type can be `typing.Union`, `typing.Optional`. (`T | None` for python 3.10+)
- string value of `Annotated` is used as a description
- enum value of `Annotated` is used as an enum schema

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

for claude, you should pass 2nd argument as SchemaFormat.claude or `claude`:

```python
from function_schema import get_function_schema

schema = get_function_schema(get_weather, "claude")
```

Please refer to the [Claude tool use](https://docs.anthropic.com/claude/docs/tool-use) documentation for more information.

You can use this schema to make a function call in OpenAI API:
```python
import openai
openai.api_key = "sk-..."

# Create an assistant with the function
assistant = client.beta.assistants.create(
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    model="gpt-4-turbo-preview",
    tools=[{
        "type": "function",
        "function": get_function_schema(get_weather),
    }]
)

run = client.beta.messages.create(
    assistant_id=assistant.id,
    messages=[
        {"role": "user", "content": "What's the weather like in Seoul?"}
    ]
)

# or with chat completion

result = openai.chat.completion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "What's the weather like in Seoul?"}
    ],
    tools=[get_function_schema(get_weather)],
    tool_call="auto",
)
```

In claude api,

```python
import anthropic

client = anthropic.Client()

response = client.beta.tools.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4096,
    tools=[get_function_schema(get_weather, "claude")],
    messages=[
        {"role": "user", "content": "What's the weather like in Seoul?"}
    ]
)
```

### CLI usage

```sh
function_schema mymodule.py my_function
```

## License
MIT License