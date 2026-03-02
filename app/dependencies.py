from fastapi import Query, Request
from typing import Optional
from app.services.i18n import i18n_service

async def get_language(
    lang: Optional[str] = Query(default=None, description="Sprachcode (de, en, it, tr, es, fr, ar)"),
    request: Request = None
) -> str:
    if lang and lang in i18n_service.get_available_languages():
        return lang
    
    if request and request.headers.get("accept-language"):
        header_lang = request.headers.get("accept-language", "").split(",")[0].split("-")[0]
        if header_lang in i18n_service.get_available_languages():
            return header_lang
    
    return "de"

def get_translation_func(lang: str):
    return lambda key, **kwargs: i18n_service.translate(key, lang, **kwargs)
