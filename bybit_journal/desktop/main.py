"""Desktop entrypoint used to start the PyWebView application."""

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from services import initialize_runtime
from bridge import DesktopBridge
from window import start_desktop_app


def main() -> None:
    """Initialize the backend runtime, then open the desktop window."""
    initialize_runtime()
    start_desktop_app(api=DesktopBridge())


if __name__ == "__main__":
    main()
