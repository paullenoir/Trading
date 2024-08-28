PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                        FROM StrategyDataMM;

DROP TABLE StrategyDataMM;

CREATE TABLE StrategyDataMM (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date   TEXT,
    MM10   NUMERIC,
    MM15   NUMERIC,
    MM20   NUMERIC,
    MM25   NUMERIC,
    MM30   NUMERIC,
    MM35   NUMERIC,
    MM40   NUMERIC,
    MM45   NUMERIC,
    MM50   NUMERIC,
    MM55   NUMERIC,
    MM60   NUMERIC,
    MM65   NUMERIC,
    MM70   NUMERIC,
    MM75   NUMERIC,
    MM80   NUMERIC,
    MM85   NUMERIC,
    MM90   NUMERIC,
    MM95   NUMERIC,
    MM100  NUMERIC,
    MM200 NUMERIC
);

INSERT INTO StrategyDataMM (
                               id,
                               symbol,
                               date
                           )
                           SELECT id,
                                  symbol,
                                  date
                             FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
