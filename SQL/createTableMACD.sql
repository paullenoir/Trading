PRAGMA foreign_keys = 0;

CREATE TABLE StrategyDataMACD (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date   TEXT,
    MACD REAL NOT NULL,
    MACD_signal REAL NOT NULL,
    close_price NUMERIC
);

PRAGMA foreign_keys = 1;