import pypandoc

markdown = r"""# Day 4 Assessment — Will It Fit, and May I Use It?

**Date checked:** 3 October 2026  
**Scenario:** A college AI assistant running locally on an 8 GB RAM laptop without a dedicated GPU. It should answer student questions and support tool-calling tasks used in the Unit 1 agent labs. The model should fit the memory budget and use an Apache 2.0 or MIT licence.

> **Evidence note:** The Ollama measurements below are from my actual Windows system. Model-card and Ollama-library facts were checked on 3 October 2026. Estimates are formula-based approximations, not guarantees of exact runtime memory.

## 3.1 Key concepts

### Model weights
Model weights are the learned numerical parameters that the model uses to generate responses. Their memory requirement mainly depends on the number of parameters and the precision used to store them. If I ignore weight size, I may choose a model that cannot be loaded into available memory. The estimate is useful for planning, but actual memory also depends on runtime and implementation details.

### Quantization
Quantization stores model weights using fewer bits than full precision. In the lab formula, Q4_K_M uses 0.57 bytes per parameter, while FP16 uses 2 bytes per parameter. Quantization reduces memory and disk requirements, but can reduce response quality in some tasks. I should test the quantized model on my own prompts rather than assuming that the smallest model always performs best.

### KV cache and context length
The key-value (KV) cache stores information used while processing the conversation context. In the lab's simplified formula, KV-cache memory grows with both parameter count and context length. A larger context can help a model handle longer prompts, but it also increases memory use. I should choose a context length that matches the task instead of automatically selecting the maximum supported context.

### Model card
A model card is the model publisher's documentation. It describes intended uses, capabilities, limitations, supported context, and often the licence. I used official Hugging Face model cards and the Ollama library pages to check these details. A model card is useful evidence, but I should still check the exact model variant and its licence before distributing or deploying it.

### Open-weight versus open-source
An open-weight model makes its trained weights available, but that alone does not mean every part of the model or its training data is open source. The exact licence determines permissions and obligations. For this scenario, I need an Apache 2.0 or MIT licence and must preserve applicable notices and comply with the licence terms. Commercial use, redistribution, and other conditions must be checked for the exact version instead of inferred from the phrase “open model.”

## 3.2 Memory estimates and model comparison

### A. Memory estimate table

The lab formula is:

- **Weights (GB)** = parameters in billions × bytes per parameter
- **KV cache (GB)** = parameters in billions × context in K tokens × 0.02
- **Total (GB)** = (weights + KV cache) × 1.10

The available-memory budget used for this exercise is **8 GB**. The verdict is a simplified comparison against that budget and does not guarantee that a model will run comfortably alongside the operating system and other applications.

| Configuration | Weights (GB) | KV cache (GB) | Estimated total (GB) | Verdict against 8 GB |
|---|---:|---:|---:|---|
| 1.5B Q4_K_M, 8K | 0.85 | 0.24 | 1.20 | Fits comfortably |
| 8B Q4_K_M, 8K | 4.56 | 1.28 | 6.42 | Fits, but tight |
| 8B FP16, 8K | 16.00 | 1.28 | 19.01 | Does not fit |
| 30B Q4_K_M, 8K | 17.10 | 4.80 | 24.09 | Does not fit |
| 70B Q4_K_M, 8K | 39.90 | 11.20 | 56.21 | Does not fit |

### B. Four-model comparison

The three families compared are Qwen, Mistral, and IBM Granite. The published context column reflects the Ollama library listing checked on 3 October 2026. Estimates use the same **8K context** to make the memory figures comparable. Model sizes on the Ollama library are approximate download sizes and can change by tag or build.

| Full model/version | Publisher/family | Parameters | Published context in Ollama | Exact licence shown | Commercial use / conditions | Tool calling documented? | Ollama Q4 download size | Estimated total at Q4, 8K | Fit against 8 GB? |
|---|---|---:|---:|---|---|---|---:|---:|---|
| `qwen2.5:1.5b` | Alibaba Cloud / Qwen | 1.54B | 32K listing; active run was 4K | Apache License 2.0 | Apache 2.0 permits commercial use subject to its terms, including retaining required notices and licence text | Yes; Ollama page lists tools | 986 MB | 1.07 GB | Yes; locally verified on CPU |
| `mistral:7b` (Mistral 7B v0.3 family) | Mistral AI / Mistral | 7B | 32K | Apache License 2.0 | Apache 2.0 terms and notices apply | Yes; v0.3 documents function calling | 4.4 GB | 5.62 GB | Estimated to fit, but tight in practical use |
| `granite3.3:2b` | IBM / Granite | 2B | 128K | Apache License 2.0 | Apache 2.0 terms and notices apply | Yes; Granite 3.3 documents function-calling tasks | 1.5 GB | 1.61 GB | Estimated to fit |

**Sources checked on 3 October 2026:**

- Qwen2.5 1.5B on Ollama: https://ollama.com/library/qwen2.5:1.5b
- Qwen2.5 1.5B Instruct model card: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct
- Mistral 7B on Ollama: https://ollama.com/library/mistral
- Mistral 7B Instruct v0.3 model card: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3
- IBM Granite 3.3 on Ollama: https://ollama.com/library/granite3.3
- IBM Granite 3.3 2B Instruct model card: https://huggingface.co/ibm-granite/granite-3.3-2b-instruct

The Ollama model pages identify the listed quantized builds and their approximate download sizes. The publishers' model cards identify the model versions and licence metadata. The licence label is not a substitute for reading the full licence before a real deployment.

### C. How the estimates were calculated

For `qwen2.5:1.5b`, the Ollama page reports 1.54B parameters and a 986 MB Q4_K_M build. Using the lab's rounded 1.5B parameter value:

- Weights = 1.5 × 0.57 = 0.855 GB
- KV cache at 8K = 1.5 × 8 × 0.02 = 0.24 GB
- Total = (0.855 + 0.24) × 1.10 = 1.2045 GB, or approximately 1.20 GB

For the 7B Mistral configuration:

- Weights = 7 × 0.57 = 3.99 GB
- KV cache at 8K = 7 × 8 × 0.02 = 1.12 GB
- Total = (3.99 + 1.12) × 1.10 = 5.621 GB, or approximately 5.62 GB

For the 2B Granite configuration:

- Weights = 2 × 0.57 = 1.14 GB
- KV cache at 8K = 2 × 8 × 0.02 = 0.32 GB
- Total = (1.14 + 0.32) × 1.10 = 1.606 GB, or approximately 1.61 GB

These are estimates using the assessment's formula. They are not measured memory results for Mistral or Granite; I have not installed those models on my machine.

## 3.3 Context and quantization experiments

### A. Change context length while keeping quantization constant

Configuration: **8B Q4_K_M**, with 8 GB available.

| Context | Weights (GB) | KV cache (GB) | Estimated total (GB) | Fit? |
|---|---:|---:|---:|---|
| 4K | 4.56 | 0.64 | 5.72 | Fits, but tight |
| 8K | 4.56 | 1.28 | 6.42 | Fits, but tight |
| 32K | 4.56 | 5.12 | 10.65 | Does not fit |
| 128K | 4.56 | 20.48 | 27.54 | Does not fit |

The weights remain constant because the parameter count and quantization do not change. The KV cache grows with context length, so the total estimated memory rises from 5.72 GB at 4K to 27.54 GB at 128K. Under an 8 GB budget, 4K uses the least memory in this experiment; 8K leaves less headroom, and 32K and 128K exceed the budget.

### B. Change quantization while keeping context constant

Configuration: **8B model at 8K context**, with 8 GB available.

| Quantization | Weights (GB) | KV cache (GB) | Estimated total (GB) | Fit? |
|---|---:|---:|---:|---|
| Q3_K_M | 3.44 | 1.28 | 5.19 | Fits comfortably by the script's rule |
| Q4_K_M | 4.56 | 1.28 | 6.42 | Fits, but tight |
| Q5_K_M | 5.44 | 1.28 | 7.39 | Fits, but tight |
| Q8_0 | 8.00 | 1.28 | 10.21 | Does not fit |
| FP16 | 16.00 | 1.28 | 19.01 | Does not fit |

At fixed context length, the KV-cache estimate remains the same, while the weight memory changes with quantization. Lower-bit quantization reduces memory, but may reduce quality; higher precision generally requires more memory. For the 8 GB scenario, Q4_K_M is a practical starting point for an 8B model, while the 1.5B Q4_K_M model leaves more memory headroom for the operating system and other applications. Quality should still be tested against the actual tasks.

## 3.4 Actual installed-model verification

I installed and ran `qwen2.5:1.5b` with Ollama on Windows.

| Measurement | Actual observation |
|---|---|
| Model | `qwen2.5:1.5b` |
| Model ID | `65ec06548149` |
| `ollama list` size | 986 MB |
| `ollama ps` size | 1.2 GB |
| Processor | 100% CPU |
| Active context reported by `ollama ps` | 4096 tokens |
| Status | Model downloaded and started successfully |

The downloaded size of 986 MB is the on-disk model footprint. The 1.2 GB shown by `ollama ps` is the runtime size reported while the model was loaded. They measure different things, so they should not be expected to match exactly.

My initial 1.5B Q4_K_M estimate at 8K context was 1.20 GB. However, the actual Ollama run showed a 4096-token context, so a like-for-like 4K estimate is:

- Weights = 1.5 × 0.57 = 0.855 GB
- KV cache at 4K = 1.5 × 4 × 0.02 = 0.12 GB
- Total = (0.855 + 0.12) × 1.10 = 1.0725 GB, approximately 1.07 GB

The measured runtime size of 1.2 GB is approximately 0.13 GB higher than this simplified 4K estimate. This difference can result from runtime allocations and the limitations of the simplified formula. The `100% CPU` result means the model was fully assigned to CPU processing; no GPU offload was reported for this run. The 986 MB download size alone would not show this processor allocation.

**Evidence to include:** screenshots of `ollama list` and `ollama ps` showing the model, size, CPU allocation, and context.

## 3.5 Recommendation for the scenario

I recommend **`qwen2.5:1.5b` in Q4_K_M, using a 4K active context initially**, for the 8 GB CPU-only college-assistant scenario. It is the model I actually installed and ran, its download size was 986 MB, and Ollama reported a 1.2 GB runtime size with 100% CPU allocation. The Ollama page lists Apache License 2.0 and tool support for this model family. This choice leaves more memory headroom than the estimated 7B alternative and directly meets the need to run locally for the agent labs.

**Runner-up:** `granite3.3:2b` in a Q4 build. Its Ollama listing shows an approximate 1.5 GB download, Apache 2.0 licensing, a 128K published context window, and function-calling tasks. Its estimated total at 8K is approximately 1.61 GB. I did not install it, so its fit and actual runtime behaviour remain unverified on my machine. I choose the already tested Qwen model for this exercise because I have direct runtime evidence for it.

I would reconsider the recommendation if the assistant needed substantially stronger performance on complex reasoning or coding, if more users had to run it concurrently, or if the available memory or hardware changed. I would then benchmark candidate models on representative tasks and measure actual runtime memory before deciding.

## 3.6 Conclusion

Model size, quantization, context length, and licence address different constraints. Size and quantization determine much of the weight-memory requirement; context length affects KV-cache memory; the machine's available RAM and runtime overhead determine whether the model can run reliably. A model can fit the arithmetic estimate but still compete with the operating system and other applications for memory.

For a memory-driven decision, an 8 GB CPU-only laptop is better served by testing a small quantized model first than assuming a 7B or larger model will run comfortably. For a licence-driven decision, a project that will be redistributed or used commercially must check the exact model version's licence and follow its conditions, regardless of how small the download is. “Open-weight” by itself is not enough to establish that the intended use is permitted.

The estimator is a planning tool, not a precise runtime predictor. I compared its result with a real Ollama run and recorded both the on-disk size and runtime size separately. Before a real deployment, I would test output quality, memory under realistic prompts, tool-calling behaviour, and the full licence terms.

## Evidence checklist

- [ ] Screenshot of the Python estimator output
- [ ] Screenshot of context-length comparison
- [ ] Screenshot of quantization comparison
- [ ] Screenshot of `ollama list`
- [ ] Screenshot of `ollama ps`
- [ ] Screenshot or saved reference for the Qwen2.5 model card and licence
- [ ] Screenshot or saved reference for the Mistral model card and licence
- [ ] Screenshot or saved reference for the Granite model card and licence
- [ ] Verify that the screenshots are stored in `AI DAY 4 LAB/screenshots/`
"""

output_path = "/mnt/data/analysis_day4.md"
pypandoc.convert_text(
    markdown,
    to="md",
    format="md",
    outputfile=output_path,
    extra_args=["--standalone"],
)
print(f"Created: {output_path}")
