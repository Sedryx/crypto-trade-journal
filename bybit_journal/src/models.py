"""Data models shared by the local database and service layer."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Trade:
    """Normalized trade record stored in SQLite and exported to the UI."""
    id: Optional[int] = None
    bybit_trade_id: str = ""
    symbol: str = ""
    side: str = ""
    qty: float = 0.0
    entry_price: float = 0.0
    exit_price: float = 0.0
    take_profit: float = 0.0
    stop_loss: float = 0.0
    leverage: float = 0.0
    pnl: float = 0.0
    invested_amount: float = 0.0
    trade_time: str = ""
    note: Optional[str] = None
    screenshot_path: Optional[str] = None
