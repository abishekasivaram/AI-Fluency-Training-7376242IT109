# Day 2 Task: Reasoning and Acting Analysis

## Scenario: Gym Membership Management System

This project evaluates three prompting approaches — Direct Prompting, Chain-of-Thought (CoT), and ReAct — using a fictional Gym Membership Management System. The system contains private membership prices, service prices, and discount information.

The private gym data used in this experiment is:

| Category | Details |
|---|---|
| Basic Membership | ₹1,000/month |
| Standard Membership | ₹1,500/month |
| Premium Membership | ₹2,000/month |
| Personal Trainer | ₹3,000/month |
| Diet Plan | ₹1,000/month |
| Fitness Assessment | ₹500 one-time |
| 3-month membership discount | 10% |
| 6-month membership discount | 15% |
| 12-month membership discount | 20% |

The main objective is to demonstrate how the three approaches behave when solving questions that require either reasoning, private information, or both.

---

# 3.1 Explanation of Each Approach

## 1. Direct Prompting

Direct prompting sends the user's question directly to the language model without giving it access to external tools. The model generates an answer based only on the information available in the prompt and its learned knowledge.

For this experiment, the following question was used:

> A customer wants a Premium gym membership for 6 months with a Personal Trainer. Find the total cost after applying the applicable membership discount.

The private gym prices were deliberately not included in the prompt, and no tools were provided to the model.

The model returned a specific answer of **$1,380**. It assumed a Premium membership price of $200 per month, a Personal Trainer price of $50 per month, and a 10% discount. None of these values matched the private gym data used in this experiment.

This demonstrates the main limitation of direct prompting for this scenario. The model can answer immediately and may produce a confident response, but it cannot retrieve information from the private gym system. When required information is missing, it may make unsupported assumptions.

Direct prompting therefore works well for simple questions, general explanations, or creative tasks where external information is not required. However, it is unreliable when the answer depends on private or changing data.

---

## 2. Chain-of-Thought Prompting

Chain-of-Thought prompting asks the model to work through a multi-step problem before producing its final answer. In this experiment, all the required information was explicitly supplied in the prompt.

The question was:

> A customer chooses the Standard gym membership for 6 months. The Standard membership costs ₹1,500 per month. The customer also purchases a Diet Plan for all 6 months. The Diet Plan costs ₹1,000 per month. A 15% discount is applied only to the membership fee. Calculate the final amount.

The model calculated the membership cost, calculated the discount, subtracted the discount from the membership fee, calculated the diet-plan cost, and finally added the two amounts.

The model correctly produced a final answer of **₹13,650**.

The calculation was:

Standard membership:

₹1,500 × 6 = ₹9,000

15% discount:

₹9,000 × 0.15 = ₹1,350

Discounted membership:

₹9,000 − ₹1,350 = ₹7,650

Diet Plan:

₹1,000 × 6 = ₹6,000

Final amount:

₹7,650 + ₹6,000 = **₹13,650**

This experiment shows that Chain-of-Thought can improve performance on multi-step reasoning when all required information is already available in the prompt. However, Chain-of-Thought does not provide access to the private gym database. If the membership price or discount were unknown, the model would still be unable to retrieve the correct value without an external tool.

---

## 3. ReAct Agent

The ReAct approach combines reasoning with actions. Instead of attempting to answer immediately, the agent identifies the information it needs, calls an appropriate tool, observes the result, and continues until it has enough information to produce an answer.

The question used for the ReAct experiment was:

> A customer wants a Premium gym membership for 6 months with a Personal Trainer. Find the total cost after applying the applicable membership discount.

The prices and discount were not included in the question. Instead, the agent had access to four tools:

- `get_membership_price()`
- `get_service_price()`
- `get_discount()`
- `calculator()`

The agent first called `get_membership_price()` and retrieved the Premium membership price of ₹2,000 per month. It then called `get_discount()` and retrieved the 6-month discount of 15%. Next, it called `get_service_price()` and retrieved the Personal Trainer price of ₹3,000 per month.

Finally, the agent used the calculator tool to calculate the final amount.

The calculation was:

Premium membership:

₹2,000 × 6 = ₹12,000

15% discount:

₹12,000 × 0.15 = ₹1,800

Discounted membership:

₹12,000 − ₹1,800 = ₹10,200

Personal Trainer:

₹3,000 × 6 = ₹18,000

Final amount:

₹10,200 + ₹18,000 = **₹28,200**

The ReAct agent therefore produced the correct final answer of **₹28,200** using the private tool data.

The experiment demonstrates the main advantage of ReAct: it can combine reasoning with external information retrieval and computation. It is therefore suitable for problems where the model needs information that is not contained in the original prompt.

---

# 3.2 Comparison Table

