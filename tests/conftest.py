import json
import os
from pathlib import Path


settings_file = Path(__file__).parent.parent / "local.settings.json"

with open(settings_file, "r") as file:
    settings = json.load(file)

for key, value in settings.get("Values", {}).items():
    os.environ[key] = value