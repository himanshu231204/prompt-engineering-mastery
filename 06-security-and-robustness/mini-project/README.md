# Prompt Injection Test Harness

**Objective**: Build a command-line tool that evaluates prompt injection attack success rates across multiple defense layers and produces a security evaluation report.

## What It Does

1. Loads a dataset of 12 prompt injection attack patterns
2. Runs each attack against 3 different defense mechanisms
3. Logs every test result (attack type, defense used, success/failure) to CSV
4. Prints a formatted security evaluation report to terminal with success rates per attack and defense type

## How to Run

```bash
# From the repo root
cd 06-security-and-robustness/mini-project

# Run with defaults (OpenAI gpt-4o)
python solution.py

# Run with Anthropic
python solution.py --provider anthropic --model claude-sonnet-4-20250514

# Run with Ollama (local)
python solution.py --provider ollama --model llama3

# Custom output directory
python solution.py --output-dir my_results/
```

## Expected Output

After running, you should see:

```
Prompt Injection Test Harness
Provider: openai | Model: gpt-4o

Loaded 12 attacks and 3 defenses
Running 36 tests...

  Testing attack 1/12 against defense 'Input Validation' (1/36)... [BLOCKED]
  Testing attack 1/12 against defense 'System Prompt Hardening' (2/36)... [BLOCKED]
  ...

Completed in 45.2s

CSV report saved to: security_report/injection_test_results.csv

================================================================
PROMPT INJECTION TEST HARNESS — SECURITY EVALUATION REPORT
================================================================
Provider: openai | Model: gpt-4o
Tests run: 36 | Attacks: 12 | Defenses: 3
================================================================

ATTACK SUCCESS RATES BY TYPE:
  Direct Injection          : 2/3 blocked (33.3% succeeded)
  Jailbreak                 : 3/3 blocked (0.0% succeeded)
  ...

DEFENSE EFFECTIVENESS:
  Input Validation          : blocked 10/12 attacks (83.3%)
  System Prompt Hardening   : blocked 11/12 attacks (91.7%)
  Output Filtering          : blocked 12/12 attacks (100.0%)

OVERALL SECURITY SCORE: 91.7% attacks blocked
================================================================

Artifacts saved to: security_report/
```

## Artifacts

| Artifact | Description |
|----------|-------------|
| `security_report/injection_test_results.csv` | Full test results with attack type, defense used, and success/failure |
| Terminal report | Formatted security evaluation with success rates per attack and defense type |

## Attack Dataset

The harness includes 12 attack patterns:

| # | Attack Type | Description |
|---|-------------|-------------|
| 1 | Direct injection | Attempts to override system instructions directly |
| 2 | Jailbreak (DAN) | Uses persona injection to bypass restrictions |
| 3 | Role-play attack | Requests unrestricted role-play to extract instructions |
| 4 | Payload splitting | Breaks attack across multiple message segments |
| 5 | Multi-turn manipulation | Gradual escalation across conversation turns |
| 6 | Indirect injection | Hides instructions within provided content |
| 7 | Output format exploitation | Requests structured output containing sensitive data |
| 8 | Instruction override | Attempts to replace system instructions entirely |
| 9 | Encoding bypass | Uses base64 or other encoding to obfuscate attacks |
| 10 | Context window attack | Floods context to push system instructions out of attention |
| 11 | Persona hijacking | Attempts to replace AI identity with unrestricted persona |
| 12 | Delimiter escape | Tries to break out of input formatting boundaries |

## Defense Mechanisms

Three defense layers are tested:

| Defense | How It Works |
|---------|--------------|
| Input Validation | Scans input for known injection patterns using regex matching |
| System Prompt Hardening | Wraps base prompt with structural defenses and safety rules |
| Output Filtering | Checks responses for sensitive pattern leakage before returning |

## Configuration

- Requires Python 3.10+
- Requires API key set in `.env` file (see `../../.env.example`)
- Uses `utils/llm_client.py` abstraction for model-agnostic execution
- Default output directory: `security_report/`
- Can customize output with `--output-dir` flag

## Requirements

```bash
pip install -r requirements.txt
```