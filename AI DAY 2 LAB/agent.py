# agent.py

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    get_membership_price,
    get_service_price,
    get_discount,
    calculator
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# --------------------------------------------------
# TOOL DEFINITIONS
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_membership_price",
            "description": "Get the monthly price of a gym membership plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plan": {
                        "type": "string",
                        "enum": ["Basic", "Standard", "Premium"]
                    }
                },
                "required": ["plan"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_service_price",
            "description": "Get the monthly price of an additional gym service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "enum": [
                            "Personal Trainer",
                            "Diet Plan",
                            "Fitness Assessment"
                        ]
                    }
                },
                "required": ["service"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_discount",
            "description": "Get the membership discount percentage for 3, 6, or 12 months.",
            "parameters": {
                "type": "object",
                "properties": {
                    "months": {
                        "type": "integer",
                        "enum": [3, 6, 12]
                    }
                },
                "required": ["months"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# --------------------------------------------------
# PYTHON FUNCTIONS
# --------------------------------------------------

available_functions = {
    "get_membership_price": get_membership_price,
    "get_service_price": get_service_price,
    "get_discount": get_discount,
    "calculator": calculator
}


# --------------------------------------------------
# USER CONVERSATION
# --------------------------------------------------

messages = [
    {
        "role": "system",
         "content":"""
You are a gym membership management agent.

All gym prices are in Indian Rupees (₹).

You have access to private gym information through tools.

IMPORTANT RULES:
- Never invent prices.
- Never invent discounts.
- Use the tools whenever information is missing.
- Use the calculator tool for the final calculation.
- Only call the exact tool names provided.
- The membership discount applies ONLY to the membership fee.
- The Personal Trainer fee is NOT discounted.
- Calculate membership and additional services separately.
- All final monetary values must be reported in ₹.
- After receiving all required observations, give the final answer.
"""
    },

    {
        "role": "user",
        "content": """
A customer wants a Premium gym membership for 6 months
with a Personal Trainer.

Find the total cost after applying the applicable
membership discount.
"""
    }
]


print("\n" + "=" * 60)
print("REACT AGENT")
print("=" * 60)

print("\nQUESTION:")
print("""
A customer wants a Premium gym membership for 6 months
with a Personal Trainer.
Find the total cost after applying the applicable
membership discount.
""")

print("\nREASONING AND TOOL EXECUTION:\n")


# --------------------------------------------------
# REACT LOOP
# --------------------------------------------------

while True:

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0
    )

    message = response.choices[0].message

    # Add assistant message
    messages.append(message)

    # ----------------------------------------------
    # FINAL ANSWER
    # ----------------------------------------------

    if not message.tool_calls:

        print("FINAL ANSWER:")
        print(message.content)

        break

    # ----------------------------------------------
    # TOOL CALLS
    # ----------------------------------------------

    for tool_call in message.tool_calls:

        function_name = tool_call.function.name

        # Fix possible Groq special-token contamination
        function_name = function_name.split("<|")[0].strip()

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("THOUGHT → Need information/calculation")
        print(
            f"ACTION → {function_name}({arguments})"
        )

        # Find function
        function = available_functions.get(function_name)

        if function is None:

            result = (
                f"Unknown tool: {function_name}"
            )

        else:

            result = function(**arguments)

        print(f"OBSERVATION → {result}\n")

        # Send observation back to model
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            }
        )