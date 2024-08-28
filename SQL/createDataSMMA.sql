WITH InitialData AS (
    SELECT
        symbol,
        date,
        close_price,
        ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date) AS row_num
    FROM
        MarketPrices
),
WITH InitialSMA AS (
    SELECT
        symbol,
        date,
        close_price,
        -- Conversion de la date en format ISO pour faciliter le tri
        strftime('%Y-%m-%d', substr(date, 8, 4) || '-' || substr(date, 1, 3) || '-' || substr(date, 5, 2)) AS converted_date,
        
        -- Calcul des SMA initiales pour les périodes de 20, 50 et 100 jours
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY strftime('%Y-%m-%d', substr(date, 8, 4) || '-' || substr(date, 1, 3) || '-' || substr(date, 5, 2))) >= 20 THEN
                AVG(close_price) OVER (PARTITION BY symbol ORDER BY strftime('%Y-%m-%d', substr(date, 8, 4) || '-' || substr(date, 1, 3) || '-' || substr(date, 5, 2)) ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS SMA20,
        
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY strftime('%Y-%m-%d', substr(date, 8, 4) || '-' || substr(date, 1, 3) || '-' || substr(date, 5, 2))) >= 50 THEN
                AVG(close_price) OVER (PARTITION BY symbol ORDER BY strftime('%Y-%m-%d', substr(date, 8, 4) || '-' || substr(date, 1, 3) || '-' || substr(date, 5, 2)) ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS SMA50,
        
        CASE
            WHEN ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY strftime('%Y-%m-%d', substr(date, 8, 4) || '-' || substr(date, 1, 3) || '-' || substr(date, 5, 2))) >= 100 THEN
                AVG(close_price) OVER (PARTITION BY symbol ORDER BY strftime('%Y-%m-%d', substr(date, 8, 4) || '-' || substr(date, 1, 3) || '-' || substr(date, 5, 2)) ROWS BETWEEN 99 PRECEDING AND CURRENT ROW)
            ELSE NULL
        END AS SMA100
    FROM
        MarketPrices
),
SMMA_Calculation AS (
    SELECT
        symbol,
        date,
        close_price,
        row_num,
        -- Calcul de la SMMA en utilisant la première valeur comme SMA
        CASE
            WHEN row_num = 20 THEN SMA20
            WHEN row_num > 20 THEN (LAG(SMMA20) OVER (PARTITION BY symbol ORDER BY row_num) * 19 + close_price) / 20
            ELSE NULL
        END AS SMMA20,
        
        CASE
            WHEN row_num = 50 THEN SMA50
            WHEN row_num > 50 THEN (LAG(SMMA50) OVER (PARTITION BY symbol ORDER BY row_num) * 49 + close_price) / 50
            ELSE NULL
        END AS SMMA50,
        
        CASE
            WHEN row_num = 100 THEN SMA100
            WHEN row_num > 100 THEN (LAG(SMMA100) OVER (PARTITION BY symbol ORDER BY row_num) * 99 + close_price) / 100
            ELSE NULL
        END AS SMMA100
    FROM
        InitialSMA
)