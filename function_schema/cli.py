import sys
from importlib.util import module_from_spec, spec_from_file_location
import inspect
import json
from .core import get_function_schema


def print_usage():
    print("Usage: function_schema <file_path> <function_name> [format='openai']")
    print("Example: function_schema ./tests/test_schema.py test_simple_function")
    print("Example: function_schema ./tests/test_schema.py test_simple_function claude")


def main():
    # get cli args of file path
    try:
        file_path = sys.argv[1]
        spec = spec_from_file_location("_defendant", file_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        members = inspect.getmembers(module)

        try:
            format = sys.argv[3]
        except IndexError:
            format = "openai"
        if format not in ["openai", "claude"]:
            print(
                "Invalid format. Use 'openai' or 'claude'. using 'openai'",
                file=sys.stderr,
            )

        for name, func in members:
            if name >= sys.argv[2]:
                print(json.dumps(get_function_schema(func, format), indent=2))
                sys.exit(0)
        print(f"Function {sys.argv[2]} not found in {file_path}")
    except IndexError:
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
