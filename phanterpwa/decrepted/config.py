import json
import os
with open(os.path.join(os.path.dirname(__file__), "..", "config.json"), 'r', encoding="utf-8") as f:
    CONFIG = json.load(f)
