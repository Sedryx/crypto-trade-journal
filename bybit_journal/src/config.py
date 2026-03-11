"""Project paths and environment loading helpers."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Racine du projet (dossier contenant README.md, requirements.txt et bybit_journal/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BASE_DIR = PROJECT_ROOT / "bybit_journal"

DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

DB_PATH = DATA_DIR / "journal.db"
LOG_PATH = DATA_DIR / "app.log"

ENV_PATH = PROJECT_ROOT / ".env"
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"

BYBIT_BASE_URL = "https://api.bybit.com"


def ensure_directories() -> None:
    """Create local folders used by the desktop app."""
    DATA_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)


def ensure_env_file() -> None:
    """Create the root .env file if it does not exist yet."""
    if ENV_PATH.exists():
        return

    ENV_PATH.write_text(
        "BYBIT_API_KEY=\nBYBIT_API_SECRET=\n",
        encoding="utf-8",
    )


def load_environment() -> None:
    """Reload the .env file into the current process."""
    ensure_env_file()
    load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_api_credentials() -> tuple[str | None, str | None]:
    """Read Bybit API credentials from the local environment."""
    load_environment()
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    return api_key, api_secret


def has_api_credentials() -> bool:
    """Return True only when both API key and secret are configured."""
    api_key, api_secret = get_api_credentials()
    return bool(api_key and api_secret)
