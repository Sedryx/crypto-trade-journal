"""Bridge exposed to PyWebView so the frontend can call Python services."""

from services import (
    configure_api_credentials,
    create_database_backup,
    delete_trade_data,
    export_trades_to_excel,
    get_api_status_data,
    get_dashboard_data,
    get_trade_detail_data,
    get_trade_stats_data,
    get_trades_data,
    load_app_settings,
    open_runtime_folder,
    restore_database_backup,
    save_app_settings,
    seed_dev_test_trades,
    sync_bybit_trades_data,
    update_trade_journal_data,
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

    def delete_trade(self, trade_id: int) -> dict:
        """Delete one trade from SQLite using its local id."""
        return self._invoke(delete_trade_data, trade_id=trade_id)

    def open_folder(self, target: str) -> dict:
        """Open one runtime folder for the user."""
        return self._invoke(open_runtime_folder, target=target)

    def get_trade_detail(self, trade_id: int) -> dict:
        """Return the full payload of one trade."""
        return self._invoke(get_trade_detail_data, trade_id=trade_id)

    def save_trade_journal(self, trade_id: int, note: str, screenshot_path: str) -> dict:
        """Update the note and screenshot path for a trade."""
        return self._invoke(
            update_trade_journal_data,
            trade_id=trade_id,
            note=note,
            screenshot_path=screenshot_path,
        )

    def get_sync_settings(self) -> dict:
        """Return the persisted sync-related app settings."""
        return self._invoke(load_app_settings)

    def save_sync_settings(self, auto_sync_on_startup: bool, default_sync_days: int) -> dict:
        """Persist sync-related app settings."""
        return self._invoke(
            save_app_settings,
            auto_sync_on_startup=auto_sync_on_startup,
            default_sync_days=default_sync_days,
        )

    def create_backup(self) -> dict:
        """Create a SQLite backup copy."""
        return self._invoke(create_database_backup)

    def restore_backup(self, backup_path: str) -> dict:
        """Restore SQLite from a backup file."""
        return self._invoke(restore_database_backup, backup_path=backup_path)
