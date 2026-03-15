# Bybit Trade Journal

Bybit Trade Journal is a local desktop application used to sync Bybit executions, store them in SQLite, analyze journal statistics, and export trades to Excel.

The application is built around:

- a modular Python backend
- a PyWebView desktop shell
- a local HTML / CSS / JavaScript frontend
- Windows packaging assets for PyInstaller and Inno Setup

## Current Features

- automatic creation of local working directories
- automatic creation of the user `.env` file
- user config stored in a Windows-friendly folder
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
- storage helpers to open config, data, and export folders
- sync preferences for startup auto-sync and default sync days
- SQLite backup and restore helpers
- development tools hidden outside dev mode
- PyInstaller build spec for Windows
- WebView2 prerequisite check
- Inno Setup installer script

## Project Structure

```text
crypto-trade-journal/
|-- README.md
|-- requirements.txt
|-- ETAPE_FUTUR.md
`-- bybit_journal/
    |-- desktop/
    |   |-- bridge.py
    |   |-- main.py
    |   |-- prerequisites.py
    |   `-- window.py
    |-- frontend/
    |   |-- app.js
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
|-- packaging/
|   |-- build_windows.ps1
|   |-- check_webview2.ps1
|   |-- pyinstaller.spec
|   `-- installer/
|       `-- BybitTradeJournal.iss
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

If you are using the project's virtual environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

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

The desktop application now uses:

- config: `%APPDATA%/BybitTradeJournal/config/.env`
- SQLite database: `%APPDATA%/BybitTradeJournal/data/journal.db`
- log file: `%APPDATA%/BybitTradeJournal/data/log`
- exports: `%USERPROFILE%/Documents/BybitTradeJournal/exports/`

If an older project-root `.env`, a project-local `bybit_journal/data/journal.db`, a local log file, or old export files already exist, the app copies them to the active user folders automatically.

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
- legacy `.env`, SQLite, log, and export files are migrated if needed
- the frontend loads the dashboard, trades, and statistics
- if the Bybit API is configured, an automatic synchronization starts after 1 second

## UX Notes

- the packaged app is intended to use `%APPDATA%` and `%Documents%` as the real runtime storage
- deletion from the trades table requires confirmation
- the settings screen can open the active config, data, and export folders
- the `DEV TEST ONLY` action is shown only in dev mode

## Windows Build

Build the application with PyInstaller:

```powershell
powershell -ExecutionPolicy Bypass -File .\packaging\build_windows.ps1
```

This produces a first Windows build in:

```text
dist/BybitTradeJournal/
```

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

## Windows Installer

An Inno Setup installer script is provided in:

```text
packaging/installer/BybitTradeJournal.iss
```

Expected flow:

1. build the app with PyInstaller
2. open the `.iss` file in Inno Setup
3. compile the installer

The generated installer is configured to:

- install the packaged desktop app into `Program Files`
- create Start Menu and Desktop shortcuts
- keep user data outside the install folder
- warn when WebView2 is missing before first launch

## Tests

Run the test suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s bybit_journal/tests -p "test_*.py" -v
```

Check compilation:

```powershell
.\.venv\Scripts\python.exe -m compileall bybit_journal/src bybit_journal/tests bybit_journal/desktop
```

## Current Limitations

- the application is currently focused on local Windows desktop usage
- the Inno Setup installer script is ready, but the installer must still be compiled on a machine with Inno Setup installed
- the `DEV TEST ONLY` button is still present for development convenience

## Note

This is a personal trading journal project for organizational and educational use.
It is not affiliated with Bybit.
