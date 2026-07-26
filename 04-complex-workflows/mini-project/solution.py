"""
Auto Prompt Optimizer — Meta-Prompting Mini Project

Uses meta-prompting to iteratively optimize prompts for specific tasks.
Evaluates prompt quality, generates improvements, and produces a comparison
artifact showing initial vs. optimized prompt performance.

Usage:
    python solution.py                         # Defaults: openai, 3 iterations
    python solution.py --provider anthropic
    python solution.py --iterations 5          # More refinement rounds
    python solution.py --task "Classify customer emails"
"""

import sys
import os
import re
import json
import time
import argparse
from dataclasses import dataclass, field
from typing import Optional

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import call_llm


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class EvalScores:
    """Quality scores for a prompt evaluation."""
    clarity: int = 5
    specificity: int = 5
    correctness: int = 5
    feedback: str = ""

    @property
    def average(self) -> float:
        return (self.clarity + self.specificity + self.correctness) / 3


@dataclass
class OptimizationStep:
    """One iteration of the optimization loop."""
    iteration: int
    prompt: str
    scores: EvalScores
    elapsed: float = 0.0


@dataclass
class OptimizationResult:
    """Full result of a meta-prompting optimization run."""
    task: str
    initial_prompt: str
    final_prompt: str
    steps: list = field(default_factory=list)
    test_cases: list = field(default_factory=list)
    total_elapsed: float = 0.0

    @property
    def improvement(self) -> float:
        """Score improvement from initial to final."""
        if len(self.steps) < 2:
            return 0.0
        return self.steps[-1].scores.average - self.steps[0].scores.average


# ---------------------------------------------------------------------------
# Meta-Prompting Core
# ---------------------------------------------------------------------------

def evaluate_prompt(task: str, prompt: str, provider: str,
                    model: Optional[str]) -> EvalScores:
    """Evaluate a prompt's quality using the LLM as judge.

    Args:
        task: The task description the prompt is meant to solve.
        prompt: The prompt to evaluate.
        provider: LLM provider name.
        model: Specific model name or None for default.

    Returns:
        EvalScores with clarity, specificity, correctness, and feedback.
    """
    eval_prompt = (
        f"You are a prompt quality evaluator. Rate the following prompt "
        f"on a scale of 1-10 for each criterion.\n\n"
        f"Task: {task}\n"
        f"Prompt to evaluate: {prompt}\n\n"
        f"Respond with ONLY a JSON object (no markdown, no explanation):\n"
        f'{{"clarity": <1-10>, "specificity": <1-10>, '
        f'"correctness": <1-10>, "feedback": "<specific improvement suggestions>"}}'
    )
    response = call_llm(eval_prompt, provider=provider, model=model, temperature=0.0)

    try:
        json_match = re.search(r'\{[^{}]+\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return EvalScores(
                clarity=min(10, max(1, int(data.get("clarity", 5)))),
                specificity=min(10, max(1, int(data.get("specificity", 5)))),
                correctness=min(10, max(1, int(data.get("correctness", 5)))),
                feedback=str(data.get("feedback", "No feedback provided")),
            )
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    return EvalScores(feedback=response[:200])


def optimize_prompt(task: str, current_prompt: str, scores: EvalScores,
                    provider: str, model: Optional[str]) -> str:
    """Generate an improved prompt based on evaluation feedback.

    Args:
        task: The task description.
        current_prompt: The current prompt to improve.
        scores: Evaluation scores for the current prompt.
        provider: LLM provider name.
        model: Specific model name or None for default.

    Returns:
        An improved prompt string.
    """
    optimize_instruction = (
        f"You are an expert prompt engineer. Improve the following prompt "
        f"based on the evaluation feedback.\n\n"
        f"Task: {task}\n\n"
        f"Current prompt: {current_prompt}\n\n"
        f"Evaluation scores: clarity={scores.clarity}/10, "
        f"specificity={scores.specificity}/10, "
        f"correctness={scores.correctness}/10\n"
        f"Feedback: {scores.feedback}\n\n"
        f"Requirements for the improved prompt:\n"
        f"1. Be specific about the desired output format\n"
        f"2. Include explicit criteria or constraints\n"
        f"3. Provide examples if helpful\n"
        f"4. Address the specific weaknesses identified in feedback\n\n"
        f"Return ONLY the improved prompt text, nothing else."
    )
    return call_llm(optimize_instruction, provider=provider, model=model, temperature=0.3)


