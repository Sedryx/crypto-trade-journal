import sqlite3

from app import (
    configure_api_env,
    initialize_application,
    list_trades,
    show_api_status,
    sync_bybit_trades,
)
from config import DB_PATH


def show_menu() -> None:
    print("\n=== Bybit Journal ===")
    print("1. Voir les trades")
    print("2. Synchroniser les trades Bybit")
    print("3. Configurer l'API Bybit (.env)")
    print("4. Quitter")


def run_cli() -> None:
    print("=== Demarrage de Bybit Journal ===")

    try:
        initialize_application()
        print(f"Application prete. Base SQLite : {DB_PATH}")
        show_api_status()

        while True:
            show_menu()
            choice = input("\nChoisis une option : ").strip()

            if choice == "1":
                list_trades()
            elif choice == "2":
                sync_bybit_trades()
            elif choice == "3":
                configure_api_env()
                show_api_status()
            elif choice == "4":
                print("\nFermeture du programme.")
                break
            else:
                print("\nOption invalide. Choisis un numero entre 1 et 4.")

    except sqlite3.DatabaseError as error:
        print("\nErreur SQLite :", error)
        print(f"Base concernee : {DB_PATH}")
    except Exception as error:
        print("\nErreur inattendue :", error)
