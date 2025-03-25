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