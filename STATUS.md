# YONDEM PLATFORM STATUS
# Stand: 2026-03-02

## Stack (modernisiert 2026-03-02)

| Komponente        | Version   | Status |
|-------------------|-----------|--------|
| Python            | 3.9 (venv)| ✅ |
| FastAPI           | 0.115     | ✅ |
| SQLAlchemy        | 2.0 async | ✅ |
| Pydantic          | v2 + pydantic-settings | ✅ |
| Alembic           | 1.14      | ✅ |
| scikit-learn ML   | 1.5       | ✅ |
| pytest-asyncio    | 1.2       | ✅ |
| aiosqlite (local) | 0.20      | ✅ |
| asyncpg (prod)    | ready     | ✅ |

## Phase 2: Smart Contracts + Bidding

### Abgeschlossen ✅
- Agent System (publisher / advertiser / arbitrage)
- Smart Contracts mit Regeln (GET /contracts/{agent_id}/list ergänzt)
- Bidding System
- Transaction Tracking
- IoT Device Registrierung
- Wallet Management (Polygon-ready)
- APScheduler Background Jobs (contract_engine, trust_scorer)
- Rate Limiting (slowapi, deaktiviert bei TESTING=true)
- i18n Service (DE/EN)
- MCP Tools (search, product, compare, deals, cashback)

## Phase 3: ML / Autonomie

### Abgeschlossen ✅
- GradientBoostingRegressor für Demand-Prediction
- IsolationForest für Trust-Score / Anomalie-Erkennung
- Modelle werden beim Start trainiert & mit joblib gespeichert
- `ensure_models_loaded()` im lifespan (nicht im TESTING-Modus)

## Phase 4: Dezentralisierung

### Abgeschlossen ✅
- YDMToken.sol (ERC-20, pragma ^0.8.20)
- PublisherContract.sol (Deals & Trust-Scoring, pragma ^0.8.20)
- web3_client.py (lazy import, kein Crash ohne web3)
- Blockchain Router (lazy, deaktiviert wenn WEB3_PROVIDER_URI fehlt)

### Offen ⏳
- DAO Governance Contract
- IPFS Integration
- Testnet Deployment

## Datenbank

| Modus       | URL |
|-------------|-----|
| Lokal (Dev) | sqlite+aiosqlite:///./yondem.db |
| Produktion  | postgresql+asyncpg://... (Supabase) |

Alembic-Migration: `alembic upgrade head`

## Tests

```
venv/bin/pytest tests/ -v
30/30 passed (6 Phase-1 Modelle + 24 Phase-2 HTTP Integration)
```

## Server starten

```bash
venv/bin/uvicorn app.main:app --reload --port 8090
```

## API Endpunkte (aktuell)

- GET  /health
- POST /agents/register, GET /agents/, GET /agents/{id}
- POST /contracts/{agent_id}/create, GET /contracts/{agent_id}/list
- POST /bidding/{agent_id}/create, GET /bidding/
- GET  /transactions/, GET /transactions/{id}
- POST /iot/devices/register, GET /iot/devices
- POST /wallets/{agent_id}/create, GET /wallets/{agent_id}
- GET  /mcp/search, /mcp/product/{id}, /mcp/compare, /mcp/deals, /mcp/cashback/{shop_id}
- POST /blockchain/deploy, /blockchain/deal, /blockchain/deal/execute
- GET  /blockchain/balance/{address}
