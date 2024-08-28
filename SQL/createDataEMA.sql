WITH MarketPricesWithEMA AS (
    SELECT
        mp.id,
        mp.symbol,
        mp.date,
        mp.close_price,
        -- Calcul de l'EMA10
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 10 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 10 THEN
                (2.0 / (10 + 1)) * mp.close_price + (1 - (2.0 / (10 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA10,
        -- Calcul de l'EMA15
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 15 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 14 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 15 THEN
                (2.0 / (15 + 1)) * mp.close_price + (1 - (2.0 / (15 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA15,
        -- Calcul de l'EMA20
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 20 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 20 THEN
                (2.0 / (20 + 1)) * mp.close_price + (1 - (2.0 / (20 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA20,
        -- Calcul de l'EMA25
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 25 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 24 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 25 THEN
                (2.0 / (25 + 1)) * mp.close_price + (1 - (2.0 / (25 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA25,
        -- Calcul de l'EMA30
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 30 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 30 THEN
                (2.0 / (30 + 1)) * mp.close_price + (1 - (2.0 / (30 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA30,
        -- Calcul de l'EMA35
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 35 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 34 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 35 THEN
                (2.0 / (35 + 1)) * mp.close_price + (1 - (2.0 / (35 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA35,
        -- Calcul de l'EMA40
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 40 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 39 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 40 THEN
                (2.0 / (40 + 1)) * mp.close_price + (1 - (2.0 / (40 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA40,
        -- Calcul de l'EMA45
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 45 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 44 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 45 THEN
                (2.0 / (45 + 1)) * mp.close_price + (1 - (2.0 / (45 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA45,
        -- Calcul de l'EMA50
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 50 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 50 THEN
                (2.0 / (50 + 1)) * mp.close_price + (1 - (2.0 / (50 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA50,
        -- Calcul de l'EMA55
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 55 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 54 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 55 THEN
                (2.0 / (55 + 1)) * mp.close_price + (1 - (2.0 / (55 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA55,
        -- Calcul de l'EMA60
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 60 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 60 THEN
                (2.0 / (60 + 1)) * mp.close_price + (1 - (2.0 / (60 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA60,
        -- Calcul de l'EMA65
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 65 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 64 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 65 THEN
                (2.0 / (65 + 1)) * mp.close_price + (1 - (2.0 / (65 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA65,
        -- Calcul de l'EMA70
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 70 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 69 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 70 THEN
                (2.0 / (70 + 1)) * mp.close_price + (1 - (2.0 / (70 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA70,
        -- Calcul de l'EMA75
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 75 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 74 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 75 THEN
                (2.0 / (75 + 1)) * mp.close_price + (1 - (2.0 / (75 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA75,
        -- Calcul de l'EMA80
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 80 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 79 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 80 THEN
                (2.0 / (80 + 1)) * mp.close_price + (1 - (2.0 / (80 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA80,
        -- Calcul de l'EMA85
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 85 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 84 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 85 THEN
                (2.0 / (85 + 1)) * mp.close_price + (1 - (2.0 / (85 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA85,
        -- Calcul de l'EMA90
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 90 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 89 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 90 THEN
                (2.0 / (90 + 1)) * mp.close_price + (1 - (2.0 / (90 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA90,
        -- Calcul de l'EMA95
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 95 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 94 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 95 THEN
                (2.0 / (95 + 1)) * mp.close_price + (1 - (2.0 / (95 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA95,
        -- Calcul de l'EMA100
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) = 100 THEN AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY mp.date ROWS BETWEEN 99 PRECEDING AND CURRENT ROW)
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY mp.date) > 100 THEN
                (2.0 / (100 + 1)) * mp.close_price + (1 - (2.0 / (100 + 1))) * LAG(mp.close_price, 1) OVER (PARTITION BY mp.symbol ORDER BY mp.date)
            ELSE NULL
        END AS EMA100
    FROM
        MarketPrices mp
)
INSERT OR REPLACE INTO StrategyDataEMA (
    id,
    symbol,
    date,
    close_price,
    EMA10,
    EMA15,
    EMA20,
    EMA25,
    EMA30,
    EMA35,
    EMA40,
    EMA45,
    EMA50,
    EMA55,
    EMA60,
    EMA65,
    EMA70,
    EMA75,
    EMA80,
    EMA85,
    EMA90,
    EMA95,
    EMA100
)
SELECT
    id,
    symbol,
    date,
    close_price,
    EMA10,
    EMA15,
    EMA20,
    EMA25,
    EMA30,
    EMA35,
    EMA40,
    EMA45,
    EMA50,
    EMA55,
    EMA60,
    EMA65,
    EMA70,
    EMA75,
    EMA80,
    EMA85,
    EMA90,
    EMA95,
    EMA100
FROM
    MarketPricesWithEMA;
