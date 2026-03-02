# Fehler-History

## Fehler #1: ModuleNotFoundError
**Datum**: 2026-03-01
**Fehler**: ModuleNotFoundError: No module named app.services.affiliate_service
**Ursache**: ShopTools hat nicht existierenden Service importiert
**Loesung**: Dummy-Implementierung ohne fehlenden Import
**Verhinderung**: Immer pruefen ob Module existieren

## Fehler #2: ImportError i18n
**Datum**: 2026-03-01
**Fehler**: ImportError: cannot import name i18n
**Ursache**: Falscher Import-Name, exportiert wird i18n_service
**Loesung**: from app.services.i18n import i18n_service
**Verhinderung**: Export-Namen immer pruefen mit: grep ^[a-zA-Z_] app/services/i18n.py

## Fehler #3: JSON Parse Error fr.json
**Datum**: 2026-03-01
**Fehler**: Invalid control character in fr.json
**Ursache**: Apostroph in franzoesischen Woertern
**Loesung**: Apostrophe entfernt: Sinscrire statt S'inscrire
**Verhinderung**: JSON validieren: python -m json.tool fr.json

## Fehler #4: Terminal haengt bei Heredoc
**Datum**: 2026-03-01
**Fehler**: Terminal reagiert nicht bei cat << EOF
**Ursache**: Terminal hat Probleme mit multi-line heredoc
**Loesung**: NUR printf oder echo verwenden, NIEMALS heredoc
**Verhinderung**: Befehle kurz halten, max 2-3 Zeilen

## Checkliste fuer neue Developer
- pip install -r requirements.txt
- .env Datei erstellen
- JSON validieren: python -m json.tool app/locales/de.json
- Server starten: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- Test-Request: curl http://localhost:8000/mcp/search?q=test&lang=de
