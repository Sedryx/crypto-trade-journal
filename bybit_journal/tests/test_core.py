import shutil
import sys
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch


# Test bootstrap:
# add the backend and desktop folders to sys.path so the test runner can import
# the local modules without packaging the project first.
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
DESKTOP_DIR = Path(__file__).resolve().parent.parent / "desktop"
TEMP_ROOT = Path(__file__).resolve().parent.parent / ".tmp_tests"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(DESKTOP_DIR) not in sys.path:
    sys.path.insert(0, str(DESKTOP_DIR))

import config
import db
import sync
import window
from bridge import DesktopBridge
from models import Trade
from services import journal_service


class TemporaryDbTestCase(unittest.TestCase):
    """Base helper that gives each test a fresh isolated SQLite database."""

    def setUp(self) -> None:
        TEMP_ROOT.mkdir(exist_ok=True)
        self.temp_dir = TEMP_ROOT / f"db-{uuid.uuid4().hex}"
        self.temp_dir.mkdir()
        self.temp_db_path = self.temp_dir / "journal.db"
        self.temp_config_dir = self.temp_dir / "config"
        self.temp_data_dir = self.temp_dir / "data"
        self.temp_exports_dir = self.temp_dir / "exports"
        self.temp_backups_dir = self.temp_dir / "backups"
        self.temp_env_path = self.temp_config_dir / ".env"
        self.temp_settings_path = self.temp_config_dir / "settings.json"

        # Patch the runtime DB path so each test writes into its own temp file.
        self.db_path_patcher = patch.object(db, "DB_PATH", self.temp_db_path)
        self.ensure_directories_patcher = patch.object(
            db, "ensure_directories", lambda: self.temp_db_path.parent.mkdir(exist_ok=True)
        )
        self.config_dir_patcher = patch.object(config, "USER_CONFIG_DIR", self.temp_config_dir)
        self.data_dir_patcher = patch.object(config, "USER_DATA_DIR", self.temp_data_dir)
        self.exports_dir_patcher = patch.object(config, "EXPORTS_DIR", self.temp_exports_dir)
        self.backups_dir_patcher = patch.object(config, "BACKUPS_DIR", self.temp_backups_dir)
        self.env_path_patcher = patch.object(config, "ENV_PATH", self.temp_env_path)
        self.settings_path_patcher = patch.object(config, "SETTINGS_PATH", self.temp_settings_path)
        self.db_runtime_path_patcher = patch.object(config, "DB_PATH", self.temp_db_path)
        self.legacy_env_patcher = patch.object(config, "LEGACY_ENV_PATH", self.temp_dir / "legacy.env")
        self.log_runtime_path_patcher = patch.object(config, "LOG_PATH", self.temp_data_dir / "log")
        self.legacy_db_patcher = patch.object(config, "LEGACY_DB_PATH", self.temp_dir / "legacy.db")
        self.legacy_log_patcher = patch.object(config, "LEGACY_LOG_PATH", self.temp_dir / "legacy.log")
        self.legacy_exports_patcher = patch.object(config, "LEGACY_EXPORTS_DIR", self.temp_dir / "legacy_exports")

        self.db_path_patcher.start()
        self.ensure_directories_patcher.start()
        self.config_dir_patcher.start()
        self.data_dir_patcher.start()
        self.exports_dir_patcher.start()
        self.backups_dir_patcher.start()
        self.env_path_patcher.start()
        self.settings_path_patcher.start()
        self.db_runtime_path_patcher.start()
        self.log_runtime_path_patcher.start()
        self.legacy_env_patcher.start()
        self.legacy_db_patcher.start()
        self.legacy_log_patcher.start()
        self.legacy_exports_patcher.start()
        db.init_db()

    def tearDown(self) -> None:
        self.legacy_exports_patcher.stop()
        self.legacy_log_patcher.stop()
        self.legacy_db_patcher.stop()
        self.legacy_env_patcher.stop()
        self.log_runtime_path_patcher.stop()
        self.db_runtime_path_patcher.stop()
        self.env_path_patcher.stop()
        self.settings_path_patcher.stop()
        self.backups_dir_patcher.stop()
        self.exports_dir_patcher.stop()
        self.data_dir_patcher.stop()
        self.config_dir_patcher.stop()
        self.ensure_directories_patcher.stop()
        self.db_path_patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def insert_trade(self, **kwargs) -> None:
        """Insert one synthetic trade with overridable fields."""
        trade = Trade(
            bybit_trade_id=kwargs.get("bybit_trade_id", str(uuid.uuid4())),
            symbol=kwargs.get("symbol", "BTCUSDT"),
            side=kwargs.get("side", "Buy"),
            qty=kwargs.get("qty", 0.1),
            entry_price=kwargs.get("entry_price", 100.0),
            exit_price=kwargs.get("exit_price", 101.0),
            take_profit=0.0,
            stop_loss=0.0,
            leverage=0.0,
            pnl=kwargs.get("pnl", 1.0),
            invested_amount=kwargs.get("invested_amount", 10.0),
            trade_time=kwargs.get("trade_time", "2026-03-10 10:00:00"),
            note=None,
            screenshot_path=None,
        )
        db.insert_trade(trade)


