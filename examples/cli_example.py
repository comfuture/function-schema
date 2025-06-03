"""
CLI usage example for function-schema library.

This example demonstrates how to use the command-line interface to generate 
function schemas from Python files.
"""

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


def calculate_distance(
    lat1: Annotated[float, Doc("Latitude of first location")],
    lon1: Annotated[float, Doc("Longitude of first location")],
    lat2: Annotated[float, Doc("Latitude of second location")],
    lon2: Annotated[float, Doc("Longitude of second location")],
    unit: Annotated[Optional[str], Doc("Unit for distance (km or miles)")] = "km"
) -> float:
    """Calculate distance between two geographic coordinates."""
    import math
    
    # Haversine formula
    R = 6371 if unit == "km" else 3959  # Earth's radius
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


if __name__ == "__main__":
    print("CLI Usage Examples for function-schema")
    print("=" * 50)
    
    print("1. Generate schema for a function (default OpenAI format):")
    print("   function_schema examples/cli_example.py get_weather")
    print()
    
    print("2. Generate schema with JSON formatting:")
    print("   function_schema examples/cli_example.py get_weather | jq")
    print()
    
    print("3. Generate schema for Claude format:")
    print("   function_schema examples/cli_example.py get_weather claude")
    print()
    
    print("4. Generate schema for another function:")
    print("   function_schema examples/cli_example.py calculate_distance")
    print()
    
    print("5. Save schema to file:")
    print("   function_schema examples/cli_example.py get_weather > weather_schema.json")
    print()
    
    print("Try running these commands from the project root directory!")
    print("Make sure the function-schema package is installed first:")
    print("   pip install -e .")
    print()
    
    print("Available functions in this file:")
    import inspect
    functions = [name for name, obj in locals().items() 
                if inspect.isfunction(obj) and not name.startswith('_')]
    for func_name in functions:
        func = locals()[func_name]
        doc = inspect.getdoc(func) or "No description"
        print(f"  - {func_name}: {doc}")