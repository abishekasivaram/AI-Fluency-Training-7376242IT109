from config import client, MODEL, banner


SYSTEM_PROMPT = """
You are a helpful student assistant.

You can answer general questions about assignments,
but you do not have access to the student's private
assignment records.

Do not invent assignment status or due dates.
If the user asks for private assignment information,
clearly say that you do not have access to those records.
"""


QUESTIONS = [
    "What is the status of my Python Recursion assignment?",
    "Which assignments are still pending?",
    "Which pending assignment is due first?",
    "I have two days available. Which pending assignment should I complete first?"
]


def chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("SYSTEM 1: PLAIN CHATBOT")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", chatbot(question))
        print("-" * 70)