from data import ASSIGNMENTS
from config import banner


def workflow(question):
    question = question.lower()

    # Q1: Check the status of Python Recursion
    if "status" in question and "python recursion" in question:
        for assignment in ASSIGNMENTS:
            if assignment["name"].lower() == "python recursion":
                return (
                    f"Python Recursion: {assignment['status']} "
                    f"(Due: {assignment['due_date']})"
                )

    # Q3: Find the earliest pending assignment
    elif "due first" in question:
        pending = [
            assignment
            for assignment in ASSIGNMENTS
            if assignment["status"].lower() == "pending"
        ]

        earliest = min(
            pending,
            key=lambda assignment: assignment["due_date"]
        )

        return (
            f"{earliest['name']} is due first "
            f"on {earliest['due_date']}."
        )

    # Q4: Choose which assignment to complete first
    elif "two days" in question and "complete first" in question:
        pending = [
            assignment
            for assignment in ASSIGNMENTS
            if assignment["status"].lower() == "pending"
        ]

        earliest = min(
            pending,
            key=lambda assignment: assignment["due_date"]
        )

        return (
            f"Complete {earliest['name']} first because "
            f"it has the earliest pending deadline: "
            f"{earliest['due_date']}."
        )

    # Q2: Find all pending assignments
    elif "pending" in question and "which" in question:
        pending = [
            assignment["name"]
            for assignment in ASSIGNMENTS
            if assignment["status"].lower() == "pending"
        ]

        return "Pending assignments: " + ", ".join(pending)

    return "Sorry, I do not have a rule for this question."


QUESTIONS = [
    "What is the status of my Python Recursion assignment?",
    "Which assignments are still pending?",
    "Which pending assignment is due first?",
    "I have two days available. Which pending assignment should I complete first?"
]


if __name__ == "__main__":
    banner("SYSTEM 2: RULE-BASED WORKFLOW")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)