
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from lc_config import DATA_DIR, CHROMA_DIR

# Load hospital documents
loader = DirectoryLoader(
    DATA_DIR,
    glob="*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
documents = loader.load()

print("Documents loaded:", len(documents))

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

print("Chunks created:", len(chunks))

# Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Store chunks in ChromaDB
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DIR
)

print("Hospital documents stored in ChromaDB successfully!")
