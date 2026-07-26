# Mini-Project: Prompt Eval Pipeline

## What It Does

A complete prompt evaluation pipeline that demonstrates the prompt management lifecycle:

1. **PromptRegistry** — A version-controlled store for prompts with metadata, test results, and deployment status tracking
2. **Evaluation Pipeline** — Runs test cases against prompt versions using DeepEval metrics (with a mock fallback if DeepEval isn't installed)
3. **Comparison Report** — Generates a side-by-side comparison of prompt versions with metric scores
4. **Artifact Output** — Saves JSON comparison data, registry state, and evaluation reports to `output/`

## How to Run

```bash
# From the repo root
cd 07-prompt-management/mini-project

# Run with DeepEval (recommended — requires OPENAI_API_KEY in .env)
python solution.py

# Run without DeepEval (uses mock heuristic evaluation — no API key needed)
pip install deepeval  # skip this step
python solution.py
```

The pipeline works in both modes:
- **With DeepEval**: Uses AnswerRelevancyMetric and GEval for research-backed evaluation
- **Without DeepEval**: Uses a heuristic overlap scorer for demonstration

## Expected Output

```
============================================================
  PROMPT EVAL PIPELINE — Module 7 Mini-Project
============================================================

[1/4] Registry created.
[2/4] Two versions registered.
       v1.0: basic classifier
       v2.0: block-structured with category definitions

[3/4] Running test cases against both versions...
       5 test cases defined.

  Evaluating v1.0...
  Evaluating v2.0...
[4/4] Evaluation complete.

============================================================
  EVALUATION REPORT: support-classifier
============================================================
  Framework: deepeval (or mock fallback)
  Test Cases: 5
  Metrics: relevancy, correctness
  Overall: PASS / FAIL
  ...

============================================================
  VERSION COMPARISON
============================================================
  v1.0 results: True/False
  v2.0 results: True/False

  Promoted v2.0 to production.

  Saved: output/version_comparison.json
  Saved: output/registry_state.json
  Saved: output/evaluation_report.txt

============================================================
  PIPELINE COMPLETE
============================================================
```

## Visible Artifact

The pipeline produces three saved files in `output/`:

| File | Contents |
|------|----------|
| `version_comparison.json` | Side-by-side prompt content and test results for v1.0 vs v2.0 |
| `registry_state.json` | Full registry with all versions, metadata, and evaluation scores |
| `evaluation_report.txt` | Human-readable report with metrics, scores, and version status |

These artifacts are suitable for portfolio screenshots or LinkedIn posts demonstrating prompt engineering maturity.

## Files

| File | Purpose |
|------|---------|
| `solution.py` | Full implementation — PromptRegistry, evaluation pipeline, report generation |
| `README.md` | This file |