| Basis for comparison | Direct Prompting | Chain-of-Thought | ReAct Agent |
|---|---|---|---|
| Reasoning depth | Low; answers directly from the prompt and learned knowledge. | Higher; breaks a supplied problem into multiple reasoning steps. | High; reasons about the problem and determines which tools are required. |
| Tool usage | No tools. | No tools. | Uses membership, service, discount, and calculator tools. |
| Reliability on multi-step questions | Can be unreliable when information is missing or calculations are complex. | More reliable when all required information is provided. | High for tasks requiring both reasoning and external data, provided the tools and instructions are correct. |
| Transparency | Limited; gives an answer without showing a reasoning process. | The generated solution can show the calculation steps. | Tool actions and observations can be displayed, showing how external information was obtained. |
| Speed / cost | Fastest because it requires only one model response. | Slower because the response contains additional reasoning. | Generally slower because it may require several tool calls and model interactions. |
| Consistency across repeated runs | Can vary depending on temperature and prompt. | Can vary in wording or reasoning path. | Tool results themselves are deterministic, although the agent's tool-calling sequence may vary. |

---

# 3.3 Self-Consistency Observation

Self-consistency was tested using the following reasoning question:

> A gym member chooses the Basic plan for 12 months at ₹1,000 per month. A 20% discount is applied to the membership fee. The member also pays a one-time registration fee of ₹500. What is the final amount the member must pay?

The correct calculation is:

₹1,000 × 12 = ₹12,000

20% discount = ₹2,400

₹12,000 − ₹2,400 = ₹9,600

₹9,600 + ₹500 = **₹10,100**

The question was run five times at a temperature of 0.8. All five runs returned the same numerical answer:

| Run | Answer |
|---|---:|
| Run 1 | ₹10,100 |
| Run 2 | ₹10,100 |
| Run 3 | ₹10,100 |
| Run 4 | ₹10,100 |
| Run 5 | ₹10,100 |

The majority answer was therefore **₹10,100**, with a frequency of **5 out of 5**, and the answer was correct.

The same question was then tested five times at temperature 0. All five runs also returned ₹10,100. The numerical answers were therefore identical across the five temperature-0 runs.

An important observation is that temperature 0.8 allows more variation in generated wording, but variation did not occur in the numerical answer during these five runs. Therefore, this particular experiment did not demonstrate different numerical answers at temperature 0.8. It instead showed that the model was numerically consistent for this relatively simple calculation.

---

# 3.4 Suitability Analysis

For the Gym Membership Management System, the ReAct approach is the most appropriate of the three for questions involving private membership information. The main reason is that the system contains information that is not included in the user's question, such as membership prices, service prices, and discount rates.

The Direct Prompting experiment demonstrated this limitation clearly. Without access to the private gym data, the model generated its own assumed prices and discount and returned $1,380 instead of using the actual gym data.

The Chain-of-Thought experiment demonstrated that careful multi-step reasoning can produce the correct answer when all necessary information is supplied. The model correctly calculated ₹13,650 when the membership price, diet-plan price, duration, and discount were included in the prompt. However, CoT alone cannot retrieve missing information from the private gym system.

The ReAct experiment addressed both requirements. The agent retrieved the required private information through tools and then used a calculator to perform the final calculation. It obtained ₹2,000 for the Premium membership, ₹3,000 for the Personal Trainer, and a 15% discount for six months, resulting in the correct final amount of ₹28,200.

The self-consistency experiment also showed that the model produced the correct numerical answer consistently across five runs at temperature 0.8 and five runs at temperature 0. This suggests that, for a simple deterministic calculation with all information supplied, repeated generation did not introduce numerical variation in this experiment.

Therefore, for this particular scenario, ReAct is appropriate when the question requires private or dynamic gym information. Direct Prompting remains useful for simple general questions, while Chain-of-Thought is useful for multi-step calculations when the required data is already available.

---

# 3.5 Conclusion

The three approaches are useful for different types of problems.

Direct Prompting is appropriate for simple questions, general explanations, summarization, creative writing, and other tasks where the required information is already available to the model or does not require external verification. Its main advantage is speed and simplicity, but it cannot retrieve private information through tools.

Chain-of-Thought is useful when a problem requires several logical or mathematical steps and all the necessary information is already provided. The Gym Membership experiment showed that the model could correctly calculate a multi-step membership bill when the prices and discount were included in the prompt. However, reasoning alone does not give the model access to unavailable external information.

ReAct is useful when a problem requires both reasoning and interaction with external tools. In the Gym Membership scenario, the agent retrieved private membership prices, service prices, and discount information before performing the final calculation. This allowed it to solve a problem that Direct Prompting could not reliably solve because the required information was not present in the prompt.

Overall, the experiment demonstrates that the choice of prompting approach depends on the nature of the problem. Direct Prompting is suitable for straightforward tasks, Chain-of-Thought is useful for multi-step reasoning with known information, and ReAct is appropriate when reasoning must be combined with external data retrieval or tool-based actions.