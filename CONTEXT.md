# CONTEXT.md

This file is the **ground truth source material** for building this repository. It exists so the build agent (OpenCode) does not invent, skip, or hallucinate topic coverage. Every module's content must map directly back to the curriculum below.

See `PROJECT.md` for vision/scope and `AGENTS.md` for build conventions.

---

## 1. Source Curriculum (authoritative — do not deviate from subtopic coverage)

### Module 1: Foundations of Generative AI & Prompting
- Introduction to LLMs, the Mechanics of LLMs
- Prompts and Fundamentals of Prompt Engineering
- Model Configurations and Output Parameters (Temperature, Top-P, Tokens, etc.)
- Model Configurations and Output Parameter Tuning

### Module 2: Essential Prompting Strategies
- Shot Prompting
  - Zero-Shot Prompting
  - One-Shot Prompting
  - Few-Shot Prompting
- System Instruction Prompting (Role-playing and Persona Setting)
- Delimiter Prompting (Structuring Inputs for Clarity)

### Module 3: Advanced Reasoning & Logic Techniques
- Chain of Thought (CoT) Prompting
- Consistency Prompting
- Self-Consistency Prompting
- Plan and Solve Prompting

### Module 4: Complex Workflows & System Optimization
- Chain of Draft (CoD) Prompting
- System 2 Attention (S2A) Prompting
- Prompt Chaining (Breaking Down Tasks into Sequential Prompts)
- Meta Prompting (Using AI to Write or Optimize Prompts)

### Module 5: Multimodal & Applied Prompting
- Multi-Modal Prompting (Text + Image/Audio Inputs)
- RAG (Retrieval-Augmented Generation) Prompting
- Image Generation Model Prompting
- Video Generation Prompting

### Module 6: Security & Robustness
- Adversarial Prompting
- Prompt Injections and Jailbreaking
- Defense Techniques
- Prompt Techniques for Stopping Adversarial Prompting

### Module 7: Prompt Management
- Prompt Management Lifecycle
- Phases of Prompt Management Lifecycle (Planning, Drafting, Versioning, Testing, Storage)
- Promptmethous Tool
- Evaluation of Prompts Using DeepEval Library

---

## 2. Practitioner Context — Real-World Grounding for Examples

The repo author is an AI/ML and GenAI engineer with hands-on experience in RAG systems, LLM applications, and multi-agent AI. To make module content feel authored by a practitioner rather than generated, the build agent should draw on the following real project contexts **as inspiration for examples and mini-projects** (do not fabricate specifics not provided here — ask for detail if a module needs it):

