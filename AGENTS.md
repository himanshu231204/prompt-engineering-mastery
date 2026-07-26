# AGENTS.md

This file is the operating manual for any AI coding agent (OpenCode) building this repository. Read `PROJECT.md` first for vision/scope, and `CONTEXT.md` for source curriculum content. This file defines **how** to build — conventions, standards, and rules that must stay consistent across all 7 modules.

---

## 1. Build Order & Process

- Build **one module at a time**, in order (01 → 07).
- After finishing a module, self-check it against Section 4 (Content Standards) and Section 6 (Definition of Done per Module) before starting the next.
- Do not begin scaffolding a new module until the previous one passes its own checklist.
- If a later module's technique builds on an earlier one (e.g., Module 4's Prompt Chaining builds on Module 3's Plan-and-Solve), explicitly cross-reference it rather than re-explaining from scratch.

## 2. Folder & File Conventions

Every module MUST follow this exact structure — no exceptions, no drift:

```
NN-module-slug/
├── README.md
├── notebook.ipynb
└── mini-project/
    ├── README.md        # what it does, how to run it, expected output
    ├── main.py           # or app.py — the runnable entry point
    └── (supporting files as needed)
```

- `NN` is a two-digit zero-padded prefix (`01`, `02`, ... `07`) matching module order.
- `module-slug` is lowercase-kebab-case, e.g. `01-foundations`, `03-reasoning-and-logic`.
- Never rename this pattern in later modules even if a "better" naming idea appears — consistency across the repo outranks local optimization.

## 3. Code Standards

- **Model-agnostic by default.** All notebooks and mini-projects call the shared `utils/llm_client.py` abstraction:
  ```python
  from utils.llm_client import call_llm
  response = call_llm(prompt, provider="openai")  # or "anthropic", "ollama"
  ```
- **No hardcoded API keys.** All credentials come from `.env` (see `.env.example`). Never commit real keys.
- **Type hints and docstrings required** on all functions in shared utilities and mini-project entry points.
- **Notebooks must run top-to-bottom without manual edits** (aside from setting the provider/model name in a config cell at the top).
- **Mini-projects must run in under 10 minutes** on a standard laptop with no GPU required, unless the module explicitly deals with local/open models (state this clearly if so).
- Every mini-project must produce a **visible, savable artifact** — e.g., printed comparison table, saved JSON/CSV, a generated chart, or rendered output — something that can be screenshotted for a portfolio or LinkedIn post.

## 4. Content Standards (per module README)

Every module `README.md` MUST include, in this order:

1. **Title + one-line summary**
2. **Difficulty tags** — mark each major section 🟢 Beginner / 🟡 Intermediate / 🔴 Advanced
3. **"Why this matters for an AI engineer"** — a short section connecting the technique to real production concerns (cost, latency, reliability, correctness) — never just a dictionary-style definition
4. **Concept explanation** — clear, original prose (never copy-pasted vendor docs)
5. **At least one Mermaid diagram** matched to the concept type (see Section 5)
6. **Before/After example** — a real prompt shown without the technique vs. with the technique, and the resulting difference in output quality/behavior
7. **Link to the module's notebook and mini-project**
8. **"Common pitfalls" section** — at least 2–3 real failure modes engineers hit with this technique

## 5. Mermaid Diagram Rules

Every concept gets a diagram type matched to its nature — don't default to flowcharts for everything:

| Module | Diagram type | What it should show |
|---|---|---|
| 01 – Foundations | Flowchart / decision diagram | How temperature/top-p/top-k affect output distribution and when to tune each |
| 02 – Essential Strategies | Decision tree | When to use zero-shot vs one-shot vs few-shot vs system prompting |
| 03 – Reasoning & Logic | Flowchart with branches | CoT reasoning steps; Self-Consistency's multiple-paths-then-vote pattern; Plan-and-Solve's plan→execute split |
| 04 – Complex Workflows | Sequence diagram + feedback loop diagram | Prompt Chaining as a sequence of calls; Meta Prompting as a generate→evaluate→refine loop |
| 05 – Multimodal & Applied | Architecture diagram | Full RAG pipeline (query → retrieve → augment → generate); multimodal input handling |
| 06 – Security & Robustness | Attack/defense flow diagram | Injection attempt → detection layer → mitigation → safe output |
| 07 – Prompt Management | Lifecycle diagram | Full loop: plan → draft → version → test → store → deploy → monitor |

Diagrams are embedded directly in the README using fenced ` ```mermaid ` blocks — never as external image files.

## 6. Definition of Done — Per Module

A module is complete only when:

- [ ] Folder structure matches Section 2 exactly
- [ ] README follows all 8 required sections from Section 4
- [ ] At least one Mermaid diagram is present and matches Section 5's guidance
- [ ] Notebook runs standalone and demonstrates real before/after model output
- [ ] Mini-project runs in under 10 minutes and produces a visible artifact
- [ ] No hardcoded credentials; uses `llm_client` abstraction
- [ ] Content reflects the actual course outline topic from `CONTEXT.md` — no invented subtopics, no skipped subtopics
- [ ] Tone matches Section 7 (below)

## 7. Tone & Voice Rules

- Write for someone who **can already code** but is new to *this specific discipline* — skip "what is a variable" energy, skip "what is an LLM" 101 fluff.
- Be direct and engineering-first. No motivational filler like "prompting is a superpower" or "unlock the potential of AI."
- Prefer concrete examples over abstract description. Show, don't just tell.
- It is acceptable — encouraged — to note real limitations and tradeoffs of a technique (e.g., "Self-Consistency improves accuracy but multiplies token cost N times, so use it selectively").

## 8. Do-Not Rules

- Do NOT copy-paste OpenAI/Anthropic/Google documentation, even reworded closely — write original explanations.
- Do NOT pad module READMEs with generic filler to hit a length target.
- Do NOT introduce vendor lock-in anywhere in code — if a technique genuinely requires a specific vendor feature, state that explicitly as an exception and explain why.
- Do NOT skip the security module's depth to save time — Module 6 gets the same engineering rigor as Modules 1–5.
- Do NOT treat later modules (6, 7) as "bonus" — they are core to the repo's differentiation from generic prompt-tip content.

## 9. Root-Level Deliverables (build once, not per module)

- `README.md` — repo overview, badges, module map/table of contents, "start here" paths for beginner vs. advanced readers, setup instructions
- `utils/llm_client.py` — the shared model-agnostic call wrapper
- `requirements.txt` — pinned dependencies
- `.env.example` — placeholder env vars for OpenAI/Anthropic/Ollama, never real keys
- `resources/cheatsheet.md` — one-page technique reference (good candidate for a LinkedIn carousel later)
- `resources/further-reading.md` — curated external resources per module

## 10. Freshness Rule
Before writing any module's theory section, fetch and cross-check against 
the current version of relevant vendor documentation (see CONTEXT.md 
Section 3). Do not rely solely on training data for technique names, 
parameter defaults, or tool capabilities — these change frequently.
---

Refer back to `PROJECT.md` if any build decision seems to conflict with the repo's overall vision or audience. Refer to `CONTEXT.md` for the exact source curriculum content each module must cover.
