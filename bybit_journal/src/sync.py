"""Conversion and import helpers for Bybit executions."""

from datetime import UTC, datetime

from api import get_executions
from db import insert_trade
from models import Trade


def _format_trade_time(exec_time: str | int | None) -> str:
    """Convert a Bybit millisecond timestamp into the local storage format."""
    if exec_time in (None, ""):
        return ""

    timestamp_ms = int(exec_time)
    timestamp_seconds = timestamp_ms / 1000
    return datetime.fromtimestamp(timestamp_seconds, tz=UTC).strftime("%Y-%m-%d %H:%M:%S")


def execution_to_trade(execution: dict) -> Trade:
    """Map a raw Bybit execution payload to the local Trade model."""
    exec_price = float(execution.get("execPrice", 0) or 0)
    exec_qty = float(execution.get("execQty", 0) or 0)
    exec_pnl = float(execution.get("execPnl", 0) or 0)
    raw_symbol = str(execution.get("symbol", "") or "").upper()
    fee_currency = str(execution.get("feeCurrency", "") or "").upper()

    symbol = raw_symbol
    # Bybit often returns USDC perpetual contracts as `BTCPERP`, `ETHPERP`, ...
    # Normalize those symbols to the more explicit `BTCUSDC`, `ETHUSDC`, etc.
    if raw_symbol.endswith("PERP") and fee_currency == "USDC":
        symbol = f"{raw_symbol[:-4]}USDC"

    return Trade(
        bybit_trade_id=execution.get("execId", ""),
        symbol=symbol,
        side=execution.get("side", ""),
        qty=exec_qty,
        entry_price=exec_price,
        exit_price=exec_price,
        take_profit=0.0,
        stop_loss=0.0,
        leverage=0.0,
        pnl=exec_pnl,
        invested_amount=exec_price * exec_qty,
        trade_time=_format_trade_time(execution.get("execTime")),
        note=None,
        screenshot_path=None,
    )


def fetch_all_executions_from_category(
    category: str,
    start_time: int,
    end_time: int,
    limit: int = 100,
) -> list[dict]:
    """Follow Bybit pagination and return the full execution list for one category."""
    all_executions = []
    cursor = None

    while True:
        data = get_executions(
            category=category,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
            cursor=cursor,
        )

        if data.get("retCode") != 0:
            raise ValueError(f"Erreur Bybit [{category}] : {data.get('retMsg')}")

        result = data.get("result", {})
        executions = result.get("list", [])
        next_cursor = result.get("nextPageCursor") or ""

        if not executions:
            break

        all_executions.extend(executions)

        if not next_cursor:
            break

        cursor = next_cursor

    return all_executions


def sync_executions_from_category(
    category: str,
    start_time: int,
    end_time: int,
    limit: int = 100,
) -> int:
    """Insert a category execution batch into SQLite and return the inserted count."""
    executions = fetch_all_executions_from_category(
        category=category,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    inserted_count = 0
    for execution in executions:
        trade = execution_to_trade(execution)
        if insert_trade(trade):
            inserted_count += 1

    return inserted_count
