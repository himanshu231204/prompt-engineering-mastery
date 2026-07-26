# Mini-Project: Prompt Strategy Comparator

**Objective**: Build a command-line tool that runs all five prompting strategies (zero-shot, one-shot, few-shot, system-prompted, delimited) on real NLP tasks and generates a comparison report.

## What It Does

1. Runs 5 prompting strategies across 3 task types (classification, extraction, summarization)
2. Logs every strategy's output, token count, and any errors to CSV and JSON
3. Generates a grouped bar chart comparing token usage across strategies
4. Prints a formatted summary table to stdout

## How to Run

```bash
# From the repo root
cd 02-essential-strategies/mini-project

# Run with defaults (OpenAI gpt-4o)
python solution.py

# Run with Anthropic
python solution.py --provider anthropic --model claude-sonnet-4-20250514

# Run with Ollama (local)
python solution.py --provider ollama --model llama3

# Run a single task type
python solution.py --task classification
python solution.py --task extraction
python solution.py --task summarization
```

## Expected Output

After running, you should see:

```
Prompt Strategy Comparator
Provider: openai | Model: gpt-4o
Tasks: sentiment_classification, support_ticket_parsing, one_sentence_summary

Running strategy comparisons...
  Running zero_shot on sentiment_classification...
  Running one_shot on sentiment_classification...
  ...

==========================================================================================
PROMPT STRATEGY COMPARISON RESULTS
==========================================================================================

--- SENTIMENT CLASSIFICATION ---
Strategy           Tokens   Output
------------------------------------------------------------------------------------------
zero_shot          22       Neutral...
one_shot           24       Neutral...
few_shot           26       Neutral...
system_prompt      1        Neutral...
delimited          18       Neutral...

--- SUPPORT TICKET PARSING ---
...

--- ONE SENTENCE SUMMARY ---
...

==========================================================================================

CSV saved to: strategy_results/strategy_comparison.csv
JSON saved to: strategy_results/strategy_comparison.json
Visualization saved to: strategy_results/strategy_comparison.png

Done! 15/15 strategies completed successfully.
Artifacts saved to: strategy_results/
```

## Artifacts

| File | Description |
|------|-------------|
| `strategy_results/strategy_comparison.csv` | Full results table with all strategies and tasks |
| `strategy_results/strategy_comparison.json` | Structured JSON for programmatic access |
| `strategy_results/strategy_comparison.png` | Grouped bar chart comparing token usage |

## Task Types

| Task | What It Tests | Expected Pattern |
|------|---------------|------------------|
| Sentiment Classification | Label consistency across strategies | Few-shot and delimited produce most consistent labels |
| Support Ticket Parsing | Structured extraction | System prompt + delimiters produce cleanest output |
| One-Sentence Summary | Length constraint adherence | System prompt enforces one-sentence constraint |

## Configuration

Default settings (edit in `solution.py`):
- **Tasks**: 3 tasks covering classification, extraction, summarization
- **Strategies**: zero_shot, one_shot, few_shot, system_prompt, delimited
- **Temperature**: 0.0 (deterministic for fair comparison)
- **Max tokens**: 150 per response

## Requirements

- Python 3.10+
- `openai` or `anthropic` package installed (depending on provider)
- API key set in `.env` (see `../../.env.example`)
- `matplotlib` for visualization (optional — skips gracefully if missing)
