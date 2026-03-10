# TradeJournal

TradeJournal is a CLI application that imports trades from the Bybit API, stores them in a local SQLite database, and exports them to Excel for easy trading analysis.

The goal of this project is to provide a simple trading journal that automatically collects trades and allows users to review their performance.

---

# Features

- Import trades from the Bybit API
- Store trades locally using SQLite
- Prevent duplicate trades
- Export trades to Excel (.xlsx)
- Add personal notes to trades
- Attach screenshots to trades
- Simple CLI interface
- Works on Linux, macOS, and Windows

---

# Project Structure

```
bybit-trade-journal/
│
├── main.py
├── config.py
├── api.py
├── db.py
├── export_excel.py
├── utils.py
│
├── data/
│   └── journal.db
│
├── exports/
│   └── trades.xlsx
│
├── screenshots/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# Requirements

- Python 3.10+
- Bybit API key
- Internet connection

Python libraries:

- requests
- python-dotenv
- openpyxl

---

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/bybit-trade-journal.git
cd bybit-trade-journal
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

Example:

```
BYBIT_API_KEY=your_api_key
BYBIT_API_SECRET=your_api_secret
BYBIT_BASE_URL=https://api.bybit.com
```

Make sure your API key has permission to read trades.

---

# Usage

Initialize the database:

```bash
python main.py init-db
```

Sync trades from Bybit:

```bash
python main.py sync
```

List stored trades:

```bash
python main.py list
```

Export trades to Excel:

```bash
python main.py export
```

Add a note to a trade:

```bash
python main.py add-note --id 1 --note "Late entry"
```

Attach a screenshot:

```bash
python main.py add-screenshot --id 1 --path screenshots/trade1.png
```

---

# Database

Trades are stored locally in SQLite:

```
data/journal.db
```

Main table:

```
trades
```

Fields include:

- trade id
- symbol
- side
- quantity
- entry price
- exit price
- take profit
- stop loss
- leverage
- pnl
- notes
- screenshot path

---

# Export

Trades can be exported to Excel:

```
exports/trades.xlsx
```

This file can be opened in:

- Microsoft Excel
- LibreOffice
- Google Sheets

---

# Future Improvements

Possible future features:

- statistics dashboard
- win rate calculation
- risk/reward analysis
- automatic chart screenshots
- simple web interface
- Docker deployment

---

# License

This project is open source and available under the MIT License.

---

# Disclaimer

This tool is for educational and personal trading journal purposes only.  
It is not affiliated with Bybit.
