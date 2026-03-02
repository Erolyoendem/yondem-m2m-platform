# YONDEM PLATFORM STRATEGY
# Multi-Agent Affiliate & IoT Ecosystem

**Version:** 2.0 (Multi-Agent)
**Date:** 2026-03-02
**Status:** ACTIVE DEVELOPMENT

---

## 1. VISION & KONZEPT

Yondem ist eine **dezentrale Multi-Agent Affiliate Plattform** die drei Welten verbindet:

1. **IoT-Geräte** (Publisher) - Autonome Agenten die Provisionen verdienen
2. **Shops** (Advertiser) - Bieten Provisionen für Verkäufe
3. **Arbitrage-Agenten** - Nutzen Preisunterschiede automatisch

**Unique Selling Point:** Vollständig autonomes Ökosystem ohne menschliches Zutun. Geräte handeln, verkaufen und verdienen eigenständig.

---

## 2. AGENT-ARCHITEKTUR

### 2.1 Agent-Typen

#### A) Publisher-Agent (IoT-Gerät)
- **Rolle:** Produkte empfehlen & verkaufen
- **Einnahmen:** Provision pro Sale (5-20%%)
- **Beispiele:** Kühlschrank bestellt Milch, Drucker bestellt Toner
- **Intelligenz:** ML-basierte Bedarfserkennung

#### B) Advertiser-Agent (Shop)
- **Rolle:** Produkte anbieten & Provisionen zahlen
- **Strategie:** Bidding um Publisher-Aufmerksamkeit
- **Zahlung:** Automatisch bei erfolgreichem Sale
- **Vorteil:** Direkter Zugang zu IoT-Bedarf

#### C) Arbitrage-Agent (Optional)
- **Rolle:** Preisunterschiede ausnutzen
- **Strategie:** Kaufen bei Shop A, verkaufen bei Shop B
- **Risiko:** Selbstständige Risikobewertung

### 2.2 Agent-Attribute
```json
{
  "agent_id": "uuid",
  "type": "publisher|advertiser|arbitrage",
  "status": "active|inactive|suspended",
  "performance_score": 0.0-1.0,
  "commission_earned": 0.00,
  "trust_level": 0-100,
  "smart_contracts": []
}
```

---

## 3. SMART CONTRACT SYSTEM

### 3.1 Vertragstypen

#### Publisher-Contract:
```json
{
  "contract_id": "uuid",
  "publisher_id": "fridge_001",
  "rules": [
    {
      "product_category": "dairy",
      "trigger": "stock < 2",
      "max_price": 2.50,
      "min_cashback": 5,
      "auto_execute": true
    }
  ],
  "monthly_budget": 100.00,
  "preferred_shops": ["shop_a", "shop_b"],
  "commission_split": {
    "publisher": 70,
    "platform": 20,
    "staking_pool": 10
  }
}
```

#### Advertiser-Contract:
```json
{
  "contract_id": "uuid",
  "advertiser_id": "shop_amazon",
  "bidding_strategy": {
    "max_cpc": 0.50,
    "commission_rate": "8%%",
    "target_agents": ["fridge", "printer"],
    "budget_daily": 100.00
  },
  "auto_approve": true,
  "payment_terms": "immediate"
}
```

---

## 4. AUTONOME PROZESSE

### 4.1 Publisher-Workflow (Autonom)
```
1. Gerät scannt Bestand (Kamera/Sensoren)
2. Erkennt Bedarf via ML (z.B. "Milch fast leer")
3. Prüft Smart Contract Regeln
4. Fragt Preise bei Advertisern an (Bidding)
5. Wählt optimalen Shop (Preis + Cashback + Trust)
6. Führt Bestellung autonom durch
7. Empfängt Provision nach Bestätigung
8. Aktualisiert Performance-Score
```

### 4.2 Advertiser-Workflow (Autonom)
```
1. Shop registriert Produkte mit Provision
2. Bietet Echtzeit-Preise für Publisher
3. Empfängt Bestellanfragen
4. Prüft Kreditlimit des Publishers
5. Führt Sale durch
6. Zahlt Provision automatisch (Smart Contract)
7. Aktualisiert Bidding-Strategie via ML
```