- **RAGNOVA** — a Retrieval-Augmented Generation chatbot built with Groq, LangChain, FAISS, and Streamlit. Relevant to **Module 5** (RAG Prompting) — use it as the reference architecture for the RAG pipeline diagram and mini-project, generalized so it isn't tied to one specific stack.
- **Autonomous AI Research Operating System** — a multi-agent system design using LangGraph, FastAPI, Next.js, Ollama (local models), ChromaDB, PostgreSQL, Redis, Playwright, and LangSmith. Relevant to **Module 4** (Prompt Chaining, Meta Prompting) — the agent orchestration and reflection-loop patterns from this project are good grounding for how chaining/meta-prompting work in real multi-agent systems, not just toy demos.
- **Custom MCP web search server** (hosted on Render, integrated via Anthropic API's `mcp_servers` parameter) — relevant background for **Module 5** (tool-augmented / agentic prompting context) and **Module 7** (prompt management in agentic tool-calling systems).
- **DSA CheatSheet GPT** and **GATE CS custom GPTs** (with PYQ Priority Engine, subject-aware detection, hallucination guards) — relevant to **Module 2** (System Instruction Prompting / persona design) and **Module 6** (hallucination guard patterns relate to defense techniques) as real examples of system-prompt engineering for custom GPTs.

> **Note to build agent:** where a module would benefit from a specific real-world example beyond what's listed here, flag it rather than inventing fictional company/product names. Placeholder/generic examples (e.g., "a customer support bot," "a code review assistant") are acceptable when no real project maps cleanly.

---

## 3. Verified Living Sources (checked July 26, 2026)

These are confirmed current as of this date. Fetch them fresh at build time anyway — vendor docs move.

| Module | Resource | URL | Notes |
|---|---|---|---|
| 01 – Foundations | Claude prompt engineering overview | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | **Domain changed**: Anthropic migrated from `docs.anthropic.com` to `platform.claude.com`. Use the new domain. |
| 01 – Foundations | Claude 4 best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices | Model-specific tuning guidance |
| 01 – Foundations | OpenAI prompt engineering guide | https://developers.openai.com/api/docs/guides/prompt-engineering | **Domain changed**: moved from `platform.openai.com` to `developers.openai.com`. OpenAI is also de-emphasizing reusable prompt objects in the API from June 2026, shutting down `v1/prompts` Nov 30, 2026 — don't build examples around that deprecated feature. |
| 03 – Reasoning | Chain-of-Thought paper (Wei et al.) | https://arxiv.org/abs/2201.11903 | Stable, foundational |
| 03 – Reasoning | Self-Consistency paper (Wang et al.) | https://arxiv.org/abs/2203.11171 | Stable, foundational |
| 04 – Complex Workflows | Chain of Draft paper (Xu et al., 2025) | https://arxiv.org/abs/2502.18600 | Confirmed real. CoD matches/beats CoT accuracy using ~7.6% of the tokens — good concrete stat for the module's "why this matters" section (cost/latency argument). Code: https://github.com/sileix/chain-of-draft |
| 05 – RAG | Anthropic context engineering guide | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Anthropic now frames "context engineering" as the natural evolution of prompt engineering — worth a callout box in Module 5 or 7 distinguishing the two terms |
| 06 – Security | OWASP Top 10 for LLM Applications (2025, v2.0) | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Covers prompt injection, sensitive info disclosure, supply chain, data/model poisoning, improper output handling, excessive agency, system prompt leakage, vector/embedding weaknesses, misinformation, unbounded consumption |
| 06 – Security | OWASP Top 10 for Agentic Applications (2026, new) | (search "OWASP Top 10 Agentic Applications 2026" — actively updated, no single stable canonical URL confirmed yet) | **New in 2026**, covers agent-specific risks: goal hijacking, tool misuse, identity/privilege abuse, supply chain compromise, unexpected code execution, memory/context poisoning, insecure inter-agent comms, cascading failures, trust exploitation, rogue agents. Given this repo's multi-agent context (Module 4, 5), this is arguably MORE relevant than the base LLM Top 10 — recommend covering both in Module 6, with agentic risks as the advanced (🔴) layer |
| 07 – Management | DeepEval docs | https://deepeval.com/docs/getting-started | Confirmed active, Pytest-style local evaluation, model-agnostic |
| 07 – Management | DeepEval GitHub | https://github.com/confident-ai/deepeval | 16.7k+ stars, actively maintained. Also note: DeepEval has an official "5-min Vibe Coder Quickstart" specifically for AI coding agents (Cursor, Claude Code, Codex, etc.) to write the test suite for you — worth pointing OpenCode at this directly for Module 7's mini-project |

## 4. OpenCode-Specific Build Notes (verified July 26, 2026)

- **OpenCode natively reads `AGENTS.md`** — this is not a generic convention we invented, it's OpenCode's actual supported format. Confirmed via OpenCode's own ecosystem docs.
- **OpenCode supports Agent Skills** (`skills/SKILL.md` format, same convention used by Claude). If useful, we could add a `skills/` folder to this repo itself with reusable prompting-technique skills OpenCode can invoke.
- **OpenCode supports MCP servers** declared in `opencode.json` under the `mcp` key, both local (stdio subprocess) and remote (HTTPS, with automatic OAuth via Dynamic Client Registration). This means your own MCP web search server (hosted on Render) can be wired in directly:
  ```json
  {
    "mcp": {
      "web-search": {
        "type": "remote",
        "url": "https://your-render-url.onrender.com/mcp"
      }
    }
  }
  ```
- **Recommendation**: add this MCP server config to the repo-root setup step (Section 9 of `AGENTS.md`) so OpenCode can verify doc URLs live during the build, not just rely on training data — directly implementing the "Freshness Rule" discussed for `AGENTS.md`.

---

## 4. Tooling Called Out By Name in Curriculum

These two tools are explicitly named in the source curriculum and must be addressed directly rather than substituted silently:

- **Promptmetheus** (RESOLVED — the course PDF's "Promptmethous" was a transcription typo, verified July 26, 2026) — referenced in Module 7. Official site: https://promptmetheus.com, docs: https://docs.promptmetheus.com. It's a **prompt engineering IDE**: prompts are decomposed into composable "blocks" (Context → Task → Instructions → Samples/Shots → Primer), with per-block performance insights, cost estimation across model providers, dataset-driven testing, prompt-chain/agent tracing, and export to CSV/XLS/JSON. Module 7's README should introduce it as a concrete example of the "drafting" and "versioning" lifecycle phases — screenshot or describe the block-based composition model directly (verify current UI via docs before writing, since SaaS tools change their interface often).
- **DeepEval** — an open-source LLM evaluation library (confirmed at https://deepeval.com and https://github.com/confident-ai/deepeval, 16.7k+ GitHub stars). Module 7's evaluation mini-project should use this directly (real installable package: `pip install deepeval`), not a mocked substitute. Note: DeepEval publishes a "5-min Vibe Coder Quickstart" specifically written for AI coding agents to consume — worth having OpenCode fetch that page directly when building this mini-project.

---

## 5. Open Items Before Full Build

- [x] ~~Confirm exact name/spelling and feature set of "Promptmethous" tool~~ — Resolved: it's **Promptmetheus**, see Section 4
- [x] ~~Verify Chain of Draft paper exists and is correctly cited~~ — Confirmed: arXiv:2502.18600, real paper, real GitHub repo
- [x] ~~Verify current OWASP/DeepEval/vendor doc URLs~~ — Done, see Section 3. Two domain migrations found: Anthropic docs moved to `platform.claude.com`, OpenAI docs moved to `developers.openai.com`
- [ ] Confirm whether real project names (RAGNOVA, etc.) should be named explicitly in the public repo or generalized/anonymized
- [ ] Decide default LLM providers to wire into `utils/llm_client.py` (OpenAI + Anthropic + Ollama assumed per `PROJECT.md`)
- [ ] Decide whether to cover both OWASP LLM Top 10 (2025) AND the newer OWASP Agentic Top 10 (2026) in Module 6, given this repo's multi-agent context — recommended: yes, layer the agentic one as the 🔴 Advanced section
- [ ] Wire your own MCP web search server (Render-hosted) into `opencode.json` so OpenCode can verify doc URLs live during build — see Section 4 for exact config snippet