import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"

questions = [
    "Read notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.",
    "What is the purpose of a merit scholarship?",
    "What information is required to calculate the final fee after a scholarship?"
]

for question in questions:

    print("\n" + "=" * 60)
    print("PLAIN LLM — NO TOOL")
    print("=" * 60)

    print("\nQUESTION:")
    print(question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are answering a simple AI agent assessment. "
                    "Give concise answers in 1-3 sentences. "
                    "Do not access files, tools, websites, or external systems. "
                    "If the user asks about notice.html, clearly state that "
                    "you cannot access the file."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    print("\nANSWER:")
    print(response.choices[0].message.content)

    print("=" * 60)