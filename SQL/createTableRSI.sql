PRAGMA foreign_keys = 0;

CREATE TABLE StrategyDataRSI (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date   TEXT,
    RSI  NUMERIC,
    close_price NUMERIC
);

PRAGMA foreign_keys = 1;