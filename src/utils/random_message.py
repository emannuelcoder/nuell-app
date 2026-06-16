from pathlib import Path
import json
import random

messages_json = Path(__file__).parent.parent / "data" / "messages.json"

def random_message():
    with open(messages_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    ran = random.randint(0, 89)

    message = random.choice(data["messages"])
    return message