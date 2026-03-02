# YONDEM ROADMAP
# Multi-Agent Affiliate Platform

**Version:** 2.0 | **Last Updated:**
2026-03-02

---

## ÜBERSICHT

Diese Roadmap beschreibt die Entwicklung der Yondem Multi-Agent Affiliate Plattform.
Jede Phase baut auf der vorherigen auf und führt neue Agent-Typen ein.

---

## PHASE 1: FOUNDATION (Woche 1-2) ✅

### Ziel:
Basis-Infrastruktur für Agent-System

### Deliverables:
- ✅ IoT Device Model (SQLite)
- ✅ Device Registration API
- ✅ Device Status & Listing
- ✅ Agent-Profile Basis-Struktur

### Status:
**ABGESCHLOSSEN**

---

## PHASE 2: SMART CONTRACTS (Woche 3-4) 🔄

### Ziel:
Autonome Regelausführung für Publisher-Agenten

### Deliverables:
- ⏳ Agent Model erweitern (Publisher/Advertiser/Arbitrage)
- ⏳ Smart Contract Regel-Engine
- ⏳ Publisher Rules (Trigger → Aktion)
- ⏳ Advertiser Bidding-System
- ⏳ Automatische Bestell-Logik
- ⏳ Provision-Berechnung & Tracking

### Technische Details:
- Tabelle: `agents` mit type & performance_score
- Tabelle: `smart_contracts` mit rules (JSON)
- Tabelle: `transactions` für Provisionen
- Endpunkt: `POST /agents/{id}/rules` (Regeln definieren)
- Endpunkt: `POST /bidding/offer` (Advertiser bieten)
- Background Job: Regel-Prüfung alle 60 Sekunden

---

## PHASE 3: AUTONOMIE (Woche 5-8) ⏳

### Ziel:
Vollständig autonomes System ohne menschliches Zutun

### Deliverables:
- ⏳ ML-basierte Bedarfserkennung (Publisher)
- ⏳ Dynamisches Bidding (Advertiser)
- ⏳ Preis-Arbitrage Detection
- ⏳ Trust-Scoring Algorithmus
- ⏳ Wallet-Integration für Provisionen
- ⏳ Autonome Zahlungsabwicklung

### Technische Details:
- Python `scikit-learn` für ML
- Echtzeit-Preisvergleich über MCP-Tools
- Trust-Score basierend auf:
  - Erfolgsrate (90%% Gewichtung)
  - Zahlungshistorie (10%% Gewichtung)
- Crypto-Wallet (Ethereum/Polygon) optional

---

## PHASE 4: DEZENTRALISIERUNG (Woche 9-12) ⏳

### Ziel:
Blockchain-basiertes, dezentrales Ökosystem

### Deliverables:
- ⏳ Smart Contracts auf Blockchain (Solidity)
- ⏳ Yondem Token (YDM) für Provisionen
- ⏳ DAO-Governance für Plattform-Entscheidungen
- ⏳ Dezentrale Agent-Registry
- ⏳ Cross-Chain Kompatibilität

### Technische Details:
- Ethereum/Polygon für Smart Contracts
- ERC-20 Token für YDM
- IPFS für Agent-Metadaten
- Snapshot für DAO-Abstimmungen

---

## MEILENSTEINE

| Datum | Meilenstein | Status |
|-------|-------------|--------|
| Woche 2 | Foundation fertig | ✅ |
| Woche 4 | Erste autonome Bestellung | 🔄 |
| Woche 6 | 100+ aktive Agents | ⏳ |
| Woche 8 | Vollständige Autonomie | ⏳ |
| Woche 12 | DAO-Launch | ⏳ |

---

## ABHÄNGIGKEITEN

### Externe Services:
- Stripe/PayPal (Zahlungen bis Phase 4)
- Ethereum Node (ab Phase 4)
- MQTT Broker (IoT-Kommunikation)

### Interne Abhängigkeiten:
```
Phase 2 benötigt: Phase 1 ✅
Phase 3 benötigt: Phase 2
Phase 4 benötigt: Phase 3
```

---

## RISIKEN & MITIGATION

| Risiko | Wahrscheinlichkeit | Mitigation |
|--------|-------------------|------------|
| Agent-Missbrauch | Mittel | Trust-Score + Limits |
| Preismanipulation | Niedrig | Mehrere Datenquellen |
| Blockchain-Kosten | Mittel | Layer-2 (Polygon) |
| Regulierung | Unbekannt | Compliance-Module |

---

## DEFINITION OF DONE

Jede Phase gilt als abgeschlossen wenn:
1. ✅ Alle Features implementiert
2. ✅ Tests > 85%% Coverage
3. ✅ Dokumentation aktualisiert (STRATEGY.md)
4. ✅ API-Doku (Swagger) aktuell
5. ✅ Performance-Test bestanden
6. ✅ Security-Audit (ab Phase 3)

---

**Document Owner:** Yondem Development Team
**Review Cycle:** Weekly
**Next Review:**
2026-03-09
