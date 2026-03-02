"""
Phase 2 – Integration tests via httpx AsyncClient.
Covers: Agents, Contracts, Bidding, Transactions, IoT, Wallets, Health.
"""
import pytest
from httpx import AsyncClient


# ── Health ─────────────────────────────────────────────────────────────────

async def test_health_endpoint(client: AsyncClient):
    r = await client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["version"] == "2.0.0"
    assert body["db"] == "connected"


# ── Agents ─────────────────────────────────────────────────────────────────

async def test_register_publisher_agent(client: AsyncClient):
    r = await client.post("/agents/register", json={"name": "Kühlschrank Agent", "type": "publisher"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert body["type"] == "publisher"
    assert "agent_id" in body


async def test_register_advertiser_agent(client: AsyncClient):
    r = await client.post("/agents/register", json={"name": "Amazon DE Agent", "type": "advertiser"})
    assert r.status_code == 200
    body = r.json()
    assert body["type"] == "advertiser"


async def test_register_invalid_agent_type(client: AsyncClient):
    r = await client.post("/agents/register", json={"name": "Bad Agent", "type": "hacker"})
    assert r.status_code == 400


async def test_list_agents(client: AsyncClient):
    await client.post("/agents/register", json={"name": "Agent 1", "type": "publisher"})
    await client.post("/agents/register", json={"name": "Agent 2", "type": "advertiser"})
    r = await client.get("/agents/")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 2


async def test_get_agent_detail(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "Detail Agent", "type": "arbitrage"})
    agent_id = reg.json()["agent_id"]
    r = await client.get(f"/agents/{agent_id}")
    assert r.status_code == 200
    assert r.json()["agent"]["type"] == "arbitrage"


async def test_get_agent_not_found(client: AsyncClient):
    r = await client.get("/agents/nonexistent-id-12345")
    assert r.status_code == 404


# ── Smart Contracts ────────────────────────────────────────────────────────

async def test_create_contract_publisher(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "Fridge", "type": "publisher"})
    agent_id = reg.json()["agent_id"]
    r = await client.post(
        f"/contracts/{agent_id}/create",
        json={"product": "Milch", "condition": "stock < 2", "max_price": 2.50},
        params={"monthly_budget": 100.0},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert "contract_id" in body


async def test_create_contract_advertiser_forbidden(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "Shop", "type": "advertiser"})
    agent_id = reg.json()["agent_id"]
    r = await client.post(
        f"/contracts/{agent_id}/create",
        json={"product": "Shirt", "condition": "stock < 5", "max_price": 10.0},
    )
    assert r.status_code == 403


async def test_list_contracts_by_agent(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "Printer", "type": "publisher"})
    agent_id = reg.json()["agent_id"]
    # Create two contracts
    await client.post(
        f"/contracts/{agent_id}/create",
        json={"product": "Toner", "condition": "stock < 1", "max_price": 15.0},
    )
    await client.post(
        f"/contracts/{agent_id}/create",
        json={"product": "Paper", "condition": "stock < 5", "max_price": 8.0},
    )
    r = await client.get(f"/contracts/{agent_id}/list")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 2
    assert body["agent_id"] == agent_id


async def test_list_contracts_agent_not_found(client: AsyncClient):
    r = await client.get("/contracts/no-such-agent/list")
    assert r.status_code == 404


# ── Bidding ────────────────────────────────────────────────────────────────

async def test_create_bid_advertiser(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "Rewe Shop", "type": "advertiser"})
    agent_id = reg.json()["agent_id"]
    r = await client.post(
        f"/bidding/{agent_id}/create",
        json={"product_category": "dairy", "commission_rate": 0.08, "daily_budget": 50.0},
    )
    assert r.status_code == 200
    assert "bid_id" in r.json()


async def test_list_bids_empty(client: AsyncClient):
    r = await client.get("/bidding/")
    assert r.status_code == 200
    assert r.json()["count"] == 0


async def test_list_bids_after_creation(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "DM Shop", "type": "advertiser"})
    agent_id = reg.json()["agent_id"]
    await client.post(
        f"/bidding/{agent_id}/create",
        json={"product_category": "beauty", "commission_rate": 0.12},
    )
    r = await client.get("/bidding/")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


# ── Transactions ───────────────────────────────────────────────────────────

async def test_list_transactions(client: AsyncClient):
    r = await client.get("/transactions/")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert "transactions" in body


async def test_get_transaction_not_found(client: AsyncClient):
    r = await client.get("/transactions/nonexistent-tx-id")
    assert r.status_code == 404


# ── IoT Devices ────────────────────────────────────────────────────────────

async def test_register_iot_device(client: AsyncClient):
    r = await client.post(
        "/iot/devices/register",
        json={"name": "Kühlschrank v2", "device_type": "fridge"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert "device_id" in body
    assert "api_key" in body


async def test_list_iot_devices(client: AsyncClient):
    await client.post("/iot/devices/register", json={"name": "Drucker", "device_type": "printer"})
    r = await client.get("/iot/devices")
    assert r.status_code == 200
    assert r.json()["count"] >= 1


# ── Wallets ────────────────────────────────────────────────────────────────

async def test_wallet_creation(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "Wallet Agent", "type": "publisher"})
    agent_id = reg.json()["agent_id"]
    r = await client.post(
        f"/wallets/{agent_id}/create",
        json={"address": "0xABCDEF1234567890", "wallet_type": "polygon"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert body["address"] == "0xABCDEF1234567890"
    assert body["ydm_balance"] == 0.0


async def test_wallet_duplicate_rejected(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "Dup Agent", "type": "advertiser"})
    agent_id = reg.json()["agent_id"]
    await client.post(f"/wallets/{agent_id}/create", json={"address": "0x111"})
    r2 = await client.post(f"/wallets/{agent_id}/create", json={"address": "0x222"})
    assert r2.status_code == 400


async def test_get_wallet(client: AsyncClient):
    reg = await client.post("/agents/register", json={"name": "WalletGet", "type": "arbitrage"})
    agent_id = reg.json()["agent_id"]
    await client.post(f"/wallets/{agent_id}/create", json={"address": "0xDEADBEEF"})
    r = await client.get(f"/wallets/{agent_id}")
    assert r.status_code == 200
    assert r.json()["wallet"]["address"] == "0xDEADBEEF"


# ── Background Scheduler ────────────────────────────────────────────────────

def test_background_scheduler_imports():
    """Verify scheduler can be imported without errors."""
    from app.services.scheduler import init_scheduler, shutdown_scheduler
    assert callable(init_scheduler)
    assert callable(shutdown_scheduler)


# ── ML Predictors ──────────────────────────────────────────────────────────

def test_ml_demand_prediction():
    from app.services.ml_predictor import check_ml_based_demand
    should_order, confidence = check_ml_based_demand("agent_test_123", "dairy")
    assert isinstance(should_order, bool)
    assert 0.0 <= confidence <= 1.0


def test_trust_score_calculation():
    from app.services.ml_predictor import calculate_trust_score_ml
    score = calculate_trust_score_ml(
        success_rate=0.9,
        weekly_tx_count=5,
        avg_tx_value=15.0,
        refund_rate=0.02,
    )
    assert isinstance(score, int)
    assert 0 <= score <= 100
