#!/usr/bin/env python3
"""
Setup script for prompt-engineering-mastery project structure.
Creates directories and placeholder files as per the specification.
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create the folder structure for the prompt-engineering-mastery project."""
    
    base_path = Path(".")
    
    # Define the structure
    structure = {
        "utils": {
            "llm_client.py": '''"""Thin wrapper for calling different LLM providers."""

import os
from typing import Optional

def call_llm(
    prompt: str,
    provider: str = "openai",
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    **kwargs
) -> str:
    """
    Call an LLM provider with the given prompt.
    
    Args:
        prompt: The input prompt
        provider: LLM provider ("openai", "anthropic", "ollama")
        model: Model name (defaults to provider-specific default)
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        **kwargs: Additional provider-specific arguments
    
    Returns:
        Generated response as string
    """
    # TODO: Implement provider-specific API calls
    # For now, return a placeholder
    return f"[{provider}] Response to: {prompt[:50]}..."
'''
        },
        "01-foundations": {
            "README.md": """# Prompt Engineering Foundations

## Topics
- How LLMs work
- Tokens and tokenization
- Temperature, top-p, and top-k parameters
- The generation process

## Learning Objectives
- Understand the mechanics of large language models
- Learn how configuration parameters affect outputs
- Experiment with different settings

## Key Concepts

### Temperature
Controls randomness in token selection. Lower = more deterministic, higher = more creative.

### Top-p (Nucleus Sampling)
Limits token selection to a cumulative probability mass.

### Top-k
Limits token selection to the k most likely tokens.

## Exercises
1. Compare outputs with different temperature settings
2. Experiment with top-p and top-k combinations
3. Analyze token probabilities in generated text
""",
            "notebook.ipynb": '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Parameter Playground\\n",
    "Experiment with LLM configuration parameters and compare outputs."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from utils.llm_client import call_llm\\n",
    "import pandas as pd\\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Test different temperatures\\n",
    "temperatures = [0.0, 0.3, 0.7, 1.0, 1.5]\\n",
    "prompt = \\"Explain quantum computing in simple terms.\\"\\n",
    "\\n",
    "results = []\\n",
    "for temp in temperatures:\\n",
    "    response = call_llm(prompt, temperature=temp)\\n",
    "    results.append({\'temperature\': temp, \'response\': response})\\n",
    "    print(f\'Temperature {temp}:\\n{response[:200]}...\\\\n\')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''',
            "mini-project": {
                "README.md": """# Mini Project: Parameter Playground

## Objective
Sweep temperature and top-p parameters, log outputs, and analyze how different settings affect LLM responses.

## Tasks
1. Implement parameter sweep across temperature and top-p values
2. Log inputs, outputs, and metadata
3. Create visualizations comparing outputs
4. Write analysis of parameter effects

## Expected Outputs
- Parameter sweep results in CSV/JSON format
- Visualization plots
- Analysis report
""",
                "solution.py": '''"""Parameter Sweep Solution"""

import json
from pathlib import Path
from utils.llm_client import call_llm

def parameter_sweep():
    """Sweep parameters and log results."""
    # TODO: Implement parameter sweep
    pass

if __name__ == "__main__":
    parameter_sweep()
'''
            }
        },
        "02-essential-strategies": {
            "README.md": """# Essential Prompting Strategies

## Topics
- Zero-shot prompting
- One-shot prompting
- Few-shot prompting
- System prompts
- Delimiters and formatting

## Learning Objectives
- Master different prompting techniques
- Learn when to use each strategy
- Practice creating effective few-shot examples

## Key Concepts

### Zero-shot
No examples provided - rely entirely on the model's pre-training.

### One-shot
Single example to demonstrate desired behavior.

### Few-shot
Multiple examples to establish patterns.

### System Prompts
High-level instructions that set context and behavior.

## Exercises
1. Compare zero-shot vs few-shot performance
2. Design effective system prompts
3. Create few-shot classifiers for different tasks
""",
            "notebook.ipynb": '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Prompting Strategy Comparison\\n",
    "Compare different prompting approaches and their effectiveness."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from utils.llm_client import call_llm"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''',
            "mini-project": {
                "README.md": """# Mini Project: Few-Shot Classifier Builder

## Objective
Build a few-shot classifier that can categorize text into predefined categories using LLMs.

## Tasks
1. Design a few-shot classification prompt
2. Create example sets for different categories
3. Test classifier accuracy on validation data
4. Compare performance with different numbers of examples

## Expected Outputs
- Classification prompt template
- Example database
- Accuracy metrics
""",
                "solution.py": '''"""Few-Shot Classifier Solution"""

from utils.llm_client import call_llm

def classify_text(text: str, examples: list) -> str:
    """Classify text using few-shot prompting."""
    # TODO: Implement few-shot classification
    pass

if __name__ == "__main__":
    # Test classifier
    pass
'''
            }
        },
        "03-reasoning-and-logic": {
            "README.md": """# Reasoning and Logic Techniques

## Topics
- Chain-of-Thought (CoT) prompting
- Self-Consistency
- Plan-and-Solve
- Step-by-step reasoning

## Learning Objectives
- Implement chain-of-thought reasoning
- Apply self-consistency for complex problems
- Design step-by-step solution prompts

## Key Concepts

### Chain-of-Thought (CoT)
Instruct model to show reasoning steps before giving final answer.

### Self-Consistency
Sample multiple reasoning paths and take majority vote.

### Plan-and-Solve
Break complex problems into planning and execution phases.

## Exercises
1. Compare CoT vs direct prompting for math problems
2. Implement self-consistency with multiple samples
3. Design plan-and-solve prompts for word problems
""",
            "notebook.ipynb": '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Reasoning Technique Comparison\\n",
    "Compare CoT, self-consistency, and direct prompting."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''',
            "mini-project": {
                "README.md": """# Mini Project: Math Word Problem Solver

## Objective
Build a solver that compares Chain-of-Thought, direct prompting, and self-consistency approaches for math word problems.

## Tasks
1. Create dataset of math word problems
2. Implement CoT prompting strategy
3. Implement self-consistency with multiple samples
4. Compare accuracy across approaches

## Expected Outputs
- Problem dataset
- Implementation of each approach
- Accuracy comparison analysis
""",
                "solution.py": '''"""Math Word Problem Solver"""

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
'''
            }
        },
        "04-complex-workflows": {
            "README.md": """# Complex Prompt Workflows

## Topics
- Chain-of-Density (CoD)
- Self-Ask and Answer (S2A)
- Prompt Chaining
- Meta Prompting

## Learning Objectives
- Design multi-step prompt workflows
- Implement meta-prompting for optimization
- Build prompt chains for complex tasks

## Key Concepts

### Chain-of-Density
Iteratively refine summaries through multiple prompting steps.

### Prompt Chaining
Connect multiple prompts where output of one becomes input of next.

### Meta Prompting
Use prompts to generate or optimize other prompts.

## Exercises
1. Build a prompt chain for document summarization
2. Implement meta-prompting for prompt optimization
3. Design multi-step workflows for complex tasks
""",
            "notebook.ipynb": '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Complex Workflow Examples\\n",
    "Implement and test various prompt chaining and meta-prompting techniques."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''',
            "mini-project": {
                "README.md": """# Mini Project: Auto Prompt Optimizer

## Objective
Build a meta-prompting system that automatically optimizes prompts for specific tasks.

## Tasks
1. Design meta-prompt that evaluates prompt quality
2. Implement iterative optimization loop
3. Create evaluation metrics for prompts
4. Test on sample optimization tasks

## Expected Outputs
- Meta-prompt template
- Optimization algorithm
- Evaluation framework
""",
                "solution.py": '''"""Auto Prompt Optimizer"""

from utils.llm_client import call_llm

def meta_optimize(task: str, initial_prompt: str, iterations: int = 3) -> str:
    """Optimize a prompt using meta-prompting."""
    # TODO: Implement meta-optimization
    pass

if __name__ == "__main__":
    # Test optimizer
    pass
'''
            }
        },
        "05-multimodal-and-applied": {
            "README.md": """# Multimodal and Applied Prompting

## Topics
- Multimodal prompting (text + images)
- RAG prompting techniques
- Image generation prompting
- Video generation prompting

## Learning Objectives
- Design prompts for multimodal models
- Implement RAG-aware prompting
- Master image/video generation prompts

## Key Concepts

### Multimodal Prompting
Combining text with image, audio, or video inputs.

### RAG Prompting
Designing prompts that work with retrieved context.

### Generation Prompting
Crafting prompts for image/video generation models.

## Exercises
1. Create multimodal analysis prompts
2. Design RAG-aware question answering prompts
3. Experiment with image generation prompt styles
""",
            "notebook.ipynb": '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Multimodal Prompting Examples\\n",
    "Explore prompting techniques for multimodal models."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''',
            "mini-project": {
                "README.md": """# Mini Project: Mini RAG Prompting Kit

## Objective
Build a mini RAG (Retrieval-Augmented Generation) prompting system that demonstrates effective retrieval-aware prompting.

## Tasks
1. Design prompts that incorporate retrieved context
2. Implement context-aware question answering
3. Create prompts for different retrieval scenarios
4. Test with sample documents

## Expected Outputs
- RAG prompt templates
- Context integration examples
- Performance evaluation
""",
                "solution.py": '''"""Mini RAG Prompting Kit"""

from utils.llm_client import call_llm

def rag_prompt(question: str, context: str) -> str:
    """Create a RAG-aware prompt."""
    # TODO: Implement RAG prompting
    pass

if __name__ == "__main__":
    # Test RAG prompting
    pass
'''
            }
        },
        "06-security-and-robustness": {
            "README.md": """# Security and Robustness

## Topics
- Adversarial prompting
- Prompt injection attacks
- Jailbreaking techniques
- Defense mechanisms

## Learning Objectives
- Identify common attack vectors
- Implement basic defense mechanisms
- Test prompt robustness

## Key Concepts

### Prompt Injection
Malicious input that hijacks the original prompt's intent.

### Jailbreaking
Bypassing safety restrictions through clever prompting.

### Defenses
Techniques to prevent adversarial attacks.

## Exercises
1. Test common injection attacks
2. Implement input validation and sanitization
3. Design defense mechanisms against attacks
""",
            "notebook.ipynb": '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Security Testing Examples\\n",
    "Explore adversarial prompting and defense mechanisms."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''',
            "mini-project": {
                "README.md": """# Mini Project: Prompt Injection Test Harness

## Objective
Build a test harness for evaluating prompt injection attacks and defenses.

## Tasks
1. Create dataset of common injection attacks
2. Implement basic defense mechanisms
3. Test attacks against defenses
4. Generate security evaluation report

## Expected Outputs
- Attack dataset
- Defense implementations
- Evaluation results
""",
                "solution.py": '''"""Prompt Injection Test Harness"""

from utils.llm_client import call_llm

def test_injection(attack_prompt: str) -> str:
    """Test an injection attack."""
    # TODO: Implement attack testing
    pass

def defend_against_injection(user_input: str) -> str:
    """Apply defense against injection."""
    # TODO: Implement defense
    pass

if __name__ == "__main__":
    # Test harness
    pass
'''
            }
        },
        "07-prompt-management": {
            "README.md": """# Prompt Management

## Topics
- Prompt lifecycle management
- Version control for prompts
- Testing and evaluation
- Storage and retrieval

## Learning Objectives
- Design prompt management systems
- Implement version control for prompts
- Build evaluation pipelines

## Key Concepts

### Lifecycle Management
Managing prompts from creation to retirement.

### Version Control
Tracking changes and maintaining multiple prompt versions.

### Evaluation
Testing prompts for quality, safety, and performance.

## Exercises
1. Design a prompt versioning system
2. Implement automated prompt testing
3. Create a simple prompt registry
""",
            "notebook.ipynb": '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Prompt Management Examples\\n",
    "Explore prompt lifecycle, versioning, and evaluation."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''',
            "mini-project": {
                "README.md": """# Mini Project: Prompt Eval Pipeline

## Objective
Build a prompt evaluation pipeline using DeepEval with a simple prompt registry.

## Tasks
1. Design prompt registry schema
2. Implement evaluation metrics
3. Create automated testing pipeline
4. Generate evaluation reports

## Expected Outputs
- Prompt registry system
- Evaluation pipeline
- Performance metrics
""",
                "solution.py": '''"""Prompt Eval Pipeline"""

from utils.llm_client import call_llm

class PromptRegistry:
    """Simple prompt registry."""
    
    def __init__(self):
        self.prompts = {}
    
    def register(self, name: str, prompt: str, version: str = "1.0"):
        """Register a prompt."""
        # TODO: Implement registration
        pass
    
    def get(self, name: str, version: str = None):
        """Get a prompt."""
        # TODO: Implement retrieval
        pass

def evaluate_prompt(prompt: str, test_cases: list) -> dict:
    """Evaluate a prompt using test cases."""
    # TODO: Implement evaluation
    pass

if __name__ == "__main__":
    # Test pipeline
    pass
'''
            }
        },
        "resources": {
            "cheatsheet.md": """# Prompt Engineering Cheatsheet

## Basic Techniques
- **Zero-shot**: Direct instructions without examples
- **One-shot**: Single example for demonstration
- **Few-shot**: Multiple examples for pattern establishment

## Configuration Parameters
- **Temperature**: 0.0 (deterministic) → 1.5 (creative)
- **Top-p**: Nucleus sampling threshold
- **Top-k**: Number of top tokens to consider

## Reasoning Techniques
- **Chain-of-Thought**: Show reasoning steps
- **Self-Consistency**: Multiple samples + majority vote
- **Plan-and-Solve**: Break down complex problems

## Safety Considerations
- Validate user inputs
- Implement content filtering
- Test for adversarial attacks

## Best Practices
1. Be specific and clear
2. Use examples when helpful
3. Iterate and test
4. Consider edge cases
5. Document your prompts
""",
            "further-reading.md": """# Further Reading

## Research Papers
- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- "Self-Consistency Improves Chain of Thought Reasoning"
- "Constitutional AI: Harmlessness from AI Feedback"

## Online Resources
- OpenAI Prompt Engineering Guide
- Anthropic Prompt Engineering Documentation
- Google AI Prompt Design Strategies

## Books
- "Prompt Engineering for Generative AI"
- "The Art of Prompt Engineering with ChatGPT"

## Communities
- r/PromptEngineering
- Prompt Engineering Discord
- AI Safety communities
"""
        }
    }
    
    # Create README.md
    readme_content = """# Prompt Engineering Mastery

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🎯 Learning Roadmap

```
01-foundations → 02-essential-strategies → 03-reasoning-and-logic
                     ↓                            ↓
              04-complex-workflows → 05-multimodal-and-applied
                     ↓                            ↓
              06-security-and-robustness → 07-prompt-management
```

## 📚 Module Overview

| Module | Topic | Mini-Project |
|--------|-------|--------------|
| 01 | Foundations | Parameter Playground |
| 02 | Essential Strategies | Few-Shot Classifier Builder |
| 03 | Reasoning & Logic | Math Word Problem Solver |
| 04 | Complex Workflows | Auto Prompt Optimizer |
| 05 | Multimodal & Applied | Mini RAG Prompting Kit |
| 06 | Security & Robustness | Prompt Injection Test Harness |
| 07 | Prompt Management | Prompt Eval Pipeline |

## 🚀 Quick Start

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up API keys in `.env` (copy from `.env.example`)
4. Start with `01-foundations/README.md`

## 🛠️ Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

## 📖 Each Module Contains

- **README.md**: Theory and concepts
- **notebook.ipynb**: Interactive experiments
- **mini-project/**: Hands-on practice

## 🤝 Contributing

Feel free to open issues or submit PRs with improvements!

## 📄 License

MIT License - see [LICENSE](LICENSE) for details
"""
    
    # Create requirements.txt
    requirements_content = """openai>=1.0.0
anthropic>=0.18.0
python-dotenv>=1.0.0
pandas>=1.5.0
matplotlib>=3.6.0
jupyter>=1.0.0
ipykernel>=6.0.0
deepeval>=0.20.0
"""
    
    # Create .env.example
    env_example_content = """# API Keys for LLM Providers
# Copy this file to .env and fill in your keys

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
"""
    
    # Create files and directories
    print("Creating project structure...")
    
    # Write root files
    with open(base_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("[OK] Created README.md")
    
    with open(base_path / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print("[OK] Created requirements.txt")
    
    with open(base_path / ".env.example", "w", encoding="utf-8") as f:
        f.write(env_example_content)
    print("[OK] Created .env.example")
    
    # Create directories and files
    for dir_name, content in structure.items():
        dir_path = base_path / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"[OK] Created {dir_name}/")
        
        if isinstance(content, dict):
            for file_name, file_content in content.items():
                file_path = dir_path / file_name
                if isinstance(file_content, dict):
                    # It's a subdirectory with files
                    sub_dir_path = dir_path / file_name
                    # Remove file if it exists with same name (from previous partial run)
                    if sub_dir_path.is_file():
                        sub_dir_path.unlink()
                    sub_dir_path.mkdir(exist_ok=True)
                    print(f"  [OK] Created {dir_name}/{file_name}/")
                    for sub_file_name, sub_file_content in file_content.items():
                        sub_file_path = sub_dir_path / sub_file_name
                        with open(sub_file_path, "w", encoding="utf-8") as f:
                            f.write(sub_file_content)
                        print(f"    [OK] Created {dir_name}/{file_name}/{sub_file_name}")
                else:
                    # It's a file - remove if it exists as a file (from previous partial run)
                    if file_path.is_file():
                        file_path.unlink()
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(file_content)
                    print(f"  [OK] Created {dir_name}/{file_name}")
    
    print("\n[DONE] Project structure created successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your API keys to .env")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start with 01-foundations/README.md")

if __name__ == "__main__":
    create_directory_structure()