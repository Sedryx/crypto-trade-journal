"""PyWebView window creation helpers."""

import sys
from pathlib import Path


APP_TITLE = "Bybit Trade Journal"


def get_project_base_dir() -> Path:
    """Resolve the bundled base dir both in dev mode and PyInstaller mode."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent


def get_app_icon_path() -> Path:
    """Return the .ico file used by the desktop shell and packaged build."""
    return get_project_base_dir() / "frontend" / "asset" / "icon.ico"


def get_frontend_entrypoint() -> str:
    """Return the local file:// URL used to load the frontend entry page."""
    frontend_path = get_project_base_dir() / "frontend" / "index.html"
    return frontend_path.resolve().as_uri()


def _apply_native_window_icon(window) -> None:
    """Set the WinForms window icon in development and packaged modes."""
    icon_path = get_app_icon_path()
    if not icon_path.exists():
        return

    try:
        window.events.shown.wait(10)
        native = getattr(window, "native", None)
        if native is None:
            return

        import clr

        clr.AddReference("System.Drawing")
        from System.Drawing import Icon

        native.Icon = Icon(str(icon_path))
    except Exception:
        # The app should still start even if the icon cannot be applied.
        return


def start_desktop_app(api=None) -> None:
    """Create the desktop window and inject the Python bridge into the UI."""
    import webview

    window = webview.create_window(
        APP_TITLE,
        url=get_frontend_entrypoint(),
        js_api=api,
        width=1360,
        height=860,
        min_size=(1080, 720),
        text_select=True,
    )
    webview.start(
        _apply_native_window_icon,
        args=(window,),
        debug=not getattr(sys, "frozen", False),
    )
