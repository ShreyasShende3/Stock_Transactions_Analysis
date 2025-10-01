# I use yfinance because it doesn't require an API key

import os
import yfinance as yf
import pandas as pd
import time

# Directory to save stock data
OUTPUT_DIR = os.path.join("data", "stocks")
os.makedirs(OUTPUT_DIR, exist_ok=True)

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "MS", "GS", "META", "NVDA"]

print(f"📡 Fetching stock data for {len(tickers)} tickers...")

for ticker in tickers:
    try:
        print(f"🔎 Fetching: {ticker}")
        df = yf.download(
            ticker,
            period="1mo",
            interval="1d"
        )

        if df.empty:
            print(f"⚠️ {ticker}: No data returned, skipping.")
            continue

        df.reset_index(inplace=True)

        out_path = os.path.join(OUTPUT_DIR, f"{ticker}_prices.csv")
        df.to_csv(out_path, index=False)
        print(f"✅ Saved {ticker} data to {out_path}")

        time.sleep(2)

    except Exception as e:
        print(f"❌ Failed to fetch {ticker}: {e}")
