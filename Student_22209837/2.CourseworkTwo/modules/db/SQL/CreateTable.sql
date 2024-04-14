
-- create trades table
CREATE TABLE IF NOT EXISTS trades (
    _id TEXT PRIMARY KEY,
    DateTime TEXT,
    TradeId TEXT,
    Trader TEXT,
    Symbol TEXT,
    Quantity INTEGER,
    Notional REAL,
    TradeType TEXT,
    Ccy TEXT,
    Counterparty TEXT
);

-- create portfolio_positions table
CREATE TABLE IF NOT EXISTS portfolio_positions (
    date TEXT,
    trader TEXT,
    symbol TEXT,
    ccy TEXT,
    total_quantity INTEGER,
    total_notional REAL,
    num_trades INTEGER
);

-- create trades_suspects table
CREATE TABLE IF NOT EXISTS trades_suspects (
    _id TEXT PRIMARY KEY,
    DateTime TEXT,
    TradeId TEXT,
    Trader TEXT,
    Symbol TEXT,
    Quantity INTEGER,
    Notional REAL,
    TradeType TEXT,
    Ccy TEXT,
    Counterparty TEXT
);

