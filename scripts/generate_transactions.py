# I wrote this to quickly create a realistic-ish transactions CSV for the small project.

import os
import pandas as pd
import random
import datetime

OUTPUT_DIR = os.path.join("data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

out_path = os.path.join(OUTPUT_DIR, "transactions_mock.csv")

users = [f"user_{i}" for i in range(1, 6)]

# Full ticker list (must match yfinance stock history)
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
           "JPM", "MS", "GS", "META", "NVDA"]

# Rough baseline prices to simulate realistic transactions
base_prices = {
    "AAPL": 170, "MSFT": 320, "GOOGL": 135,
    "AMZN": 140, "TSLA": 250, "JPM": 145,
    "MS": 90, "GS": 330, "META": 300, "NVDA": 450
}

transactions = []
for i in range(250):
    ticker = random.choice(tickers)

    # Simulate txn price around the base (±10%)
    txn_price = round(random.uniform(base_prices[ticker] * 0.9,
                                     base_prices[ticker] * 1.1), 2)

    # Quantity: small retail orders (1–50 shares)
    quantity = random.randint(1, 50)

    transactions.append({
        "transaction_id": i + 1,
        "user_id": random.choice(users),
        "ticker": ticker,
        "quantity": quantity,
        "txn_price": txn_price,
        "txn_type": random.choice(["BUY", "SELL"]),
        "txn_date": (datetime.datetime.now() -
                     datetime.timedelta(days=random.randint(0, 30))).date()
    })

df = pd.DataFrame(transactions)
df.to_csv(out_path, index=False)

print(f"✅ Wrote {len(df)} mock transactions to {out_path}")