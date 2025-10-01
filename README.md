# Stock Transactions Data Pipeline & Power BI Dashboard

This project simulates retail stock trading transactions, loads them into a PostgreSQL database, enriches them with real market prices from Yahoo Finance, and visualizes insights in Power BI.

---

## 📂 Project Structure
```

data/
├── transactions_mock.csv         # Generated mock transactions
└── stocks/                       # Daily stock price history per ticker
├── AAPL_prices.csv
├── MSFT_prices.csv
└── ...
scripts/
├── 01_generate_transactions.py   # Creates random mock transactions
├── 02_fetch_stock_data.py        # Downloads stock price history (yfinance)
├── 03_load_to_postgres.py        # Loads transactions & tickers into PostgreSQL
powerbi/
└── schema.png                    # Data model screenshot

````

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/ShreyasShende3/stock-transactions-pipeline.git
cd stock-transactions-pipeline
````

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a `.env` file in the root directory:

```
DB_NAME=financedb
DB_USER=finance_user
DB_PASSWORD=finance_pass
DB_HOST=127.0.0.1
DB_PORT=5432
```

Make sure PostgreSQL is running and the schema is created.

---

## 🚀 Running the Pipeline

### 1. Generate Mock Transactions

```bash
python scripts/generate_transactions.py
```

### 2. Fetch Stock Data

```bash
python scripts/extract_stocks.py
```

### 3. Load Data into PostgreSQL

```bash
python scripts/load_transactions.py
```

---

## 📊 Power BI Dashboard

The **data model** integrates:

* **Transactions** → User trades (BUY/SELL, price, quantity)
* **Stocks** → Market prices (open, close, daily return)
* **Dim Tickers** → Company reference table
* **Roles** → Role-based access (for BI permissions)

---

## 🛠️ Tech Stack

* **Python** (pandas, yfinance, psycopg2)
* **PostgreSQL** (data storage)
* **Power BI** (analytics & reporting)
