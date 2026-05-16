import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".mornin"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "endpoint": "http://localhost:11434",
    "model": "llama3.2",
    "days": 1,
    "format": "bullet",
    "author_filter": True,
    "repos": [],
}


def load_config():
    if not CONFIG_FILE.exists():
        return DEFAULTS.copy()
    with open(CONFIG_FILE) as f:
        data = json.load(f)
    return {**DEFAULTS, **data}


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
