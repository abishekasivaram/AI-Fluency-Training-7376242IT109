import json
from validator import validate_arguments
from tools import TOOLS


def handle_call(tool_name, raw_arguments):
    # Stage 1: Parse JSON
    try:
        arguments = json.loads(raw_arguments)
    except (json.JSONDecodeError, TypeError):
        return "Error: Invalid JSON arguments."

    # Stage 2: Look up the tool
    if tool_name not in TOOLS:
        return f"Error: Unknown tool '{tool_name}'."

    # Stage 3: Validate arguments
    error = validate_arguments(tool_name, arguments)
    if error:
        return error

    # Stage 4: Execute tool
    try:
        return str(TOOLS[tool_name](**arguments))
    except Exception as error:
        return f"Tool execution error: {error}"


faults = [
    ("Invalid JSON", "get_menu", '{"meal":'),
    ("Unknown tool", "get_unknown", '{"meal":"lunch"}'),
    ("Missing argument", "get_menu", '{}'),
    ("Wrong type", "get_menu", '{"meal":123}'),
    ("Invalid enum", "get_menu", '{"meal":"snack"}'),
    ("Extra argument", "get_menu", '{"meal":"lunch","price":50}'),
    # Additional fault 1: JSON array instead of object
    ("Wrong JSON shape", "get_menu", '["lunch"]'),
    # Additional fault 2: Null instead of a meal name
    ("Null argument", "get_menu", '{"meal":null}')
]


if __name__ == "__main__":
    print("=== Fault Injection Results ===")

    for name, tool, arguments in faults:
        result = handle_call(tool, arguments)
        print(f"\nFault: {name}")
        print(f"Returned: {result}")
        print("Continued: Y")