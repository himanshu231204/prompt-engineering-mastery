# Mini Project: Math Reasoning Technique Benchmark

Benchmarks four prompting techniques — Direct, Chain-of-Thought, Plan-and-Solve+, and Self-Consistency — on 8 math word problems. Produces an accuracy comparison table and a JSON results artifact.

## What It Does

1. Loads 8 math word problems (easy/medium/hard) with known correct answers
2. Runs each problem through 4 techniques:
   - **Direct**: Standard Q&A with no reasoning instruction
   - **CoT**: Zero-shot Chain-of-Thought ("Let's think step by step")
   - **Plan-and-Solve+**: Structured decomposition before solving
   - **Self-Consistency (N=5)**: 5 independent CoT samples with majority vote
3. Prints a comparison table with accuracy, correct count, and average latency
4. Saves results to `results.json` for portfolio use

## How to Run

```bash
# Default (OpenAI)
python solution.py

# Use Anthropic
python solution.py --provider anthropic

# Use Ollama (local)
python solution.py --provider ollama

# Fewer SC samples (faster, cheaper)
python solution.py --samples 3
```

Requires `.env` with API keys (see `../../.env.example`).

## Expected Output

```
======================================================================
  MATH REASONING BENCHMARK RESULTS
======================================================================

Technique            Accuracy    Correct    Avg Latency
----------------------------------------------------------------------
Direct                    62%        5/8          1.2s
CoT                       88%        7/8          2.1s
Plan-and-Solve            88%        7/8          2.4s
SC(n=5)                  100%        8/8         10.3s
----------------------------------------------------------------------

PER-PROBLEM BREAKDOWN:
#    Correct Ans
 1              Direct     CoT         Plan-and-Solve SC(n=5)
----------------------------------------------------------------------
1    24           Y=24      Y=24       Y=24           Y=24
2    18           N=14      Y=18       Y=18           Y=18
...
```

Results are also saved to `results.json` as a machine-readable artifact.

## Visible Artifact

The benchmark produces two artifacts:
- **Console table**: Formatted comparison table (screenshot this)
- **results.json**: Full benchmark data including per-problem predictions
