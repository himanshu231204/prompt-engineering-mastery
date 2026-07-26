# PROJECT.md

## Vision

This repository is a **production-grade, engineering-first reference for AI engineers and AI software developers** who build LLM-powered systems — not a tutorial for casual prompt tinkerers.

Prompting is treated here as a **software engineering discipline**: it has design patterns, failure modes, security threats, testing strategies, versioning practices, and evaluation pipelines — the same way REST API design or database schema design does. This repo documents and demonstrates that discipline end-to-end.

## What This Is NOT

To keep every contributor and every AI agent building this repo aligned, we explicitly reject the following patterns:

- ❌ A "50 best ChatGPT prompts" listicle repo
- ❌ Prompt collections with no explanation of *why* they work
- ❌ Content that assumes the reader can't code
- ❌ Vendor-locked examples (OpenAI-only or Claude-only)
- ❌ Copy-pasted vendor documentation reworded
- ❌ Theory without a runnable artifact to prove the concept

## What This IS

- ✅ A **model-agnostic** curriculum — every technique demonstrated works across OpenAI, Anthropic, and local/open models via a shared abstraction
- ✅ **Layered for beginner → advanced** — every module has a 🟢 Beginner, 🟡 Intermediate, and 🔴 Advanced layer, so a CS student and a working AI engineer both get value without needing separate repos
- ✅ **Provable, not just explained** — every technique ships with a notebook that demonstrates the before/after difference with real model output
- ✅ **Applied through mini-projects** — each module ends in a small, runnable project that produces a visible artifact (console output, saved JSON, chart, screenshot-worthy result)
- ✅ **Visualized** — every core concept has a Mermaid diagram embedded directly in its README (flowcharts for reasoning logic, sequence diagrams for chaining, architecture diagrams for RAG, etc.)
- ✅ **Security-aware** — adversarial prompting, injection, and jailbreaking are treated as first-class engineering concerns (Module 6), not an afterthought
- ✅ **Lifecycle-aware** — prompts are versioned, tested, and evaluated like code (Module 7), using real tooling (DeepEval)

## Target Audience

| Audience | What they get from this repo |
|---|---|
| Students / early-career devs learning GenAI | A structured, credible on-ramp into prompt engineering as a real discipline |
| Practicing AI/ML & GenAI engineers | Reusable patterns, a reference they can point teammates to, techniques they can lift directly into production RAG/agent systems |
| Recruiters / hiring managers evaluating a candidate | Proof of engineering maturity — not just "knows prompts" but "engineers prompts like software" |

## Repository Scope

The repo is organized into **7 modules**, mapped directly from the course curriculum:

1. **Foundations of Generative AI & Prompting** — LLM mechanics, model configuration (temperature, top-p, top-k, tokens)
2. **Essential Prompting Strategies** — zero/one/few-shot, system instructions & persona, delimiter prompting
3. **Advanced Reasoning & Logic Techniques** — Chain of Thought, Consistency, Self-Consistency, Plan-and-Solve
4. **Complex Workflows & System Optimization** — Chain of Draft, System 2 Attention, Prompt Chaining, Meta Prompting
5. **Multimodal & Applied Prompting** — multimodal inputs, RAG prompting, image/video generation prompting
6. **Security & Robustness** — adversarial prompting, prompt injection, jailbreaking, defense techniques
7. **Prompt Management** — lifecycle (plan/draft/version/test/store), prompt tooling, evaluation with DeepEval

Each module folder contains:

```
NN-module-name/
├── README.md          # theory + why it matters + Mermaid diagram(s) + before/after example
├── notebook.ipynb      # runnable, model-agnostic demonstration
└── mini-project/       # small applied project with a visible output artifact
```

Shared infrastructure lives at the repo root (`utils/llm_client.py`, `requirements.txt`, `.env.example`).

## Success Criteria ("Definition of Done")

The repo is considered complete when:

- [ ] All 7 modules follow the identical structural pattern (no drift in later modules)
- [ ] Every module's README has at least one Mermaid diagram matched to its content type
- [ ] Every technique has a documented before/after comparison with real model output
- [ ] Every mini-project runs standalone in under 10 minutes and produces a visible artifact
- [ ] All code uses the shared `llm_client` abstraction — zero hardcoded vendor lock-in
- [ ] Root `README.md` gives a newcomer a clear map and a "start here" path for both beginner and advanced readers
- [ ] Module 6 and 7 (security + management) are given equal engineering weight to modules 1–5, not treated as bonus content

## Build Philosophy

This repo is built **module by module**, not in a single pass. Each module is reviewed against `AGENTS.md` conventions before the next one starts. This prevents quality drift, shallow content in later modules, and structural inconsistency — a known failure mode when large-scope repos are generated in one shot.

See `AGENTS.md` for build conventions and `CONTEXT.md` for the full source curriculum and reference material.
