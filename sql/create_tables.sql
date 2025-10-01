-- Fact table: transactions (this is the main fact for reporting)
CREATE TABLE IF NOT EXISTS fact_transactions (
  transaction_id SERIAL PRIMARY KEY,
  ticker VARCHAR(16) NOT NULL,
  txn_date DATE NOT NULL,
  txn_type VARCHAR(10) CHECK (txn_type IN ('BUY','SELL')),
  quantity INT CHECK (quantity > 0),
  txn_price NUMERIC(12,4) CHECK (txn_price > 0)
);

-- Dimension : ticker metadata
CREATE TABLE IF NOT EXISTS dim_tickers (
  ticker VARCHAR(16) PRIMARY KEY,
  company_name TEXT
);