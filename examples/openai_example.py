"""
OpenAI API integration example for function-schema library.

This example demonstrates how to use function schemas with OpenAI's API for:
1. Assistant API with tool calling
2. Chat completion with function calling

Note: This example requires the openai library to be installed and an API key to be set.
For demonstration purposes, this shows the structure without actually making API calls.
"""

from typing import Annotated, Optional
from function_schema import Doc, get_function_schema
import enum
import json

# For actual usage, uncomment the following:
# import openai
# openai.api_key = "sk-your-api-key-here"


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


def get_current_time(
    timezone: Annotated[Optional[str], Doc("Timezone (e.g., 'UTC', 'EST')")] = "UTC"
) -> str:
    """Get the current time in the specified timezone."""
    from datetime import datetime
    return f"Current time in {timezone}: {datetime.now().isoformat()}"


def openai_assistant_example():
    """Example of using function schema with OpenAI Assistant API."""
    
    # Generate function schema for OpenAI format
    weather_tool = {
        "type": "function",
        "function": get_function_schema(get_weather)
    }
    
    time_tool = {
        "type": "function", 
        "function": get_function_schema(get_current_time)
    }
    
    print("OpenAI Assistant API Example:")
    print("Tool definitions:")
    print(json.dumps([weather_tool, time_tool], indent=2))
    
    print("\nExample assistant creation code:")
    print("""
import openai

client = openai.OpenAI(api_key="your-api-key")

# Create an assistant with the function
assistant = client.beta.assistants.create(
    instructions="You are a helpful assistant. Use the provided functions to answer questions.",
    model="gpt-4-turbo-preview",
    tools=[
        {
            "type": "function",
            "function": get_function_schema(get_weather),
        },
        {
            "type": "function", 
            "function": get_function_schema(get_current_time),
        }
    ]
)

# Create a thread and run
thread = client.beta.threads.create()

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    messages=[
        {"role": "user", "content": "What's the weather like in Seoul?"}
    ]
)
""")


def openai_chat_completion_example():
    """Example of using function schema with OpenAI Chat Completion API."""
    
    # Generate function schemas
    tools = [
        {
            "type": "function",
            "function": get_function_schema(get_weather)
        },
        {
            "type": "function",
            "function": get_function_schema(get_current_time)
        }
    ]
    
    print("\nOpenAI Chat Completion API Example:")
    print("Tools for chat completion:")
    print(json.dumps(tools, indent=2))
    
    print("\nExample chat completion code:")
    print("""
import openai

client = openai.OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "What's the weather like in Seoul and what time is it?"}
    ],
    tools=[
        {
            "type": "function",
            "function": get_function_schema(get_weather)
        },
        {
            "type": "function",
            "function": get_function_schema(get_current_time)
        }
    ],
    tool_choice="auto",
)

# Handle tool calls in the response
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == "get_weather":
            # Parse arguments and call the actual function
            import json
            args = json.loads(tool_call.function.arguments)
            result = get_weather(**args)
            print(f"Weather result: {result}")
        elif tool_call.function.name == "get_current_time":
            args = json.loads(tool_call.function.arguments)
            result = get_current_time(**args)
            print(f"Time result: {result}")
""")


if __name__ == "__main__":
    print("Function Schema - OpenAI Integration Examples")
    print("=" * 50)
    
    openai_assistant_example()
    print("\n" + "=" * 50)
    openai_chat_completion_example()