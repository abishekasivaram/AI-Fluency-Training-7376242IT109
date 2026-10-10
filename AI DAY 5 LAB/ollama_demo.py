import requests
import time
import json

URL = "http://localhost:11434/api/chat"
MODEL = "mess-assistant:latest"

def chat(prompt, stream=False):
    print(f"\nPrompt: {prompt}")
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": stream
    }

    start = time.perf_counter()
    first_token_time = None
    answer = ""
    result = {}

    if stream:
        response = requests.post(URL, json=payload, stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line)
            chunk = data.get("message", {}).get("content", "")

            if chunk:
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                print(chunk, end="", flush=True)
                answer += chunk

            if data.get("done"):
                result = data

        end = time.perf_counter()
        print()

        ttft = (
            first_token_time - start
            if first_token_time is not None else None
        )
        print(f"TTFT: {ttft:.3f} seconds" if ttft is not None
              else "TTFT: Not measured")

    else:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result.get("message", {}).get("content", "")
        end = time.perf_counter()
        print(answer)
        print("TTFT: Not measured for non-streaming")

    total_time = end - start
    tokens = result.get("eval_count", 0)
    eval_duration = result.get("eval_duration", 0)

    tokens_per_sec = (
        tokens / (eval_duration / 1_000_000_000)
        if eval_duration else 0
    )

    print(f"Total time: {total_time:.3f} seconds")
    print(f"Output tokens: {tokens}")
    print(f"Tokens/second: {tokens_per_sec:.2f}")

if __name__ == "__main__":
    prompts = [
        "What are your responsibilities?",
        "What is today's lunch menu?",
        "What should I do if I have a food allergy?"
    ]

    print("=== NON-STREAMING TESTS ===")
    for prompt in prompts:
        chat(prompt, stream=False)

    print("\n=== REPEATED PROMPT TEST ===")
    chat(prompts[0], stream=False)

    print("\n=== STREAMING TEST ===")
    chat(prompts[0], stream=True)