def run_optimization(task: str, initial_prompt: str, provider: str,
                     model: Optional[str], iterations: int = 3) -> OptimizationResult:
    """Run the full meta-prompting optimization loop.

    Args:
        task: Description of the task the prompt should solve.
        initial_prompt: The starting prompt to optimize.
        provider: LLM provider name.
        model: Specific model name or None for default.
        iterations: Number of optimization rounds.

    Returns:
        OptimizationResult with all steps and the final optimized prompt.
    """
    result = OptimizationResult(task=task, initial_prompt=initial_prompt, final_prompt="")
    current_prompt = initial_prompt

    print(f"Optimizing prompt for: {task}")
    print(f"Iterations: {iterations}")
    print("-" * 60)

    total_start = time.time()

    for i in range(iterations):
        print(f"\n--- Iteration {i + 1}/{iterations} ---")

        # Evaluate
        step_start = time.time()
        scores = evaluate_prompt(task, current_prompt, provider, model)
        step_elapsed = time.time() - step_start

        step = OptimizationStep(
            iteration=i + 1,
            prompt=current_prompt,
            scores=scores,
            elapsed=step_elapsed,
        )
        result.steps.append(step)

        print(f"Scores: clarity={scores.clarity}, specificity={scores.specificity}, "
              f"correctness={scores.correctness} (avg: {scores.average:.1f})")
        print(f"Feedback: {scores.feedback[:100]}...")

        # Optimize (skip on last iteration)
        if i < iterations - 1:
            current_prompt = optimize_prompt(task, current_prompt, scores, provider, model)
            print(f"New prompt: {current_prompt[:80]}...")

    result.final_prompt = current_prompt
    result.total_elapsed = time.time() - total_start

    return result


# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------

def test_prompt(prompt: str, test_inputs: list, provider: str,
                model: Optional[str]) -> list:
    """Test a prompt against a list of test inputs.

    Args:
        prompt: The prompt template (should contain {input} placeholder).
        test_inputs: List of test input strings.
        provider: LLM provider name.
        model: Specific model name or None for default.

    Returns:
        List of (input, output) tuples.
    """
    results = []
    for test_input in test_inputs:
        full_prompt = prompt.replace("{input}", test_input)
        output = call_llm(full_prompt, provider=provider, model=model, temperature=0.0)
        results.append((test_input, output))
    return results


# ---------------------------------------------------------------------------
# Output — Visible Artifact
# ---------------------------------------------------------------------------

def print_results(result: OptimizationResult) -> str:
    """Print and return a formatted optimization report."""
    lines = []
    lines.append("")
    lines.append("=" * 70)
    lines.append("  AUTO PROMPT OPTIMIZER — RESULTS")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Task: {result.task}")
    lines.append(f"Iterations: {len(result.steps)}")
    lines.append(f"Total time: {result.total_elapsed:.1f}s")
    lines.append("")

    # Score progression
    lines.append("SCORE PROGRESSION:")
    lines.append(f"{'Iter':<6} {'Clarity':>8} {'Specific':>9} {'Correct':>9} {'Average':>9}")
    lines.append("-" * 50)
    for step in result.steps:
        lines.append(
            f"{step.iteration:<6} {step.scores.clarity:>8} "
            f"{step.scores.specificity:>9} {step.scores.correctness:>9} "
            f"{step.scores.average:>9.1f}"
        )
    lines.append("-" * 50)
    lines.append(f"Improvement: {result.improvement:+.1f} avg points")
    lines.append("")

    # Before/After comparison
    lines.append("PROMPT COMPARISON:")
    lines.append("")
    lines.append("BEFORE (initial):")
    lines.append(f"  {result.initial_prompt}")
    lines.append("")
    lines.append("AFTER (optimized):")
    lines.append(f"  {result.final_prompt}")
    lines.append("")

    # Test case results
    if result.test_cases:
        lines.append("TEST CASE RESULTS:")
        lines.append("-" * 70)
        for i, (test_input, output) in enumerate(result.test_cases, 1):
            lines.append(f"Test {i}: {test_input[:50]}...")
            lines.append(f"  Output: {output[:100]}...")
            lines.append("")

    lines.append("=" * 70)

    report = "\n".join(lines)
    print(report)
    return report


