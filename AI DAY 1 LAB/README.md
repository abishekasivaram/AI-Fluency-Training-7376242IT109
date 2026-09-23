# Assignment Tracker - Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## Overview

This Day 1 Agentic AI practice project compares three ways to solve the same private-data problem: a **Student Assignment Tracker**.

The project answers the same assignment questions using:

1. A plain chatbot that uses an LLM without access to the private records.
2. A rule-based workflow that uses direct Python logic and the local data.
3. An AI agent that combines an LLM, tools, and an execution loop.

The assignment data is stored locally in this project for demonstration purposes. It is private project data and is not sent to the plain chatbot as part of its prompt.

## Objective

The goal is to understand the practical differences between conversational AI, deterministic program logic, and tool-using AI agents. The comparison focuses on how each approach handles private data, decision-making, flexible questions, and multi-step tasks.

## Scenario

The system is a Student Assignment Tracker containing assignment names, subjects, statuses, and due dates.

The questions tested are:

1. What is the status of my Python Recursion assignment?
2. Which assignments are still pending?
3. Which pending assignment is due first?
4. I have two days available. Which pending assignment should I complete first?

## Assignment Data

| Assignment | Subject | Status | Due date |
|---|---|---|---|
| Python Recursion | Python | Pending | 2026-09-24 |
| CN Lab Record | Computer Networks | Completed | 2026-09-23 |
| IoT Mini Project | IoT | Pending | 2026-09-26 |
| Multimedia Assignment | Multimedia | Pending | 2026-09-25 |
| Communication Record | Communication | Completed | 2026-09-22 |

## Three Approaches

### Plain Chatbot

The plain chatbot uses an LLM only. It does not have access to the local assignment records, lookup tools, or predefined assignment rules.

It can explain that it cannot access the student's private records and can provide general advice. It cannot reliably report an actual status, list the student's pending assignments, or identify the earliest due date.

### Rule-Based Workflow

The rule-based workflow uses Python conditions and direct access to `data.py`. It does not use an LLM.

It recognizes the four question patterns used in this project, filters the assignment data, and compares due dates where needed. Its answers are predictable for the supported patterns, but a differently worded request may require another rule to be added.

### AI Agent

The AI agent uses an LLM, tools, and a loop. The LLM can request `get_assignment_info` to retrieve private assignment data and can use the calculator tool when arithmetic is required.

The Python program executes each requested tool, returns the result to the LLM, and allows the LLM to produce a final response. The agent decides when a tool is needed; the calculator is available but is not claimed to be used for every question.

## Architecture / How It Works

For a question that needs private assignment information, the agent follows this general flow:

```text
User Question
      |
      v
    LLM
      |
      v
Tool Selection
      |
      v
Tool Execution
      |
      v
Tool Result
      |
      v
    LLM
      |
      v
Final Answer
```

The available tools are:

- `get_assignment_info`: looks up assignments by exact name or status.
- `calculator`: performs supported basic arithmetic expressions safely.

The agent repeats the reasoning and tool-use cycle until the LLM returns a final answer or the maximum number of steps is reached.

## Technologies Used

- Python
- Groq API
- OpenAI-compatible Python SDK
- `python-dotenv`
- Visual Studio Code
- Git and GitHub

## Project Structure

```text
AI DAY 1 LAB/
├── agent.py
├── analysis.md
├── chatbot.py
├── check_setup.py
├── config.py
├── data.py
├── requirements.txt
├── tools.py
├── workflow.py
└── Output/
```

## Setup and Installation

Open PowerShell in the project folder and create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell prevents activation because of its execution policy, activate the environment from Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

## Environment Variables

Create a file named `.env` in the project root. Use your own Groq API key; do not paste a real key into the README or commit it to GitHub.

```env
PROVIDER=groq
MODEL=openai/gpt-oss-20b
GROQ_API_KEY=your_groq_api_key_here
```

The application loads these values through `python-dotenv`. The `.env` file is ignored by Git in this project.

