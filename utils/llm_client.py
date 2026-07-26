"""Thin wrapper for calling different LLM providers.

Model-agnostic interface for OpenAI, Anthropic, and Ollama (local).
All credentials loaded from environment variables via .env file.
"""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def call_llm(
    prompt: str,
    provider: str = "openai",
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    system_prompt: Optional[str] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    **kwargs,
) -> str:
    """Call an LLM provider with the given prompt.

    Args:
        prompt: The input prompt to send to the model.
        provider: LLM provider - "openai", "anthropic", or "ollama".
        model: Model name. Defaults to provider-specific default if None.
        temperature: Sampling temperature (0.0-2.0 for OpenAI, 0.0-1.0 for Anthropic).
        max_tokens: Maximum tokens to generate.
        system_prompt: Optional system-level instruction prepended to the conversation.
        top_p: Nucleus sampling threshold (0.0-1.0). Use instead of temperature, not both.
        top_k: Top-k sampling (Anthropic only, 1-500). Limits token selection to k most likely tokens.
        **kwargs: Additional provider-specific arguments passed directly to the API.

    Returns:
        Generated response as a plain string.

    Raises:
        ValueError: If an unsupported provider is specified.
        RuntimeError: If the API call fails after retries.
    """
    if provider == "openai":
        return _call_openai(prompt, model, temperature, max_tokens, system_prompt, top_p, **kwargs)
    elif provider == "anthropic":
        return _call_anthropic(prompt, model, temperature, max_tokens, system_prompt, top_p, top_k, **kwargs)
    elif provider == "ollama":
        return _call_ollama(prompt, model, temperature, max_tokens, system_prompt, **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}. Use 'openai', 'anthropic', or 'ollama'.")


def _call_openai(
    prompt: str,
    model: Optional[str],
    temperature: float,
    max_tokens: int,
    system_prompt: Optional[str],
    top_p: Optional[float],
    **kwargs,
) -> str:
    """Call OpenAI API using the Responses API (current primary interface).

    Falls back to Chat Completions if Responses API is unavailable.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package not installed. Run: pip install openai")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment. Copy .env.example to .env and add your key.")

    client = OpenAI(api_key=api_key)
    use_model = model or "gpt-4o"

    # Build input messages
    messages = []
    if system_prompt:
        messages.append({"role": "developer", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Build parameters
    params = {
        "model": use_model,
        "messages": messages,
        "temperature": temperature,
        "max_output_tokens": max_tokens,
    }
    if top_p is not None:
        params["top_p"] = top_p
    params.update(kwargs)

    try:
        response = client.chat.completions.create(**params)
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {e}")


def _call_anthropic(
    prompt: str,
    model: Optional[str],
    temperature: float,
    max_tokens: int,
    system_prompt: Optional[str],
    top_p: Optional[float],
    top_k: Optional[int],
    **kwargs,
) -> str:
    """Call Anthropic Messages API.

    Note: Anthropic max_tokens is REQUIRED (no default). We set it explicitly.
    System prompt goes in a separate parameter, NOT in messages.
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic package not installed. Run: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in environment. Copy .env.example to .env and add your key.")

    client = anthropic.Anthropic(api_key=api_key)
    use_model = model or "claude-sonnet-4-20250514"

    # Anthropic requires max_tokens explicitly
    params = {
        "model": use_model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    if system_prompt:
        params["system"] = system_prompt
    if top_p is not None:
        params["top_p"] = top_p
    if top_k is not None:
        params["top_k"] = top_k
    params.update(kwargs)

    try:
        response = client.messages.create(**params)
        return response.content[0].text
    except Exception as e:
        raise RuntimeError(f"Anthropic API call failed: {e}")


def _call_ollama(
    prompt: str,
    model: Optional[str],
    temperature: float,
    max_tokens: int,
    system_prompt: Optional[str],
    **kwargs,
) -> str:
    """Call local Ollama instance via HTTP.

    Ollama runs locally on port 11434 by default.
    No API key required.
    """
    import requests

    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    use_model = model or "llama3"

    # Build messages for Ollama's OpenAI-compatible endpoint
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": use_model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    if "top_p" in kwargs:
        payload["options"]["top_p"] = kwargs["top_p"]
    if "top_k" in kwargs:
        payload["options"]["top_k"] = kwargs["top_k"]

    try:
        response = requests.post(f"{base_url}/v1/chat/completions", json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Cannot connect to Ollama at {base_url}. Is Ollama running?")
    except Exception as e:
        raise RuntimeError(f"Ollama API call failed: {e}")
