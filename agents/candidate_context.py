import json
from pathlib import Path


def load_candidate():
    path = Path(__file__).resolve().parent.parent / "data" / "candidate.json"

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)