-- CreateTable.sql

-- Create trades_suspects table
CREATE TABLE IF NOT EXISTS trades_suspects (
    trade_id TEXT PRIMARY KEY,
    datetime TEXT,
    trader TEXT,
    isin TEXT,
    quantity INTEGER,
    notional REAL,
    trade_type TEXT,
    ccy TEXT,
    counterparty TEXT
);

-- Create portfolio_positions table
CREATE TABLE IF NOT EXISTS portfolio_positions (
    date TEXT,
    trader TEXT,
    symbol TEXT,
    ccy TEXT,
    total_quantity INTEGER,
    total_notional REAL,
    PRIMARY KEY (date, trader, symbol, ccy)
);
