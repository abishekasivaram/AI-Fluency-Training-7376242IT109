import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq")
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
API_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = "https://api.groq.com/openai/v1"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


def banner(title):
    print()
    print("=" * 70)
    print(title)
    print(f"Provider : {PROVIDER}")
    print(f"Model    : {MODEL}")
    print("=" * 70)