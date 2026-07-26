"""Math Word Problem Solver"""

from utils.llm_client import call_llm

def solve_with_cot(problem: str) -> str:
    """Solve problem using Chain-of-Thought."""
    # TODO: Implement CoT solving
    pass

def solve_with_self_consistency(problem: str, n_samples: int = 5) -> str:
    """Solve problem using self-consistency."""
    # TODO: Implement self-consistency
    pass

if __name__ == "__main__":
    # Test solver
    pass
