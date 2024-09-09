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

for claude, you should pass 2nd argument as SchemaFormat.claude or `claude`:

```python
from function_schema import get_function_schema

schema = get_function_schema(get_weather, "claude")
```

Please refer to the [Claude tool use](https://docs.anthropic.com/claude/docs/tool-use) documentation for more information.

You can use any type hinting supported by python for the first argument of `Annotated`. including:
`typing.Literal`, `typing.Optional`, `typing.Union`, and `T | None` for python 3.10+.  
`Doc` class or plain string in `Annotated` is used for describe the parameter.
`Doc` metadata is the [PEP propose](https://peps.python.org/pep-0727/) for standardizing the metadata in type hints.
currently, implemented in `typing-extensions` module. Also `function_schema.Doc` is provided for compatibility.

Enumeratable candidates can be defined with `enum.Enum` in the argument of `Annotated`.

```python
import enum

class AnimalType(enum.Enum):
    dog = enum.auto()
    cat = enum.auto()

def get_animal(
    animal: Annotated[str, Doc("The animal to get"), AnimalType],
) -> str:
    """Returns the animal."""
    return f"Animal is {animal.value}"
```
In this example, each name of `AnimalType` enums(`dog`, `cat`) is used as an enum schema.
In shorthand, you can use `typing.Literal` as the type will do the same thing.

```python
def get_animal(
    animal: Annotated[Literal["dog", "cat"], Doc("The animal to get")],
) -> str:
    """Returns the animal."""
    return f"Animal is {animal}"
```


### Plain String in Annotated

The string value of `Annotated` is used as a description for convenience.

```python
def get_weather(
    city: Annotated[str, "The city to get the weather for"], # <- string value of Annotated is used as a description
    unit: Annotated[Optional[str], "The unit to return the temperature in"] = "celcius",
) -> str:
    """Returns the weather for the given city."""
    return f"Weather for {city} is 20°C"
```

But this would create a predefined meaning for any plain string inside of `Annotated`,
and any tool that was using plain strings in them for any other purpose, which is currently allowed, would now be invalid.
Please refer to the [PEP 0727, Plain String in Annotated](https://peps.python.org/pep-0727/#plain-string-in-annotated) for more information.

### Usage with OpenAI API

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
    tools=[{
      "type": "function",
      "function": get_function_schema(get_weather)
    }],
    tool_call="auto",
)
```

### Usage with Anthropic Claude

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
function_schema mymodule.py my_function | jq
```

## License
MIT License
