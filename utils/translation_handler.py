from src.state import state_manager
import json
import os

# Get the absolute path of the project root (one level up from src/) to find translations.json
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
translations_path = os.path.join(project_root, "translations.json")

bruteforce_path_json = "/Users/achoubey/Desktop/KTH/2025/ICM Paris/PVT-PSQI-KSS-Protocol/utils/translations.json"

try:
    with open(bruteforce_path_json, "r", encoding="utf-8") as f:
        TRANSLATIONS = json.load(f)
except FileNotFoundError:
    print(f"Could not find translations file at: {translations_path}")
    TRANSLATIONS = {}

def tr(key):
    lang = state_manager.get_language()
    return TRANSLATIONS.get(lang, {}).get(key, key)

# Load the translations
with open("utils/translations.json", encoding="utf-8") as f:
    translations = json.load(f)

def get_translation_key_by_value(displayed_value, current_lang):
    """
    Given a displayed translation (e.g., in French), return the corresponding translation key.
    """
    for key, value in translations[current_lang].items():
        if value == displayed_value:
            return key
    return None

def get_english_from_displayed(displayed_value):
    """
    Given a translated value shown to the user (e.g., French),
    find and return the English version.
    """
    current_lang = state_manager.get_language()
    key = get_translation_key_by_value(displayed_value, current_lang)
    if key and key in translations["en"]:
        return translations["en"][key]
    return displayed_value  # fallback if not found
