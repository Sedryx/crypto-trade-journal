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
    DATA_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)


def ensure_env_file() -> None:
    if ENV_PATH.exists():
        return

    ENV_PATH.write_text(
        "BYBIT_API_KEY=\nBYBIT_API_SECRET=\n",
        encoding="utf-8",
    )


def load_environment() -> None:
    ensure_env_file()
    load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_api_credentials() -> tuple[str | None, str | None]:
    load_environment()
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    return api_key, api_secret


def has_api_credentials() -> bool:
    api_key, api_secret = get_api_credentials()
    return bool(api_key and api_secret)
