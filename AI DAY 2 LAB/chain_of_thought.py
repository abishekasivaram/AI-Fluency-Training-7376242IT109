# chain_of_thought.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

prompt = """
You are a gym membership assistant.

Solve the following problem carefully:

A customer chooses the Standard gym membership for 6 months.
The Standard membership costs ₹1,500 per month.

The customer also purchases a Diet Plan for all 6 months.
The Diet Plan costs ₹1,000 per month.

A 15% discount is applied only to the membership fee.

Calculate the final amount the customer must pay.

Work through the calculation step by step and then provide the final answer.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

print("\n" + "=" * 60)
print("CHAIN-OF-THOUGHT PROMPTING")
print("=" * 60)

print("\nQUESTION:")
print("""
A customer chooses the Standard gym membership for 6 months.
The Standard membership costs ₹1,500 per month.

The customer also purchases a Diet Plan for all 6 months.
The Diet Plan costs ₹1,000 per month.

A 15% discount is applied only to the membership fee.

Calculate the final amount the customer must pay.
""")

print("\nANSWER:")
print(response.choices[0].message.content)

print("=" * 60)