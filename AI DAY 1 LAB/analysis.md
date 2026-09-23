# Day 1 Task: Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## 1. Scenario

The scenario selected for this task is a **Student Assignment Tracker**. The system contains private assignment information such as assignment name, subject, status, and due date.

The assignment data used in this project is:

| Assignment | Subject | Status | Due Date |
|---|---|---|---|
| Python Recursion | Python | Pending | 2026-09-24 |
| CN Lab Record | Computer Networks | Completed | 2026-09-23 |
| IoT Mini Project | IoT | Pending | 2026-09-26 |
| Multimedia Assignment | Multimedia | Pending | 2026-09-25 |
| Communication Record | Communication | Completed | 2026-09-22 |

The same scenario and the same private data are used to compare the three approaches.

The questions tested were:

1. What is the status of my Python Recursion assignment?
2. Which assignments are still pending?
3. Which pending assignment is due first?
4. I have two days available. Which pending assignment should I complete first?

---

## 2. Plain Chatbot

The plain chatbot uses an LLM to generate responses but does not have access to the student's private assignment records. It does not use assignment lookup tools or predefined rules.

For the first question, the chatbot explained that it could not access the student's personal assignment records and therefore could not provide the assignment status. For the questions about pending assignments and due dates, it similarly explained that it did not have access to the private data.

For the final question, the chatbot could still provide general advice, such as considering due dates, effort, importance, and available time. However, it could not identify the student's actual assignment because the private assignment information was not available to it.

This demonstrates the main limitation of a plain chatbot in this scenario. It can understand the language of the user's request and provide useful general guidance, but it cannot reliably answer questions that depend on private assignment data that has not been provided to the model.

---

## 3. Rule-Based Workflow

The rule-based workflow directly accesses the private assignment data stored in `data.py`. It does not use an LLM. Instead, it uses predefined conditions and Python operations to determine how each question should be handled.

For the first question, the workflow searches for the Python Recursion assignment and returns its status and due date. For the second question, it filters the records whose status is `Pending`. For the third question, it filters the pending assignments and compares their due dates to find the earliest deadline. For the fourth question, it again identifies the pending assignment with the earliest deadline and recommends completing it first.

The workflow produced correct and predictable answers for all four tested questions. Its main limitation is flexibility. The program depends on predefined rules, so a differently worded question or a new type of request may require additional conditions to be added to the code.

---

## 4. AI Agent

The AI agent combines an LLM, tools, and a loop. The private assignment data is not directly placed into the LLM's prompt. Instead, the agent can access it through the `get_assignment_info` tool.

When a user asks a question, the LLM first determines whether a tool is required. If private assignment information is needed, it requests the appropriate tool. The Python program executes the tool and sends the result back to the LLM. The LLM then observes the result and produces the final answer.

For example, when asked about the Python Recursion assignment, the agent called `get_assignment_info` with the assignment name and received its status and due date. When asked for all pending assignments, it called the same tool with the `Pending` status. For the question about the earliest deadline, it retrieved the pending assignments and determined that Python Recursion was due first.

In the final question, the agent again retrieved the pending assignments and identified Python Recursion as the assignment with the earliest due date. This demonstrates the LLM + Tools + Loop structure of an AI agent.

---

## 5. Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | High for general language and open-ended conversation | Limited to predefined rules and conditions | High because the LLM can interpret different requests |
| Decision-making | Generates responses but has no access to the private records | Decisions are explicitly programmed in the rules | LLM decides which tool to use and how to proceed |
| Tool usage | No tools | No external AI tools; directly uses predefined program logic | Uses tools such as `get_assignment_info`; calculator is available when arithmetic is required |
| Private-data access | No access to the assignment records | Direct access to `data.py` | Accesses private data through tools |
| Multi-step task handling | Limited when private information is required | Can perform programmed multi-step operations | Can retrieve information, observe results, and continue through the agent loop |
| Automation | Can generate general guidance but cannot automate access to the private tracker | Automates predefined assignment operations | Automates information retrieval and decision-making through LLM + tools |
| Reliability | Reliable about its lack of access in the tested scenario, but cannot answer private-data questions | Predictable for the cases covered by its rules | Can handle flexible requests, but depends on LLM tool selection and behavior |

---

## 6. Suitability Analysis

For the Student Assignment Tracker scenario, the **AI agent is the most suitable approach when the user wants flexible natural-language interaction with private assignment data**. The agent can understand the user's request, select the assignment information tool, observe the returned data, and produce an answer without requiring a separate hard-coded rule for every possible wording of the question.

The rule-based workflow is also suitable when the required questions are fixed and predictable. It produced correct results for all four tested questions and has deterministic program logic. However, new question patterns or new types of decisions would require additional rules to be programmed.

The plain chatbot is useful for general guidance and conversational interaction, but it is not suitable for answering questions that require access to the student's private assignment records because it does not have access to that data.

Therefore, for this particular scenario, the AI agent provides the most flexible interaction with the private assignment data, while the rule-based workflow provides predictable behavior for predefined tasks.

---

## 7. Conclusion

A plain chatbot, a rule-based workflow, and an AI agent solve problems in different ways.

A plain chatbot is appropriate when the main requirement is natural-language conversation, explanation, or general assistance and private-data access is not required.

A rule-based workflow is appropriate when the problem has clearly defined conditions, predictable inputs, and deterministic steps. It is useful when consistent and explicitly programmed behavior is important.

An AI agent is appropriate when a problem requires natural-language understanding together with access to tools or private data and may involve multiple steps. The agent can use an LLM to interpret the request, select appropriate tools, observe their results, and continue until the task is completed.

The Assignment Tracker demonstrates the difference between these approaches using the same private-data scenario. The chatbot could provide general guidance but could not access the records, the workflow could reliably process predefined operations, and the agent could combine an LLM with tools and a loop to interact with the private assignment data.