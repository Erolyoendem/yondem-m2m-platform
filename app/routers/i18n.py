from fastapi import APIRouter, Query
from app.services.i18n import get_text, get_available_languages

router = APIRouter(prefix="/i18n", tags=["internationalization"])

@router.get("/welcome")
def welcome(lang: str = Query(default="de", description="Sprache: de, en, it, tr, es, fr, ar")):
    """Begrüßung in der gewählten Sprache"""
    return {
        "language": lang,
        "welcome": get_text("welcome", lang),
        "message": get_text("deal_created", lang)
    }

@router.get("/languages")
def languages():
    """Alle verfügbaren Sprachen anzeigen"""
    return {
        "available_languages": get_available_languages(),
        "count": len(get_available_languages())
    }
