"""Prompt Strategy Comparator — Module 2 Mini-Project

Runs zero-shot, one-shot, few-shot, system-prompted, and delimited prompting
on test tasks, logs results to CSV/JSON, and generates a comparison visualization.

Usage:
    python solution.py
    python solution.py --provider anthropic --model claude-sonnet-4-20250514
    python solution.py --task classification

Outputs:
    strategy_results/strategy_comparison.csv — full results table
    strategy_results/strategy_comparison.json — structured JSON
    strategy_results/strategy_comparison.png — comparison visualization
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.llm_client import call_llm


# ---------------------------------------------------------------------------
# Test tasks — each task has a zero-shot prompt, one-shot version, few-shot
# version, system prompt, and delimited version so we can compare all five
# strategies on the same input.
# ---------------------------------------------------------------------------

CLASSIFICATION_TASK = {
    "name": "sentiment_classification",
    "input": "The product works fine but the shipping was slow.",
    "expected": "Neutral",  # ground truth for accuracy check
    "zero_shot": (
        "Classify the following text as positive, negative, or neutral:\n\n"
        "Text: The product works fine but the shipping was slow.\n"
        "Sentiment:"
    ),
    "one_shot": (
        "Classify the following text as positive, negative, or neutral:\n\n"
        "Text: I love this product!\n"
        "Sentiment: Positive\n\n"
        "Text: The product works fine but the shipping was slow.\n"
        "Sentiment:"
    ),
    "few_shot": (
        "Classify the following text as positive, negative, or neutral:\n\n"
        "Text: I love this product!\n"
        "Sentiment: Positive\n\n"
        "Text: Terrible experience, would not recommend.\n"
        "Sentiment: Negative\n\n"
        "Text: It's okay, nothing special.\n"
        "Sentiment: Neutral\n\n"
        "Text: The product works fine but the shipping was slow.\n"
        "Sentiment:"
    ),
    "system_prompt": "You are a sentiment classifier. Output ONLY the label: Positive, Negative, or Neutral.",
    "delimited": (
        "### Instructions\n"
        "Classify the sentiment of the ticket.\n\n"
        "### Ticket\n"
        "The product works fine but the shipping was slow.\n\n"
        "### Label:"
    ),
}

EXTRACTION_TASK = {
    "name": "support_ticket_parsing",
    "input": "The app crashes when I upload files larger than 10MB. This is blocking our team.",
    "expected": "Bug Report",
    "zero_shot": (
        "Extract the category from this support ticket. "
        "Categories: Billing, Bug Report, Feature Request, Account.\n\n"
        "Ticket: The app crashes when I upload files larger than 10MB. This is blocking our team.\n"
        "Category:"
    ),
    "one_shot": (
        "Extract the category from this support ticket. "
        "Categories: Billing, Bug Report, Feature Request, Account.\n\n"
        "Ticket: I was charged twice this month.\n"
        "Category: Billing\n\n"
        "Ticket: The app crashes when I upload files larger than 10MB. This is blocking our team.\n"
        "Category:"
    ),
    "few_shot": (
        "Extract the category from this support ticket. "
        "Categories: Billing, Bug Report, Feature Request, Account.\n\n"
        "Ticket: I was charged twice this month.\n"
        "Category: Billing\n\n"
        "Ticket: Can you add dark mode to the app?\n"
        "Category: Feature Request\n\n"
        "Ticket: I can't reset my password.\n"
        "Category: Account\n\n"
        "Ticket: The app crashes when I upload files larger than 10MB. This is blocking our team.\n"
        "Category:"
    ),
    "system_prompt": "You are a support ticket classifier. Output ONLY the category label.",
    "delimited": (
        "### Instructions\n"
        "Extract the category from the ticket below.\n"
        "Categories: Billing, Bug Report, Feature Request, Account.\n\n"
        "### Ticket\n"
        "The app crashes when I upload files larger than 10MB. This is blocking our team.\n\n"
        "### Category:"
    ),
}

SUMMARIZATION_TASK = {
    "name": "one_sentence_summary",
    "input": (
        "Climate change is causing sea levels to rise at an accelerating rate. "
        "Since 1900, global sea levels have risen approximately 8 inches, with the rate "
        "doubling in the last two decades. Coastal cities like Miami, Jakarta, and Mumbai "
        "face increasing flooding risk."
    ),
    "expected": "One sentence about sea level rise",
    "zero_shot": (
        "Summarize the following in exactly one sentence:\n\n"
        "Climate change is causing sea levels to rise at an accelerating rate. "
        "Since 1900, global sea levels have risen approximately 8 inches, with the rate "
        "doubling in the last two decades. Coastal cities like Miami, Jakarta, and Mumbai "
        "face increasing flooding risk.\n\n"
        "Summary:"
    ),
    "one_shot": (
        "Summarize the following in exactly one sentence:\n\n"
        "Example input: Python is a high-level programming language created by Guido van Rossum "
        "in 1991. It emphasizes code readability and supports multiple programming paradigms.\n"
        "Example summary: Python is a readable, multi-paradigm programming language created in 1991.\n\n"
        "Input: Climate change is causing sea levels to rise at an accelerating rate. "
        "Since 1900, global sea levels have risen approximately 8 inches, with the rate "
        "doubling in the last two decades. Coastal cities like Miami, Jakarta, and Mumbai "
        "face increasing flooding risk.\n\n"
        "Summary:"
    ),
    "few_shot": (
        "Summarize the following in exactly one sentence:\n\n"
        "Example input: Python is a high-level programming language created by Guido van Rossum "
        "in 1991.\n"
        "Example summary: Python is a readable, multi-paradigm programming language created in 1991.\n\n"
        "Example input: Docker containers package applications with their dependencies.\n"
        "Example summary: Docker packages apps with dependencies into portable containers.\n\n"
        "Example input: Kubernetes orchestrates container deployment across clusters.\n"
        "Example summary: Kubernetes manages container deployment at scale.\n\n"
        "Input: Climate change is causing sea levels to rise at an accelerating rate. "
        "Since 1900, global sea levels have risen approximately 8 inches, with the rate "
        "doubling in the last two decades. Coastal cities like Miami, Jakarta, and Mumbai "
        "face increasing flooding risk.\n\n"
        "Summary:"
    ),
    "system_prompt": "You are a concise summarizer. Output exactly one sentence.",
    "delimited": (
        "### Instructions\n"
        "Summarize the article in exactly one sentence.\n\n"
        "### Article\n"
        "Climate change is causing sea levels to rise at an accelerating rate. "
        "Since 1900, global sea levels have risen approximately 8 inches, with the rate "
        "doubling in the last two decades. Coastal cities like Miami, Jakarta, and Mumbai "
        "face increasing flooding risk.\n\n"
        "### Summary:"
    ),
}

ALL_TASKS = [CLASSIFICATION_TASK, EXTRACTION_TASK, SUMMARIZATION_TASK]

OUTPUT_DIR = Path(__file__).resolve().parent / "strategy_results"


# ---------------------------------------------------------------------------
# Runner functions — each returns a result dict
# ---------------------------------------------------------------------------

def run_strategy(task: dict, strategy: str, provider: str, model: str) -> dict:
    """Run a single strategy on a single task and return the result."""
    prompt_key = strategy
    system_prompt = None

    if strategy == "system_prompt":
        # System prompt strategy: use the task's input directly, with system as context
        prompt = task["input"]
        system_prompt = task["system_prompt"]
    else:
        prompt = task[prompt_key]

    try:
        response = call_llm(
            prompt,
            provider=provider,
            model=model,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=150,
        )
        return {
            "task": task["name"],
            "strategy": strategy,
            "input": task["input"][:100],
            "expected": task["expected"],
            "output": response.strip(),
            "token_count": len(response.split()),
            "error": None,
        }
    except Exception as e:
        return {
            "task": task["name"],
            "strategy": strategy,
            "input": task["input"][:100],
            "expected": task["expected"],
            "output": f"ERROR: {e}",
            "token_count": 0,
            "error": str(e),
        }


def run_all(tasks: list[dict], provider: str, model: str) -> list[dict]:
    """Run all strategies on all tasks."""
    strategies = ["zero_shot", "one_shot", "few_shot", "system_prompt", "delimited"]
    results = []

    for task in tasks:
        for strategy in strategies:
            print(f"  Running {strategy} on {task['name']}...")
            result = run_strategy(task, strategy, provider, model)
            results.append(result)

    return results


# ---------------------------------------------------------------------------
# Output functions
# ---------------------------------------------------------------------------

def save_csv(results: list[dict], path: Path) -> None:
    """Save results to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["task", "strategy", "input", "expected", "output", "token_count", "error"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"CSV saved to: {path}")


