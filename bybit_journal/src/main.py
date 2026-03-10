from config import ensure_directories, DB_PATH
from db import init_db, insert_trade, get_all_trades, create_test_trade
from api import get_wallet_balance
import sqlite3


def display_trades(trades) -> None:
    if not trades:
        print("Aucun trade enregistré.")
        return

    print("\nTrades en base :")
    for trade in trades:
        print(
            f"[{trade.id}] "
            f"{trade.symbol} | "
            f"{trade.side} | "
            f"Entry: {trade.entry_price} | "
            f"Exit: {trade.exit_price} | "
            f"Qty: {trade.qty} | "
            f"PnL: {trade.pnl} | "
            f"Date: {trade.trade_time}"
        )


def display_wallet(wallet: dict) -> None:
    if wallet.get("retCode") != 0:
        print("Erreur Bybit :", wallet.get("retMsg"))
        return

    result = wallet.get("result", {})
    accounts = result.get("list", [])

    if not accounts:
        print("Aucun compte retourné par l'API.")
        return

    account = accounts[0]

    print("\nRésumé portefeuille Bybit :")
    print(f"Type de compte : {account.get('accountType')}")
    print(f"Total equity : {account.get('totalEquity')}")
    print(f"Total wallet balance : {account.get('totalWalletBalance')}")

    coins = account.get("coin", [])
    non_zero_coins = [coin for coin in coins if float(coin.get("equity", 0) or 0) > 0]

    if not non_zero_coins:
        print("Aucun solde non nul.")
        return

    print("\nSoldes non nuls :")
    for coin in non_zero_coins:
        print(
            f"{coin.get('coin')} | "
            f"Equity: {coin.get('equity')} | "
            f"Wallet: {coin.get('walletBalance')} | "
            f"USD Value: {coin.get('usdValue')}"
        )


def test_api() -> None:
    print("\nTest API privée Bybit")

    try:
        wallet = get_wallet_balance()
        display_wallet(wallet)
    except Exception as e:
        print("Erreur API :", e)


def main() -> None:
    print("=== Démarrage de Bybit Journal ===")

    try:
        ensure_directories()
        print("Dossiers prêts.")

        init_db()
        print(f"Base SQLite prête : {DB_PATH}")

        test_trade = create_test_trade()
        insert_trade(test_trade)
        print("Trade de test inséré si absent.")

        trades = get_all_trades()
        display_trades(trades)

        test_api()

        print("\n=== Fin du programme ===")

    except sqlite3.DatabaseError as e:
        print("Erreur SQLite :", e)
        print(f"Base corrompue : {DB_PATH}")

    except Exception as e:
        print("Erreur inattendue :", e)


if __name__ == "__main__":
    main()