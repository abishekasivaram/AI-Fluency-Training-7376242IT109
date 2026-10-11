import json
from tools import SCHEMAS


def validate_arguments(tool_name, arguments):
    # 1. Check whether the tool exists
    if tool_name not in SCHEMAS:
        return f"Error: Unknown tool '{tool_name}'."

    # 2. Parse JSON arguments
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            return "Error: Invalid JSON arguments."

    # 3. Arguments must be a dictionary
    if not isinstance(arguments, dict):
        return "Error: Arguments must be a JSON object."

    schema = SCHEMAS[tool_name]["function"]["parameters"]
    properties = schema["properties"]
    required = schema.get("required", [])

    # 4. Check missing required arguments
    for key in required:
        if key not in arguments:
            return f"Error: Missing required argument '{key}'."

    # 5. Reject invented extra arguments
    if schema.get("additionalProperties") is False:
        for key in arguments:
            if key not in properties:
                return f"Error: Unexpected argument '{key}'."

    # 6. Check types and allowed values
    for key, value in arguments.items():
        if key not in properties:
            continue

        rule = properties[key]
        expected_type = rule.get("type")

        if expected_type == "string" and not isinstance(value, str):
            return f"Error: '{key}' must be a string."

        if "enum" in rule and value not in rule["enum"]:
            return (
                f"Error: Invalid value for '{key}'. "
                f"Expected one of: {rule['enum']}."
            )

    return None