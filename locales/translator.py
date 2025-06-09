import json
import os

LOCALES_DIR = os.path.join(os.path.dirname(__file__))
translations = {}


def load_translations(lang: str):
    if lang not in translations:
        path = os.path.join(LOCALES_DIR, f"{lang}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                translations[lang] = json.load(f)
        else:
            translations[lang] = {}


def translate(key: str, lang_code: str) -> str:
    if not lang_code:
        lang_code = "ru"
    lang_code = lang_code.split("-")[0]

    if lang_code not in translations:
        load_translations(lang_code)
    return translations.get(lang_code, {}).get(key, key)