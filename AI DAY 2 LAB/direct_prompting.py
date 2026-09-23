# direct_prompting.py

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

A customer asks:

"I want a Premium gym membership for 6 months with a Personal Trainer.
What will be the total cost after applying the applicable membership discount?"

Answer the customer's question directly.
"""

response = client.responses.create(
    model="openai/gpt-oss-20b",
    input=prompt
)

print("\n" + "=" * 60)
print("DIRECT PROMPTING")
print("=" * 60)

print("\nQUESTION:")
print("""
A customer wants a Premium gym membership for 6 months
with a Personal Trainer. Find the total cost after applying
the applicable membership discount.
""")

print("\nANSWER:")
print(response.output_text)

print("=" * 60)