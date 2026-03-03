# YONDEM – Geschäftsstrategie 2026

## Vision
Die erste autonome AI Affiliate Plattform die ohne manuellen Sales oder Werbung skaliert.

## Assets
- 44 spezialisierte AI Agents (yondem-runtime)
- M2M Affiliate Platform (Yondem-M2M-Platform)
- 7.000 EU Shops Kontaktdatenbank
- 2.400 Decision Maker Emails
- 26.000 LinkedIn Follower
- CEOfluencer Buch + persönliche Brand

## Drei Kernstrategien

### 1. Token Cost Minimierung
- Claude Opus: Komplexe Entscheidungen (Dirigent A27, Orchestrator A31)
- Claude Sonnet: Standard Agents (32 operative Agents)
- Deepseek R1: Routine Tasks, Bulk Processing (80% günstiger)
- Ollama lokal: Startup-Phase, 0 Kosten
- Router Agent entscheidet Modell je nach Komplexität → Ziel: 80% Kostenersparnis

### 2. MCP auf Kunden-Infrastruktur
- Kunde betreibt eigene Infrastruktur (0 Hosting-Kosten für uns)
- Daten bleiben beim Kunden (DSGVO automatisch gelöst)
- Yondem wird Betriebssystem des Kunden (tief integriert, Lock-in)
- Netzwerkeffekt: Je mehr Shops, desto besser werden die Agents
- Kunden können Yondem Orchestration Agent (A27) in eigene Agent-Systeme einbinden

### 3. Agent-as-a-Service (Roomba-Modell)
- Agent lernt aus Kundendaten → wird kontinuierlich besser
- Monatliche Subscription statt Einmalkauf
- Je länger Kunde dabei, desto wertvoller der Agent
- Wechselkosten steigen mit der Zeit

## Pricing Modell

| Tier | Preis | Inhalt |
|------|-------|--------|
| Starter | 0€ | Auf Kunden-Rechner, Deepseek, 5 Agents, MCP |
| Growth | 299€/Monat | Cloud, Claude Sonnet, 20 Agents, Support |
| Enterprise | 999€/Monat | Alle 44 Agents, Custom MCP, White-Label, SLA |

## Distribution Strategie

### Phase 1 – Sofort (diese Woche)
- Plattform online auf Railway
- Landing Page mit Waitlist
- LinkedIn Post: "Erste autonome AI Affiliate Plattform"

### Phase 2 – Woche 2
- Email Kampagne an 2.400 Decision Makers (via Outlook automatisiert)
- Shopware App Store Listing
- Klaviyo Marketplace Listing
- Erste 10 Advertiser onboarden

### Phase 3 – Woche 3-4
- Publisher Self-Registration live
- Erste echte Transaktionen mit Shopware Shops
- LinkedIn Case Study: "Erster Publisher verdient passiv mit IoT"
- ProductHunt Launch vorbereiten

### Phase 4 – Monat 2
- Polygon Mainnet (echte YDM Token)
- Deepseek Router live (Kostenoptimierung)
- Erste Enterprise Kunden aus 7.000 Shop Datenbank

## Wettbewerbsvorteil
Kein Wettbewerber hat:
1. 44 spezialisierte E-Commerce Agents
2. M2M Affiliate Platform mit Smart Contracts
3. MCP Integration für Kunden-Infrastruktur
4. CEOfluencer Distribution (26.000 LinkedIn + 2.400 DM Emails)

## Claude Computer Use / Remote Control
- Claude steuert autonom Browser und Desktop
- Outlook Emails automatisch lesen und beantworten
- Shopware Shops automatisch analysieren und onboarden
- LinkedIn Posts automatisch veröffentlichen
- 2.400 Decision Maker Emails autonom bearbeiten
- Kombination mit 44 Agents = vollautonome Plattform ohne menschlichen Eingriff

## OpenRouter
- Einziger API Endpunkt für alle LLMs
- Claude, Deepseek, Llama, Gemini über eine API
- Automatisches Failover
- Gratis Tier verfügbar
- Ziel: 80% Token-Kostenersparnis in Startup Phase

## Claude Code / MCP Distribution Kanal
- Kunden nutzen bereits Claude Code (Handy, Mac, überall)
- Yondem MCP Server = ein Eintrag in ihrer Claude Code Config
- Sofortiger Zugriff auf alle 44 Agents ohne Installation
- Pricing: per API Call abrechnen (Metered Billing)
- Zielgruppe: 10M+ Claude Code Nutzer weltweit
- Onboarding: eine Zeile Config reicht

Beispiel Kunde Config:
```json
{
  "mcpServers": {
    "yondem": {
      "url": "https://yondem.railway.app/mcp",
      "apiKey": "yk_live_xxx"
    }
  }
}
```

Kunden können dann in Claude Code sagen:
"Analysiere meinen Shopware Shop" → Yondem Agent antwortet