## How to Run Each System

Make sure the virtual environment is activated and `.env` contains a valid key for the LLM-based programs.

### Check the API setup

```powershell
python check_setup.py
```

### Run the plain chatbot

```powershell
python chatbot.py
```

This calls the LLM without assignment lookup tools.

### Run the rule-based workflow

```powershell
python workflow.py
```

This uses local Python logic and does not make an LLM request, although the script imports the shared banner configuration.

### Run the AI agent

```powershell
python agent.py
```

This sends the four test questions to the LLM and prints tool activity when the agent makes a tool call.

### Test the tools directly

```powershell
python tools.py
```

## Sample Outputs

The exact LLM wording can vary. The expected behavior for the four test questions is:

| System | Expected result |
|---|---|
| Plain chatbot | Explains that it cannot access the student's private assignment records; may provide general guidance. |
| Rule-based workflow | Reports Python Recursion as Pending and due on 2026-09-24; lists the three pending assignments; identifies Python Recursion as due first; recommends completing it first. |
| AI agent | Uses `get_assignment_info` when private data is required and produces an answer based on the returned local records. |

For the tested data, the pending assignments are **Python Recursion**, **IoT Mini Project**, and **Multimedia Assignment**. The earliest pending due date is **2026-09-24**, for **Python Recursion**.

## Comparison Summary

| Criterion | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | Flexible for general conversation | Limited to coded patterns | Flexible natural-language interpretation |
| Decision-making | Generates an answer without private records | Explicitly programmed conditions | LLM decides whether and how to use a tool |
| Tool usage | No tools | No LLM tools; uses direct Python logic | Uses `get_assignment_info` and has a calculator available |
| Private-data access | No access to local assignment data | Direct access to `data.py` | Access through `get_assignment_info` |
| Multi-step task handling | Limited for private-data tasks | Handles only programmed steps | Can request tools, observe results, and continue in a loop |
| Automation | General guidance only in this scenario | Automates supported assignment operations | Automates flexible information retrieval and response generation |
| Reliability | Does not invent records when correctly prompted, but cannot answer private-data questions | Predictable for supported patterns | Depends on model behavior and correct tool selection |

## Key Learning Outcomes

- An LLM cannot answer private-data questions if the data is not available to it.
- Rule-based programs are predictable, but their coverage depends on the rules that were written.
- An AI agent combines language understanding with controlled access to tools.
- Tool results give the agent factual project data instead of requiring it to guess.
- An agent loop can support multi-step tasks, but its behavior still depends on the LLM and tool definitions.

## Repository Contents

| File or folder | Purpose |
|---|---|
| `config.py` | Loads Groq/API configuration and creates the OpenAI-compatible client. |
| `data.py` | Stores the local private assignment data. |
| `check_setup.py` | Tests the API and model configuration. |
| `chatbot.py` | Implements the plain chatbot. |
| `workflow.py` | Implements the rule-based workflow. |
| `tools.py` | Defines assignment lookup, calculator, and tool schemas. |
| `agent.py` | Implements the LLM + tools + loop agent. |
| `analysis.md` | Contains the detailed comparison and analysis. |
| `requirements.txt` | Lists Python dependencies. |
| `.env` | Local API configuration; must not be committed. |
| `Output/` | Contains screenshots of the three systems. |

## Security Note

The assignment records are local project data for this practice task. Treat them as private data in a real application.

Never commit `.env`, API keys, or other secrets to GitHub. The project also ignores `.venv/`, which contains the local Python environment and should not be committed. Before pushing changes, check that no secret has been added to a tracked file.

## Conclusion

This Assignment Tracker demonstrates three distinct approaches to the same problem. The plain chatbot can communicate and provide general guidance but cannot access private records. The rule-based workflow gives predictable results for predefined questions. The AI agent adds flexible language understanding and tool-based access to the local assignment data.

Together, the three implementations provide a practical introduction to the differences between an LLM response, a deterministic workflow, and an agentic system.