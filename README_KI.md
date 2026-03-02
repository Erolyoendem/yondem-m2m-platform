# YONDEM M2M PLATFORM - KI ASSISTENT GUIDE

## WILLKOMMEN
Du arbeitest an der Yondem Multi-Agent Affiliate Plattform.
Diese Plattform ermöglicht autonome IoT-Geräte, Produkte zu verkaufen und Provisionen zu verdienen.

## WICHTIGE REGELN

1. **IMMER LESEN VOR ÄNDERUNGEN:**
   - STRATEGY.md (Konzept)
   - ROADMAP.md (Phasen)
   - API.md (Endpoints)
   - CONTEXT_PROMPT.md (Kontext)

2. **ARBEITSWEISE:**
   - Schritt-für-Schritt arbeiten
   - Auf "OK" warten vor nächstem Befehl
   - Max 2-3 Zeilen pro Befehl
   - NIE heredoc verwenden (nur printf/echo)

3. **ARCHITEKTUR-PRINZIPIEN:**
   - Alles ist ein Agent
   - Alles ist autonom
   - Smart Contracts > Manuelle Eingriffe
   - Trust-Score vor Funktionalität

## SYSTEM STATUS

**Aktuelle Phase:** Phase 2 - Smart Contracts ✅

**Funktioniert:**
- ✅ IoT Device Registrierung
- ✅ Agent System (Publisher/Advertiser/Arbitrage)
- ✅ Smart Contracts mit Regeln
- ✅ Rate Limiting
- ✅ API Dokumentation

**In Arbeit:**
- 🔄 Automatische Contract-Ausführung
- ⏳ Bidding-System
- ⏳ Provision-Tracking

## DATEISTRUKTUR

```
/app
  /core           # error_handlers.py, rate_limiter.py
  /database       # session.py
  /models         # product.py, shop.py, deal.py, iot_device.py, agent.py, smart_contract.py
  /routers        # deals.py, i18n.py, mcp.py, iot.py, agents.py, contracts.py
  /schemas        # mcp.py
  /services       # i18n.py
  /tools          # shop_tools.py
```

## WICHTIGE MODELLE

### Agent
- type: publisher | advertiser | arbitrage
- trust_level: 0-100
- performance_score: 0.0-1.0
- commission_earned_total

### SmartContract
- agent_id: UUID des Publishers
- rules: JSON {product, condition, max_price}
- monthly_budget
- execution_count, success_count

## BEISPIEL WORKFLOW

```bash
# 1. IoT Gerät registrieren
curl -X POST /iot/devices/register -d {"name":"Kühlschrank","device_type":"fridge"}

# 2. Agent erstellen (Publisher)
curl -X POST /agents/register -d {"name":"Kühlschrank Agent","type":"publisher"}

# 3. Smart Contract erstellen
curl -X POST /contracts/{agent_id}/create -d {"product":"Milch","condition":"stock < 2","max_price":2.50}
```

## TESTS

Immer ausführen nach Änderungen:
```bash
pytest tests/ -v
```

## KONTAKT
Bei Fragen: Dokumentation in STRATEGY.md lesen

**Letztes Update:**
2026-03-02
