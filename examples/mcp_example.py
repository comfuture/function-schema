"""
MCP (Model Context Protocol) integration example for function-schema library.

This example demonstrates how to use function schemas with the Model Context Protocol,
which is a standard for AI assistants to interact with external tools and data sources.

MCP allows AI models to:
1. Access tools (functions) through a standardized interface
2. Read and write resources (files, databases, APIs)
3. Maintain context across interactions

Note: This is a conceptual example showing how function-schema can be used 
to generate tool definitions compatible with MCP.
"""

from typing import Annotated, Optional, List, Dict, Any
from function_schema import Doc, get_function_schema
import enum
import json


class Priority(enum.Enum):
    low = "low"
    medium = "medium" 
    high = "high"
    urgent = "urgent"


def read_file(
    path: Annotated[str, Doc("File path to read")]
) -> str:
    """Read contents of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(
    path: Annotated[str, Doc("File path to write to")],
    content: Annotated[str, Doc("Content to write to the file")],
    append: Annotated[Optional[bool], Doc("Whether to append to file")] = False
) -> str:
    """Write content to a file."""
    try:
        mode = 'a' if append else 'w'
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        return f"Successfully {'appended to' if append else 'wrote'} file: {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def list_directory(
    path: Annotated[str, Doc("Directory path to list")],
    show_hidden: Annotated[Optional[bool], Doc("Include hidden files")] = False
) -> List[str]:
    """List contents of a directory."""
    import os
    try:
        items = os.listdir(path)
        if not show_hidden:
            items = [item for item in items if not item.startswith('.')]
        return sorted(items)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]


def create_task(
    title: Annotated[str, Doc("Task title")],
    description: Annotated[Optional[str], Doc("Task description")] = "",
    priority: Annotated[Optional[str], Doc("Task priority")] = "medium",
    due_date: Annotated[Optional[str], Doc("Due date (YYYY-MM-DD format)")] = None
) -> str:
    """Create a new task."""
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }
    return f"Created task: {json.dumps(task, indent=2)}"


def search_web(
    query: Annotated[str, Doc("Search query")],
    max_results: Annotated[Optional[int], Doc("Maximum results to return")] = 10,
    site: Annotated[Optional[str], Doc("Specific site to search within")] = None
) -> str:
    """Search the web for information."""
    search_params = {
        "query": query,
        "max_results": max_results,
        "site_filter": site
    }
    # This would integrate with a real search API
    return f"Web search executed with params: {json.dumps(search_params, indent=2)}"


def send_email(
    to: Annotated[str, Doc("Recipient email address")],
    subject: Annotated[str, Doc("Email subject")],
    body: Annotated[str, Doc("Email body content")],
    cc: Annotated[Optional[str], Doc("CC recipients (comma-separated)")] = None,
    priority: Annotated[Optional[str], Doc("Email priority (low, normal, high)")] = "normal"
) -> str:
    """Send an email."""
    email_data = {
        "to": to,
        "subject": subject, 
        "body": body,
        "cc": cc.split(",") if cc else [],
        "priority": priority
    }
    return f"Email queued for sending: {json.dumps(email_data, indent=2)}"


def mcp_server_manifest():
    """Generate an MCP server manifest with available tools."""
    
    # Define specific functions to include (avoid dynamic inspection issues)
    functions_to_include = [
        read_file,
        write_file, 
        list_directory,
        create_task,
        search_web,
        send_email
    ]
    
    # Generate tool definitions
    tools = []
    for func in functions_to_include:
        try:
            schema = get_function_schema(func)
            # Convert to MCP tool format
            mcp_tool = {
                "name": schema["name"],
                "description": schema["description"],
                "inputSchema": schema["parameters"]
            }
            tools.append(mcp_tool)
        except Exception as e:
            print(f"Warning: Could not generate schema for {func.__name__}: {e}")
            continue
    
    # MCP server manifest
    manifest = {
        "name": "function-schema-example-server",
        "version": "1.0.0",
        "description": "Example MCP server using function-schema generated tools",
        "tools": tools,
        "resources": [
            {
                "uri": "file:///*",
                "name": "File System",
                "description": "Access to local file system"
            }
        ],
        "capabilities": {
            "tools": {
                "supportsProgressNotifications": True
            },
            "resources": {
                "subscribe": True,
                "listChanged": True
            }
        }
    }
    
    return manifest


def mcp_tool_call_example():
    """Example of how an MCP client might call tools."""
    
    print("MCP Tool Call Examples:")
    print("=" * 30)
    
    # Example tool calls in MCP format
    examples = [
        {
            "name": "read_file",
            "arguments": {"path": "/tmp/example.txt"}
        },
        {
            "name": "create_task", 
            "arguments": {
                "title": "Review MCP integration",
                "description": "Test the Model Context Protocol integration",
                "priority": "high",
                "due_date": "2024-01-15"
            }
        },
        {
            "name": "search_web",
            "arguments": {
                "query": "Model Context Protocol documentation",
                "max_results": 5
            }
        }
    ]
    
    for example in examples:
        print(f"\nTool Call: {example['name']}")
        print(f"Arguments: {json.dumps(example['arguments'], indent=2)}")
        
        # Simulate tool execution
        if example['name'] == 'read_file':
            result = read_file(**example['arguments'])
        elif example['name'] == 'create_task':
            result = create_task(**example['arguments'])
        elif example['name'] == 'search_web':
            result = search_web(**example['arguments'])
        
        print(f"Result: {result}")
        print("-" * 40)


if __name__ == "__main__":
    print("Function Schema - MCP (Model Context Protocol) Integration")
    print("=" * 60)
    
    # Generate and display MCP server manifest
    manifest = mcp_server_manifest()
    print("MCP Server Manifest:")
    print(json.dumps(manifest, indent=2))
    
    print("\n" + "=" * 60)
    
    # Show tool call examples
    mcp_tool_call_example()
    
    print("\n" + "=" * 60)
    print("This example demonstrates how function-schema can generate")
    print("tool definitions compatible with the Model Context Protocol,")
    print("enabling AI assistants to discover and use your functions")
    print("through a standardized interface.")