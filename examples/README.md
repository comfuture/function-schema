# Function Schema Examples

This directory contains practical examples of how to use the `function-schema` library with various AI platforms and protocols.

## Examples

### 🔧 Basic Usage (`basic_usage.py`)
Demonstrates the fundamental features of function-schema:
- Creating functions with type annotations and Doc metadata
- Generating JSON schemas
- Using enums and Literal types for parameter constraints
- Different annotation styles

**Run:** `python examples/basic_usage.py`

### 🤖 OpenAI Integration (`openai_example.py`)
Shows how to integrate with OpenAI's APIs:
- Assistant API with tool calling
- Chat Completion API with function calling
- Multiple tool definitions

**Run:** `python examples/openai_example.py`

### 🧠 Claude Integration (`claude_example.py`)
Demonstrates Anthropic Claude tool calling:
- Basic tool calling setup
- Multi-turn conversations with tools
- Claude-specific schema format

**Run:** `python examples/claude_example.py`

### 📟 CLI Usage (`cli_example.py`)
Examples of using the command-line interface:
- Generating schemas from Python files
- Different output formats
- Working with multiple functions

**Test the CLI:**
```bash
# Install the package first
pip install -e .

# Generate schema for a function
function_schema examples/cli_example.py get_weather

# Generate with pretty JSON formatting
function_schema examples/cli_example.py get_weather | jq

# Generate for Claude format
function_schema examples/cli_example.py get_weather claude
```

### 🔌 MCP Integration (`mcp_example.py`)
Shows integration with Model Context Protocol:
- Creating MCP-compatible tool definitions
- Server manifest generation
- Tool calling examples
- Resource access patterns

**Run:** `python examples/mcp_example.py`

## Running the Examples

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Run any example:**
   ```bash
   python examples/basic_usage.py
   python examples/openai_example.py
   python examples/claude_example.py
   python examples/mcp_example.py
   ```

3. **Test CLI functionality:**
   ```bash
   function_schema examples/cli_example.py get_weather
   ```

## Integration Notes

- **OpenAI**: Requires `openai` library and API key for actual usage
- **Claude**: Requires `anthropic` library and API key for actual usage  
- **MCP**: Conceptual example showing schema compatibility
- **CLI**: Works out of the box with the installed package

## Schema Formats

The library supports multiple output formats:
- **OpenAI format** (default): Uses `parameters` key
- **Claude format**: Uses `input_schema` key

Specify format with: `get_function_schema(func, "claude")`