def save_json(results: list[dict], path: Path) -> None:
    """Save results to JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"JSON saved to: {path}")


def generate_visualization(results: list[dict], output_path: Path) -> None:
    """Generate grouped bar chart comparing token usage by strategy."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("matplotlib not installed — skipping visualization. Run: pip install matplotlib")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    tasks = list({r["task"] for r in results})
    strategies = ["zero_shot", "one_shot", "few_shot", "system_prompt", "delimited"]
    strategy_labels = ["Zero-Shot", "One-Shot", "Few-Shot", "System", "Delimited"]
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"]

    fig, axes = plt.subplots(1, len(tasks), figsize=(5 * len(tasks), 5))
    if len(tasks) == 1:
        axes = [axes]

    fig.suptitle("Prompt Strategy Comparison: Token Usage by Task", fontsize=14, y=1.02)

    for ax, task_name in zip(axes, tasks):
        token_counts = []
        for strat in strategies:
            matching = [r for r in results if r["task"] == task_name and r["strategy"] == strat]
            count = matching[0]["token_count"] if matching and matching[0]["error"] is None else 0
            token_counts.append(count)

        bars = ax.bar(strategy_labels, token_counts, color=colors, alpha=0.8)
        ax.set_title(task_name.replace("_", " ").title())
        ax.set_ylabel("Approx. Token Count")
        ax.tick_params(axis="x", rotation=30)

        # Add value labels on bars
        for bar, count in zip(bars, token_counts):
            if count > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                        str(count), ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Visualization saved to: {output_path}")


