WITH MarketPricesWithMA AS (
    SELECT
        mp.id,
        mp.symbol,
        mp.date,
        mp.close_price,
        -- Conversion de la date en format ISO pour faciliter le tri
        strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) AS converted_date,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 10 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 9 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM10,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 15 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 14 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM15,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 20 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM20,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 25 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 24 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM25,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 30 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM30,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 35 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 34 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM35,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 40 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 39 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM40,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 45 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 44 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM45,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 50 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM50,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 55 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 54 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM55,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 60 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 59 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM60,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 65 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 64 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM65,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 70 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 69 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM70,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 75 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 74 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM75,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 80 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 79 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM80,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 85 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 84 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM85,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 90 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 89 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM90,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 95 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 94 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM95,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 100 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 99 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM100,
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2))) >= 200 THEN
                AVG(mp.close_price) OVER (PARTITION BY mp.symbol ORDER BY strftime('%Y-%m-%d', substr(mp.date, 8, 4) || '-' || substr(mp.date, 1, 3) || '-' || substr(mp.date, 5, 2)) ROWS BETWEEN 199 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS MM200
    FROM
        MarketPrices mp
)
INSERT OR REPLACE INTO StrategyDataMM (
    id,
    symbol,
    date,
    close_price,
    MM10,
    MM15,
    MM20,
    MM25,
    MM30,
    MM35,
    MM40,
    MM45,
    MM50,
    MM55,
    MM60,
    MM65,
    MM70,
    MM75,
    MM80,
    MM85,
    MM90,
    MM95,
    MM100,
    MM200
)
SELECT
    id,
    symbol,
    date,
    close_price,
    MM10,
    MM15,
    MM20,
    MM25,
    MM30,
    MM35,
    MM40,
    MM45,
    MM50,
    MM55,
    MM60,
    MM65,
    MM70,
    MM75,
    MM80,
    MM85,
    MM90,
    MM95,
    MM100,
    MM200
FROM
    MarketPricesWithMA;
