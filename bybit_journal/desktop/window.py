"""PyWebView window creation helpers."""

import sys
from pathlib import Path


APP_TITLE = "Bybit Trade Journal"


def get_project_base_dir() -> Path:
    """Resolve the bundled base dir both in dev mode and PyInstaller mode."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent


def get_frontend_entrypoint() -> str:
    """Return the local file:// URL used to load the frontend entry page."""
    frontend_path = get_project_base_dir() / "frontend" / "index.html"
    return frontend_path.resolve().as_uri()


def start_desktop_app(api=None) -> None:
    """Create the desktop window and inject the Python bridge into the UI."""
    import webview

    webview.create_window(
        APP_TITLE,
        url=get_frontend_entrypoint(),
        js_api=api,
        width=1360,
        height=860,
        min_size=(1080, 720),
        text_select=True,
    )
    webview.start(debug=not getattr(sys, "frozen", False))
