from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

from app.routers import deals, i18n, mcp, iot, agents, contracts, transactions, bidding, wallets
from app.services.i18n import load_translations, get_available_languages, translate
from app.dependencies import get_language, get_translation_func
from app.database.session import init_db
from app.core.error_handlers import http_exception_handler, general_exception_handler
from app.core.rate_limiter import limiter, setup_rate_limiting
from app.services.scheduler import init_scheduler, shutdown_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("yondem")
load_translations()
init_db()
init_scheduler()
app = FastAPI(title="Yondem", description="Agent Deal Platform - Multilingual", version="0.2.0", docs_url=None, redoc_url=None)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
setup_rate_limiting(app)

app.include_router(deals.router)
app.include_router(i18n.router)
app.include_router(mcp.router)
app.include_router(iot.router)
app.include_router(agents.router)
app.include_router(contracts.router)
app.include_router(transactions.router)os.makedirs("static/avatars", exist_ok=True)
app.include_router(bidding.router)app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(wallets.router)

# Blockchain
from app.routers.blockchain import router as blockchain_router
app.include_router(blockchain_router)@app.get("/")
def root(lang: str = Depends(get_language)):
    t = get_translation_func(lang)
    return {"message": t("welcome"), "version": "0.2.0", "features": ["deals", "i18n", "multilingual", "mcp_tools"], "languages": get_available_languages(), "current_language": lang}

@app.get("/health")
def health_check(lang: str = Depends(get_language)):
    t = get_translation_func(lang)
    return {"status": "healthy", "database": "connected", "message": t("health.status_ok"), "language": lang}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return HTMLResponse(content="<!DOCTYPE html><html><head><title>Yondem API</title><link rel=stylesheet type=text/css href=https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css><link href=https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap rel=stylesheet></head><body><div id=swagger-ui></div><script src=https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js></script><script>SwaggerUIBundle({url:\"/openapi.json\",dom_id:\"#swagger-ui\",presets:[SwaggerUIBundle.presets.apis],layout:\"BaseLayout\"});</script></body></html>")
