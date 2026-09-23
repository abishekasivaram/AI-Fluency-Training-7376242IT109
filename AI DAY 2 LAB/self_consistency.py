# self_consistency.py

import os
import re
from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


question = """
A gym member chooses the Basic plan for 12 months
at ₹1,000 per month.

A 20% discount is applied to the membership fee.

The member also pays a one-time registration fee
of ₹500.

What is the final amount the member must pay?

Return only the final amount in ₹.
"""


def get_answer(temperature):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
You are a gym membership calculation assistant.

Calculate the answer carefully.
Return ONLY the final amount.
All prices are in Indian Rupees.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


def extract_amount(text):

    numbers = re.findall(
        r"(?:₹\s*)?(\d{1,3}(?:,\d{3})+|\d{4,6})",
        text
    )

    if numbers:
        return int(numbers[-1].replace(",", ""))

    return None


# ==================================================
# HEADER
# ==================================================

print("\n" + "=" * 60)
print("SELF-CONSISTENCY EXPERIMENT")
print("=" * 60)

print("\nQUESTION:")
print(question)


# ==================================================
# TEMPERATURE 0.8
# ==================================================

print("-" * 60)
print("5 RUNS — TEMPERATURE = 0.8")
print("-" * 60)

answers_08 = []

for i in range(5):

    response = get_answer(0.8)

    amount = extract_amount(response)

    answers_08.append(amount)

    print(f"Run {i + 1}: ₹{amount:,}")


counts = Counter(answers_08)

majority_answer, frequency = counts.most_common(1)[0]

print("\nMajority answer:")
print(f"₹{majority_answer:,}")

print(f"Frequency: {frequency}/5")

if majority_answer == 10100:
    print("Correctness: CORRECT")
else:
    print("Correctness: INCORRECT")


# ==================================================
# TEMPERATURE 0
# ==================================================

print("\n" + "-" * 60)
print("5 RUNS — TEMPERATURE = 0")
print("-" * 60)

answers_0 = []

for i in range(5):

    response = get_answer(0)

    amount = extract_amount(response)

    answers_0.append(amount)

    print(f"Run {i + 1}: ₹{amount:,}")


# Compare numerical answers rather than wording

if len(set(answers_0)) == 1:

    print("\nNumerical consistency: IDENTICAL")

else:

    print("\nNumerical consistency: DIFFERENT")


print("\n" + "=" * 60)