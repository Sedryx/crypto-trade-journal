"""SQLite access layer for trades and derived statistics."""

import sqlite3

from config import DB_PATH, ensure_directories
from models import Trade


def get_connection() -> sqlite3.Connection:
    """Open a SQLite connection using the configured project database path."""
    ensure_directories()
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Create the trades table when the application starts."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bybit_trade_id TEXT UNIQUE,
            symbol TEXT NOT NULL,
            side TEXT,
            qty REAL,
            entry_price REAL,
            exit_price REAL,
            take_profit REAL,
            stop_loss REAL,
            leverage REAL,
            pnl REAL,
            invested_amount REAL,
            trade_time TEXT,
            note TEXT,
            screenshot_path TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def insert_trade(trade: Trade) -> bool:
    """Insert one trade and return True only when SQLite stored a new row."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO trades (
            bybit_trade_id,
            symbol,
            side,
            qty,
            entry_price,
            exit_price,
            take_profit,
            stop_loss,
            leverage,
            pnl,
            invested_amount,
            trade_time,
            note,
            screenshot_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            trade.bybit_trade_id,
            trade.symbol,
            trade.side,
            trade.qty,
            trade.entry_price,
            trade.exit_price,
            trade.take_profit,
            trade.stop_loss,
            trade.leverage,
            trade.pnl,
            trade.invested_amount,
            trade.trade_time,
            trade.note,
            trade.screenshot_path,
        ),
    )

    inserted = cursor.rowcount == 1
    conn.commit()
    conn.close()
    return inserted


def delete_trade_by_id(trade_id: int) -> bool:
    """Delete one trade by SQLite id and return True if a row was removed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
    deleted = cursor.rowcount == 1
    conn.commit()
    conn.close()
    return deleted


def get_trade_by_id(trade_id: int) -> Trade | None:
    """Return one trade by SQLite id, or None when it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            bybit_trade_id,
            symbol,
            side,
            qty,
            entry_price,
            exit_price,
            take_profit,
            stop_loss,
            leverage,
            pnl,
            invested_amount,
            trade_time,
            note,
            screenshot_path
        FROM trades
        WHERE id = ?
        """,
        (trade_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return _row_to_trade(row) if row else None


def update_trade_journal_fields(trade_id: int, note: str | None, screenshot_path: str | None) -> bool:
    """Update the journal-only fields for one trade."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE trades
        SET note = ?, screenshot_path = ?
        WHERE id = ?
        """,
        (note, screenshot_path, trade_id),
    )
    updated = cursor.rowcount == 1
    conn.commit()
    conn.close()
    return updated


def _row_to_trade(row: tuple) -> Trade:
    """Convert a SQLite row into the Trade dataclass."""
    return Trade(
        id=row[0],
        bybit_trade_id=row[1],
        symbol=row[2],
        side=row[3],
        qty=row[4],
        entry_price=row[5],
        exit_price=row[6],
        take_profit=row[7],
        stop_loss=row[8],
        leverage=row[9],
        pnl=row[10],
        invested_amount=row[11],
        trade_time=row[12],
        note=row[13],
        screenshot_path=row[14],
    )


def _build_trade_filters(
    symbol: str | None = None,
    side: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    min_pnl: float | None = None,
    max_pnl: float | None = None,
) -> tuple[str, list]:
    """Build the WHERE clause shared by listing and statistics queries."""
    conditions = []
    params = []

    if symbol:
        conditions.append("symbol = ?")
        params.append(symbol.upper())

    if side:
        conditions.append("LOWER(side) = ?")
        params.append(side.lower())

    if start_time:
        conditions.append("trade_time >= ?")
        params.append(start_time)

    if end_time:
        conditions.append("trade_time <= ?")
        params.append(end_time)

    if min_pnl is not None:
        conditions.append("pnl >= ?")
        params.append(min_pnl)

    if max_pnl is not None:
        conditions.append("pnl <= ?")
        params.append(max_pnl)

    if not conditions:
        return "", params

    return "WHERE " + " AND ".join(conditions), params


def get_all_trades() -> list[Trade]:
    """Return the full trade list using the default ordering."""
    return query_trades()


def query_trades(
    symbol: str | None = None,
    side: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    min_pnl: float | None = None,
    max_pnl: float | None = None,
    limit: int | None = None,
) -> list[Trade]:
    """Return trades filtered by symbol, side, date and PnL bounds."""
    conn = get_connection()
    cursor = conn.cursor()

    where_clause, params = _build_trade_filters(
        symbol=symbol,
        side=side,
        start_time=start_time,
        end_time=end_time,
        min_pnl=min_pnl,
        max_pnl=max_pnl,
    )

    query = f"""
        SELECT
            id,
            bybit_trade_id,
            symbol,
            side,
            qty,
            entry_price,
            exit_price,
            take_profit,
            stop_loss,
            leverage,
            pnl,
            invested_amount,
            trade_time,
            note,
            screenshot_path
        FROM trades
        {where_clause}
        ORDER BY trade_time DESC, id DESC
    """

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [_row_to_trade(row) for row in rows]


def get_trade_stats(
    symbol: str | None = None,
    side: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
) -> dict:
    """Compute aggregate trade statistics directly in SQLite."""
    conn = get_connection()
    cursor = conn.cursor()

    where_clause, params = _build_trade_filters(
        symbol=symbol,
        side=side,
        start_time=start_time,
        end_time=end_time,
    )

    query = f"""
        SELECT
            COUNT(*) AS total_trades,
            COALESCE(SUM(pnl), 0),
            COALESCE(AVG(pnl), 0),
            SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END),
            SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END),
            SUM(CASE WHEN pnl = 0 THEN 1 ELSE 0 END),
            COALESCE(MAX(pnl), 0),
            COALESCE(MIN(pnl), 0),
            COALESCE(SUM(invested_amount), 0)
        FROM trades
        {where_clause}
    """

    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()

    total_trades = row[0] or 0
    wins = row[3] or 0
    losses = row[4] or 0

    win_rate = 0.0
    if total_trades:
        win_rate = (wins / total_trades) * 100

    return {
        "total_trades": total_trades,
        "total_pnl": row[1] or 0.0,
        "average_pnl": row[2] or 0.0,
        "winning_trades": wins,
        "losing_trades": losses,
        "breakeven_trades": row[5] or 0,
        "best_trade": row[6] or 0.0,
        "worst_trade": row[7] or 0.0,
        "total_invested_amount": row[8] or 0.0,
        "win_rate": win_rate,
    }


def create_test_trade() -> Trade:
    """Return one deterministic trade used by tests."""
    return Trade(
        bybit_trade_id="TEST001",
        symbol="BTCUSDT",
        side="Buy",
        qty=0.01,
        entry_price=65000.0,
        exit_price=65500.0,
        take_profit=66000.0,
        stop_loss=64500.0,
        leverage=5.0,
        pnl=5.0,
        invested_amount=130.0,
        trade_time="2026-03-10 14:00:00",
        note="Trade de test",
        screenshot_path=None,
    )
