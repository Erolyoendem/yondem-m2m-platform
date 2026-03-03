"""
LLM Router via OpenRouter API + NVIDIA NIM
-------------------------------------------
4-Stufen Routing für optimale Kosten:
  complex  → anthropic/claude-opus-4    (OpenRouter, ~15$/1M Token)
  standard → deepseek/deepseek-chat     (OpenRouter, ~0.14$/1M Token)
  simple   → meta/llama-3.1-8b         (NVIDIA NIM, kostenlos)
  fallback → meta-llama/llama-3.2-3b:free (OpenRouter, kostenlos)

Automatisches Failover innerhalb der Kette.
"""
from __future__ import annotations

import logging
import os
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 4-Stufen Modell-Konfiguration
# ---------------------------------------------------------------------------
MODELS = {
    "complex":  "anthropic/claude-opus-4",              # teuerste, beste Qualität
    "standard": "deepseek/deepseek-chat",               # Standard, günstig
    "simple":   "nvidia/meta/llama-3.1-8b-instruct",   # NVIDIA NIM, kostenlos
    "local":    "meta-llama/llama-3.2-3b-instruct:free",  # OpenRouter Free Fallback
}

# Fallback-Kette (günstigstes zuerst nach Versagen des primären Modells)
FALLBACK_CHAIN = [
    "deepseek/deepseek-chat",
    "nvidia/meta/llama-3.1-8b-instruct",
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemma-3-4b-it:free",
]

# Agents die immer das komplexe Modell brauchen
_COMPLEX_AGENTS = frozenset({"agent-dirigent", "agent-orchestrator", "agent-compliance"})

# Agents die mit NVIDIA NIM (kostenlos) auskommen
_SIMPLE_AGENTS = frozenset({
    "agent-product-catalog-sync",
    "agent-gdpr-data-retention-manager",
    "agent-affiliate-data-refresh",
    "agent-digistore-feed-parser",
})


def _get_openrouter_client() -> OpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY", "sk-or-free")
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def _get_nvidia_client() -> OpenAI:
    api_key = os.getenv("NVIDIA_API_KEY", "placeholder")
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )


def select_model(agent_id: str = "", task_complexity: str = "standard") -> str:
    """
    Wählt das optimale Modell anhand Agent-ID und Komplexität.

    Routing-Logik:
    1. Bekannte komplexe Agents → claude-opus-4
    2. Bekannte simple Agents → NVIDIA NIM (kostenlos)
    3. task_complexity="local" → OpenRouter Free
    4. Sonst → task_complexity Mapping
    """
    if agent_id in _COMPLEX_AGENTS:
        return MODELS["complex"]
    if agent_id in _SIMPLE_AGENTS:
        return MODELS["simple"]
    if task_complexity == "local":
        return MODELS["local"]
    return MODELS.get(task_complexity, MODELS["standard"])


def _is_nvidia_model(model: str) -> bool:
    return model.startswith("nvidia/")


def _nvidia_model_name(model: str) -> str:
    """Extrahiert den reinen Modell-Namen für NVIDIA NIM API."""
    return model.replace("nvidia/", "")


def complete(
    prompt: str,
    agent_id: str = "",
    task_complexity: str = "standard",
    system: Optional[str] = None,
    max_tokens: int = 512,
    temperature: float = 0.3,
) -> str:
    """
    Sendet einen Prompt an das optimale LLM.
    Automatisches Failover durch 4-Stufen-Kette.

    NVIDIA NIM Modelle werden direkt an NVIDIA API geroutet.
    Alle anderen gehen über OpenRouter.

    Returns:
        Antwort-Text des Modells.
    Raises:
        RuntimeError: wenn alle Modelle fehlschlagen.
    """
    model = select_model(agent_id=agent_id, task_complexity=task_complexity)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    # Aufbau der Kandidaten-Kette (primary + fallbacks ohne Duplikate)
    candidates = [model] + [m for m in FALLBACK_CHAIN if m != model]

    for candidate in candidates:
        try:
            logger.debug("LLMRouter: model=%s agent=%s", candidate, agent_id)

            if _is_nvidia_model(candidate):
                # NVIDIA NIM Endpunkt
                client = _get_nvidia_client()
                nim_model = _nvidia_model_name(candidate)
                response = client.chat.completions.create(
                    model=nim_model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=False,
                )
            else:
                # OpenRouter Endpunkt
                client = _get_openrouter_client()
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
            tokens = response.usage.total_tokens if response.usage else "?"
            logger.info("LLMRouter OK: model=%s tokens=%s", candidate, tokens)
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
