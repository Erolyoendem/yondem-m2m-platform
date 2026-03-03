"""
Awin + Affiliate Integration Tests
------------------------------------
T1  – awin_client importiert korrekt
T2  – get_programmes() gibt Liste zurück (gemockt)
T3  – get_best_offers() filtert nach min_commission korrekt
T4  – search_products() gibt Liste zurück (gemockt)
T5  – digistore_client importiert korrekt
T6  – get_top_products() gibt Sample-Daten zurück wenn Feed offline
T7  – Affiliate Router GET /affiliate/offers erreichbar
T8  – Affiliate Router GET /affiliate/match/{id} erreichbar
T9  – Affiliate Router POST /affiliate/track erreichbar
T10 – LLM Router select_model() gibt korrekte Modelle zurück
T11 – LLM Router NVIDIA NIM Routing für simple Agents
T12 – NVIDIA NIM Client importiert korrekt
"""
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient


# ---------------------------------------------------------------------------
# T1 – awin_client Import
# ---------------------------------------------------------------------------

def test_t1_awin_client_imports():
    from app.services import awin_client
    assert hasattr(awin_client, "get_programmes")
    assert hasattr(awin_client, "get_best_offers")
    assert hasattr(awin_client, "search_products")
    assert hasattr(awin_client, "get_publisher_transactions")


# ---------------------------------------------------------------------------
# T2 – get_programmes() mit Mock
# ---------------------------------------------------------------------------

def test_t2_get_programmes_returns_list():
    from app.services.awin_client import get_programmes

    mock_response = [
        {"name": "Amazon DE", "commissionRange": {"min": 5.0, "max": 10.0}, "clickThroughUrl": "https://awin.com/1"},
        {"name": "Zalando", "commissionRange": {"min": 3.0, "max": 8.0}, "clickThroughUrl": "https://awin.com/2"},
    ]

    with patch("app.services.awin_client._get", return_value=mock_response):
        result = get_programmes("DE")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Amazon DE"


# ---------------------------------------------------------------------------
# T3 – get_best_offers() filtert korrekt
# ---------------------------------------------------------------------------

def test_t3_get_best_offers_filters_by_commission():
    from app.services.awin_client import get_best_offers

    mock_programmes = [
        {"name": "HighCommission Shop", "commissionRange": {"min": 15.0, "max": 20.0}, "clickThroughUrl": "https://a.com/1"},
        {"name": "LowCommission Shop", "commissionRange": {"min": 1.0, "max": 2.0}, "clickThroughUrl": "https://a.com/2"},
        {"name": "MidCommission Shop", "commissionRange": {"min": 8.0, "max": 10.0}, "clickThroughUrl": "https://a.com/3"},
    ]

    with patch("app.services.awin_client._get", return_value=mock_programmes):
        # Minimum 5% Commission
        offers = get_best_offers(min_commission=5.0, max_results=10)

    assert isinstance(offers, list)
    # Nur HighCommission (20%) und MidCommission (10%) sollen durch
    assert all(o["commission_rate"] >= 5.0 for o in offers)
    # Sortiert nach höchster Commission
    if len(offers) >= 2:
        assert offers[0]["commission_rate"] >= offers[1]["commission_rate"]


# ---------------------------------------------------------------------------
# T4 – search_products() mit Mock
# ---------------------------------------------------------------------------

def test_t4_search_products_returns_list():
    from app.services.awin_client import search_products

    mock_result = {
        "products": [
            {"title": "Produkt A", "price": 29.99, "url": "https://shop.com/a"},
            {"title": "Produkt B", "price": 49.99, "url": "https://shop.com/b"},
        ]
    }

    with patch("app.services.awin_client._get", return_value=mock_result):
        result = search_products("laptop", max_results=5)

    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# T5 – digistore_client Import
# ---------------------------------------------------------------------------

