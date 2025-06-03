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

See the [examples directory](./examples/) for comprehensive usage examples with different AI platforms:

- **[Basic Usage](./examples/basic_usage.py)** - Core features and function definition patterns
- **[OpenAI Integration](./examples/openai_example.py)** - Assistant API and Chat Completion examples  
- **[Claude Integration](./examples/claude_example.py)** - Anthropic Claude tool calling examples
- **[MCP Integration](./examples/mcp_example.py)** - Model Context Protocol examples
- **[CLI Usage](./examples/cli_example.py)** - Command-line interface examples

### Quick Start

```python
from typing import Annotated
from function_schema import Doc, get_function_schema

def get_weather(city: Annotated[str, Doc("The city to get the weather for")]) -> str:
    """Returns the weather for the given city."""
    return f"Weather for {city} is 20°C"

# Generate schema
schema = get_function_schema(get_weather)
```

### Key Features

- **Type Annotations**: Use `typing.Annotated` with `Doc` metadata for parameter descriptions
- **Multiple Formats**: Support for OpenAI (`"openai"`) and Claude (`"claude"`) schema formats
- **Enum Support**: Use `enum.Enum` or `typing.Literal` for parameter constraints
- **CLI Tool**: Generate schemas from command line using `function_schema`

For detailed examples and advanced usage patterns, see the [examples directory](./examples/).

### Platform Integration

#### OpenAI API
For detailed OpenAI integration examples including Assistant API and Chat Completion, see [examples/openai_example.py](./examples/openai_example.py).

#### Anthropic Claude
For Claude tool calling examples and multi-turn conversations, see [examples/claude_example.py](./examples/claude_example.py).

#### Model Context Protocol (MCP)
For MCP server and tool integration examples, see [examples/mcp_example.py](./examples/mcp_example.py).

#### CLI Usage
Generate schemas from command line:
```bash
function_schema examples/cli_example.py get_weather | jq
```
For more CLI examples, see [examples/cli_example.py](./examples/cli_example.py).

## License
MIT License
