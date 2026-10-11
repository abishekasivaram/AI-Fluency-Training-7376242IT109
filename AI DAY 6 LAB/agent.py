import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import SCHEMAS, TOOLS
from validator import validate_arguments

load_dotenv()

MODEL = "mess-assistant:latest"

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "ollama")
)

SYSTEM_PROMPT = """
You are a College Mess Assistant.
Use tools to answer questions about meal timings and menus.
Never invent menu information.
If menu data is not configured, say so clearly.
Use simple, polite English.
"""


def run_agent(question, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    previous_calls = set()
    repeated_calls = 0
    max_tokens = 300

    for step in range(1, max_steps + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=list(SCHEMAS.values()),
                tool_choice="auto",
                max_tokens=max_tokens
            )
        except Exception as error:
            return f"API error: {error}"

        choice = response.choices[0]
        message = choice.message
        finish_reason = choice.finish_reason

        # Retry a truncated reply with a larger token limit
        if finish_reason == "length":
            if max_tokens < 1200:
                max_tokens *= 2
                print("Truncated response; retrying with more tokens.")
                continue
            return "Error: Response remained truncated after retries."

        # No tool requested: return the assistant's final answer
        if finish_reason == "stop" or not message.tool_calls:
            return message.content or "The model returned an empty response."

        # Process every tool call, including parallel calls
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        for call in message.tool_calls:
            name = call.function.name
            raw_arguments = call.function.arguments

            try:
                arguments = json.loads(raw_arguments)
            except (json.JSONDecodeError, TypeError):
                error_message = "Error: Invalid JSON arguments."
                arguments = None

            if arguments is None:
                result = error_message
            else:
                validation_error = validate_arguments(name, arguments)

                if validation_error:
                    result = validation_error
                elif name not in TOOLS:
                    result = f"Error: Unknown tool '{name}'."
                else:
                    try:
                        result = str(TOOLS[name](**arguments))
                    except Exception as error:
                        result = f"Tool execution error: {error}"

            signature = (name, raw_arguments)

            if signature in previous_calls:
                repeated_calls += 1
            else:
                repeated_calls = 0

            previous_calls.add(signature)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

            print(f"Step {step} | Tool: {name} | Result: {result}")

            if repeated_calls >= 2:
                return "Stopped: repeated identical tool calls detected."

    return "Stopped: maximum agent steps reached."


if __name__ == "__main__":
    print("College Mess Assistant")
    while True:
        question = input("\nYou (type exit to quit): ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        print("\nAssistant:", run_agent(question))