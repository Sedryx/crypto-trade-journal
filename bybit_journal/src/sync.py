from models import Trade
from api import get_executions
from db import insert_trade


def execution_to_trade(execution: dict) -> Trade:
    """
    Convertit une exécution Bybit en objet Trade.
    """
    exec_price = float(execution.get("execPrice", 0) or 0)
    exec_qty = float(execution.get("execQty", 0) or 0)
    exec_pnl = float(execution.get("execPnl", 0) or 0)

    return Trade(
        bybit_trade_id=execution.get("execId", ""),
        symbol=execution.get("symbol", ""),
        side=execution.get("side", ""),
        qty=exec_qty,
        entry_price=exec_price,
        exit_price=exec_price,
        take_profit=0.0,
        stop_loss=0.0,
        leverage=0.0,
        pnl=exec_pnl,
        invested_amount=exec_price * exec_qty,
        trade_time=execution.get("execTime", ""),
        note=None,
        screenshot_path=None
    )


def sync_executions_from_category(category: str, start_time: int, end_time: int, limit: int = 50) -> int:
    """
    Récupère les exécutions d'une catégorie et les insère dans SQLite.
    Retourne le nombre de trades traités.
    """
    data = get_executions(
        category=category,
        limit=limit,
        start_time=start_time,
        end_time=end_time
    )

    if data.get("retCode") != 0:
        print(f"Erreur Bybit [{category}] : {data.get('retMsg')}")
        return 0

    executions = data.get("result", {}).get("list", [])

    if not executions:
        return 0

    count = 0

    for execution in executions:
        trade = execution_to_trade(execution)
        insert_trade(trade)
        count += 1

    return count