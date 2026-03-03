"""
NVIDIA NIM Inference Client
-----------------------------
Kostenlose Inferenz via NVIDIA NIM API für simple Agents.
Kompatibel mit llm_router.py complete() Signatur.

Basis URL: https://integrate.api.nvidia.com/v1
API Key: .env → NVIDIA_API_KEY
Kostenlose Modelle:
  - meta/llama-3.1-8b-instruct   (empfohlen, schnell)
  - mistralai/mistral-7b-instruct-v0.3
"""
from __future__ import annotations

import logging
import os
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Verfügbare kostenlose NVIDIA NIM Modelle (Stand März 2026)
NVIDIA_MODELS = {
    "default": "meta/llama-3.1-8b-instruct",
    "fast":    "meta/llama-3.1-8b-instruct",
    "quality": "mistralai/mistral-7b-instruct-v0.3",
}

# Agenten die ideal für NVIDIA NIM Tier sind (simple, kostengünstig)
_NVIDIA_SUITABLE_AGENTS = frozenset({
    "agent-product-catalog-sync",
    "agent-gdpr-data-retention-manager",
    "agent-affiliate-data-refresh",
    "agent-digistore-feed-parser",
})


def _get_nvidia_client() -> OpenAI:
    """OpenAI-kompatibler Client gegen NVIDIA NIM Endpoint."""
    api_key = os.getenv("NVIDIA_API_KEY", "placeholder")
    return OpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=api_key,
    )


def complete(
    prompt: str,
    model: str = "meta/llama-3.1-8b-instruct",
    system: Optional[str] = None,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """
    Sendet einen Prompt an NVIDIA NIM.
    API-kompatibel mit llm_router.complete() – gleiche Signatur.

    Args:
        prompt: User-Prompt
        model: NVIDIA NIM Modell-ID
        system: Optionaler System-Prompt
        max_tokens: Max Output Tokens
        temperature: Sampling Temperature

    Returns:
        Antwort-Text des Modells.

    Raises:
        RuntimeError: wenn NIM nicht erreichbar.
    """
    client = _get_nvidia_client()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        logger.debug("NVIDIA NIM: model=%s", model)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=False,
        )
        content = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else "?"
        logger.info("NVIDIA NIM OK: model=%s tokens=%s", model, tokens)
        return content
    except Exception as exc:
        logger.warning("NVIDIA NIM FAIL model=%s: %s", model, exc)
        raise RuntimeError(f"NVIDIA NIM error: {exc}") from exc


def is_nvidia_suitable(agent_id: str) -> bool:
    """Prüft ob ein Agent ideal für NVIDIA NIM Tier ist."""
    return agent_id in _NVIDIA_SUITABLE_AGENTS


async def complete_async(
    prompt: str,
    model: str = "meta/llama-3.1-8b-instruct",
    system: Optional[str] = None,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """Async-Wrapper – kompatibel mit llm_router.complete_async()."""
    import asyncio
    from functools import partial

    loop = asyncio.get_event_loop()
    fn = partial(
        complete,
        prompt=prompt,
        model=model,
        system=system,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return await loop.run_in_executor(None, fn)