def print_summary(results: list[dict]) -> None:
    """Print a formatted summary table."""
    print("\n" + "=" * 90)
    print("PROMPT STRATEGY COMPARISON RESULTS")
    print("=" * 90)

    current_task = None
    for r in results:
        if r["task"] != current_task:
            current_task = r["task"]
            print(f"\n--- {current_task.replace('_', ' ').upper()} ---")
            print(f"{'Strategy':<18} {'Tokens':<8} {'Output'}")
            print("-" * 90)

        preview = r["output"][:65].replace("\n", " ") + "..." if len(r["output"]) > 65 else r["output"].replace("\n", " ")
        error_flag = " [ERR]" if r["error"] else ""
        print(f"{r['strategy']:<18} {r['token_count']:<8} {preview}{error_flag}")

    print("\n" + "=" * 90)


def main():
    parser = argparse.ArgumentParser(description="Prompt Strategy Comparator — Module 2 Mini-Project")
    parser.add_argument("--provider", default="openai", choices=["openai", "anthropic", "ollama"])
    parser.add_argument("--model", default=None, help="Model name (defaults to provider-specific default)")
    parser.add_argument("--task", default=None, choices=["classification", "extraction", "summarization", "all"],
                        help="Run a specific task or all (default: all)")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Output directory for results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    model = args.model or ("gpt-4o" if args.provider == "openai" else "claude-sonnet-4-20250514" if args.provider == "anthropic" else "llama3")

    # Select tasks
    if args.task == "classification":
        tasks = [CLASSIFICATION_TASK]
    elif args.task == "extraction":
        tasks = [EXTRACTION_TASK]
    elif args.task == "summarization":
        tasks = [SUMMARIZATION_TASK]
    else:
        tasks = ALL_TASKS

    print("Prompt Strategy Comparator")
    print(f"Provider: {args.provider} | Model: {model}")
    print(f"Tasks: {', '.join(t['name'] for t in tasks)}")
    print()

    # Run all strategies
    print("Running strategy comparisons...")
    results = run_all(tasks, args.provider, model)

    # Print summary
    print_summary(results)

    # Save artifacts
    csv_path = output_dir / "strategy_comparison.csv"
    json_path = output_dir / "strategy_comparison.json"
    chart_path = output_dir / "strategy_comparison.png"

    save_csv(results, csv_path)
    save_json(results, json_path)
    generate_visualization(results, chart_path)

    # Count successes
    successes = sum(1 for r in results if r["error"] is None)
    print(f"\nDone! {successes}/{len(results)} strategies completed successfully.")
    print(f"Artifacts saved to: {output_dir}/")


if __name__ == "__main__":
    main()
