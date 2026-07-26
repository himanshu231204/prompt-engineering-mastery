# Mini Project: Auto Prompt Optimizer

Uses meta-prompting to iteratively optimize prompts for specific tasks. Evaluates prompt quality, generates improvements, and produces a comparison artifact showing initial vs. optimized prompt performance.

## What It Does

1. Takes a task description and a mediocre initial prompt
2. Runs an iterative meta-prompting optimization loop:
   - **Evaluate**: LLM scores the prompt on clarity, specificity, and correctness (1-10)
   - **Optimize**: LLM generates an improved prompt based on evaluation feedback
   - **Repeat** for N iterations
3. Tests the final optimized prompt against sample inputs
4. Prints a score progression table and prompt comparison
5. Saves results to `results.json` for portfolio use

## How to Run

```bash
# Default (OpenAI, 3 iterations)
python solution.py

# Use Anthropic
python solution.py --provider anthropic

# Use Ollama (local)
python solution.py --provider ollama

# More refinement rounds
python solution.py --iterations 5

# Run the second demo task (news headline extraction)
python solution.py --task-index 1
```

Requires `.env` with API keys (see `../../.env.example`).

## Expected Output

```
======================================================================
  AUTO PROMPT OPTIMIZER — RESULTS
======================================================================

Task: Classify a customer support email as: URGENT, BILLING, TECHNICAL, or GENERAL
Iterations: 3
Total time: 12.4s

SCORE PROGRESSION:
Iter   Clarity  Specific   Correct   Average
--------------------------------------------------
1            4         3         5       4.0
2            7         7         8       7.3
3            9         8         9       8.7
--------------------------------------------------
Improvement: +4.7 avg points

PROMPT COMPARISON:

BEFORE (initial):
  Read this email and tell me what it's about.

AFTER (optimized):
  Classify the following customer support email into exactly one
  category: URGENT, BILLING, TECHNICAL, or GENERAL.
  Return ONLY the category label, nothing else.

  Email: {input}

  Category:

TEST CASE RESULTS:
----------------------------------------------------------------------
Test 1: Hi, I was charged twice for my subscription...
  Output: BILLING

Test 2: My app keeps crashing when I try to upload...
  Output: TECHNICAL
...
```

Results are also saved to `results.json` as a machine-readable artifact.

## Visible Artifact

The optimizer produces two artifacts:
- **Console table**: Score progression + prompt comparison (screenshot this)
- **results.json**: Full optimization data including all iterations, scores, and test results

## Techniques Demonstrated

This mini-project directly applies Module 4 concepts:

- **Meta Prompting**: The core optimization loop (evaluate → optimize → repeat)
- **LLM-as-Judge**: Using the model to evaluate prompt quality
- **Iterative Refinement**: Progressive improvement through feedback
- **Prompt Chaining**: The evaluation → optimization pipeline is itself a chain
