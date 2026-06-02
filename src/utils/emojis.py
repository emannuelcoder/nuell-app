from pathlib import Path
import json

emojis_json = Path(__file__).parent.parent / "data" / "emojis.json"

def load_emojis():
    with open(emojis_json, "r", encoding="utf-8") as f:
        return json.load(f)
    
emojis = load_emojis()

def emoji(name: str):
    return emojis.get(name)
