# Load in the transactions and the ticker info into the tables and do some data quality and integrity checks.

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "financedb")
DB_USER = os.getenv("DB_USER", "finance_user")
DB_PASS = os.getenv("DB_PASSWORD", "finance_pass")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")

CSV_PATH = os.path.join("data", "transactions_mock.csv")

# Ticker → Company mapping
TICKER_MAP = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com, Inc.",
    "TSLA": "Tesla, Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "MS": "Morgan Stanley",
    "GS": "Goldman Sachs Group, Inc.",
    "META": "Meta Platforms, Inc.",
    "NVDA": "NVIDIA Corporation"
}


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Sanity checks before loading."""
    df = df.drop_duplicates(subset=["transaction_id"])
    df = df[df["txn_price"] > 0]
    df = df[df["txn_type"].isin(["BUY", "SELL"])]
    df = df[df["quantity"] > 0]
    # Ensure txn_date is proper datetime
    df["txn_date"] = pd.to_datetime(df["txn_date"]).dt.date
    return df


def load_dim_tickers(df: pd.DataFrame, conn):
    """Insert unique tickers into dim_tickers table."""
    tickers_df = df[["ticker"]].drop_duplicates()
    cur = conn.cursor()
    insert_query = """
        INSERT INTO dim_tickers (ticker, company_name)
        VALUES %s
        ON CONFLICT (ticker) DO NOTHING;
    """
    values = [(row["ticker"], TICKER_MAP.get(row["ticker"], row["ticker"]))
              for _, row in tickers_df.iterrows()]

    execute_values(cur, insert_query, values)
    conn.commit()
    cur.close()
    print(f"✅ Loaded {len(values)} tickers into dim_tickers.")


def load_fact_transactions(df: pd.DataFrame, conn):
    """Insert validated transactions into fact_transactions."""
    cur = conn.cursor()
    insert_query = """
        INSERT INTO fact_transactions (transaction_id, ticker, txn_date, txn_type, quantity, txn_price)
        VALUES %s
        ON CONFLICT (transaction_id) DO NOTHING;
    """
    df_to_load = df[["transaction_id", "ticker", "txn_date", "txn_type", "quantity", "txn_price"]].copy()

    # Convert to native Python types
    df_to_load["transaction_id"] = df_to_load["transaction_id"].apply(int)
    df_to_load["quantity"] = df_to_load["quantity"].apply(int)
    df_to_load["txn_price"] = df_to_load["txn_price"].apply(float)
    df_to_load["txn_date"] = df_to_load["txn_date"].apply(lambda x: pd.Timestamp(x).date())
    df_to_load["ticker"] = df_to_load["ticker"].astype(str)
    df_to_load["txn_type"] = df_to_load["txn_type"].astype(str)

    values = [tuple(x) for x in df_to_load.to_numpy()]

    execute_values(cur, insert_query, values)
    conn.commit()
    cur.close()
    print(f"✅ Loaded {len(values)} transactions into fact_transactions.")


if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"❌ CSV not found at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print(f"📂 Read {len(df)} rows from {CSV_PATH}")

    validated_df = validate_data(df)
    print(f"🔍 After validation: {len(validated_df)} rows remain")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

    load_dim_tickers(validated_df, conn)
    load_fact_transactions(validated_df, conn)

    conn.close()
    print("🎉 All data loaded successfully!")

