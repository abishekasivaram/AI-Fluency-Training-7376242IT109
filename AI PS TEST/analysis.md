# Day 8 — Hospital Helpdesk Agent Results

## Configuration
- **Problem Statement:** Hospital Helpdesk Assistant
- **Vector Database:** ChromaDB
- **Embedding Model:** nomic-embed-text
- **Chat Model:** Check your `MODEL_NAME` in `lc_config.py`
- **Agent Framework:** LangGraph
- **Memory:** MemorySaver

## Test Results

| No. | Question | Tools Called | Correct? | Notes |
|---|---|---|---|---|
| 1 | What are the hospital visiting hours? | Fill after testing | Fill | Expected: 4 PM–6 PM daily |
| 2 | How much does a specialist consultation cost? | Fill after testing | Fill | Expected: Rs. 800 |
| 3 | What documents are required for health insurance? | Fill after testing | Fill | Expected: insurance card, ID and medical documents |
| 4 | What happens if I arrive 20 minutes late for an appointment? | Fill after testing | Fill | Expected: rescheduling may be required |
| 5 | What is the capital of France? | Fill after testing | Fill | Expected: outside the handbook scope |

## Observations
Record whether the agent used the correct tools, retrieved relevant documents, remembered follow-up questions and avoided unsupported answers.

## Limitations
Record any incorrect answers