class ConfigTests(unittest.TestCase):
    """Configuration tests for .env bootstrapping."""

    def test_ensure_env_file_creates_expected_template(self) -> None:
        TEMP_ROOT.mkdir(exist_ok=True)
        temp_dir = TEMP_ROOT / f"config-{uuid.uuid4().hex}"
        temp_dir.mkdir()
        config_dir = temp_dir / "config"
        data_dir = temp_dir / "data"
        exports_dir = temp_dir / "exports"
        backups_dir = temp_dir / "backups"
        env_path = config_dir / ".env"

        try:
            with (
                patch.object(config, "USER_CONFIG_DIR", config_dir),
                patch.object(config, "USER_DATA_DIR", data_dir),
                patch.object(config, "EXPORTS_DIR", exports_dir),
                patch.object(config, "BACKUPS_DIR", backups_dir),
                patch.object(config, "ENV_PATH", env_path),
                patch.object(config, "SETTINGS_PATH", config_dir / "settings.json"),
                patch.object(config, "DB_PATH", data_dir / "journal.db"),
                patch.object(config, "LOG_PATH", data_dir / "log"),
                patch.object(config, "LEGACY_ENV_PATH", temp_dir / "missing.env"),
                patch.object(config, "LEGACY_DB_PATH", temp_dir / "missing.db"),
                patch.object(config, "LEGACY_LOG_PATH", temp_dir / "missing.log"),
                patch.object(config, "LEGACY_EXPORTS_DIR", temp_dir / "missing_exports"),
            ):
                config.ensure_env_file()

            self.assertTrue(env_path.exists())
            self.assertEqual(
                env_path.read_text(encoding="utf-8"),
                "BYBIT_API_KEY=\nBYBIT_API_SECRET=\n",
            )
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_ensure_directories_migrates_legacy_env_file(self) -> None:
        TEMP_ROOT.mkdir(exist_ok=True)
        temp_dir = TEMP_ROOT / f"migrate-{uuid.uuid4().hex}"
        temp_dir.mkdir()
        legacy_env_path = temp_dir / "legacy.env"
        new_config_dir = temp_dir / "config"
        new_data_dir = temp_dir / "data"
        new_exports_dir = temp_dir / "exports"
        new_backups_dir = temp_dir / "backups"
        new_env_path = new_config_dir / ".env"
        new_db_path = new_data_dir / "journal.db"
        legacy_env_path.write_text("BYBIT_API_KEY=old\nBYBIT_API_SECRET=secret\n", encoding="utf-8")

        try:
            with (
                patch.object(config, "LEGACY_ENV_PATH", legacy_env_path),
                patch.object(config, "USER_CONFIG_DIR", new_config_dir),
                patch.object(config, "USER_DATA_DIR", new_data_dir),
                patch.object(config, "EXPORTS_DIR", new_exports_dir),
                patch.object(config, "BACKUPS_DIR", new_backups_dir),
                patch.object(config, "ENV_PATH", new_env_path),
                patch.object(config, "SETTINGS_PATH", new_config_dir / "settings.json"),
                patch.object(config, "DB_PATH", new_db_path),
                patch.object(config, "LOG_PATH", new_data_dir / "log"),
                patch.object(config, "LEGACY_EXPORTS_DIR", temp_dir / "missing_exports"),
                patch.object(config, "LEGACY_DB_PATH", temp_dir / "missing.db"),
                patch.object(config, "LEGACY_LOG_PATH", temp_dir / "missing.log"),
            ):
                config.ensure_directories()

            self.assertTrue(new_env_path.exists())
            self.assertIn("BYBIT_API_KEY=old", new_env_path.read_text(encoding="utf-8"))
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class DatabaseTests(TemporaryDbTestCase):
    """Low-level SQLite behavior: insert, filter and aggregate."""

    def test_insert_trade_ignores_duplicate_bybit_trade_id(self) -> None:
        trade = db.create_test_trade()

        first_insert = db.insert_trade(trade)
        second_insert = db.insert_trade(trade)
        trades = db.get_all_trades()

        self.assertTrue(first_insert)
        self.assertFalse(second_insert)
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].bybit_trade_id, "TEST001")

    def test_query_trades_applies_filters(self) -> None:
        self.insert_trade(
            bybit_trade_id="A",
            symbol="BTCUSDT",
            side="Buy",
            pnl=10.0,
            trade_time="2026-03-01 12:00:00",
        )
        self.insert_trade(
            bybit_trade_id="B",
            symbol="ETHUSDT",
            side="Sell",
            pnl=-3.0,
            trade_time="2026-03-02 12:00:00",
        )
        self.insert_trade(
            bybit_trade_id="C",
            symbol="BTCUSDT",
            side="Buy",
            pnl=2.0,
            trade_time="2026-03-03 12:00:00",
        )

        trades = db.query_trades(
            symbol="BTCUSDT",
            side="Buy",
            start_time="2026-03-02 00:00:00",
            min_pnl=1.0,
        )

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].bybit_trade_id, "C")

    def test_get_trade_stats_returns_base_metrics(self) -> None:
        self.insert_trade(bybit_trade_id="A", pnl=10.0, invested_amount=100.0)
        self.insert_trade(bybit_trade_id="B", pnl=-4.0, invested_amount=50.0)
        self.insert_trade(bybit_trade_id="C", pnl=0.0, invested_amount=25.0)

        stats = db.get_trade_stats()

        self.assertEqual(stats["total_trades"], 3)
        self.assertEqual(stats["winning_trades"], 1)
        self.assertEqual(stats["losing_trades"], 1)
        self.assertEqual(stats["breakeven_trades"], 1)
        self.assertEqual(stats["total_pnl"], 6.0)
        self.assertEqual(stats["best_trade"], 10.0)
        self.assertEqual(stats["worst_trade"], -4.0)
        self.assertEqual(stats["total_invested_amount"], 175.0)
        self.assertAlmostEqual(stats["win_rate"], 33.3333, places=3)

    def test_delete_trade_by_id_removes_row(self) -> None:
        self.insert_trade(bybit_trade_id="A")
        trade = db.get_all_trades()[0]

        deleted = db.delete_trade_by_id(trade.id)
        trades = db.get_all_trades()

        self.assertTrue(deleted)
        self.assertEqual(len(trades), 0)


