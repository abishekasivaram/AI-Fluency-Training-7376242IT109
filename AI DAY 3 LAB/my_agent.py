import os
from openai import OpenAI
from dotenv import load_dotenv

from tools import read_notice

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_notice",
            "description": "Read the college fee notice from notice.html.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


questions = [
    "Read the college notice and tell me the total fee for CS101 and AI202 after the merit scholarship.",
    "What is the purpose of a merit scholarship?",
    "What information is required to calculate the final fee after a scholarship?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("LLM + ONE TOOL")
    print("=" * 60)

    print("\nQUESTION:")
    print(question)

    messages = [
        {
            "role": "system",
            "content": (
                "Answer briefly in 1-2 sentences. "
                "Use read_notice only when information from the college "
                "notice is required."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool_call = message.tool_calls[0]

        print("\nTOOL CALL:")
        print("read_notice()")

        result = read_notice()

        # Show only a short confirmation instead of the entire file
        print("TOOL RESULT:")
        print("Notice information retrieved successfully.")

        messages.append(message)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0
        )

        answer = final_response.choices[0].message.content

    else:
        answer = message.content

    print("\nFINAL ANSWER:")
    print(answer)

    print("=" * 60)