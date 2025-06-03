"""
Anthropic Claude API integration example for function-schema library.

This example demonstrates how to use function schemas with Claude's tool calling feature.

Note: This example requires the anthropic library to be installed and an API key to be set.
For demonstration purposes, this shows the structure without actually making API calls.
"""

from typing import Annotated, Optional
from function_schema import Doc, get_function_schema
import enum
import json

# For actual usage, uncomment the following:
# import anthropic
# client = anthropic.Anthropic(api_key="your-api-key-here")


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


def search_web(
    query: Annotated[str, Doc("The search query")],
    max_results: Annotated[Optional[int], Doc("Maximum number of results")] = 5
) -> str:
    """Search the web for information."""
    return f"Search results for '{query}': Found {max_results} results"


def calculate(
    expression: Annotated[str, Doc("Mathematical expression to calculate")]
) -> str:
    """Calculate a mathematical expression."""
    try:
        # Note: In production, use a safer eval method
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


def claude_tool_calling_example():
    """Example of using function schema with Claude's tool calling feature."""
    
    # Generate function schemas for Claude format
    tools = [
        get_function_schema(get_weather, "claude"),
        get_function_schema(search_web, "claude"),
        get_function_schema(calculate, "claude")
    ]
    
    print("Claude Tool Calling Example:")
    print("Tool definitions for Claude:")
    print(json.dumps(tools, indent=2))
    
    print("\nExample Claude API usage:")
    print("""
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

response = client.beta.tools.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4096,
    tools=[
        get_function_schema(get_weather, "claude"),
        get_function_schema(search_web, "claude"),
        get_function_schema(calculate, "claude")
    ],
    messages=[
        {
            "role": "user", 
            "content": "What's the weather like in Seoul? Also search for 'Claude AI news' and calculate 15 * 24"
        }
    ]
)

# Handle tool use in the response
if response.content:
    for content_block in response.content:
        if content_block.type == "tool_use":
            tool_name = content_block.name
            tool_args = content_block.input
            
            # Call the appropriate function
            if tool_name == "get_weather":
                result = get_weather(**tool_args)
            elif tool_name == "search_web":
                result = search_web(**tool_args)
            elif tool_name == "calculate":
                result = calculate(**tool_args)
            
            print(f"Tool {tool_name} result: {result}")
""")


def claude_conversational_example():
    """Example of a conversational Claude interaction with tools."""
    
    print("\nClaude Conversational Example with Tools:")
    print("""
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Multi-turn conversation with tool use
messages = [
    {"role": "user", "content": "Can you help me plan a trip to Tokyo?"}
]

response = client.beta.tools.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    tools=[
        get_function_schema(get_weather, "claude"),
        get_function_schema(search_web, "claude")
    ],
    messages=messages
)

# Continue the conversation based on tool results
messages.append({"role": "assistant", "content": response.content})

# Claude might use tools to get weather info and search for travel tips
if any(block.type == "tool_use" for block in response.content):
    # Process tool calls and add results to conversation
    for content_block in response.content:
        if content_block.type == "tool_use":
            # Execute tool and add result
            tool_result = execute_tool(content_block.name, content_block.input)
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": tool_result
                    }
                ]
            })
    
    # Get Claude's response after tool execution
    final_response = client.beta.tools.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        tools=[
            get_function_schema(get_weather, "claude"),
            get_function_schema(search_web, "claude")
        ],
        messages=messages
    )
""")


if __name__ == "__main__":
    print("Function Schema - Claude Integration Examples")
    print("=" * 50)
    
    claude_tool_calling_example()
    print("\n" + "=" * 50)
    claude_conversational_example()