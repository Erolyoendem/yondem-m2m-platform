# Railway Deployment – Yondem M2M Platform

## Voraussetzungen
- GitHub Repository mit diesem Code
- Railway Account: https://railway.app
- Supabase PostgreSQL Datenbank (bereits konfiguriert)
- OpenRouter API Key: https://openrouter.ai (Gratis Tier verfügbar)

## Schritt-für-Schritt Anleitung

### 1. Railway öffnen
Gehe zu https://railway.app und melde dich an.

### 2. Neues Projekt erstellen
- Klicke auf **"New Project"**
- Wähle **"Deploy from GitHub repo"**
- Verbinde dein GitHub-Konto falls nötig

### 3. Repository auswählen
- Wähle das Repository `Yondem-M2M-Platform` (oder den Fork)
- Railway erkennt automatisch den `03-Implementation/mcp-server` Ordner
- Alternativ: Root Directory auf `03-Implementation/mcp-server` setzen

### 4. Environment Variables eintragen
Gehe zu **Settings → Variables** und trage ein:

| Variable | Wert | Pflicht |
|----------|------|---------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres.XXX:Passwort@aws-1-eu-central-1.pooler.supabase.com:6543/postgres` | ✅ |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` (von openrouter.ai) | ✅ |
| `JWT_SECRET` | Zufälliger 32-Zeichen String | ✅ |
| `REQUIRE_API_KEY` | `false` (Development) / `true` (Production) | ✅ |
| `API_KEY` | Dein API Key für geschützte Endpunkte | ✅ |
| `BLOCKCHAIN_PROVIDER` | Polygon Mumbai RPC URL | Optional |
| `PLATFORM_PRIVATE_KEY` | Wallet Private Key | Optional |

### 5. Deploy starten
- Klicke auf **"Deploy"**
- Railway baut das Image via NIXPACKS (Python 3.11)
- Start-Befehl: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health Check: `GET /health` → `{"status": "ok"}`

### 6. Domain konfigurieren
- Gehe zu **Settings → Networking**
- Klicke **"Generate Domain"** für automatische `*.railway.app` URL
- Optional: Custom Domain eintragen

### 7. Datenbank-Migration ausführen
Nach dem ersten Deploy einmalig ausführen:
```bash
# Via Railway CLI
railway run alembic upgrade head

# Oder via Railway Shell (Settings → Shell)
alembic upgrade head
```

## Deployment-Dateien

| Datei | Zweck |
|-------|-------|
| `Procfile` | `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| `runtime.txt` | `python-3.11.9` |
| `railway.json` | Builder NIXPACKS, Health Check `/health`, Restart ON_FAILURE |
| `requirements.txt` | Alle Python Dependencies |

## Health Check
```bash
curl https://DEINE-URL.railway.app/health
# {"status":"ok","version":"2.0.0","db":"connected"}
```

## Logs prüfen
```bash
# Via Railway CLI
railway logs

# Via Dashboard
Railway Dashboard → Dein Projekt → Logs Tab
```

## Kosten
- Railway Hobby Plan: 5$ / Monat (ausreichend für MVP)
- Supabase Free Tier: 0$ (500MB DB, 2GB Transfer)
- OpenRouter Free Tier: 0$ (Rate-limited Deepseek/Llama Zugang)
- **Gesamt MVP: ~5$ / Monat**
