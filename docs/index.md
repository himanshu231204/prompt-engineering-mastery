---
title: Prompt Engineering Mastery
description: A model-agnostic, engineering-first curriculum for building reliable LLM-powered systems.
hide:
  - navigation
  - toc
---

<div class="pem-hero" markdown>

<p class="pem-eyebrow">Model-agnostic · OpenAI · Anthropic · Ollama</p>

# Prompt engineering, treated like software — not a listicle of tips.

<p class="pem-sub">A production-grade curriculum for engineers building reliable LLM systems: design
patterns, failure modes, security threats, testing strategies, and evaluation pipelines — each
backed by a runnable notebook and a mini-project with real model output.</p>

<div class="pem-cta-row" markdown>
[Start at Module 01 →](modules/01-foundations.md){ .md-button .md-button--primary }
[View Quick Start](quick-start.md){ .md-button }
</div>

</div>

<div class="pem-terminal" markdown>
```bash
# clone & enter
$ git clone https://github.com/himanshu231204/prompt-engineering-mastery.git
$ cd prompt-engineering-mastery

# set up environment
$ python -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt

# configure a provider
$ cp .env.example .env
# edit .env → OPENAI_API_KEY | ANTHROPIC_API_KEY | (Ollama needs none)

# launch module 01
$ jupyter notebook 01-foundations/notebook.ipynb
[NotebookApp] Serving notebooks from 01-foundations/
[NotebookApp] Kernel started — ready.
```
</div>

<div class="pem-stats" markdown>

| | | | |
|---|---|---|---|
| **7** <br><span>Modules, foundations → security & eval</span> | **7** <br><span>Mini-projects with visible artifacts</span> | **3** <br><span>Supported providers — OpenAI, Anthropic, Ollama</span> | **MIT** <br><span>License — free to use, fork, extend</span> |

</div>

## Why this repo

Every claim below is a design decision made in this repo, not marketing copy.

<div class="grid cards" markdown>

-   :material-circle-outline: **Model-agnostic by construction**

    Every example runs through the shared `utils/llm_client.py` abstraction. Switch
    OpenAI → Anthropic → Ollama by changing one parameter, never rewriting a prompt.

-   :material-check-bold: **Proof, not theory**

    Every technique ships a runnable notebook demonstrating real before/after model
    output, plus a mini-project that produces a visible artifact you can inspect.

-   :material-shield-alert-outline: **Security is a full module**

    [Module 06](modules/06-security-and-robustness.md) covers adversarial prompting, injection, jailbreaking, and OWASP
    Top 10 for LLM Applications — treated as an architectural requirement, not an
    afterthought.

-   :material-chart-timeline-variant: **Evaluation is automated**

    [Module 07](modules/07-prompt-management.md) introduces DeepEval — pytest-native, CI-compatible evaluation —
    so prompt regressions are caught the same way code regressions are.

-   :material-sitemap-outline: **Diagrams matched to concept**

    Mermaid diagrams are chosen by what they depict — flowcharts for logic, sequence
    diagrams for calls, architecture diagrams for systems — not dropped in decoratively.

-   :material-rhombus-outline: **Lifecycle, not one-off strings**

    Prompts move through plan → draft → version → test → store → deploy → monitor,
    with Promptmetheus for drafting and versioning.

</div>

## Curriculum

Start at Module 01 and work forward. Already shipping LLM systems? Jump straight to 06
and 07 — the parts most prompt content skips.

| # | Module | What you learn | Mini-project | Difficulty |
|---|--------|-----------------|---------------|-------------|
| 01 | [Foundations](modules/01-foundations.md) | LLM mechanics, temperature, top-p, top-k, tokens | Parameter Playground | :material-circle:{ .pem-beg } Beginner |
| 02 | [Essential Strategies](modules/02-essential-strategies.md) | Zero/one/few-shot, system instructions, delimiters | Few-Shot Classifier Builder | :material-circle:{ .pem-beg } Beginner |
| 03 | [Reasoning & Logic](modules/03-reasoning-and-logic.md) | Chain of Thought, Self-Consistency, Plan-and-Solve | Math Word Problem Solver | :material-circle:{ .pem-int } Intermediate |
| 04 | [Complex Workflows](modules/04-complex-workflows.md) | Chain of Draft, System 2 Attention, chaining, meta prompting | Auto Prompt Optimizer | :material-circle:{ .pem-adv } Advanced |
| 05 | [Multimodal & Applied](modules/05-multimodal-and-applied.md) | RAG prompting, image/video generation, multimodal inputs | Mini RAG Prompting Kit | :material-circle:{ .pem-int } Intermediate |
| 06 | [Security & Robustness](modules/06-security-and-robustness.md) | Adversarial prompting, injection, jailbreaking, OWASP Top 10 | Prompt Injection Test Harness | :material-circle:{ .pem-adv } Advanced |
| 07 | [Prompt Management](modules/07-prompt-management.md) | Lifecycle, versioning, Promptmetheus, DeepEval evaluation | Prompt Eval Pipeline | :material-circle:{ .pem-adv } Advanced |
