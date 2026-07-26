"""
Math Reasoning Benchmark — Compares Direct, CoT, Self-Consistency, and Plan-and-Solve.

Benchmarks four reasoning techniques on math word problems and produces an
accuracy comparison table. Runs in under 5 minutes on a standard laptop.

Usage:
    python solution.py                    # Uses defaults (openai provider)
    python solution.py --provider anthropic
    python solution.py --samples 3        # Fewer SC samples = faster
"""

import sys
import os
import time
import re
import json
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import call_llm


# ---------------------------------------------------------------------------
# Problem Dataset
# ---------------------------------------------------------------------------

PROBLEMS = [
    {
        "id": 1,
        "question": (
            "A juggler has 12 balls. He loses 3 and buys 5 times as many as he "
            "lost. How many balls does he have now?"
        ),
        "answer": 24,
        "difficulty": "easy",
    },
    {
        "id": 2,
        "question": (
            "Janet's ducks lay 16 eggs per day. She eats three for breakfast "
            "every morning and bakes muffins for her friends every day with four. "
            "She sells the remainder for $2 per egg. How much does she make every day?"
        ),
        "answer": 18,
        "difficulty": "medium",
    },
    {
        "id": 3,
        "question": (
            "Roger has 5 tennis balls. He buys 2 cans of tennis balls. Each can "
            "has 3 tennis balls. How many tennis balls does he have now?"
        ),
        "answer": 11,
        "difficulty": "easy",
    },
    {
        "id": 4,
        "question": (
            "Grace weighs 125 pounds. Alex weighs 498 pounds. Together with their "
            "dog Rex, the three weigh 700 pounds. How much does Rex weigh?"
        ),
        "answer": 77,
        "difficulty": "medium",
    },
    {
        "id": 5,
        "question": (
            "Every day, Wendi feeds each of her chickens three cups of mixed "
            "chicken feed, containing 4% corn, 1% wheat and 51% ground feed. "
            "How many pounds of chicken feed does she need for her 5 chickens "
            "over 4 weeks?"
        ),
        "answer": 42,
        "difficulty": "hard",
    },
    {
        "id": 6,
        "question": (
            "Kylar went to the store to get some cups. Each pack of cups has 3 "
            "cups in it. Kylar needs 14 cups total for a party. How many packs "
            "of cups does Kylar need to buy?"
        ),
        "answer": 5,
        "difficulty": "easy",
    },
    {
        "id": 7,
        "question": (
            "A deep-sea monster rises from the depths once every 377 years. "
            "It last appeared in 1983. In what year will it next appear?"
        ),
        "answer": 2360,
        "difficulty": "easy",
    },
    {
        "id": 8,
        "question": (
            "A semi-truck can hold 2,000 pounds of cargo. It is loaded with "
            "30 boxes weighing 55 pounds each and 20 crates weighing 10 pounds "
            "each. How much more weight can the truck hold?"
        ),
        "answer": 300,
        "difficulty": "medium",
    },
]


# ---------------------------------------------------------------------------
# Prompt Templates
# ---------------------------------------------------------------------------

DIRECT_TEMPLATE = "Q: {question}\nA:"
COT_TEMPLATE = "Q: {question}\nA: Let's think step by step."
PS_TEMPLATE = (
    "Q: {question}\n"
    "A: Let's first understand the problem and devise a plan to solve "
    "the problem. Then, let's carry out the plan and solve the problem "
    "step by step."
)
PS_PLUS_TEMPLATE = (
    "Q: {question}\n"
    "A: Let's first understand the problem, extract relevant variables "
    "and their corresponding numerals, and devise a plan to solve the "
    "problem. Then, let's carry out the plan, calculate intermediate "
    "results, and solve the problem step by step. Pay attention to "
    "calculation and commonsense."
)


# ---------------------------------------------------------------------------
# Answer Extraction
# ---------------------------------------------------------------------------

