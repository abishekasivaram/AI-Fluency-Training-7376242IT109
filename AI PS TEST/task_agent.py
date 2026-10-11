
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from lc_config import CHROMA_DIR, MODEL_NAME, TOP_K

# Load hospital handbook
embeddings = OllamaEmbeddings(model="nomic-embed-text")

db = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

# Tool 1: Search hospital handbook
@tool
def search_hospital_handbook(query: str) -> str:
    """Search hospital documents for relevant administrative information."""
    results = db.similarity_search_with_score(query, k=TOP_K)

    if not results:
        return "NO_MATCH: This is not covered in the hospital handbook."

    content = []
    for doc, score in results:
        content.append(
            f"Distance: {score:.4f}\n"
            f"Source: {doc.metadata.get('source', 'Unknown')}\n"
            f"Content: {doc.page_content}"
        )

    return "\n\n".join(content)


# Tool 2: Check consultation fees
@tool
def get_consultation_fee(specialty: str) -> str:
    """Return consultation fees for General Medicine or specialist consultations."""
    specialty = specialty.lower().strip()

    if specialty in ["general medicine", "general"]:
        return "General Medicine consultation fee: Rs. 500."

    if specialty in ["specialist", "specialist consultation"]:
        return "Specialist consultation fee: Rs. 800."

    return "Fee not available for this department. Check with the hospital billing desk."


# Tool 3: Check visiting hours
@tool
def get_visiting_hours() -> str:
    """Return the hospital's general ward visiting hours."""
    return "General ward visiting hours: 4:00 PM to 6:00 PM daily. ICU visits require staff permission."


# Configure model and memory
model = ChatOllama(model=MODEL_NAME, temperature=0)

memory = MemorySaver()

agent = create_react_agent(
    model=model,
    tools=[
        search_hospital_handbook,
        get_consultation_fee,
        get_visiting_hours
    ],
    prompt=(
        "You are a hospital administrative helpdesk assistant. "
        "Answer using the hospital handbook and available tools. "
        "Do not invent hospital policies or fees. "
        "If information is unavailable, clearly say it is not covered in the handbook "
        "and suggest contacting the hospital helpdesk. "
        "Do not diagnose illnesses or replace professional medical advice."
    ),
    checkpointer=memory
)


# Chat loop
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "hospital-session"}}

    print("Hospital Helpdesk Assistant")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            result = agent.invoke(
                {"messages": [("user", question)]},
                config=config
            )
            print("\nAssistant:", result["messages"][-1].content, "\n")
        except Exception as e:
            print("Error:", e)
