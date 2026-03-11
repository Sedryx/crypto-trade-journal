"""Bridge exposed to PyWebView so the frontend can call Python services."""

from services import (
    configure_api_credentials,
    export_trades_to_excel,
    get_api_status_data,
    get_dashboard_data,
    get_trade_stats_data,
    get_trades_data,
    seed_dev_test_trades,
    sync_bybit_trades_data,
)


class DesktopBridge:
    def _invoke(self, handler, *args, **kwargs) -> dict:
        """Wrap service calls in a consistent success/data/error payload."""
        try:
            return {
                "success": True,
                "data": handler(*args, **kwargs),
                "error": None,
            }
        except Exception as error:
            return {
                "success": False,
                "data": None,
                "error": str(error),
            }

    def get_dashboard(self) -> dict:
        """Return the dashboard payload for the main desktop view."""
        return self._invoke(get_dashboard_data)

    def get_trades(self, filters: dict | None = None) -> dict:
        """Return filtered trades for the trades screen."""
        payload = filters or {}
        return self._invoke(get_trades_data, **payload)

    def get_stats(self, filters: dict | None = None) -> dict:
        """Return aggregate performance stats."""
        payload = filters or {}
        return self._invoke(get_trade_stats_data, **payload)

    def sync_trades(self, days: int = 30) -> dict:
        """Run the Bybit synchronization flow."""
        return self._invoke(sync_bybit_trades_data, days=days)

    def get_api_status(self) -> dict:
        """Return the current API configuration state."""
        return self._invoke(get_api_status_data)

    def save_api_config(self, api_key: str, api_secret: str) -> dict:
        """Write API credentials into the root .env file."""
        return self._invoke(
            configure_api_credentials,
            api_key=api_key,
            api_secret=api_secret,
        )

    def seed_dev_trades(self, count: int = 20) -> dict:
        """Insert synthetic trades to populate the GUI during development."""
        return self._invoke(seed_dev_test_trades, count=count)

    def export_trades_excel(self, filters: dict | None = None) -> dict:
        """Create an Excel export from the currently selected trade filters."""
        payload = filters or {}
        return self._invoke(export_trades_to_excel, **payload)
