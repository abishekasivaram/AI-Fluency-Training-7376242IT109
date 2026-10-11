
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from lc_config import CHROMA_DIR, TOP_K

# Load embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load existing ChromaDB
db = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

# Get user query
query = input("Ask a hospital-related question: ")

# Search relevant documents
results = db.similarity_search_with_score(query, k=TOP_K)

print("\n--- Search Results ---")

for doc, score in results:
    print("\nDocument:", doc.metadata.get("source", "Unknown"))
    print("Distance:", round(score, 4))
    print("Content:", doc.page_content)
