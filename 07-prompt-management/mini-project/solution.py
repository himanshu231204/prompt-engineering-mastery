"""Prompt Eval Pipeline — Module 7 Mini-Project

A prompt evaluation pipeline using DeepEval with a simple prompt registry.
Demonstrates the prompt management lifecycle: version, evaluate, compare.

Usage:
    python solution.py

Requires:
    - deepeval (pip install deepeval)
    - An OpenAI API key (for GEval metrics) OR run in offline mode with mock metrics
    - utils/llm_client.py (shared LLM abstraction)
"""

import json
import hashlib
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path

from utils.llm_client import call_llm


# ---------------------------------------------------------------------------
# Prompt Registry
# ---------------------------------------------------------------------------

@dataclass
class PromptVersion:
    """A single versioned prompt entry."""
    version: str
    content: str
    system_prompt: Optional[str] = None
    model: str = "gpt-4o"
    temperature: float = 0.7
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    author: str = "auto"
    notes: str = ""
    status: str = "draft"  # draft | staging | production | retired
    test_results: dict = field(default_factory=dict)

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content.encode()).hexdigest()[:12]


class PromptRegistry:
    """Version-controlled prompt registry.

    Stores prompt versions with metadata, test results, and deployment status.
    Each prompt is identified by a unique name and supports multiple versions.

    Example:
        registry = PromptRegistry()
        registry.register("support-classifier", "Classify this message...", version="1.0")
        registry.register("support-classifier", "Classify this customer message...", version="2.0")
        prompt = registry.get("support-classifier", version="2.0")
    """

    def __init__(self, storage_path: Optional[str] = None):
        self._registry: dict[str, list[PromptVersion]] = {}
        self._storage_path = Path(storage_path) if storage_path else None
        if self._storage_path and self._storage_path.exists():
            self._load()

    def register(
        self,
        name: str,
        content: str,
        version: str = "1.0",
        system_prompt: Optional[str] = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        author: str = "auto",
        notes: str = "",
    ) -> PromptVersion:
        """Register a new prompt version.

        Args:
            name: Unique prompt identifier (e.g., 'support-classifier').
            content: The prompt text.
            version: Semantic version string (e.g., '1.0', '2.1.0').
            system_prompt: Optional system-level instruction.
            model: Target model name.
            temperature: Sampling temperature.
            author: Who created this version.
            notes: Description of what changed and why.

        Returns:
            The created PromptVersion instance.
        """
        entry = PromptVersion(
            version=version,
            content=content,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            author=author,
            notes=notes,
        )

        if name not in self._registry:
            self._registry[name] = []

        # Check for duplicate version
        existing_versions = [p.version for p in self._registry[name]]
        if version in existing_versions:
            raise ValueError(
                f"Version '{version}' already exists for prompt '{name}'. "
                f"Existing versions: {existing_versions}"
            )

        self._registry[name].append(entry)
        self._save()
        return entry

    def get(self, name: str, version: Optional[str] = None) -> PromptVersion:
        """Retrieve a prompt version.

        Args:
            name: Prompt identifier.
            version: Specific version to retrieve. If None, returns the latest.

        Returns:
            The matching PromptVersion.

        Raises:
            KeyError: If the prompt name or version doesn't exist.
        """
        if name not in self._registry:
            raise KeyError(f"Prompt '{name}' not found in registry.")

        versions = self._registry[name]
        if not versions:
            raise KeyError(f"Prompt '{name}' has no versions.")

        if version is None:
            return versions[-1]  # Latest version

        for v in versions:
            if v.version == version:
                return v

        existing = [v.version for v in versions]
        raise KeyError(
            f"Version '{version}' not found for prompt '{name}'. "
            f"Available: {existing}"
        )

    def list_versions(self, name: str) -> list[dict]:
        """List all versions for a prompt with metadata.

        Args:
            name: Prompt identifier.

        Returns:
            List of version summaries (dicts).
        """
        if name not in self._registry:
            return []

        return [
            {
                "version": p.version,
                "created_at": p.created_at,
                "author": p.author,
                "status": p.status,
                "notes": p.notes,
                "content_hash": p.content_hash,
            }
            for p in self._registry[name]
        ]

    def update_status(self, name: str, version: str, status: str) -> None:
        """Update the deployment status of a prompt version.

        Args:
            name: Prompt identifier.
            version: Version to update.
            status: New status (draft, staging, production, retired).
        """
        valid_statuses = {"draft", "staging", "production", "retired"}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Must be one of: {valid_statuses}")

        prompt = self.get(name, version)
        prompt.status = status
        self._save()

    def update_test_results(self, name: str, version: str, results: dict) -> None:
        """Store evaluation results for a prompt version.

        Args:
            name: Prompt identifier.
            version: Version to update.
            results: Metric scores and pass/fail status.
        """
        prompt = self.get(name, version)
        prompt.test_results = results
        self._save()

    def compare(self, name: str, v1: str, v2: str) -> dict:
        """Compare two versions side by side.

        Args:
            name: Prompt identifier.
            v1: First version.
            v2: Second version.

        Returns:
            Comparison dict with content and test result differences.
        """
        p1 = self.get(name, v1)
        p2 = self.get(name, v2)

        return {
            "prompt": name,
            "v1": {
                "version": p1.version,
                "content": p1.content,
                "test_results": p1.test_results,
            },
            "v2": {
                "version": p2.version,
                "content": p2.content,
                "test_results": p2.test_results,
            },
        }

    @property
    def prompt_names(self) -> list[str]:
        """List all registered prompt names."""
        return list(self._registry.keys())

    def _save(self) -> None:
        """Persist registry to disk if storage path is set."""
        if not self._storage_path:
            return
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        for name, versions in self._registry.items():
            data[name] = [asdict(v) for v in versions]
        self._storage_path.write_text(json.dumps(data, indent=2))

    def _load(self) -> None:
        """Load registry from disk."""
        if not self._storage_path or not self._storage_path.exists():
            return
        data = json.loads(self._storage_path.read_text())
        for name, versions in data.items():
            self._registry[name] = [PromptVersion(**v) for v in versions]


