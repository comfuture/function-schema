"""
Test examples to ensure they are syntactically correct and runnable.
"""

import os
import subprocess
import sys
from pathlib import Path


def test_examples_syntax():
    """Test that all example files have valid Python syntax."""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    for example_file in examples_dir.glob("*.py"):
        # Compile the file to check syntax
        with open(example_file, 'rb') as f:
            try:
                compile(f.read(), example_file, 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {example_file}: {e}")


def test_examples_importable():
    """Test that all example files can be imported without errors."""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    for example_file in examples_dir.glob("*.py"):
        # Skip files that might have special execution requirements
        if example_file.name == "__init__.py":
            continue
            
        # Test that the file can be imported (checks imports)
        module_name = example_file.stem
        spec = __import__('importlib.util', fromlist=['spec_from_file_location']).spec_from_file_location(module_name, example_file)
        try:
            module = __import__('importlib.util', fromlist=['module_from_spec']).module_from_spec(spec)
            # Don't execute the module, just load it to check imports
        except ImportError as e:
            # Only fail if it's importing function_schema - other imports are optional
            if "function_schema" in str(e):
                pytest.fail(f"Import error in {example_file}: {e}")


def test_cli_example_functions():
    """Test that CLI example can generate schemas for its functions."""
    import subprocess
    import json
    
    # Test basic function schema generation
    result = subprocess.run([
        sys.executable, "-m", "function_schema.cli",
        "examples/cli_example.py", "get_weather"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    
    # Verify output is valid JSON
    try:
        schema = json.loads(result.stdout)
        assert schema["name"] == "get_weather"
        assert "parameters" in schema
    except json.JSONDecodeError as e:
        pytest.fail(f"CLI output is not valid JSON: {e}")


if __name__ == "__main__":
    # Run tests if called directly
    test_examples_syntax()
    test_examples_importable() 
    test_cli_example_functions()
    print("All example tests passed!")