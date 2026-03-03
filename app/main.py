"""
Yondem M2M Platform – FastAPI 0.115 / Python 3.12 / SQLAlchemy 2.0 async
"""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core.error_handlers import general_exception_handler, http_exception_handler
from app.core.rate_limiter import limiter, setup_rate_limiting
from app.database.session import init_db
from app.services.i18n import load_translations
from app.services.scheduler import init_scheduler, shutdown_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("yondem")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ────────────────────────────────────────────────────────────
    load_translations()
    await init_db()
    os.makedirs("static/avatars", exist_ok=True)

    # Pre-load ML models in a thread so startup stays non-blocking
    if os.getenv("TESTING") != "true":
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            from app.services.ml_predictor import ensure_models_loaded
            await loop.run_in_executor(None, ensure_models_loaded)
        except Exception as exc:
            logger.warning("ML model preload skipped: %s", exc)

        init_scheduler()

    logger.info("Yondem M2M Platform 2.0.0 started")
    yield
    # ── Shutdown ───────────────────────────────────────────────────────────
    if os.getenv("TESTING") != "true":
        shutdown_scheduler()
    logger.info("Yondem M2M Platform shutdown complete")


app = FastAPI(
    title="Yondem M2M Platform",
    description="Multi-Agent Affiliate & IoT Ecosystem – Phase 2",
    version="2.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
setup_rate_limiting(app)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# ── Routers ────────────────────────────────────────────────────────────────
from app.routers import agents, bidding, contracts, deals, iot, transactions, wallets
from app.routers import i18n, mcp, waitlist, affiliate

app.include_router(deals.router)
app.include_router(i18n.router)
app.include_router(mcp.router)
app.include_router(iot.router)
app.include_router(agents.router)
app.include_router(contracts.router)
app.include_router(transactions.router)
app.include_router(bidding.router)
app.include_router(wallets.router)
app.include_router(waitlist.router)
app.include_router(affiliate.router)

# Blockchain: optional – only loaded when web3 is installed
try:
    from app.routers.blockchain import router as blockchain_router
    app.include_router(blockchain_router)
    logger.info("Blockchain router loaded (web3 available)")
except (ImportError, Exception) as _bc_err:
    logger.warning("Blockchain router not loaded: %s", _bc_err)

# ── Core endpoints ─────────────────────────────────────────────────────────


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "2.0.0", "db": "connected"}


@app.get("/api", include_in_schema=False)
async def api_info():
    return {
        "message": "Yondem M2M Platform",
        "version": "2.0.0",
        "features": ["agents", "smart_contracts", "bidding", "transactions", "iot", "wallets"],
        "docs": "/docs",
    }


@app.get("/docs", include_in_schema=False)
async def swagger_ui():
    return HTMLResponse(
        content=(
            "<!DOCTYPE html><html><head>"
            "<title>Yondem API 2.0</title>"
            "<link rel=stylesheet href=https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css>"
            "<link href=https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap rel=stylesheet>"
            "</head><body><div id=swagger-ui></div>"
            "<script src=https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js></script>"
            "<script>SwaggerUIBundle({url:'/openapi.json',dom_id:'#swagger-ui',"
            "presets:[SwaggerUIBundle.presets.apis],layout:'BaseLayout'});</script>"
            "</body></html>"
        )
    )


# ── Static files (Landing Page) – mount LAST so API routes take priority ───
app.mount("/", StaticFiles(directory="static", html=True), name="static")
