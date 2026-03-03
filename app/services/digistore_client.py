"""
Digistore24 Feed Client
------------------------
Lädt den öffentlichen RSS/XML Produkt-Feed von Digistore24
und stellt Top-Produkte nach Conversion Rate für Agent A41
(cross-sell-recommender) bereit.

Feed URL: https://www.digistore24.com/rss/products
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from typing import Any

import requests

logger = logging.getLogger(__name__)

FEED_URL = "https://www.digistore24.com/rss/products"
_TIMEOUT = 15


def _fetch_feed(url: str = FEED_URL) -> str | None:
    """Lädt den RSS/XML Feed als Text."""
    try:
        resp = requests.get(url, timeout=_TIMEOUT, headers={"User-Agent": "Yondem-Bot/2.0"})
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.RequestException as exc:
        logger.warning("Digistore24 feed error: %s", exc)
        return None


def _parse_feed(xml_text: str) -> list[dict[str, Any]]:
    """Parst den RSS XML Feed und extrahiert Produkt-Metadaten."""
    products = []
    try:
        root = ET.fromstring(xml_text)
        # RSS 2.0: root → channel → item
        channel = root.find("channel")
        if channel is None:
            channel = root

        for item in channel.findall("item"):
            def tag(name: str) -> str:
                el = item.find(name)
                return el.text.strip() if el is not None and el.text else ""

            # Versuche Commission und Conversion Rate aus Namespaced Tags
            commission = 0.0
            conversion = 0.0
            for child in item:
                local = child.tag.split("}")[-1].lower()
                val = (child.text or "").strip().replace("%", "").replace(",", ".")
                if local in ("commission", "commissionrate"):
                    try:
                        commission = float(val)
                    except ValueError:
                        pass
                if local in ("conversionrate", "conversion"):
                    try:
                        conversion = float(val)
                    except ValueError:
                        pass

            product = {
                "network": "digistore24",
                "advertiser_name": "Digistore24",
                "product_name": tag("title"),
                "commission_rate": commission,
                "conversion_rate": conversion,
                "url": tag("link"),
                "description": tag("description")[:200] if tag("description") else "",
            }
            products.append(product)
    except ET.ParseError as exc:
        logger.warning("Digistore24 XML parse error: %s", exc)

    return products


def get_top_products(
    min_commission: float = 0.0,
    max_results: int = 20,
) -> list[dict[str, Any]]:
    """
    Lädt den Digistore24 Feed und gibt Top-Produkte zurück,
    sortiert nach Conversion Rate (für Agent A41).

    Args:
        min_commission: Mindest-Provision in Prozent (Filter).
        max_results: Maximale Anzahl zurückgegebener Produkte.

    Returns:
        Liste mit Produkt-Dicts: network, advertiser_name, product_name,
        commission_rate, conversion_rate, url.
    """
    xml_text = _fetch_feed()
    if not xml_text:
        # Fallback: leere Liste mit Beispiel-Daten für Tests
        logger.info("Digistore24 feed not reachable – returning sample data")
        return _sample_products()[:max_results]

    products = _parse_feed(xml_text)
    filtered = [p for p in products if p["commission_rate"] >= min_commission]
    filtered.sort(key=lambda x: x["conversion_rate"], reverse=True)
    return filtered[:max_results]


def _sample_products() -> list[dict[str, Any]]:
    """Fallback-Daten wenn Feed nicht erreichbar (Tests, Offline)."""
    return [
        {
            "network": "digistore24",
            "advertiser_name": "Digistore24",
            "product_name": "Online Marketing Kurs",
            "commission_rate": 50.0,
            "conversion_rate": 3.2,
            "url": "https://www.digistore24.com/product/sample1",
            "description": "Kompletter Online Marketing Kurs für Einsteiger",
        },
        {
            "network": "digistore24",
            "advertiser_name": "Digistore24",
            "product_name": "E-Commerce Masterclass",
            "commission_rate": 40.0,
            "conversion_rate": 2.8,
            "url": "https://www.digistore24.com/product/sample2",
            "description": "Shopware & WooCommerce von A bis Z",
        },
        {
            "network": "digistore24",
            "advertiser_name": "Digistore24",
            "product_name": "Affiliate Marketing Bibel",
            "commission_rate": 60.0,
            "conversion_rate": 4.1,
            "url": "https://www.digistore24.com/product/sample3",
            "description": "Passives Einkommen mit Affiliate Marketing",
        },
    ]
