"""Parameter Sweep Tool — Module 1 Mini-Project

Sweeps temperature, top_p, and max_tokens parameters across an LLM,
logs results to CSV, and generates a comparison visualization.

Usage:
    python solution.py
    python solution.py --provider anthropic --model claude-sonnet-4-20250514
    python solution.py --prompt "Write a haiku about coding"

Outputs:
    sweep_results/parameter_sweep.csv — full results table
    sweep_results/parameter_sweep.png — comparison visualization
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.llm_client import call_llm


# Default sweep configuration
DEFAULT_PROMPT = "Explain the difference between a stack and a queue in one paragraph."
DEFAULT_TEMPERATURES = [0.0, 0.3, 0.7, 1.0, 1.5]
DEFAULT_TOP_P_VALUES = [0.1, 0.5, 0.9, 1.0]
DEFAULT_MAX_TOKENS_VALUES = [50, 100, 200, 500]

OUTPUT_DIR = Path(__file__).resolve().parent / "sweep_results"


def run_temperature_sweep(prompt: str, provider: str, model: str) -> list[dict]:
    """Sweep temperature values while holding other parameters constant."""
    results = []
    for temp in DEFAULT_TEMPERATURES:
        try:
            response = call_llm(
                prompt,
                provider=provider,
                model=model,
                temperature=temp,
                max_tokens=200,
            )
            results.append({
                "sweep_type": "temperature",
                "parameter": "temperature",
                "value": temp,
                "response": response,
                "token_count": len(response.split()),
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            results.append({
                "sweep_type": "temperature",
                "parameter": "temperature",
                "value": temp,
                "response": f"ERROR: {e}",
                "token_count": 0,
                "timestamp": datetime.now().isoformat(),
            })
    return results


def run_top_p_sweep(prompt: str, provider: str, model: str) -> list[dict]:
    """Sweep top_p values while holding temperature constant at 0.7."""
    results = []
    for top_p in DEFAULT_TOP_P_VALUES:
        try:
            response = call_llm(
                prompt,
                provider=provider,
                model=model,
                temperature=0.7,
                top_p=top_p,
                max_tokens=200,
            )
            results.append({
                "sweep_type": "top_p",
                "parameter": "top_p",
                "value": top_p,
                "response": response,
                "token_count": len(response.split()),
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            results.append({
                "sweep_type": "top_p",
                "parameter": "top_p",
                "value": top_p,
                "response": f"ERROR: {e}",
                "token_count": 0,
                "timestamp": datetime.now().isoformat(),
            })
    return results


def run_max_tokens_sweep(prompt: str, provider: str, model: str) -> list[dict]:
    """Sweep max_tokens values to demonstrate truncation effects."""
    results = []
    for max_t in DEFAULT_MAX_TOKENS_VALUES:
        try:
            response = call_llm(
                prompt,
                provider=provider,
                model=model,
                temperature=0.3,
                max_tokens=max_t,
            )
            results.append({
                "sweep_type": "max_tokens",
                "parameter": "max_tokens",
                "value": max_t,
                "response": response,
                "token_count": len(response.split()),
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            results.append({
                "sweep_type": "max_tokens",
                "parameter": "max_tokens",
                "value": max_t,
                "response": f"ERROR: {e}",
                "token_count": 0,
                "timestamp": datetime.now().isoformat(),
            })
    return results


def save_results_csv(all_results: list[dict], output_path: Path) -> None:
    """Save sweep results to CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sweep_type", "parameter", "value", "response", "token_count", "timestamp"])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"Results saved to: {output_path}")


def save_results_json(all_results: list[dict], output_path: Path) -> None:
    """Save sweep results to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"Results saved to: {output_path}")


def generate_visualization(all_results: list[dict], output_path: Path) -> None:
    """Generate comparison bar chart of response lengths by parameter."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed — skipping visualization. Run: pip install matplotlib")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Parameter Sweep: Response Token Counts by Configuration", fontsize=14)

    sweep_types = ["temperature", "top_p", "max_tokens"]
    colors = ["#2196F3", "#4CAF50", "#FF9800"]

    for ax, sweep_type, color in zip(axes, sweep_types, colors):
        subset = [r for r in all_results if r["sweep_type"] == sweep_type and not r["response"].startswith("ERROR")]
        if not subset:
            ax.text(0.5, 0.5, "No data", ha="center", va="center")
            ax.set_title(sweep_type)
            continue

        labels = [str(r["value"]) for r in subset]
        counts = [r["token_count"] for r in subset]

        ax.bar(labels, counts, color=color, alpha=0.8)
        ax.set_title(sweep_type)
        ax.set_xlabel(sweep_type)
        ax.set_ylabel("Approx. Token Count")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Visualization saved to: {output_path}")


def print_summary_table(all_results: list[dict]) -> None:
    """Print a formatted summary table to stdout."""
    print("\n" + "=" * 80)
    print("PARAMETER SWEEP RESULTS")
    print("=" * 80)

    current_type = None
    for r in all_results:
        if r["sweep_type"] != current_type:
            current_type = r["sweep_type"]
            print(f"\n--- {current_type.upper()} SWEEP ---")
            print(f"{'Value':<12} {'Tokens':<10} {'Response Preview'}")
            print("-" * 80)

        preview = r["response"][:80].replace("\n", " ") + "..." if len(r["response"]) > 80 else r["response"].replace("\n", " ")
        print(f"{str(r['value']):<12} {r['token_count']:<10} {preview}")

    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(description="LLM Parameter Sweep Tool")
    parser.add_argument("--provider", default="openai", choices=["openai", "anthropic", "ollama"])
    parser.add_argument("--model", default=None, help="Model name (defaults to provider-specific default)")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt to use for all sweeps")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Output directory for results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    model = args.model or ("gpt-4o" if args.provider == "openai" else "claude-sonnet-4-20250514" if args.provider == "anthropic" else "llama3")

    print(f"Parameter Sweep Tool")
    print(f"Provider: {args.provider} | Model: {model}")
    print(f"Prompt: {args.prompt[:60]}...")
    print()

    # Run all sweeps
    print("Running temperature sweep...")
    temp_results = run_temperature_sweep(args.prompt, args.provider, model)

    print("Running top_p sweep...")
    top_p_results = run_top_p_sweep(args.prompt, args.provider, model)

    print("Running max_tokens sweep...")
    max_tokens_results = run_max_tokens_sweep(args.prompt, args.provider, model)

    all_results = temp_results + top_p_results + max_tokens_results

    # Print summary
    print_summary_table(all_results)

    # Save artifacts
    csv_path = output_dir / "parameter_sweep.csv"
    json_path = output_dir / "parameter_sweep.json"
    chart_path = output_dir / "parameter_sweep.png"

    save_results_csv(all_results, csv_path)
    save_results_json(all_results, json_path)
    generate_visualization(all_results, chart_path)

    print(f"\nDone! {len(all_results)} parameter configurations tested.")
    print(f"Artifacts saved to: {output_dir}/")


if __name__ == "__main__":
    main()
