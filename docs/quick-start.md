# Quick Start

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

## Supported providers

| Provider | Default Model | Key Required |
|----------|--------------|--------------|
| OpenAI | gpt-4o | `OPENAI_API_KEY` |
| Anthropic | claude-sonnet-4-20250514 | `ANTHROPIC_API_KEY` |
| Ollama | llama3 | None (runs locally) |

All code uses the shared `utils/llm_client.py` abstraction — switch providers by changing
one parameter, not rewriting prompts.

## Project structure

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
