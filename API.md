# YONDEM API DOCUMENTATION
# Multi-Agent Affiliate Platform

**Version:** 2.1 | **Updated:** 2026-03-02

---

## ENDPUNKTE ÜBERSICHT

### Agents
- `POST /agents/register` - Agent registrieren
- `GET /agents/{id}` - Agent Details
- `GET /agents/` - Alle Agents listen

### Smart Contracts
- `POST /contracts/{agent_id}/create` - Contract erstellen
- `GET /contracts/{agent_id}/list` - Contracts eines Agents

### Transactions (NEU)
- `GET /transactions/` - Alle Transaktionen listen
- `GET /transactions/?publisher_id=xxx` - Nach Publisher filtern
- `GET /transactions/?advertiser_id=xxx` - Nach Advertiser filtern
- `GET /transactions/{id}` - Einzelne Transaktion

### IoT Devices
- `POST /iot/devices/register` - Gerät registrieren
- `GET /iot/devices/` - Alle Geräte

### Legacy
- `GET /deals/` - Deals anzeigen
- `GET /mcp/tools` - MCP Tools

---

## AUTONOME FUNKTIONEN

### Background Job (alle 60 Sekunden)
- Prüft alle aktiven Smart Contracts
- Sucht Produkte nach Regeln
- Führt automatische Bestellungen durch
- Trackt Provisionen

---

## BEISPIEL WORKFLOW

1. Publisher-Agent registrieren
2. Smart Contract erstellen (z.B. "Milch < 2€")
3. Background Job prüft alle 60s
4. Bei Treffer: Automatische Bestellung
5. Transaction wird erstellt
6. Provision wird verteilt


## Blockchain Endpoints

### POST /blockchain/deploy
Deploy Smart Contracts to Blockchain.
```json
{
  "provider_url": "https://polygon-mumbai.g.alchemy.com/v2/KEY",
  "private_key": "0x..."
}
```

### POST /blockchain/deal
Create on-chain deal.
```json
{
  "publisher": "0x...",
  "advertiser": "0x...",
  "product_id": 123,
  "amount": 1000000000000000000,
  "commission": 100000000000000000
}
```

### POST /blockchain/deal/execute
Execute deal and transfer tokens.
```json
{
  "deal_id": 1
}
```

### GET /blockchain/balance/{address}
Get YDM token balance.
