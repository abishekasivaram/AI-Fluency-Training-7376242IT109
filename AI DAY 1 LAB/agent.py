import json
from datetime import datetime

from config import client, MODEL, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a student's assignment-tracking assistant.

You have access to private assignment information through tools.

Rules:
1. Never guess assignment information.
2. Always use get_assignment_info when the question requires
   private assignment data.
3. Use the calculator tool whenever arithmetic is required.
4. For questions about which assignment is due first,
   retrieve the pending assignments and compare their due dates.
5. Give a concise answer based only on the tool results.
6. Available assignment statuses are Pending and Completed.
"""


QUESTIONS = [
    "What is the status of my Python Recursion assignment?",
    "Which assignments are still pending?",
    "Which pending assignment is due first?",
    "I have two days available. Which pending assignment should I complete first?"
]


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # 1. REASON
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=1,
            parallel_tool_calls=False
        )

        message = response.choices[0].message

        # 2. FINISH if no tool is required
        if not message.tool_calls:
            return message.content.strip()

        # Add assistant tool request to conversation
        messages.append({
            "role": "assistant",
            "content": message.content or "",
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

        # 3. ACT + OBSERVE
        for call in message.tool_calls:

            name = call.function.name

            # Handle malformed tool names if they occur
            if "<|channel|>" in name:
                name = name.split("<|channel|>")[0]

            arguments = json.loads(
                call.function.arguments or "{}"
            )

            function = TOOL_FUNCTIONS.get(name)

            if function:
                result = function(**arguments)
            else:
                result = f"Unknown tool: {name}"

            if verbose:
                print(
                    f" step {step}: {name}({arguments}) -> {result}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", agent(question))
        print("-" * 70)