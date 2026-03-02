# YONDEM M2M PLATFORM - KI ASSISTENT GUIDE

## WILLKOMMEN
Du arbeitest an der Yondem Multi-Agent Affiliate Plattform.
Diese Plattform ermöglicht autonomen IoT-Geräten, Produkte zu verkaufen und Provisionen zu verdienen.

## WICHTIGE REGELN

1. **IMMER LESEN VOR ÄNDERUNGEN:**
   - STRATEGY.md (Konzept)
   - ROADMAP.md (Phasen)
   - API.md (Endpoints)
   - STATUS.md (aktueller Stand)

2. **TESTS IMMER MIT VENV:**
   ```bash
   venv/bin/pytest tests/ -v
   ```
   Erwartetes Ergebnis: **30/30 passed**

3. **ARCHITEKTUR-PRINZIPIEN:**
   - Alles ist ein Agent
   - Alles ist autonom
   - Smart Contracts > Manuelle Eingriffe
   - Trust-Score vor Funktionalität

## SYSTEM STATUS (Stand 2026-03-02)

**Aktuelle Phase:** Phase 4 – Dezentralisierung (in Arbeit)
**Tests:** 30/30 ✅

**Stack:**
- FastAPI 0.115 + lifespan (kein `@app.on_event`)
- SQLAlchemy 2.0 async (`Mapped[]` / `mapped_column()`)
- Pydantic v2 + pydantic-settings (`BaseSettings`)
- aiosqlite (lokal) / asyncpg (Produktion / Supabase)
- scikit-learn 1.5 (GradientBoosting + IsolationForest)
- pytest-asyncio (asyncio_mode = auto)

**Funktioniert vollständig:**
- ✅ Agent System (publisher / advertiser / arbitrage)
- ✅ Smart Contracts inkl. GET /contracts/{agent_id}/list
- ✅ Bidding System
- ✅ Transaction Tracking
- ✅ IoT Device Registrierung
- ✅ Wallet Management
- ✅ ML Demand-Prediction + Trust-Scoring (scikit-learn)
- ✅ APScheduler Background Jobs
- ✅ Rate Limiting (deaktiviert bei TESTING=true)
- ✅ Alembic Migrations
- ✅ Blockchain lazy import (kein Crash ohne web3)

**In Arbeit:**
- 🔄 DAO Governance Contract
- ⏳ IPFS Integration
- ⏳ Testnet Deployment

## DATEISTRUKTUR

```
/app
  /blockchain     # __init__.py (lazy import), web3_client.py
  /core           # error_handlers.py, rate_limiter.py
  /database       # session.py (async + sync engine)
  /models         # base.py, product.py, shop.py, deal.py,
                  # iot_device.py, agent.py, smart_contract.py,
                  # transaction.py, bid.py, wallet.py
  /routers        # agents.py, contracts.py, bidding.py,
                  # transactions.py, iot.py, wallets.py,
                  # deals.py, mcp.py, blockchain.py
  /services       # i18n.py, scheduler.py, ml_predictor.py
  /tools          # shop_tools.py
  config.py       # pydantic-settings BaseSettings
  main.py         # lifespan, CORS, alle Router
/migrations       # Alembic async env.py
/tests
  conftest.py     # async fixtures, in-memory SQLite, TESTING=true
  test_phase1.py  # 6 Model-Tests
  test_phase2.py  # 24 HTTP Integration-Tests
/blockchain
  /contracts      # YDMToken.sol, PublisherContract.sol (^0.8.20)
  /scripts        # compile.py, deploy.py
```

## SETUP

```bash
# Abhängigkeiten
venv/bin/pip install -r requirements.txt

# Datenbank initialisieren (lokal SQLite)
venv/bin/alembic upgrade head

# Server starten
venv/bin/uvicorn app.main:app --reload --port 8090

# Tests
venv/bin/pytest tests/ -v
```

## WICHTIGE MODELLE

### Agent
- `type`: publisher | advertiser | arbitrage
- `trust_level`: 0–100
- `performance_score`: 0.0–1.0
- `commission_earned_total`

### SmartContract
- `agent_id`: UUID des Publishers (nur publisher darf erstellen)
- `rules`: JSON {product, condition, max_price}
- `monthly_budget`, `execution_count`, `success_count`

### Bid
- `agent_id`: UUID des Advertisers (nur advertiser darf bieten)
- `product_category`, `commission_rate`, `daily_budget`
- `status`: active | paused | expired

## BEISPIEL WORKFLOW

```bash
# 1. IoT Gerät registrieren
curl -X POST http://localhost:8090/iot/devices/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Kühlschrank","device_type":"fridge"}'

# 2. Agent erstellen (Publisher)
curl -X POST http://localhost:8090/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Kühlschrank Agent","type":"publisher"}'

# 3. Smart Contract erstellen
curl -X POST http://localhost:8090/contracts/{agent_id}/create \
  -H "Content-Type: application/json" \
  -d '{"product":"Milch","condition":"stock < 2","max_price":2.50}'

# 4. Contracts auflisten
curl http://localhost:8090/contracts/{agent_id}/list
```

## ASYNC-PATTERN (SQLAlchemy 2.0)

```python
# Korrekt (immer so):
result = await db.execute(select(Agent).where(Agent.id == agent_id))
agent = result.scalar_one_or_none()

# NICHT mehr:
agent = db.query(Agent).filter(Agent.id == agent_id).first()
```

## LETZTES UPDATE
2026-03-02 – Vollständige Modernisierung (FastAPI 0.115, SQLAlchemy 2.0, Pydantic v2, scikit-learn ML, 30/30 Tests grün)
