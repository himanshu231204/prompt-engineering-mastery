<p align="center">
  <h1 align="center">Prompt Engineering Mastery</h1>
  <p align="center">
    <strong>The production-grade reference for engineering prompts like software — not prompt tips, but prompt engineering as a discipline.</strong>
  </p>
  <p align="center">
    <a href="#modules">Modules</a> · <a href="#quick-start">Quick Start</a> · <a href="#what-makes-this-different">Why This Repo</a> · <a href="#contributing">Contribute</a>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/LLM-Agnostic-FF6B6B" alt="LLM Agnostic">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Modules-7-9B59B6" alt="Modules">
  <img src="https://img.shields.io/badge/Mini--Projects-7-E67E22" alt="Mini-Projects">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen" alt="Status">
</p>

<p align="center">
  <a href="https://github.com/himanshu231204" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-himanshu231204-181717?logo=github&logoColor=white" alt="GitHub">
  </a>
  <a href="https://linkedin.com/in/himanshu231204" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-himanshu231204-0A66C2?logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://twitter.com/himanshu231204" target="_blank">
    <img src="https://img.shields.io/badge/Twitter-himanshu231204-1DA1F2?logo=x&logoColor=white" alt="Twitter">
  </a>
</p>

---

## What This Is

Prompt Engineering Mastery is a **model-agnostic, engineering-first curriculum** for building reliable LLM-powered systems. It treats prompting as a software engineering discipline — with design patterns, failure modes, security threats, testing strategies, versioning practices, and evaluation pipelines.

Every technique ships with a runnable notebook demonstrating real before/after model output, and a mini-project that produces a visible artifact.

**This is not** a "50 best ChatGPT prompts" listicle. It's a structured reference for engineers who build production LLM applications.

---

## What Makes This Different

| Aspect | Typical Prompt Repos | This Repo |
|--------|---------------------|-----------|
| **Scope** | Prompt collections | End-to-end engineering discipline |
| **Vendor lock-in** | OpenAI-only examples | Model-agnostic via shared abstraction (OpenAI, Anthropic, Ollama) |
| **Depth** | Surface-level tips | Security (Module 6), evaluation (Module 7), versioning, lifecycle management |
| **Proof** | Theory only | Every technique has runnable notebook + mini-project with real model output |
| **Visuals** | None | Mermaid diagrams matched to concept type (flowcharts, sequence, architecture) |
| **Security** | Ignored | Full module on adversarial prompting, injection, jailbreaking, and defense |
| **Evaluation** | Manual testing only | Automated evaluation with DeepEval (pytest-native, CI-compatible) |

---

## Modules

| # | Module | What You Learn | Mini-Project | Difficulty |
|---|--------|---------------|--------------|------------|
| 01 | [Foundations](01-foundations/) | LLM mechanics, temperature, top-p, top-k, tokens | Parameter Playground | Beginner |
| 02 | [Essential Strategies](02-essential-strategies/) | Zero/one/few-shot, system instructions, delimiters | Few-Shot Classifier Builder | Beginner |
| 03 | [Reasoning & Logic](03-reasoning-and-logic/) | Chain of Thought, Self-Consistency, Plan-and-Solve | Math Word Problem Solver | Intermediate |
| 04 | [Complex Workflows](04-complex-workflows/) | Chain of Draft, System 2 Attention, Prompt Chaining, Meta Prompting | Auto Prompt Optimizer | Advanced |
| 05 | [Multimodal & Applied](05-multimodal-and-applied/) | RAG prompting, image/video generation, multimodal inputs | Mini RAG Prompting Kit | Intermediate |
| 06 | [Security & Robustness](06-security-and-robustness/) | Adversarial prompting, injection, jailbreaking, OWASP Top 10 | Prompt Injection Test Harness | Advanced |
| 07 | [Prompt Management](07-prompt-management/) | Lifecycle, versioning, Promptmetheus, DeepEval evaluation | Prompt Eval Pipeline | Advanced |

### Learning Paths

**New to prompt engineering?** Start at Module 01 and work forward. Each module builds on the previous.

**Experienced engineer?** Jump to [Module 06](06-security-and-robustness/) (security) and [Module 07](07-prompt-management/) (evaluation/management) — these are the differentiators from generic prompt content.

---

## Quick Start

```bash
# Clone
git clone https://github.com/himanshu231204/prompt-engineering-mastery.git
cd prompt-engineering-mastery

# Setup
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your API keys to .env (OpenAI, Anthropic, or Ollama)

# Start
jupyter notebook 01-foundations/notebook.ipynb
```

### Supported Providers

| Provider | Default Model | Key Required |
|----------|--------------|--------------|
| OpenAI | gpt-4o | `OPENAI_API_KEY` |
| Anthropic | claude-sonnet-4-20250514 | `ANTHROPIC_API_KEY` |
| Ollama | llama3 | None (runs locally) |

All code uses the shared `utils/llm_client.py` abstraction — switch providers by changing one parameter, not rewriting prompts.

---

## Project Structure

```
prompt-engineering-mastery/
├── README.md                          # You are here
├── requirements.txt                   # Pinned dependencies
├── .env.example                       # API key placeholders
├── utils/
│   └── llm_client.py                  # Model-agnostic LLM call wrapper
├── resources/
│   ├── cheatsheet.md                  # One-page technique reference
│   └── further-reading.md             # Curated external resources
├── 01-foundations/                    # Module 1
│   ├── README.md                      # Theory + Mermaid diagrams
│   ├── notebook.ipynb                 # Interactive demo
│   └── mini-project/                  # Applied project
├── 02-essential-strategies/           # Module 2
├── 03-reasoning-and-logic/            # Module 3
├── 04-complex-workflows/              # Module 4
├── 05-multimodal-and-applied/         # Module 5
├── 06-security-and-robustness/        # Module 6
└── 07-prompt-management/              # Module 7
```

Each module README includes:
- Difficulty tags (Beginner / Intermediate / Advanced)
- "Why this matters for an AI engineer" — real production concerns
- Concept explanations with original prose
- Mermaid diagrams matched to concept type
- Before/after examples with real model output
- Common pitfalls section

---

## Each Module Contains

| File | Purpose |
|------|---------|
| `README.md` | Theory, concepts, Mermaid diagrams, before/after examples, pitfalls |
| `notebook.ipynb` | Runnable top-to-bottom demo with real model output |
| `mini-project/solution.py` | Applied project with visible artifact output |
| `mini-project/README.md` | What it does, how to run, expected output |

---

## Who This Is For

| Audience | What You Get |
|----------|-------------|
| **AI/ML Engineers** | Reusable patterns for production RAG, agents, and LLM workflows |
| **Software Developers** | Engineering-first approach to prompt design — patterns, not tips |
| **Students** | Structured curriculum from foundations to security and evaluation |
| **Hiring Managers** | Proof of engineering maturity beyond "knows how to use ChatGPT" |

---

## Contributing

Contributions are welcome. Before submitting:

1. Check that your change aligns with the module structure in `AGENTS.md`
2. Ensure notebooks run top-to-bottom without manual edits
3. Verify mini-projects produce visible artifacts
4. No hardcoded API keys — all credentials via `.env`

```bash
# Run the full test suite (when available)
deepeval test run
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built by <a href="https://github.com/himanshu231204"><strong>himanshu231204</strong></a> · 
  <a href="https://github.com/himanshu231204/prompt-engineering-mastery">GitHub</a> · 
  <a href="https://linkedin.com/in/himanshu231204">LinkedIn</a> · 
  <a href="https://twitter.com/himanshu231204">Twitter/X</a>
</p>
