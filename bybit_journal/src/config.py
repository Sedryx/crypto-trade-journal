import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

DB_PATH = DATA_DIR / "journal.db"
LOG_PATH = DATA_DIR / "app.log"

BYBIT_BASE_URL = "https://api.bybit.com"

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")


def ensure_directories() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)