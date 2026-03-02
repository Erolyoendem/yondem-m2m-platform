import json
import os
from typing import Dict, Any

translations: Dict[str, Dict[str, Any]] = {}

def load_translations():
    global translations
    translations = {}
    locales_dir = os.path.join(os.path.dirname(__file__), "..", "locales")
    if not os.path.exists(locales_dir):
        print(f"⚠️ Locales-Verzeichnis nicht gefunden: {locales_dir}")
        return
    for filename in os.listdir(locales_dir):
        if filename.endswith(".json"):
            lang_code = filename[:-5]
            filepath = os.path.join(locales_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    translations[lang_code] = json.load(f)
                print(f"✅ Geladen: {lang_code}")
            except Exception as e:
                print(f"❌ Fehler beim Laden von {filename}: {e}")

def get_text(key: str, lang: str = "de") -> str:
    if lang not in translations:
        lang = "de"
    return translations.get(lang, {}).get(key, key)

def translate(key: str, lang: str = "de", **kwargs) -> str:
    """Übersetzt einen Key mit optionalen Platzhaltern (z.B. errors.deal_not_found)"""
    if lang not in translations:
        lang = "de"
    keys = key.split(".")
    value = translations.get(lang, {})
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return key
    if isinstance(value, str):
        return value.format(**kwargs) if kwargs else value
    return key

def get_available_languages() -> list:
    return list(translations.keys())

class I18NService:
    """Service-Klasse für i18n"""
    @staticmethod
    def translate(key: str, lang: str = "de", **kwargs) -> str:
        return translate(key, lang, **kwargs)
    
    @staticmethod
    def get_available_languages() -> list:
        return get_available_languages()
    
    @staticmethod
    def load_translations():
        load_translations()

i18n_service = I18NService()