def save_results(result: OptimizationResult, report: str) -> str:
    """Save results to a JSON artifact for portfolio use.

    Args:
        result: The full optimization result.
        report: The formatted report string.

    Returns:
        Path to the saved file.
    """
    artifact = {
        "project": "Auto Prompt Optimizer",
        "task": result.task,
        "iterations": len(result.steps),
        "total_elapsed_seconds": round(result.total_elapsed, 2),
        "initial_prompt": result.initial_prompt,
        "final_prompt": result.final_prompt,
        "score_improvement": round(result.improvement, 2),
        "steps": [
            {
                "iteration": step.iteration,
                "prompt": step.prompt,
                "scores": {
                    "clarity": step.scores.clarity,
                    "specificity": step.scores.specificity,
                    "correctness": step.scores.correctness,
                    "average": round(step.scores.average, 2),
                },
                "feedback": step.scores.feedback,
                "elapsed_seconds": round(step.elapsed, 2),
            }
            for step in result.steps
        ],
        "test_results": [
            {"input": inp, "output": out}
            for inp, out in result.test_cases
        ],
    }

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(output_path, "w") as f:
        json.dump(artifact, f, indent=2)
    print(f"\nResults saved to: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# Demo Tasks
# ---------------------------------------------------------------------------

DEMO_TASKS = [
    {
        "task": "Classify a customer support email as: URGENT, BILLING, TECHNICAL, or GENERAL",
        "initial_prompt": "Read this email and tell me what it's about.",
        "test_inputs": [
            "Hi, I was charged twice for my subscription this month. My card shows two charges of $29.99.",
            "My app keeps crashing when I try to upload a photo. I've tried restarting but it still fails.",
            "When does the Black Friday sale start? I want to upgrade my plan.",
        ],
    },
    {
        "task": "Extract key facts from a news article headline and return structured JSON",
        "initial_prompt": "Summarize this headline.",
        "test_inputs": [
            "Apple Announces $500M AI Research Center in Austin, Creating 200 Jobs",
            "Global Chip Shortage Expected to Ease by Q3 2026, Says Industry Report",
        ],
    },
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Auto Prompt Optimizer — Meta-Prompting Mini Project")
    parser.add_argument("--provider", default="openai",
                        choices=["openai", "anthropic", "ollama"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--iterations", type=int, default=3,
                        help="Number of optimization rounds (default: 3)")
    parser.add_argument("--task-index", type=int, default=0,
                        help="Index of demo task to run (default: 0)")
    args = parser.parse_args()

    demo = DEMO_TASKS[args.task_index]

    # Run optimization
    result = run_optimization(
        task=demo["task"],
        initial_prompt=demo["initial_prompt"],
        provider=args.provider,
        model=args.model,
        iterations=args.iterations,
    )

    # Test the optimized prompt
    print("\nTesting optimized prompt on sample inputs...")
    result.test_cases = test_prompt(
        result.final_prompt,
        demo["test_inputs"],
        args.provider,
        args.model,
    )

    # Print and save results
    report = print_results(result)
    save_results(result, report)

    print(f"\nTotal time: {result.total_elapsed:.1f}s")


if __name__ == "__main__":
    main()
