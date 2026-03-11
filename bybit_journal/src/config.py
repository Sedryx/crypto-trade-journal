"""Project paths and environment loading helpers."""

import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

APP_NAME = "BybitTradeJournal"

# Project source root used for code, packaging metadata and legacy migration.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BASE_DIR = PROJECT_ROOT / "bybit_journal"

# Legacy in-repo locations kept for migration only.
LEGACY_DATA_DIR = BASE_DIR / "data"
LEGACY_DB_PATH = LEGACY_DATA_DIR / "journal.db"
LEGACY_LOG_PATH = LEGACY_DATA_DIR / "log"
LEGACY_ENV_PATH = PROJECT_ROOT / ".env"
LEGACY_EXPORTS_DIR = BASE_DIR / "exports"

# Windows-friendly user storage.
APPDATA_ROOT = Path(os.getenv("APPDATA") or (Path.home() / "AppData" / "Roaming"))
DOCUMENTS_ROOT = Path(os.getenv("USERPROFILE") or Path.home()) / "Documents"

USER_ROOT = APPDATA_ROOT / APP_NAME
USER_CONFIG_DIR = USER_ROOT / "config"
USER_DATA_DIR = USER_ROOT / "data"
USER_EXPORTS_DIR = DOCUMENTS_ROOT / APP_NAME / "exports"

ENV_PATH = USER_CONFIG_DIR / ".env"
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"
DB_PATH = USER_DATA_DIR / "journal.db"
LOG_PATH = USER_DATA_DIR / "log"
EXPORTS_DIR = USER_EXPORTS_DIR

BYBIT_BASE_URL = "https://api.bybit.com"


def _copy_if_missing(source: Path, destination: Path) -> None:
    """Copy a legacy file only when the new location is still empty."""
    if source.exists() and not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _migrate_legacy_storage() -> None:
    """Copy previous in-repo runtime files into the user folders on first launch."""
    _copy_if_missing(LEGACY_ENV_PATH, ENV_PATH)
    _copy_if_missing(LEGACY_DB_PATH, DB_PATH)
    _copy_if_missing(LEGACY_LOG_PATH, LOG_PATH)

    if LEGACY_EXPORTS_DIR.exists():
        for legacy_file in LEGACY_EXPORTS_DIR.glob("*.xlsx"):
            target = EXPORTS_DIR / legacy_file.name
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(legacy_file, target)


def ensure_directories() -> None:
    """Create the Windows user folders used by the desktop app."""
    USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    _migrate_legacy_storage()


def ensure_env_file() -> None:
    """Create the user .env file if it does not exist yet."""
    ensure_directories()
    if ENV_PATH.exists():
        return

    ENV_PATH.write_text(
        "BYBIT_API_KEY=\nBYBIT_API_SECRET=\n",
        encoding="utf-8",
    )


def load_environment() -> None:
    """Reload the active .env file into the current process."""
    ensure_env_file()
    load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_api_credentials() -> tuple[str | None, str | None]:
    """Read Bybit API credentials from the active user environment."""
    load_environment()
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    return api_key, api_secret


def has_api_credentials() -> bool:
    """Return True only when both API key and secret are configured."""
    api_key, api_secret = get_api_credentials()
    return bool(api_key and api_secret)
