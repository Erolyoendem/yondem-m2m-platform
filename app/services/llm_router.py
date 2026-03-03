"""
LLM Router via OpenRouter API
------------------------------
Einziger LLM-Endpunkt für alle Modelle.
Routing: complex → Claude Opus, standard/simple → Deepseek Chat
Automatisches Failover auf nächstgünstiges Modell.
"""
from __future__ import annotations

import logging
import os
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Modell-Konfiguration (günstigstes zuerst = Fallback-Reihenfolge)
# ---------------------------------------------------------------------------
MODELS = {
    "complex":  "anthropic/claude-opus-4",
    "standard": "deepseek/deepseek-chat",
    "simple":   "deepseek/deepseek-chat",
    "local":    "meta-llama/llama-3.2-3b-instruct:free",
}

# Fallback-Kette: wenn Modell nicht verfügbar → nächstes probieren
FALLBACK_CHAIN = [
    "deepseek/deepseek-chat",
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemma-3-4b-it:free",
]

# Agents die immer das komplexe Modell brauchen
_COMPLEX_AGENTS = frozenset({"agent-dirigent", "agent-orchestrator", "agent-compliance"})
# Agents die mit dem günstigsten Modell auskommen
_SIMPLE_AGENTS = frozenset({"agent-product-catalog-sync", "agent-gdpr-data-retention-manager"})


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY", "sk-or-free")
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def select_model(agent_id: str = "", task_complexity: str = "standard") -> str:
    """Wählt das optimale Modell anhand Agent-ID und Komplexität."""
    if agent_id in _COMPLEX_AGENTS:
        return MODELS["complex"]
    if agent_id in _SIMPLE_AGENTS:
        return MODELS["simple"]
    if task_complexity == "local":
        return MODELS["local"]
    return MODELS.get(task_complexity, MODELS["standard"])


def complete(
    prompt: str,
    agent_id: str = "",
    task_complexity: str = "standard",
    system: Optional[str] = None,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """
    Sendet einen Prompt an OpenRouter.
    Automatisches Failover: wenn das gewählte Modell nicht antwortet,
    wird die Fallback-Kette probiert.

    Returns:
        Antwort-Text des Modells.
    Raises:
        RuntimeError: wenn alle Modelle fehlschlagen.
    """
    model = select_model(agent_id=agent_id, task_complexity=task_complexity)
    client = _get_client()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    # Erste Anfrage mit gewähltem Modell
    candidates = [model] + [m for m in FALLBACK_CHAIN if m != model]

    for candidate in candidates:
        try:
            logger.debug("LLMRouter: model=%s agent=%s", candidate, agent_id)
            response = client.chat.completions.create(
                model=candidate,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                extra_headers={
                    "HTTP-Referer": "https://yondem.io",
                    "X-Title": "Yondem M2M Platform",
                },
            )
            content = response.choices[0].message.content or ""
            logger.info("LLMRouter OK: model=%s tokens=%s", candidate, response.usage.total_tokens if response.usage else "?")
            return content
        except Exception as exc:
            logger.warning("LLMRouter FAIL model=%s: %s – trying next", candidate, exc)

    raise RuntimeError("LLMRouter: alle Modelle fehlgeschlagen")


# ---------------------------------------------------------------------------
# Async-Wrapper (für FastAPI Routen)
# ---------------------------------------------------------------------------
async def complete_async(
    prompt: str,
    agent_id: str = "",
    task_complexity: str = "standard",
    system: Optional[str] = None,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """Async-Wrapper – läuft sync complete() in Thread-Pool."""
    import asyncio
    from functools import partial

    loop = asyncio.get_event_loop()
    fn = partial(
        complete,
        prompt=prompt,
        agent_id=agent_id,
        task_complexity=task_complexity,
        system=system,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return await loop.run_in_executor(None, fn)
