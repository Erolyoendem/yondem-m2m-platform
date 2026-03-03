"""
Awin Affiliate Network Client
------------------------------
Verbindet sich mit der Awin API (https://api.awin.com) um:
- Provisionen (Transactions) des Publishers abzurufen
- Verfügbare Advertiser-Programme zu laden
- Produkte für Agent A36 zu suchen

API Key aus .env: AWIN_API_KEY
"""
from __future__ import annotations

import logging
import os
from typing import Any

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.awin.com"


def _headers() -> dict[str, str]:
    api_key = os.getenv("AWIN_API_KEY", "placeholder")
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }


def _get(path: str, params: dict | None = None, timeout: int = 10) -> Any:
    """HTTP GET gegen Awin API mit Fehlerbehandlung."""
    url = f"{BASE_URL}{path}"
    try:
        resp = requests.get(url, headers=_headers(), params=params or {}, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as exc:
        logger.warning("Awin HTTP error %s %s: %s", exc.response.status_code, url, exc)
        return None
    except requests.exceptions.RequestException as exc:
        logger.warning("Awin request error %s: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_publisher_transactions(publisher_id: str | int) -> list[dict]:
    """
    GET /publishers/{publisherId}/transactions
    Gibt Liste der Provisionen (Transaktionen) des Publishers zurück.
    """
    data = _get(f"/publishers/{publisher_id}/transactions")
    if data is None:
        return []
    # Awin gibt {"data": [...]} oder direkt eine Liste zurück
    if isinstance(data, list):
        return data
    return data.get("data", [])


def get_programmes(country_code: str = "DE") -> list[dict]:
    """
    GET /publishers/{publisherId}/programmes
    Lädt alle verfügbaren Advertiser-Programme für ein Land.
    Gibt Liste mit id, name, commissionRange, clickThroughUrl zurück.
    """
    publisher_id = os.getenv("AWIN_PUBLISHER_ID", "0")
    data = _get(
        f"/publishers/{publisher_id}/programmes",
        params={"relationship": "joined", "countryCode": country_code},
    )
    if data is None:
        return []
    if isinstance(data, list):
        return data
    return data.get("data", [])


def search_products(
    keyword: str,
    advertiser_id: str | int | None = None,
    max_results: int = 20,
) -> list[dict]:
    """
    GET /product/search – Produktsuche für Agent A36.
    Gibt Liste mit Produktname, Preis, Provisions-URL zurück.
    """
    params: dict[str, Any] = {
        "term": keyword,
        "pageSize": max_results,
    }
    if advertiser_id:
        params["advertiserId"] = advertiser_id

    data = _get("/product/search", params=params)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    return data.get("products", data.get("data", []))


def get_best_offers(min_commission: float = 5.0, max_results: int = 10) -> list[dict]:
    """
    Kombiniert get_programmes() und filtert nach höchster Commission.
    Wird vom Background Job und /affiliate/offers verwendet.
    """
    programmes = get_programmes()
    offers = []
    for p in programmes:
        # Awin commissionRange kann {"min": x, "max": y} sein
        commission = 0.0
        cr = p.get("commissionRange") or p.get("commission", {})
        if isinstance(cr, dict):
            commission = float(cr.get("max", cr.get("min", 0)) or 0)
        elif isinstance(cr, (int, float)):
            commission = float(cr)

        if commission >= min_commission:
            offers.append({
                "network": "awin",
                "advertiser_name": p.get("name", "Unknown"),
                "product_name": p.get("description", ""),
                "commission_rate": commission,
                "conversion_rate": float(p.get("conversionRate", 0) or 0),
                "url": p.get("clickThroughUrl", ""),
            })

    # Sortiert nach höchster Commission, begrenzt auf max_results
    offers.sort(key=lambda x: x["commission_rate"], reverse=True)
    return offers[:max_results]
