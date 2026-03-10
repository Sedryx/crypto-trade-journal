import sqlite3
from config import DB_PATH, ensure_directories
from models import Trade


def get_connection() -> sqlite3.Connection:
    """
    Ouvre une connexion vers la base SQLite.
    """
    ensure_directories()
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """
    Crée la table trades si elle n'existe pas.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
    """)

    conn.commit()
    conn.close()


def insert_trade(trade: Trade) -> None:
    """
    Insère un Trade dans la base.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
    """, (
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
        trade.screenshot_path
    ))

    conn.commit()
    conn.close()


def get_all_trades() -> list[Trade]:
    """
    Retourne tous les trades sous forme de liste d'objets Trade.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    trades = []
    for row in rows:
        trade = Trade(
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
            screenshot_path=row[14]
        )
        trades.append(trade)

    return trades


def create_test_trade() -> Trade:
    """
    Crée un faux trade de test.
    """
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
        screenshot_path=None
    )