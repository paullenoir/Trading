CREATE TABLE StrategySMMA (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol  TEXT,
    date    TEXT,
    close_price NUMERIC,
    SMMA20  NUMERIC,
    SMMA50  NUMERIC,
    SMMA200 NUMERIC
);