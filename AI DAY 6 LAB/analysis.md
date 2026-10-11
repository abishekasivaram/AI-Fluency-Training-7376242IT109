# Day 6: Reliable Tool Calling

## 1. Scenario

My project is a College Mess Assistant. It uses two tools: `get_mess_timing` and `get_menu`. The model decides when a tool may be useful, but Python validates the arguments and executes the function.

The menu data is currently unconfigured. Therefore, the assistant must not invent menu items.

## 2. Concepts

### Chat Completions

Chat Completions sends a `messages` array to the model. Each message contains a role and content. A tool-enabled request can also include `tools`, `tool_choice`, and generation parameters.

The response contains choices with an assistant message and a `finish_reason`.

- `stop`: the assistant turn ended normally.
- `length`: generation stopped because of the token limit; the program may retry with a larger limit.
- `tool_calls`: the model requested tool execution.

When the model requests a tool, `message.content` may be empty because its response contains tool-call instructions instead of ordinary text.

### OpenAI-compatible APIs

An OpenAI-compatible server accepts requests using an API format similar to OpenAI's API. A client can often connect to another provider by changing the base URL, model name, and credentials.

Compatibility does not guarantee identical model behaviour or support for every API feature.

### Streaming

Streaming delivers response chunks while generation is in progress. It can reduce the time a user waits before seeing output.

An agent loop often disables streaming for tool decisions because it needs to collect and inspect the complete tool-call response before processing it.

The Responses API uses a different request and event structure from Chat Completions. This project uses Chat Completions because the assignment focuses on that format.

### Five steps of tool calling

1. Python sends conversation messages and tool definitions to the model.
2. The model returns a tool-call request.
3. Python parses the arguments and validates them against the schema.
4. Python executes the approved function and returns a tool message containing its result.
5. Python sends the updated conversation back to the model, which produces the final answer.

The model does not execute Python functions. My application does, so tool-call arguments must be treated as untrusted input.

### JSON Schema and tool choice

The tool definitions use descriptions, properties, required arguments, enums, `additionalProperties: false`, and `strict`.

- `description` explains the tool's purpose.
- `properties` defines accepted arguments.
- `enum` restricts meal names.
- `required` prevents omitted mandatory arguments.
- `additionalProperties: false` rejects extra arguments.
- `strict` requests stricter schema adherence when supported.

`tool_choice: auto` lets the model decide whether to call a tool. `none` prohibits tool calls. `required` requires a tool call. A named function directs the model to a specific tool when supported.

### JSON mode and schema mode

JSON mode requests valid JSON but does not necessarily enforce a particular structure. Schema mode requests data matching a specified schema.

Tools are appropriate when the program must fetch information or calculate something. Structured outputs are appropriate when the program needs data in a predictable format.

Correctly shaped JSON can still contain incorrect or unsupported information, so application-level checks remain necessary.

### Parallel tool calls

A model can request multiple tools in one response. The application must process each call and return one tool message for every `tool_call_id` before asking the model to continue.

If a tool-call ID is left unanswered, the conversation may be rejected or the agent loop may fail.

### Validation, repair and fault injection

The validator checks JSON parsing, tool names, required arguments, unexpected arguments, argument types, and enum values before execution.

A repair pattern returns useful error messages to the model rather than allowing invalid input to crash the application. Truncated output can be retried with a larger token limit, while malformed tool arguments can be reported to the model for correction.

Fault injection tests deliberately constructed failures without relying on the model to generate them. It helps test application safeguards consistently.

A schema can prevent an unsupported meal name from being accepted, but it cannot guarantee that the stored meal timing is factually correct.

## 3. Tool Calling vs Structured Outputs

| Basis | Tool calling | Structured outputs |
|---|---|---|
| Model's task | Request an action | Produce formatted data |
| Who performs the action? | Application code executes the tool | Application consumes the generated data |
| Shape control | Tool schema and validation | JSON mode or output schema |
| Remaining risks | Invalid arguments, incorrect data, execution errors | Incorrect facts or unsupported values |
| Application safeguards | Validate before executing | Parse and validate before consuming |
| Provider support | Depends on server and model | Depends on server and model |
| Fetch or calculate | Preferred when external action is needed | Not a replacement for executing a tool |
| Extract fields from text | Can be used, but may be unnecessary | Preferred when only structured data is needed |

## 4. Experimental Results

Complete the following tables after running the programs. Record actual output and do not assume every provider feature succeeded.

### 4.1 Fault Injection

| Fault | Returned message | Continued (Y/N) |
|---|---|---|
| Invalid JSON | Pending test | Pending test |
| Unknown tool | Pending test | Pending test |
| Missing argument | Pending test | Pending test |
| Wrong type | Pending test | Pending test |
| Invalid enum | Pending test | Pending test |
| Extra argument | Pending test | Pending test |
| Wrong JSON shape | Pending test | Pending test |
| Null argument | Pending test | Pending test |

### 4.2 Agent Behaviour

| Question | Steps | Tool calls | Parallel? | Finish reason `length`? | Actual final answer |
|---|---|---|---|---|---|
| What time is lunch served? | Pending test | Pending test | Pending test | Pending test | Pending test |
| What is the lunch menu? | Pending test | Pending test | Pending test | Pending test | Pending test |
| Tell me breakfast and dinner timings | Pending test | Pending test | Pending test | Pending test | Pending test |
| Hello, how are you? | Pending test | Pending test | Pending test | Pending test | Pending test |

### 4.3 Structured Outputs

| Mode | Provider response | Valid JSON? | Expected schema? |
|---|---|---|---|
| Unconstrained | Pending test | Pending test | Pending test |
| JSON mode | Pending test | Pending test | Pending test |
| Schema mode | Pending test | Pending test | Pending test |

### 4.4 Before and After Guards

Run a controlled comparison between the unguarded and guarded versions before completing this table.

| Measure | Before guards | After guards |
|---|---|---|
| Invalid input handling | Pending test | Pending test |
| Steps used | Pending test | Pending test |
| Final result | Pending test | Pending test |
| Repeated-call behaviour | Pending test | Pending test |

## 5. Suitability and Conclusion

Tool calling is suitable when the College Mess Assistant needs to retrieve configured timings or menus through application functions. Structured outputs are more suitable when extracting fixed fields from a sentence.

The model's tool calls cannot be trusted automatically because the generated arguments may be malformed, incomplete, or outside the permitted values. Every call must be parsed, validated, checked against an allowed tool, and executed safely. Every tool-call ID must receive a response.

Schemas prevent certain structural mistakes but cannot guarantee factual correctness or protect against every execution failure. Fault injection allows the safeguards to be tested deliberately and repeatedly, even when the model does not naturally produce an error.

Complete this conclusion with the actual failures observed during testing and the most effective safeguard in this experiment.