---

## 5. TECHNISCHE ARCHITEKTUR

### 5.1 Komponenten

```
┌─────────────────────────────────────────────────────────────┐
|                     YONDEM PLATFORM                         |
├─────────────────────────────────────────────────────────────┤
|  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      |
|  │   PUBLISHER  │  │  ADVERTISER  │  │  ARBITRAGE   │      |
|  │    AGENTS    │  │    AGENTS    │  │    AGENTS    │      |
|  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      |
|         │                 │                 │               |
|  ┌──────▼─────────────────▼─────────────────▼───────┐      |
|  │           SMART CONTRACT ENGINE                  │      |
|  │  - Regelausführung  - Provisionierung           │      |
|  │  - Bidding          - Trust-Scoring             │      |
|  └──────┬───────────────────────────────────────────┘      |
|         │                                                   |
|  ┌──────▼───────────────────────────────────────────┐      |
|  │              BLOCKCHAIN LAYER (Optional)          │      |
|  │  - Unveränderliche Vertrags-History             │      |
|  │  - Dezentrale Provision-Zahlungen               │      |
|  └──────────────────────────────────────────────────┘      |
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Datenbank-Schema (Erweitert)

#### Tabelle: agents
- id, type, status, performance_score
- wallet_address, commission_earned_total
- trust_level, created_at, updated_at

#### Tabelle: smart_contracts
- id, agent_id, contract_type, rules (JSON)
- status, execution_count, success_rate

#### Tabelle: transactions
- id, publisher_id, advertiser_id, product_id
- amount, commission_paid, timestamp
- status (pending/completed/refunded)

#### Tabelle: bids
- id, advertiser_id, publisher_id
- product_category, bid_amount, commission_offer
- valid_until, status

---

## 6. IMPLEMENTIERUNGSPHASEN

### Phase 1: Foundation (AKTUELL)
- ✅ IoT-Gerät-Registrierung
- ✅ Basis API & Auth
- ✅ Datenbank-Models
- 🔄 Agent-Profile System

### Phase 2: Smart Contracts (NÄCHSTE)
- ⏳ Regel-Engine für Publisher
- ⏳ Bidding-System für Advertiser
- ⏳ Automatische Bestellung
- ⏳ Provision-Berechnung

### Phase 3: Autonomie (Q2)
- ⏳ ML-basierte Bedarfserkennung
- ⏳ Dynamisches Bidding
- ⏳ Arbitrage-Detection
- ⏳ Trust-Scoring Algorithmus

### Phase 4: Dezentralisierung (Q3)
- ⏳ Blockchain-Integration
- ⏳ Token-Ökonomie
- ⏳ DAO-Governance

---

## 7. WICHTIGE REGELN FÜR KI-ASSISTENTEN

**VOR JEDER ÄNDERUNG:**
1. Diese Datei lesen
2. ROADMAP.md prüfen
3. Kontext aus CONTEXT_PROMPT.md beachten
4. Schritt-für-Schritt arbeiten
5. Nie heredoc verwenden (nur printf/echo)

**ARCHITEKTUR-PRINZIPIEN:**
- Alles ist ein Agent
- Alles ist autonom
- Vertrauen, aber verifizieren (Trust-Score)
- Smart Contracts > Manuelle Eingriffe

---

## 8. GLOSSAR

- **Publisher:** Verkauft/empfiehlt Produkte (IoT-Gerät)
- **Advertiser:** Bietet Produkte mit Provision (Shop)
- **Arbitrage:** Nutzt Preisunterschiede
- **Smart Contract:** Automatisch ausgeführte Regeln
- **Bidding:** Echtzeit-Auktion um Agent-Aufmerksamkeit
- **Trust-Score:** Vertrauenswürdigkeit eines Agents

---

**Document Owner:** Yondem Development Team
**Last Updated:**
2026-03-02
**Next Review:** Weekly