def test_t5_digistore_client_imports():
    from app.services import digistore_client
    assert hasattr(digistore_client, "get_top_products")
    assert hasattr(digistore_client, "_sample_products")


# ---------------------------------------------------------------------------
# T6 – get_top_products() gibt Sample-Daten zurück wenn Feed offline
# ---------------------------------------------------------------------------

def test_t6_digistore_returns_sample_when_offline():
    from app.services.digistore_client import get_top_products

    # Feed offline simulieren
    with patch("app.services.digistore_client._fetch_feed", return_value=None):
        result = get_top_products(max_results=10)

    assert isinstance(result, list)
    assert len(result) > 0
    assert all("product_name" in p for p in result)
    assert all("commission_rate" in p for p in result)
    assert all(p["network"] == "digistore24" for p in result)


# ---------------------------------------------------------------------------
# T7 – GET /affiliate/offers erreichbar
# ---------------------------------------------------------------------------

async def test_t7_affiliate_offers_endpoint(client: AsyncClient):
    r = await client.get("/affiliate/offers")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "offers" in body
    assert isinstance(body["offers"], list)


# ---------------------------------------------------------------------------
# T8 – GET /affiliate/match/{publisher_id} erreichbar
# ---------------------------------------------------------------------------

async def test_t8_affiliate_match_endpoint(client: AsyncClient):
    r = await client.get("/affiliate/match/test-publisher-001")
    # 200 OK (DB leer → live fetch) oder 404 wenn kein Angebot
    assert r.status_code in (200, 404)
    if r.status_code == 200:
        body = r.json()
        assert body["status"] == "ok"
        assert "publisher_id" in body


# ---------------------------------------------------------------------------
# T9 – POST /affiliate/track
# ---------------------------------------------------------------------------

async def test_t9_affiliate_track_endpoint(client: AsyncClient):
    # Erst ein Offer erstellen ist nötig (DB leer) → 404 erwartet
    r = await client.post(
        "/affiliate/track",
        json={"publisher_id": "pub-001", "offer_id": 9999, "amount": 100.0},
    )
    # 404 weil kein Offer mit id=9999 in Test-DB
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# T10 – LLM Router select_model() korrekte Modelle
# ---------------------------------------------------------------------------

def test_t10_llm_router_select_model_complex():
    from app.services.llm_router import select_model, MODELS
    model = select_model(agent_id="agent-dirigent")
    assert model == MODELS["complex"]


def test_t10b_llm_router_select_model_standard():
    from app.services.llm_router import select_model, MODELS
    model = select_model(agent_id="agent-unknown", task_complexity="standard")
    assert model == MODELS["standard"]


# ---------------------------------------------------------------------------
# T11 – NVIDIA NIM Routing für simple Agents
# ---------------------------------------------------------------------------

def test_t11_llm_router_nvidia_for_simple_agents():
    from app.services.llm_router import select_model, MODELS
    model = select_model(agent_id="agent-product-catalog-sync")
    assert model == MODELS["simple"]
    assert "nvidia" in model or "llama" in model


def test_t11b_llm_router_local_fallback():
    from app.services.llm_router import select_model, MODELS
    model = select_model(task_complexity="local")
    assert model == MODELS["local"]
    assert "free" in model


# ---------------------------------------------------------------------------
# T12 – NVIDIA NIM Client Import
# ---------------------------------------------------------------------------

def test_t12_nvidia_nim_client_imports():
    from app.services import nvidia_nim_client
    assert hasattr(nvidia_nim_client, "complete")
    assert hasattr(nvidia_nim_client, "complete_async")
    assert hasattr(nvidia_nim_client, "is_nvidia_suitable")
    assert hasattr(nvidia_nim_client, "NVIDIA_MODELS")


def test_t12b_nvidia_nim_suitable_agents():
    from app.services.nvidia_nim_client import is_nvidia_suitable
    assert is_nvidia_suitable("agent-product-catalog-sync") is True
    assert is_nvidia_suitable("agent-dirigent") is False