# ---------------------------------------------------------------------------
# Evaluation Pipeline
# ---------------------------------------------------------------------------

def build_test_cases(
    prompt_content: str,
    test_inputs: list[dict],
    provider: str = "openai",
    model: Optional[str] = None,
) -> list[dict]:
    """Run a prompt against test inputs and return results.

    Args:
        prompt_content: The prompt template (use {input} as placeholder).
        test_inputs: List of dicts with 'input' and optional 'expected_output'.
        provider: LLM provider name.
        model: Model name (provider default if None).

    Returns:
        List of result dicts with input, actual_output, expected_output.
    """
    results = []
    for case in test_inputs:
        user_input = case["input"]
        # Replace placeholder if present
        if "{input}" in prompt_content:
            filled_prompt = prompt_content.replace("{input}", user_input)
        else:
            filled_prompt = f"{prompt_content}\n\n{user_input}"

        actual_output = call_llm(
            prompt=filled_prompt,
            provider=provider,
            model=model,
            temperature=0.3,
            max_tokens=200,
        )

        results.append({
            "input": user_input,
            "actual_output": actual_output.strip(),
            "expected_output": case.get("expected_output", ""),
        })

    return results


def evaluate_with_deepeval(
    test_results: list[dict],
    metric_names: Optional[list[str]] = None,
) -> dict:
    """Evaluate prompt outputs using DeepEval metrics.

    Args:
        test_results: Output from build_test_cases().
        metric_names: List of metric names to use. Defaults to relevancy + correctness.

    Returns:
        Evaluation summary with scores and pass/fail status.
    """
    try:
        from deepeval import evaluate
        from deepeval.test_case import LLMTestCase, SingleTurnParams
        from deepeval.metrics import GEval, AnswerRelevancyMetric
    except ImportError:
        return _mock_evaluate(test_results)

    if metric_names is None:
        metric_names = ["relevancy", "correctness"]

    # Build metrics
    metrics = []
    if "relevancy" in metric_names:
        metrics.append(AnswerRelevancyMetric(threshold=0.7))
    if "correctness" in metric_names:
        metrics.append(GEval(
            name="Correctness",
            criteria="Determine if the actual output is correct based on the expected output.",
            evaluation_params=[
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=0.6,
        ))

    # Build test cases
    deepeval_cases = []
    for r in test_results:
        kwargs = {
            "input": r["input"],
            "actual_output": r["actual_output"],
        }
        if r.get("expected_output"):
            kwargs["expected_output"] = r["expected_output"]
        deepeval_cases.append(LLMTestCase(**kwargs))

    # Run evaluation
    result = evaluate(test_cases=deepeval_cases, metrics=metrics)

    return {
        "framework": "deepeval",
        "test_cases_evaluated": len(deepeval_cases),
        "metrics_used": metric_names,
        "overall_success": result.success if hasattr(result, "success") else None,
        "individual_results": [
            {
                "input": r["input"][:80],
                "output": r["actual_output"][:80],
            }
            for r in test_results
        ],
    }


def _mock_evaluate(test_results: list[dict]) -> dict:
    """Fallback evaluation when DeepEval is not installed.

    Provides a basic heuristic evaluation for demonstration purposes.
    """
    scores = []
    for r in test_results:
        actual = r["actual_output"].lower().strip()
        expected = r.get("expected_output", "").lower().strip()

        # Simple heuristic: check if expected appears in actual or vice versa
        if expected and (expected in actual or actual in expected):
            score = 0.9
        elif expected and actual[:20] in expected or expected[:20] in actual:
            score = 0.7
        else:
            score = 0.5
        scores.append(score)

    avg_score = sum(scores) / len(scores) if scores else 0.0

    return {
        "framework": "mock (deepeval not installed)",
        "test_cases_evaluated": len(test_results),
        "metrics_used": ["heuristic overlap"],
        "average_score": round(avg_score, 3),
        "overall_success": avg_score >= 0.6,
        "individual_results": [
            {
                "input": r["input"][:80],
                "output": r["actual_output"][:80],
                "score": round(s, 3),
            }
            for r, s in zip(test_results, scores)
        ],
    }


def generate_report(
    registry: PromptRegistry,
    prompt_name: str,
    evaluation_results: dict,
) -> str:
    """Generate a human-readable evaluation report.

    Args:
        registry: The prompt registry.
        prompt_name: Name of the evaluated prompt.
        evaluation_results: Output from evaluate_with_deepeval().

    Returns:
        Formatted report string.
    """
    versions = registry.list_versions(prompt_name)
    lines = [
        "=" * 60,
        f"  EVALUATION REPORT: {prompt_name}",
        "=" * 60,
        "",
        f"  Framework: {evaluation_results.get('framework', 'unknown')}",
        f"  Test Cases: {evaluation_results.get('test_cases_evaluated', 0)}",
        f"  Metrics: {', '.join(evaluation_results.get('metrics_used', []))}",
        f"  Overall: {'PASS' if evaluation_results.get('overall_success') else 'FAIL'}",
        "",
        "-" * 60,
        "  Registered Versions:",
        "-" * 60,
    ]

    for v in versions:
        status_icon = {"production": "🟢", "staging": "🟡", "draft": "⚪", "retired": "🔴"}.get(v["status"], "?")
        lines.append(f"    {status_icon} v{v['version']} — {v['status']} — {v['notes'][:50]}")

    lines.extend([
        "",
        "-" * 60,
        "  Individual Results:",
        "-" * 60,
    ])

    for i, r in enumerate(evaluation_results.get("individual_results", []), 1):
        score = r.get("score", "N/A")
        lines.append(f"    {i}. Input: {r['input'][:60]}...")
        lines.append(f"       Output: {r['output'][:60]}...")
        if score != "N/A":
            lines.append(f"       Score: {score}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main: Demo Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full prompt eval pipeline demonstration.

    Steps:
        1. Create a registry and register two prompt versions
        2. Run test cases against both versions
        3. Evaluate outputs with DeepEval (or mock fallback)
        4. Generate and print a comparison report
    """
    print("=" * 60)
    print("  PROMPT EVAL PIPELINE — Module 7 Mini-Project")
    print("=" * 60)
    print()

    # Step 1: Create registry
    registry = PromptRegistry()
    print("[1/4] Registry created.")

    # Step 2: Register two prompt versions
    registry.register(
        name="support-classifier",
        content="Classify this customer message into one category: billing, technical, general. Return only the category name.",
        version="1.0",
        author="alice",
        notes="Initial version — basic 3-category classifier",
    )

    registry.register(
        name="support-classifier",
        content=(
            "You are a customer support classifier.\n\n"
            "Classify the customer message below into exactly one category:\n"
            "- billing (payment issues, invoices, refunds)\n"
            "- technical (bugs, errors, setup problems)\n"
            "- general (everything else)\n\n"
            "Customer message: {input}\n\n"
            "Respond with ONLY the category name, nothing else."
        ),
        version="2.0",
        author="bob",
        notes="Rewrite with block structure and explicit category definitions",
    )

    print("[2/4] Two versions registered.")
    print(f"       v1.0: basic classifier")
    print(f"       v2.0: block-structured with category definitions")
    print()

    # Step 3: Define test cases
    test_cases = [
        {"input": "I was charged twice for my subscription", "expected_output": "billing"},
        {"input": "The app keeps crashing when I open settings", "expected_output": "technical"},
        {"input": "What are your business hours?", "expected_output": "general"},
        {"input": "I need a refund for my last payment", "expected_output": "billing"},
        {"input": "How do I reset my password?", "expected_output": "technical"},
    ]

    print("[3/4] Running test cases against both versions...")
    print(f"       {len(test_cases)} test cases defined.")
    print()

    # Evaluate v1.0
    print("  Evaluating v1.0...")
    results_v1 = build_test_cases(
        prompt_content=registry.get("support-classifier", "1.0").content,
        test_inputs=test_cases,
        provider="openai",
    )
    eval_v1 = evaluate_with_deepeval(results_v1)
    registry.update_test_results("support-classifier", "1.0", eval_v1)

    # Evaluate v2.0
    print("  Evaluating v2.0...")
    results_v2 = build_test_cases(
        prompt_content=registry.get("support-classifier", "2.0").content,
        test_inputs=test_cases,
        provider="openai",
    )
    eval_v2 = evaluate_with_deepeval(results_v2)
    registry.update_test_results("support-classifier", "2.0", eval_v2)

    print("[4/4] Evaluation complete.")
    print()

    # Step 4: Generate reports
    report_v1 = generate_report(registry, "support-classifier", eval_v1)
    print(report_v1)
    print()

    report_v2 = generate_report(registry, "support-classifier", eval_v2)
    print(report_v2)
    print()

    # Step 5: Compare versions
    comparison = registry.compare("support-classifier", "1.0", "2.0")
    print("=" * 60)
    print("  VERSION COMPARISON")
    print("=" * 60)
    print(f"  v1.0 results: {comparison['v1']['test_results'].get('overall_success', 'N/A')}")
    print(f"  v2.0 results: {comparison['v2']['test_results'].get('overall_success', 'N/A')}")
    print()

    # Step 6: Promote winning version
    best_version = "2.0" if eval_v2.get("overall_success", False) else "1.0"
    registry.update_status("support-classifier", best_version, "production")
    print(f"  Promoted v{best_version} to production.")
    print()

    # Save artifacts
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Save comparison as JSON
    comparison_path = output_dir / "version_comparison.json"
    comparison_path.write_text(json.dumps(comparison, indent=2, default=str))
    print(f"  Saved: {comparison_path}")

    # Save full registry state
    registry_path = output_dir / "registry_state.json"
    registry._storage_path = registry_path
    registry._save()
    print(f"  Saved: {registry_path}")

    # Save reports
    report_path = output_dir / "evaluation_report.txt"
    report_path.write_text(f"{report_v1}\n\n{report_v2}")
    print(f"  Saved: {report_path}")

    print()
    print("=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
