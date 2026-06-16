from pathlib import Path
import json
import random

jokes_json = Path(__file__).parent.parent / "data" / "jokes.json"

def random_joke():
    with open(jokes_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    joke, answer = random.choice(
        list(data["jokes"].items())
    )

    return joke, answer