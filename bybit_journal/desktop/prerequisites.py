"""Windows prerequisite checks used before starting the desktop shell."""

from __future__ import annotations

import platform
import webbrowser

WEBVIEW2_CLIENT_GUID = "{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
WEBVIEW2_DOWNLOAD_URL = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"


def is_windows() -> bool:
    """Return True only on Windows hosts."""
    return platform.system().lower() == "windows"


def get_webview2_version() -> str | None:
    """Return the installed WebView2 runtime version when available."""
    if not is_windows():
        return None

    try:
        import winreg
    except ImportError:
        return None

    key_paths = [
        rf"SOFTWARE\Microsoft\EdgeUpdate\Clients\{WEBVIEW2_CLIENT_GUID}",
        rf"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{WEBVIEW2_CLIENT_GUID}",
    ]

    for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for key_path in key_paths:
            try:
                with winreg.OpenKey(root, key_path) as key:
                    version, _ = winreg.QueryValueEx(key, "pv")
                    if version:
                        return str(version)
            except OSError:
                continue

    return None


def ensure_webview2_available(open_download_page: bool = False) -> str | None:
    """Raise a readable error if WebView2 is missing on Windows."""
    version = get_webview2_version()
    if version or not is_windows():
        return version

    if open_download_page:
        webbrowser.open(WEBVIEW2_DOWNLOAD_URL)

    raise RuntimeError(
        "Microsoft Edge WebView2 Runtime is required to start the desktop app. "
        f"Install it first: {WEBVIEW2_DOWNLOAD_URL}"
    )
