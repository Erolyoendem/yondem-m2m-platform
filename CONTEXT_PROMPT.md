# YONDEM MCP-SERVER - CONTEXT PROMPT
# Multi-Agent Affiliate Ecosystem

**Version:** 2.0 | **Date:**
2026-03-02
| **Status:** PHASE 2 - SMART CONTRACTS

---

## PROJECT OVERVIEW
Yondem ist eine **Multi-Agent Affiliate Plattform** mit drei Agent-Typen:

1. **Publisher-Agent** (IoT-Gerät) - Empfiehlt Produkte, verdient Provision
2. **Advertiser-Agent** (Shop) - Bietet Produkte mit Provision
3. **Arbitrage-Agent** - Nutzt Preisunterschiede

**Kernkonzept:** Vollständig autonomes Ökosystem ohne menschliches Zutun.

---

## ARCHITECTUR
```
/app
  /core           # Error Handler, Rate Limiter
  /database       # Session, Models
  /models         # Product, Shop, Deal, IoTDevice, Agent (NEU)
  /routers        # deals, i18n, mcp, iot, agents (NEU)
  /schemas        # Pydantic Models
  /services       # i18n, AgentLogic (NEU)
  /tools          # ShopTools, AgentTools (NEU)
```

---

## CURRENT STATUS (Phase 2)

### ✅ Abgeschlossen (Phase 1):
- IoT Device Registrierung
- Device Status & Listing
- Basis API mit Rate Limiting

### 🔄 In Arbeit (Phase 2):
- Agent Model (Publisher/Advertiser/Arbitrage)
- Smart Contract Regel-Engine
- Bidding-System
- Automatische Bestellung

---

## KEY CONCEPTS

### Publisher-Agent:
- IoT-Gerät mit Smart Contracts
- Definiert Regeln: "Wenn X, dann bestelle Y"
- Verdient Provision pro Sale
- Beispiel: Kühlschrank bestellt Milch

### Advertiser-Agent:
- Shop mit Bidding-System
- Bietet Echtzeit-Preise & Provisionen
- Konkurriert um Publisher-Aufmerksamkeit

### Smart Contracts:
- JSON-basierte Regeln
- Automatisch ausgeführt
- Provision-Aufteilung: 70%% Publisher, 20%% Plattform, 10%% Staking

---

## API ENDPOINTS (Aktuell)

### IoT Gateway:
- `POST /iot/devices/register` - Gerät registrieren
- `GET /iot/devices` - Alle Geräte listen
- `GET /iot/devices/{id}/status` - Gerät-Status

### MCP Tools:
- `GET /mcp/search` - Produkte suchen
- `GET /mcp/compare` - Preise vergleichen
- `GET /mcp/deals` - Deals anzeigen

### Agent System (Geplant):
- `POST /agents/register` - Agent registrieren
- `POST /agents/{id}/rules` - Regeln definieren
- `POST /bidding/offer` - Angebot machen

---

## DATABASE SCHEMA

### Tabelle: iot_devices
- id, name, device_type, status
- api_key, auto_order_enabled
- budget_limit, preferred_shop_id

### Tabelle: agents (GEPLANT)
- id, type (publisher/advertiser/arbitrage)
- status, performance_score, trust_level
- wallet_address, commission_earned_total

### Tabelle: smart_contracts (GEPLANT)
- id, agent_id, rules (JSON)
- status, execution_count, success_rate

---

## WORKFLOW RULES

**FÜR KI-ASSISTENTEN:**
1. Immer STRATEGY.md lesen vor Änderungen
2. Immer ROADMAP.md prüfen für aktuelle Phase
3. Schritt-für-Schritt arbeiten
4. NIE heredoc verwenden (nur printf/echo)
5. Max 2-3 Zeilen pro Befehl
6. Auf "OK" warten vor nächstem Schritt

**ARCHITEKTUR-PRINZIPIEN:**
- Alles ist ein Agent
- Alles ist autonom
- Smart Contracts > Manuelle Eingriffe
- Trust-Score vor Funktionalität

---

## COMMANDS
```bash
# Server starten
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Tests
pytest tests/ -v

# API Test
curl http://localhost:8000/health
curl http://localhost:8000/iot/devices
```

---

## DOCUMENTATION
- STRATEGY.md - Vollständiges Konzept
- ROADMAP.md - Implementierungsplan
- ERRORS.md - Fehler-History

---

**Last Updated:**
2026-03-02
**Next Phase:** Smart Contract Engine
