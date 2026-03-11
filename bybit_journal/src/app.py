import time
from pathlib import Path

from api import get_executions, get_wallet_balance
import config
from db import create_test_trade, get_all_trades, init_db, insert_trade
from sync import sync_executions_from_category


def initialize_application() -> None:
    config.ensure_directories()
    config.ensure_env_file()
    config.load_environment()
    init_db()


def show_api_status() -> None:
    if config.has_api_credentials():
        print("Configuration API : OK")
    else:
        print("Configuration API : incomplete (.env vide ou non renseigne)")


def display_trades(trades) -> None:
    if not trades:
        print("\nAucun trade enregistre.")
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
        print("\nErreur Bybit :", wallet.get("retMsg"))
        return

    accounts = wallet.get("result", {}).get("list", [])
    if not accounts:
        print("\nAucun compte retourne par l'API.")
        return

    account = accounts[0]
    print("\nResume portefeuille Bybit :")
    print(f"Type de compte : {account.get('accountType')}")
    print(f"Total equity : {account.get('totalEquity')}")
    print(f"Total wallet balance : {account.get('totalWalletBalance')}")

    coins = account.get("coin", [])
    non_zero_coins = []
    for coin in coins:
        equity = float(coin.get("equity", 0) or 0)
        if equity > 0:
            non_zero_coins.append(coin)

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


def list_trades() -> None:
    display_trades(get_all_trades())


def seed_test_trade() -> None:
    insert_trade(create_test_trade())
    print("\nTrade de test insere si absent.")


def test_private_api() -> None:
    print("\n=== Test API privee Bybit ===")
    display_wallet(get_wallet_balance())


def test_executions_api() -> None:
    print("\n=== Test recuperation executions Bybit ===")

    now_ms = int(time.time() * 1000)
    seven_days_ms = 7 * 24 * 60 * 60 * 1000
    start_ms = now_ms - seven_days_ms

    for category in ["linear", "spot", "inverse", "option"]:
        print(f"\n--- Test categorie : {category} ---")
        data = get_executions(
            category=category,
            limit=20,
            start_time=start_ms,
            end_time=now_ms,
        )

        print("Reponse brute API :")
        print(data)

        if data.get("retCode") != 0:
            print("Erreur API :", data.get("retMsg"))
            continue

        executions = data.get("result", {}).get("list", [])
        print(f"Nombre d'executions recues : {len(executions)}")

        if executions:
            print("Premiere execution :")
            print(executions[0])


def sync_bybit_trades() -> None:
    print("\n=== Synchronisation des trades Bybit ===")

    now_ms = int(time.time() * 1000)
    seven_days_ms = 7 * 24 * 60 * 60 * 1000
    start_ms = now_ms - seven_days_ms

    total_synced = 0
    for category in ["linear", "spot", "inverse", "option"]:
        print(f"\nSynchronisation categorie : {category}")
        synced = sync_executions_from_category(
            category=category,
            start_time=start_ms,
            end_time=now_ms,
            limit=50,
        )
        print(f"{synced} execution(s) traitee(s) pour {category}")
        total_synced += synced

    print(f"\nSynchronisation terminee. Total traite : {total_synced}")


def configure_api_env() -> None:
    config.ensure_env_file()

    print("\n=== Configuration API Bybit ===")
    print(f"Fichier .env : {config.ENV_PATH}")

    api_key = input("Entre BYBIT_API_KEY : ").strip()
    api_secret = input("Entre BYBIT_API_SECRET : ").strip()

    content = (
        f"BYBIT_API_KEY={api_key}\n"
        f"BYBIT_API_SECRET={api_secret}\n"
    )
    Path(config.ENV_PATH).write_text(content, encoding="utf-8")
    config.load_environment()

    print("\nConfiguration enregistree dans .env")