class ServiceTests(TemporaryDbTestCase):
    """Service-layer tests used by the desktop bridge and frontend."""

    def test_get_trades_data_returns_serialized_trades_and_filters(self) -> None:
        self.insert_trade(
            bybit_trade_id="A",
            symbol="BTCUSDT",
            side="Buy",
            pnl=8.0,
            trade_time="2026-03-05 12:00:00",
        )

        trades_data = journal_service.get_trades_data(symbol="BTCUSDT", side="Buy", limit=5)

        self.assertEqual(trades_data["count"], 1)
        self.assertEqual(trades_data["filters"]["symbol"], "BTCUSDT")
        self.assertEqual(trades_data["trades"][0]["bybit_trade_id"], "A")
        self.assertEqual(trades_data["trades"][0]["symbol"], "BTCUSDT")

    def test_get_api_status_data_reports_missing_credentials(self) -> None:
        # A missing API key/secret should be reported as an incomplete setup.
        with patch.object(config, "has_api_credentials", return_value=False):
            status = journal_service.get_api_status_data()

        self.assertFalse(status["has_credentials"])
        self.assertIn("missing", status["message"].lower())
        self.assertIn("db_path", status)
        self.assertIn("exports_dir", status)
        self.assertIn("dev_mode", status)

    def test_sync_bybit_trades_data_returns_structured_summary(self) -> None:
        # One mocked call per Bybit category: linear, spot, inverse, option.
        with patch.object(
            journal_service,
            "sync_executions_from_category",
            side_effect=[2, 0, 1, 3],
        ):
            sync_summary = journal_service.sync_bybit_trades_data(days=7)

        self.assertEqual(sync_summary["days"], 7)
        self.assertEqual(sync_summary["total_inserted"], 6)
        self.assertEqual(sync_summary["range_count"], 1)
        self.assertEqual(sync_summary["categories"][0]["category"], "linear")
        self.assertEqual(sync_summary["categories"][3]["inserted_count"], 3)

    def test_sync_bybit_trades_data_splits_ranges_above_seven_days(self) -> None:
        # Bybit only accepts 7-day windows, so 21 days must be split into 3 ranges.
        side_effects = [1, 2, 0, 1, 0, 0, 3, 1, 0, 2, 1, 0]
        with patch.object(
            journal_service,
            "sync_executions_from_category",
            side_effect=side_effects,
        ) as mocked:
            sync_summary = journal_service.sync_bybit_trades_data(days=21, now_ms=21 * 24 * 60 * 60 * 1000)

        self.assertEqual(sync_summary["range_count"], 3)
        self.assertEqual(mocked.call_count, 12)

    def test_get_dashboard_data_returns_stats_and_recent_trades(self) -> None:
        # The dashboard aggregates API status, stats, wallet and recent rows.
        self.insert_trade(bybit_trade_id="A", symbol="BTCUSDT", pnl=3.0)

        with patch.object(
            journal_service,
            "get_wallet_summary",
            return_value={"success": True, "account": {"total_equity": "100"}, "non_zero_balances": []},
        ):
            dashboard = journal_service.get_dashboard_data()

        self.assertIn("api_status", dashboard)
        self.assertIn("stats", dashboard)
        self.assertIn("wallet", dashboard)
        self.assertIn("recent_trades", dashboard)
        self.assertEqual(dashboard["stats"]["total_trades"], 1)
        self.assertEqual(len(dashboard["recent_trades"]), 1)

    def test_get_wallet_summary_extracts_non_zero_balances(self) -> None:
        # Wallet normalization should keep only positive balances and split stables out.
        wallet = {
            "retCode": 0,
            "result": {
                "list": [
                    {
                        "accountType": "UNIFIED",
                        "totalEquity": "100.5",
                        "totalWalletBalance": "99.0",
                        "coin": [
                            {
                                "coin": "USDT",
                                "equity": "20",
                                "walletBalance": "20",
                                "usdValue": "20",
                            },
                            {
                                "coin": "BTC",
                                "equity": "0.01",
                                "walletBalance": "0.01",
                                "usdValue": "80",
                            },
                            {
                                "coin": "ETH",
                                "equity": "0",
                                "walletBalance": "0",
                                "usdValue": "0",
                            },
                        ],
                    }
                ]
            },
        }

        with patch.object(
            journal_service,
            "_get_usd_conversion_rates",
            return_value={"USD": 1.0, "JPY": 150.0, "GBP": 0.79, "CHF": 0.88, "EUR": 0.92},
        ):
            summary = journal_service.get_wallet_summary(wallet)

        self.assertTrue(summary["success"])
        self.assertEqual(summary["account"]["account_type"], "UNIFIED")
        self.assertEqual(summary["account"]["total_equity"], "100.5")
        self.assertEqual(len(summary["non_zero_balances"]), 2)
        self.assertEqual(summary["non_zero_balances"][0]["coin"], "BTC")
        self.assertEqual(summary["non_zero_balances"][1]["coin"], "USDT")
        self.assertEqual(len(summary["stable_balances"]), 1)
        self.assertEqual(summary["stable_balances"][0]["coin"], "USDT")
        self.assertEqual(summary["stable_total_usd"], 20.0)
        self.assertEqual(summary["display_currency"], "USD")
        self.assertIn("JPY", summary["conversion_rates"])

    def test_configure_api_credentials_writes_env_file(self) -> None:
        TEMP_ROOT.mkdir(exist_ok=True)
        temp_dir = TEMP_ROOT / f"env-write-{uuid.uuid4().hex}"
        temp_dir.mkdir()
        config_dir = temp_dir / "config"
        data_dir = temp_dir / "data"
        exports_dir = temp_dir / "exports"
        backups_dir = temp_dir / "backups"
        env_path = config_dir / ".env"

        try:
            with (
                patch.object(config, "USER_CONFIG_DIR", config_dir),
                patch.object(config, "USER_DATA_DIR", data_dir),
                patch.object(config, "EXPORTS_DIR", exports_dir),
                patch.object(config, "BACKUPS_DIR", backups_dir),
                patch.object(config, "ENV_PATH", env_path),
                patch.object(config, "SETTINGS_PATH", config_dir / "settings.json"),
                patch.object(config, "DB_PATH", data_dir / "journal.db"),
                patch.object(config, "LOG_PATH", data_dir / "log"),
                patch.object(config, "LEGACY_ENV_PATH", temp_dir / "missing.env"),
                patch.object(config, "LEGACY_DB_PATH", temp_dir / "missing.db"),
                patch.object(config, "LEGACY_LOG_PATH", temp_dir / "missing.log"),
                patch.object(config, "LEGACY_EXPORTS_DIR", temp_dir / "missing_exports"),
            ):
                result = journal_service.configure_api_credentials("key", "secret")

            self.assertTrue(result["saved"])
            self.assertEqual(env_path.read_text(encoding="utf-8"), "BYBIT_API_KEY=key\nBYBIT_API_SECRET=secret\n")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_seed_dev_test_trades_inserts_requested_count(self) -> None:
        # The dev helper should populate the DB with many distinct rows for UI testing.
        result = journal_service.seed_dev_test_trades(count=20)
        trades = db.get_all_trades()

        self.assertEqual(result["requested"], 20)
        self.assertEqual(result["inserted"], 20)
        self.assertEqual(len(trades), 20)
        self.assertEqual(trades[0].bybit_trade_id, "DEVTEST-020")

    def test_export_trades_to_excel_returns_export_metadata(self) -> None:
        # Mock the workbook builder so the test validates the export flow only.
        self.insert_trade(bybit_trade_id="A", symbol="BTCUSDT", pnl=5.0)
        saved_paths = []

        class FakeWorkbook:
            def save(self, path) -> None:
                saved_paths.append(str(path))

        with patch.object(
            journal_service,
            "_build_excel_workbook",
            return_value=FakeWorkbook(),
        ):
            result = journal_service.export_trades_to_excel(symbol="BTCUSDT")

        self.assertTrue(result["exported"])
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["filters"]["symbol"], "BTCUSDT")
        self.assertEqual(len(saved_paths), 1)
        self.assertTrue(saved_paths[0].endswith(".xlsx"))

    def test_delete_trade_data_returns_deleted_summary(self) -> None:
        self.insert_trade(bybit_trade_id="A")
        trade = db.get_all_trades()[0]

        result = journal_service.delete_trade_data(trade.id)

        self.assertTrue(result["deleted"])
        self.assertEqual(result["trade_id"], trade.id)
        self.assertEqual(len(db.get_all_trades()), 0)

    def test_get_trade_detail_and_update_trade_journal_data(self) -> None:
        self.insert_trade(bybit_trade_id="A", symbol="ETHUSDT", pnl=4.5)
        trade = db.get_all_trades()[0]

        detail = journal_service.get_trade_detail_data(trade.id)
        update = journal_service.update_trade_journal_data(trade.id, "My note", r"C:\shots\trade.png")

        self.assertEqual(detail["symbol"], "ETHUSDT")
        self.assertTrue(update["updated"])
        self.assertEqual(update["trade"]["note"], "My note")
        self.assertEqual(update["trade"]["screenshot_path"], r"C:\shots\trade.png")

    def test_save_app_settings_persists_sync_preferences(self) -> None:
        settings = journal_service.save_app_settings(auto_sync_on_startup=False, default_sync_days=21)
        reloaded = journal_service.load_app_settings()

        self.assertFalse(settings["auto_sync_on_startup"])
        self.assertEqual(settings["default_sync_days"], 21)
        self.assertEqual(reloaded["default_sync_days"], 21)
        self.assertFalse(reloaded["auto_sync_on_startup"])

    def test_open_runtime_folder_returns_opened_path(self) -> None:
        startfile = getattr(journal_service.os, "startfile", None)
        if startfile is None:
            self.skipTest("Windows-only startfile helper.")

        with patch.object(journal_service.os, "startfile") as mocked:
            result = journal_service.open_runtime_folder("exports")

        self.assertTrue(result["opened"])
        self.assertEqual(result["target"], "exports")
        mocked.assert_called_once()

    def test_create_and_restore_database_backup(self) -> None:
        self.insert_trade(bybit_trade_id="A")

        backup = journal_service.create_database_backup()
        db.delete_trade_by_id(db.get_all_trades()[0].id)
        restore = journal_service.restore_database_backup(backup["path"])

        self.assertTrue(backup["created"])
        self.assertTrue(Path(backup["path"]).exists())
        self.assertTrue(restore["restored"])
        self.assertEqual(len(db.get_all_trades()), 1)


