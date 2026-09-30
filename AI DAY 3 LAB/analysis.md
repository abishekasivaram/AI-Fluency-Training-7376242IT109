# Day 3 Task: From Prompt to Action

## Scenario: College Fee Notice

This project demonstrates the difference between a plain Large Language Model (LLM) and an LLM that has access to one external tool. The scenario is a college fee assistant. A file named `notice.html` contains course fee information and a merit scholarship percentage.

The notice contains the following information:

* CS101 course fee: ₹40,000
* AI202 course fee: ₹50,000
* Merit scholarship: 20%

The main question is:

> Read the college notice and tell me the total fee for CS101 and AI202 after the merit scholarship.

The correct calculation is:

CS101 + AI202 = ₹40,000 + ₹50,000 = ₹90,000

20% scholarship = ₹18,000

Final fee = ₹90,000 − ₹18,000 = ₹72,000

---

## 3.1 Explanation of Concepts

### Large Language Model

A Large Language Model is an AI model trained on large amounts of text that can understand and generate natural language. It can answer general questions using patterns and knowledge learned during training.

For example, the question "What is the purpose of a merit scholarship?" does not require the college notice. A plain LLM can reasonably answer this question from its general knowledge.

However, the LLM does not automatically have access to the current contents of `notice.html`. If asked for the exact fees in that file without being given the file contents, it may not know the answer and could guess or state that it does not have access to the notice.

Therefore, a plain LLM can generate an answer from its existing knowledge, but it cannot automatically retrieve information from a local file.

### Agent

An LLM agent is an LLM connected to tools that allow it to perform actions or obtain external information.

In this scenario, the agent has access to one tool called `read_notice`. When the user asks about information contained in the college notice, the agent can decide that it needs the tool, call it, receive the contents of the notice, and then use that information to generate the final answer.

A plain LLM only generates a response from the information available in its prompt and learned knowledge. An agent can interact with an external source through its available tools.

### Tool and Tool Call

A tool is an external function that gives the LLM an ability it does not have by itself. In this project, the tool is `read_notice`.

The tool schema tells the model:

* the tool name: `read_notice`
* what the tool does: reads the college fee notice
* what parameters it accepts

The model needs this description so it can determine when the tool is relevant. Without knowing what a tool does, the model cannot reliably decide when to call it.

A tool call occurs when the LLM requests that the external function be executed.

### Flow of a Tool Call

The tool call in this scenario follows these steps:

1. The user asks for the total fee of CS101 and AI202 after the scholarship.
2. The LLM receives the question and recognizes that the required fee information is in the college notice.
3. The LLM requests the `read_notice` tool.
4. The Python program executes `read_notice()`.
5. The tool reads `notice.html` and returns its contents as text.
6. The tool result is sent back to the LLM.
7. The LLM uses the returned fees and scholarship percentage to calculate the final amount.
8. The LLM produces the final answer of ₹72,000.

This demonstrates how a tool extends the capabilities of an LLM by providing information from an external source.

### Why the Tool Returns Text Instead of Stopping the Program

A tool should return its result as plain text even when something goes wrong. For example, if `notice.html` cannot be found, the tool can return an error message such as "Error reading notice: file not found."

Returning the error as text allows the LLM to receive the result and respond appropriately. If the function instead raises an exception that stops the program, the agent may terminate before the LLM can handle the problem.

---

## 3.2 Comparison Table

| Basis                                                       | Plain LLM Prompt                                                                                      | LLM with One Tool                                                                |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Source of the answer                                        | Learned knowledge and information in the prompt                                                       | Learned knowledge plus information returned by the tool                          |
| Can it fetch or compute information outside its own memory? | No                                                                                                    | Yes, through the available tool                                                  |
| Reliability on factual or numeric questions                 | Good when the required information is already available, but unreliable for unavailable external data | Higher for information contained in the external source                          |
| Transparency                                                | Shows the generated answer but has no external retrieval step                                         | The tool call and tool result can be displayed before the final answer           |
| Speed / cost                                                | Usually faster because there is no tool execution                                                     | Slightly more processing because the tool must be called and its result returned |

---

## 3.3 Minimal Implementation

The implementation contains one external tool called `read_notice`.

The `read_notice` function reads `notice.html` and returns its contents as text.

Two scripts were implemented.

### Plain LLM Script

`direct_prompt.py` sends the user's question directly to the Groq LLM without providing any tools.

For the question requiring the college notice, the LLM does not have access to the actual file contents. Therefore, it cannot reliably retrieve the exact course fees from the notice.

For general questions, the plain LLM can answer without external information.

### Tool-Enabled Script

`my_agent.py` provides the `read_notice` function to the LLM through a function/tool schema.

When the question requires information from the notice, the LLM requests the tool. The Python program executes the function and sends the result back to the LLM. The LLM then uses the returned information to produce the final answer.

The tool-enabled calculation gives:

CS101 = ₹40,000

AI202 = ₹50,000

Combined fee = ₹90,000

Merit scholarship = 20%

Final fee = ₹72,000

---

## 3.4 Observation

Three questions were used to observe the difference between the two approaches.

### Question 1

> Read the college notice and tell me the total fee for CS101 and AI202 after the merit scholarship.

This question genuinely requires the external notice.

The plain LLM does not have access to `notice.html`, so it cannot reliably obtain the exact fee values from the file.

The tool-enabled agent recognizes that the notice is required, calls `read_notice`, receives the fee information, and calculates the final amount.

The final tool-enabled answer is ₹72,000.

### Question 2

> What is the purpose of a merit scholarship?

This is a general conceptual question. The plain LLM can answer it using its general knowledge.

The tool is not necessary for this question.

The tool-enabled agent can also answer it without calling `read_notice`.

### Question 3

> What information is required to calculate the final fee after a scholarship?

This is also primarily a general reasoning question. The required information includes the original fee and the scholarship percentage.

The plain LLM can answer this without external information.

The tool-enabled agent does not need the notice unless the user asks for the actual values.

### Overall Observation

The experiment shows that the plain LLM is sufficient for general knowledge and conceptual questions. However, when the answer depends on information stored in an external file, the tool provides the missing information and improves the reliability of the answer.

---

## 3.5 Suitability and Conclusion

The plain LLM was suitable for questions such as explaining the purpose of a merit scholarship or identifying the information needed for a calculation. These questions did not depend on the contents of the external notice.

The external tool became necessary when the question required the exact fees and scholarship percentage stored in `notice.html`. The LLM could not automatically read the local file by itself. By giving it the `read_notice` tool, the model could request the external information and use it to produce the correct calculation.

More generally, a plain LLM prompt is sufficient when the required information is already contained in the prompt or when the question can reasonably be answered using the model's general knowledge. A tool becomes useful when the task requires external, current, private, local, or computational information that is not available to the model through the prompt alone.

This experiment demonstrates the basic transition from a language model that only generates text to an agent that can interact with an external tool and use the returned result to complete a task.
