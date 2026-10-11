import json
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "mess-assistant:latest"

QUESTION = """
Extract the following information from this sentence:
"Ravi wants lunch at 1 PM and prefers vegetarian food."

Return these fields:
name, meal, time, preference.
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "meal": {
            "type": "string",
            "enum": ["breakfast", "lunch", "dinner"]
        },
        "time": {"type": "string"},
        "preference": {"type": "string"}
    },
    "required": ["name", "meal", "time", "preference"],
    "additionalProperties": False
}


def run_test(title, response_format=None):
    print(f"\n=== {title} ===")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract only information supported by the sentence. "
                        "Do not invent missing details."
                    )
                },
                {"role": "user", "content": QUESTION}
            ],
            response_format=response_format,
            temperature=0
        )

        raw = response.choices[0].message.content
        print("Raw reply:", raw)

        try:
            parsed = json.loads(raw)
            print("Parsed result:", parsed)

            if isinstance(parsed, dict) and set(parsed) == set(SCHEMA["properties"]):
                print("Expected field names present: Yes")
            else:
                print("Expected field names present: No")

        except (json.JSONDecodeError, TypeError):
            print("Parsed result: Not valid JSON")

    except Exception as error:
        print("Provider error or unsupported feature:", error)


if __name__ == "__main__":
    # Case 1: No output constraint
    run_test("1. Unconstrained output")

    # Case 2: JSON mode
    run_test("2. JSON mode", {"type": "json_object"})

    # Case 3: JSON Schema mode
    run_test(
        "3. Schema mode",
        {
            "type": "json_schema",
            "json_schema": {
                "name": "meal_extraction",
                "strict": True,
                "schema": SCHEMA
            }
        }
    )