class SyncTests(unittest.TestCase):
    """Execution mapping and Bybit pagination behavior."""

    def test_execution_to_trade_maps_expected_fields(self) -> None:
        execution = {
            "execId": "abc123",
            "symbol": "btcusdt",
            "side": "Buy",
            "execQty": "0.25",
            "execPrice": "64000",
            "execPnl": "12.5",
            "execTime": "1710000000000",
        }

        trade = sync.execution_to_trade(execution)

        self.assertEqual(trade.bybit_trade_id, "abc123")
        self.assertEqual(trade.symbol, "BTCUSDT")
        self.assertEqual(trade.side, "Buy")
        self.assertEqual(trade.qty, 0.25)
        self.assertEqual(trade.entry_price, 64000.0)
        self.assertEqual(trade.exit_price, 64000.0)
        self.assertEqual(trade.pnl, 12.5)
        self.assertEqual(trade.invested_amount, 16000.0)
        self.assertEqual(trade.trade_time, "2024-03-09 16:00:00")

    def test_execution_to_trade_normalizes_usdc_perpetual_symbol(self) -> None:
        execution = {
            "execId": "perp123",
            "symbol": "BTCPERP",
            "feeCurrency": "USDC",
            "side": "Buy",
            "execQty": "0.01",
            "execPrice": "66000",
            "execPnl": "0",
            "execTime": "1710000000000",
        }

        trade = sync.execution_to_trade(execution)

        self.assertEqual(trade.symbol, "BTCUSDC")

    def test_fetch_all_executions_from_category_follows_pagination(self) -> None:
        # The second API call must reuse the cursor returned by the first page.
        first_page = {
            "retCode": 0,
            "result": {
                "list": [{"execId": "1"}, {"execId": "2"}],
                "nextPageCursor": "cursor-1",
            },
        }
        second_page = {
            "retCode": 0,
            "result": {
                "list": [{"execId": "3"}],
                "nextPageCursor": "",
            },
        }

        with patch.object(sync, "get_executions", side_effect=[first_page, second_page]) as mocked:
            executions = sync.fetch_all_executions_from_category(
                category="linear",
                start_time=1,
                end_time=2,
                limit=100,
            )

        self.assertEqual([item["execId"] for item in executions], ["1", "2", "3"])
        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(mocked.call_args_list[1].kwargs["cursor"], "cursor-1")


class ApiTests(unittest.TestCase):
    """Low-level Bybit request signing helpers."""

    def test_build_query_string_urlencodes_cursor_values(self) -> None:
        from api import _build_query_string

        query_string = _build_query_string(
            {
                "category": "linear",
                "limit": 100,
                "cursor": "343109%3A2%2C343109%3A2",
            }
        )

        self.assertEqual(
            query_string,
            "category=linear&limit=100&cursor=343109%253A2%252C343109%253A2",
        )


class DesktopTests(unittest.TestCase):
    """Desktop shell tests for frontend loading and bridge envelopes."""

    def test_get_frontend_entrypoint_targets_local_index_file(self) -> None:
        entrypoint = window.get_frontend_entrypoint()

        self.assertTrue(entrypoint.startswith("file:///"))
        self.assertIn("frontend/index.html", entrypoint.replace("\\", "/"))

    def test_desktop_bridge_wraps_service_response(self) -> None:
        bridge = DesktopBridge()
        fake_dashboard = {"stats": {"total_trades": 2}}

        with patch("bridge.get_dashboard_data", return_value=fake_dashboard):
            result = bridge.get_dashboard()

        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["stats"]["total_trades"], 2)

if __name__ == "__main__":
    unittest.main()
