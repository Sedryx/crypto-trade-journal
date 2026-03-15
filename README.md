# Bybit Trade Journal

Desktop trading journal for Bybit with local sync, SQLite storage, statistics, Excel export, and a Windows desktop UI built with Python and PyWebView.

## Important If You Download the project !

When you download the packaged application as a `.zip` and it does not start correctly on Windows, follow these steps before reporting an app bug:

1. Delete the extracted folder.
2. Right-click the `.zip` file, open `Properties`, and click `Unblock` if that option is available.
3. Extract the `.zip` again.
4. If needed, open PowerShell and run:

```powershell
Get-ChildItem "D:\BybitTradeJournal" -Recurse | Unblock-File
```

5. Launch `BybitTradeJournal.exe` again.
6. Also make sure Microsoft Edge WebView2 is installed.



## Stack

The application is built around:

- a modular Python backend
- a PyWebView desktop shell
- a local HTML / CSS / JavaScript frontend
- Windows packaging assets for PyInstaller and Inno Setup

## Release Snapshot

- Windows desktop application
- local SQLite journal
- Bybit sync with startup auto-sync support
- wallet overview and recent PnL chart
- trade notes and screenshot path fields
- Excel export
- backup / restore tools
- PyInstaller build

## Current Features

- automatic creation of local working directories
- automatic creation of the user `.env` file
- loading of Bybit API credentials
- SQLite database initialization
- paginated Bybit synchronization by category
- automatic synchronization at application startup
- duplicate prevention through unique `bybit_trade_id`
- dashboard with account and wallet summary
- display of `Total equity`, stablecoins, and other assets
- wallet display currency switcher (`USD`, `JPY`, `GBP`, `CHF`, `EUR`)
- filtered trade list
- trade detail panel with note and screenshot path editing
- basic trading statistics
- chart view based on recent trade PnL
- Excel export for filtered trades
- storage helpers to open config, data, export, and backup folders
- sync preferences for startup auto-sync and default sync days
- SQLite backup and restore helpers
- PyInstaller build spec for Windows
- WebView2 prerequisite check
- Windows zip distribution

## Project Structure

```text
crypto-trade-journal/
|-- README.md
|-- requirements.txt
|-- packaging/
|   |-- build_windows.ps1
|   |-- check_webview2.ps1
|   |-- pyinstaller.spec
|   `-- installer/
|       `-- BybitTradeJournal.iss
`-- bybit_journal/
    |-- data/
    |-- desktop/
    |   |-- bridge.py
    |   |-- main.py
    |   |-- prerequisites.py
    |   `-- window.py
    |-- frontend/
    |   |-- app.js
    |   |-- asset/
    |   |-- index.html
    |   `-- styles.css
    |-- src/
    |   |-- api.py
    |   |-- config.py
    |   |-- db.py
    |   |-- models.py
    |   |-- sync.py
    |   `-- services/
    |       |-- __init__.py
    |       `-- journal_service.py
    `-- tests/
        `-- test_core.py
```

## Requirements

- Python 3.13 recommended
- a Bybit API key with read access
- an internet connection for API calls

## Installation

From the project root:

```powershell
python -m pip install -r requirements.txt
```

If you are using the project virtual environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For Windows builds, `Pillow` is required so PyInstaller can process the application icon correctly. It is already included in `requirements.txt`.

## Configuration

On first launch, the application automatically creates a user `.env` file in:

```text
%APPDATA%/BybitTradeJournal/config/.env
```

with:

```env
BYBIT_API_KEY=
BYBIT_API_SECRET=
```

You can then fill in your credentials from the `Configuration` screen inside the application.

## User Storage

The packaged desktop application is intended to use:

- config: `%APPDATA%/BybitTradeJournal/config/.env`
- SQLite database: `%APPDATA%/BybitTradeJournal/data/journal.db`
- log file: `%APPDATA%/BybitTradeJournal/data/log`
- exports: `%USERPROFILE%/Documents/BybitTradeJournal/exports/`
- backups: `%USERPROFILE%/Documents/BybitTradeJournal/backups/`

The repository may still contain local development data under [`bybit_journal/data`](c:/Users/joach/OneDrive%20-%20EDUETATFR/Documents/Moi/crypto-trade-journal/bybit_journal/data), but the release build is intended to rely on the Windows user folders above.

## Launch

The desktop entrypoint is:

```text
bybit_journal/desktop/main.py
```

Run:

```powershell
python bybit_journal/desktop/main.py
```

## Main Screens

- `Dashboard`: API status, wallet, account summary, and recent trades
- `Trades`: filters, SQLite trade table, trade detail panel, notes, and Excel export
- `Synchronization`: Bybit import plus sync preferences
- `Statistics`: PnL, win rate, indicators, and a recent PnL chart
- `Configuration`: `.env` management, storage shortcuts, and backup tools

## Excel Export

The Excel export uses the current filters from the `Trades` view and creates a `.xlsx` file in:

```text
%USERPROFILE%/Documents/BybitTradeJournal/exports/
```

The file contains:

- a `Trades` worksheet
- a `Stats` worksheet

## Startup Behavior

At launch:

- the Python backend initializes folders, the `.env`, and SQLite
- the frontend loads the dashboard, trades, and statistics
- if the Bybit API is configured and auto-sync is enabled, synchronization starts automatically shortly after the window opens

## Windows Build

Build the application with PyInstaller:

```powershell
powershell -ExecutionPolicy Bypass -File .\packaging\build_windows.ps1
```

If you want a clean rebuild:

```powershell
powershell -ExecutionPolicy Bypass -File .\packaging\build_windows.ps1 -Clean
```

This produces a Windows build in:

```text
dist/BybitTradeJournal/
```

The packaged executable is:

```text
dist/BybitTradeJournal/BybitTradeJournal.exe
```

The build script expects:

- the project virtual environment in `.venv`
- `PyInstaller` installed in that virtual environment
- `Pillow` installed in that virtual environment for icon processing

## Windows Prerequisite

PyWebView relies on Microsoft Edge WebView2 on Windows.

Check it manually with:

```powershell
.\packaging\check_webview2.ps1
```

If WebView2 is missing, install it from:

```text
https://go.microsoft.com/fwlink/p/?LinkId=2124703
```

## Planned For V1

- installer-based Windows distribution instead of a raw zip
- a smoother first-run flow for prerequisites like WebView2
- less friction around downloaded file blocking on Windows

## Tests

Run the test suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s bybit_journal/tests -p "test_*.py" -v
```

Check compilation:

```powershell
.\.venv\Scripts\python.exe -m compileall bybit_journal/src bybit_journal/tests bybit_journal/desktop
```

## GitHub Release Notes

For a clean GitHub release:

- share the packaged `dist/BybitTradeJournal/` folder or an installer
- current public sharing flow is still zip-based
- do not commit `.venv`, local `.env`, runtime databases, logs, exports, or dev notes
- do not share your personal Bybit API keys or your local journal database

## Current Limitations

- the application is currently focused on local Windows desktop usage
- distribution is still zip-based for now
- unsigned builds can still trigger SmartScreen or download blocking on some Windows machines

## Note

This is a personal trading journal project for organizational and educational use. It is not affiliated with Bybit.
