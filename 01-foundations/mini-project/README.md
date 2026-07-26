# Mini-Project: Parameter Sweep Tool

**Objective**: Build a command-line tool that sweeps LLM configuration parameters, logs results to CSV/JSON, and generates a comparison visualization.

## What It Does

1. Runs three parameter sweeps: temperature, top_p, and max_tokens
2. Logs every configuration and response to CSV and JSON
3. Generates a bar chart comparing response lengths across parameter values
4. Prints a formatted summary table to stdout

## How to Run

```bash
# From the repo root
cd 01-foundations/mini-project

# Run with defaults (OpenAI gpt-4o)
python solution.py

# Run with Anthropic
python solution.py --provider anthropic --model claude-sonnet-4-20250514

# Run with Ollama (local)
python solution.py --provider ollama --model llama3

# Use a custom prompt
python solution.py --prompt "Write a haiku about debugging code"
```

## Expected Output

After running, you should see:

```
Parameter Sweep Tool
Provider: openai | Model: gpt-4o
Prompt: Explain the difference between a stack and a queue in one parag...

Running temperature sweep...
Running top_p sweep...
Running max_tokens sweep...

================================================================================
PARAMETER SWEEP RESULTS
================================================================================

--- TEMPERATURE SWEEP ---
Value        Tokens     Response Preview
--------------------------------------------------------------------------------
0.0          45         A stack is a linear data structure that follows...
0.3          42         A stack follows last-in-first-out (LIFO) order...
...

--- TOP_P SWEEP ---
...

--- MAX_TOKENS SWEEP ---
...

================================================================================

Results saved to: sweep_results/parameter_sweep.csv
Results saved to: sweep_results/parameter_sweep.json
Visualization saved to: sweep_results/parameter_sweep.png

Done! 13 parameter configurations tested.
```

## Artifacts

| File | Description |
|------|-------------|
| `sweep_results/parameter_sweep.csv` | Full results table with all configurations |
| `sweep_results/parameter_sweep.json` | Structured JSON for programmatic access |
| `sweep_results/parameter_sweep.png` | Bar chart visualization of token counts |

## Configuration

Default sweep values (edit in `solution.py`):

- **Temperatures**: `[0.0, 0.3, 0.7, 1.0, 1.5]`
- **Top-p values**: `[0.1, 0.5, 0.9, 1.0]`
- **Max tokens**: `[50, 100, 200, 500]`

## Requirements

- Python 3.10+
- `openai` or `anthropic` package installed (depending on provider)
- API key set in `.env` (see `../../.env.example`)
- `matplotlib` for visualization (optional — skips gracefully if missing)
