
import os
from dotenv import load_dotenv

load_dotenv()

# Model configuration
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")

# Vector database
CHROMA_DIR = "chroma_db"
DATA_DIR = "data"

# Retrieval settings
TOP_K = 3
MAX_DISTANCE = 1.0