def extract_number(response: str) -> Optional[int]:
    """Extract the final integer answer from a model response."""
    patterns = [
        r"(?:the answer is|answer[:=])\s*\$?(\d+)",
        r"(?:therefore|so)\s.*?(\d+)\s*$",
        r"=\s*(\d+)\s*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE | re.MULTILINE)
        if match:
            return int(match.group(1))

    # Fallback: find all numbers, return the last one
    numbers = re.findall(r"\b(\d+)\b", response)
    if numbers:
        return int(numbers[-1])
    return None


# ---------------------------------------------------------------------------
# Technique Implementations
# ---------------------------------------------------------------------------

@dataclass
class TechniqueResult:
    """Result of applying one technique to one problem."""
    technique: str
    predicted: Optional[int] = None
    correct: bool = False
    response: str = ""
    elapsed: float = 0.0


def solve_direct(question: str, correct_answer: int,
                 provider: str, model: Optional[str]) -> TechniqueResult:
    """Direct prompting — no reasoning instruction."""
    prompt = DIRECT_TEMPLATE.format(question=question)
    start = time.time()
    response = call_llm(prompt, provider=provider, model=model, temperature=0.0)
    elapsed = time.time() - start
    predicted = extract_number(response)
    return TechniqueResult(
        technique="Direct",
        predicted=predicted,
        correct=predicted == correct_answer,
        response=response,
        elapsed=elapsed,
    )


def solve_cot(question: str, correct_answer: int,
              provider: str, model: Optional[str]) -> TechniqueResult:
    """Chain-of-Thought prompting."""
    prompt = COT_TEMPLATE.format(question=question)
    start = time.time()
    response = call_llm(prompt, provider=provider, model=model, temperature=0.0)
    elapsed = time.time() - start
    predicted = extract_number(response)
    return TechniqueResult(
        technique="CoT",
        predicted=predicted,
        correct=predicted == correct_answer,
        response=response,
        elapsed=elapsed,
    )


def solve_plan_and_solve(question: str, correct_answer: int,
                         provider: str, model: Optional[str]) -> TechniqueResult:
    """Plan-and-Solve+ prompting."""
    prompt = PS_PLUS_TEMPLATE.format(question=question)
    start = time.time()
    response = call_llm(prompt, provider=provider, model=model, temperature=0.0)
    elapsed = time.time() - start
    predicted = extract_number(response)
    return TechniqueResult(
        technique="Plan-and-Solve",
        predicted=predicted,
        correct=predicted == correct_answer,
        response=response,
        elapsed=elapsed,
    )


def solve_self_consistency(question: str, correct_answer: int,
                           provider: str, model: Optional[str],
                           n_samples: int = 5,
                           temperature: float = 0.7) -> TechniqueResult:
    """Self-Consistency — sample N paths, majority vote."""
    prompt = COT_TEMPLATE.format(question=question)
    answers = []
    full_responses = []

    start = time.time()
    for _ in range(n_samples):
        response = call_llm(
            prompt, provider=provider, model=model, temperature=temperature
        )
        full_responses.append(response)
        predicted = extract_number(response)
        if predicted is not None:
            answers.append(predicted)
    elapsed = time.time() - start

    if not answers:
        return TechniqueResult(
            technique=f"SC(n={n_samples})",
            predicted=None,
            correct=False,
            response=str(full_responses),
            elapsed=elapsed,
        )

    counts = Counter(answers)
    final_answer, _ = counts.most_common(1)[0]
    return TechniqueResult(
        technique=f"SC(n={n_samples})",
        predicted=final_answer,
        correct=final_answer == correct_answer,
        response=json.dumps({
            "samples": answers,
            "vote_counts": dict(counts),
            "final": final_answer,
        }),
        elapsed=elapsed,
    )


# ---------------------------------------------------------------------------
# Benchmark Runner
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkResult:
    """Aggregated results for one technique across all problems."""
    technique: str
    correct: int = 0
    total: int = 0
    total_elapsed: float = 0.0
    results: list = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total > 0 else 0.0

    @property
    def avg_latency(self) -> float:
        return self.total_elapsed / self.total if self.total > 0 else 0.0


def run_benchmark(provider: str, model: Optional[str],
                  n_samples: int = 5) -> list[BenchmarkResult]:
    """Run all techniques on all problems and collect results."""
    techniques = ["Direct", "CoT", "Plan-and-Solve", f"SC(n={n_samples})"]
    benchmarks = {t: BenchmarkResult(technique=t) for t in techniques}

    print(f"Running benchmark: {len(PROBLEMS)} problems x {len(techniques)} techniques")
    print(f"Provider: {provider}, Model: {model or 'default'}")
    print(f"Self-consistency samples: {n_samples}")
    print("-" * 70)

    for i, problem in enumerate(PROBLEMS, 1):
        q = problem["question"]
        ans = problem["answer"]
        print(f"Problem {i}/{len(PROBLEMS)} [{problem['difficulty']}]...", end=" ", flush=True)

        # Direct
        r = solve_direct(q, ans, provider, model)
        benchmarks["Direct"].results.append(r)
        benchmarks["Direct"].correct += int(r.correct)
        benchmarks["Direct"].total += 1
        benchmarks["Direct"].total_elapsed += r.elapsed

        # CoT
        r = solve_cot(q, ans, provider, model)
        benchmarks["CoT"].results.append(r)
        benchmarks["CoT"].correct += int(r.correct)
        benchmarks["CoT"].total += 1
        benchmarks["CoT"].total_elapsed += r.elapsed

        # Plan-and-Solve
        r = solve_plan_and_solve(q, ans, provider, model)
        benchmarks["Plan-and-Solve"].results.append(r)
        benchmarks["Plan-and-Solve"].correct += int(r.correct)
        benchmarks["Plan-and-Solve"].total += 1
        benchmarks["Plan-and-Solve"].total_elapsed += r.elapsed

        # Self-Consistency
        r = solve_self_consistency(q, ans, provider, model, n_samples)
        sc_key = f"SC(n={n_samples})"
        benchmarks[sc_key].results.append(r)
        benchmarks[sc_key].correct += int(r.correct)
        benchmarks[sc_key].total += 1
        benchmarks[sc_key].total_elapsed += r.elapsed

        status = "OK" if all(
            benchmarks[t].results[-1].correct
            for t in techniques
        ) else "MIXED"
        print(f"[{status}]")

    return list(benchmarks.values())


# ---------------------------------------------------------------------------
# Output — Visible Artifact
# ---------------------------------------------------------------------------

def print_results(benchmarks: list[BenchmarkResult]) -> str:
    """Print and return a formatted comparison table."""
    lines = []
    lines.append("")
    lines.append("=" * 70)
    lines.append("  MATH REASONING BENCHMARK RESULTS")
    lines.append("=" * 70)
    lines.append("")

    # Header
    header = f"{'Technique':<20} {'Accuracy':>10} {'Correct':>10} {'Avg Latency':>14}"
    lines.append(header)
    lines.append("-" * 70)

    for b in benchmarks:
        acc_str = f"{b.accuracy:.0%}"
        corr_str = f"{b.correct}/{b.total}"
        lat_str = f"{b.avg_latency:.1f}s"
        lines.append(f"{b.technique:<20} {acc_str:>10} {corr_str:>10} {lat_str:>14}")

    lines.append("-" * 70)
    lines.append("")

    # Per-problem breakdown
    lines.append("PER-PROBLEM BREAKDOWN:")
    lines.append(f"{'#':<4} {'Correct Ans':<12}", )
    for b in benchmarks:
        lines.append(f" {b.technique:<14}")
    lines.append("-" * 70)

    for i, problem in enumerate(PROBLEMS):
        row = f"{problem['id']:<4} {problem['answer']:<12}"
        for b in benchmarks:
            r = b.results[i]
            marker = "Y" if r.correct else "N"
            pred_str = f"{r.predicted}" if r.predicted is not None else "?"
            row += f" {marker}={pred_str:<11}"
        lines.append(row)

    lines.append("")
    lines.append("=" * 70)

    report = "\n".join(lines)
    print(report)
    return report


def save_results(report: str, benchmarks: list[BenchmarkResult]) -> None:
    """Save results to a JSON artifact for portfolio use."""
    artifact = {
        "benchmark": "Math Reasoning Technique Comparison",
        "techniques": [
            {
                "name": b.technique,
                "accuracy": b.accuracy,
                "correct": b.correct,
                "total": b.total,
                "avg_latency_seconds": round(b.avg_latency, 2),
            }
            for b in benchmarks
        ],
        "problems": [
            {
                "id": p["id"],
                "question": p["question"],
                "difficulty": p["difficulty"],
                "correct_answer": p["answer"],
            }
            for p in PROBLEMS
        ],
    }

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(output_path, "w") as f:
        json.dump(artifact, f, indent=2)
    print(f"\nResults saved to: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Math Reasoning Benchmark")
    parser.add_argument("--provider", default="openai",
                        choices=["openai", "anthropic", "ollama"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--samples", type=int, default=5,
                        help="Number of SC samples (default: 5)")
    args = parser.parse_args()

    start = time.time()
    benchmarks = run_benchmark(args.provider, args.model, args.samples)
    report = print_results(benchmarks)
    save_results(report, benchmarks)

    total_time = time.time() - start
    print(f"\nTotal benchmark time: {total_time:.1f}s ({total_time/60:.1f} min)")
