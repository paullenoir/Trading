from trading_back_app_v2.models import *
import pandas_ta as ta #pip install pandas_ta
import pandas as pd

def calculate_indicators(market, interval):
    market_price_qs = MarketPrice.objects.filter(market=market, interval_time=interval).order_by('date')
    df = pd.DataFrame(list(market_price_qs.values()))
    # Ensure the 'close_price' column is in float format
    df['close_price'] = df['close_price'].astype(float)

    calculate_sma(df,market, interval)
    calculate_ema(df, market, interval)
    calculate_macd(df, market, interval)
    calculate_rsi(df, market, interval)
    calculate_bollingerband(df, market, interval)
    calculate_ichimoku(df, market, interval)
    calculate_stochastic(df, market, interval)

def calculate_sma(df, market, interval):
    for i in range(10, 205, 5):
        name = "MM" + str(i)
        df[name] = ta.sma(df['close_price'], length=i)
    
    for index, row in df.iterrows():
        row = df.loc[index]
        ema = {
            "market" : market,
            "interval_time" : interval,
            "date" :  pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "MM10" : row.get('MM10', None),
            "MM15" : row.get('MM15', None),
            "MM20" : row.get('MM20', None),
            "MM25" : row.get('MM25', None),
            "MM30" : row.get('MM30', None),
            "MM35" : row.get('MM35', None),
            "MM40" : row.get('MM40', None),
            "MM45" : row.get('MM45', None),
            "MM50" : row.get('MM50', None),
            "MM55" : row.get('MM55', None),
            "MM60" : row.get('MM60', None),
            "MM65" : row.get('MM65', None),
            "MM70" : row.get('MM70', None),
            "MM75" : row.get('MM75', None),
            "MM80" : row.get('MM80', None),
            "MM85" :  row.get('MM85', None),
            "MM90" : row.get('MM90', None),
            "MM95" : row.get('MM95', None),
            "MM100" : row.get('MM100', None),
            "MM200" : row.get('MM200', None)
        }
        
        IndicatorSMA.save_sma(ema)

def alogorythm_ema(df, column_name, period):
    # Ensure the column is in float format
    df[column_name] = df[column_name].astype(float)

    # Calculate SMMA
    smma = df[column_name].rolling(window=period, min_periods=1).mean()
    
    for i in range(period, len(df)):
        smma.iloc[i] = (smma.iloc[i-1] * (period - 1) + df[column_name].iloc[i]) / period
    
    return smma

def calculate_ema(df, market, interval):
    df['EMA20'] = alogorythm_ema(df, 'close_price', 20)
    df['EMA50'] = alogorythm_ema(df, 'close_price', 50)
    df['EMA200'] = alogorythm_ema(df, 'close_price', 200)

    for index, row in df.iterrows():
        row = df.loc[index]
        smma = {
            "market" : market,
            "interval_time" : interval,
            "date" :  pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "EMA20": row['EMA20'],
            "EMA50": row['EMA50'],
            "EMA200": row['EMA200']
        }

        IndicatorEMA.save_ema(smma)

def calculate_macd(df, market, interval):
    close_prices = df['close_price'].loc[:] 
    macd = ta.macd(close_prices, fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']  # Ligne MACD
    df['MACD_Signal'] = macd['MACDs_12_26_9']  # Ligne de signal
    df['MACD_Histogram'] = macd['MACDh_12_26_9']  # Histogramme
    for index, row in df.iterrows():
        macd = {
            "market" : market,
            "interval_time" : interval,
            "date" :  pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "macd": row.get('MACD', None),
            "macd_signal": row.get('MACD_Signal', None),
            "macd_histogram": row.get('MACD_Histogram', None)
        }

        IndicatorMACD.save_macd(macd)

def calculate_rsi(df, market, interval):
    # Calculate RSI with different periods
    df['RSI_7'] = ta.rsi(df['close_price'], timeperiod=7)
    df['RSI_14'] = ta.rsi(df['close_price'], timeperiod=14)
    df['RSI_21'] = ta.rsi(df['close_price'], timeperiod=21)

    # Loop through the DataFrame to save RSI values
    for index, row in df.iterrows():
        rsi = {
            "market": market,
            "interval_time": interval,
            "date": pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "rsi_7": row.get('RSI_7', None),
            "rsi_14": row.get('RSI_14', None),
            "rsi_21": row.get('RSI_21', None)
        }

        IndicatorRSI.save_rsi(rsi)

def calculate_bollingerband(df, market, interval):
    # Calculate Bollinger Bands
    bb = ta.bbands(df['close_price'], length=20, std=2.0, mamode='sma')
    df['BB_Lower'] = bb['BBL_20_2.0']  # Bande inférieure
    df['BB_Middle'] = bb['BBM_20_2.0']  # Bande moyenne (SMA 20)
    df['BB_Upper'] = bb['BBU_20_2.0']  # Bande supérieure
    df['BB_Bandwidth'] = bb['BBB_20_2.0']  # largeur de la bande de Bollinger (BBU - BBL) / BBM
    df['BB_Percent'] = bb['BBP_20_2.0']  # situe le prix actuel par rapport aux bandes (Close - BBL) / (BBU - BBL)

    for index, row in df.iterrows():
        bb_data = {
            "market": market,
            "interval_time": interval,
            "date": pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "BB_Lower": row.get('BB_Lower', None),
            "BB_Middle": row.get('BB_Middle', None),
            "BB_Upper": row.get('BB_Upper', None),
            "BB_Bandwidth": row.get('BB_Bandwidth', None),
            "BB_Percent": row.get('BB_Percent', None)
        }

        IndicatorBollingerBand.save_bollinger_band(bb_data)

def calculate_ichimoku(df, market, interval):
    # Calculate Ichimoku indicators
    ichimoku = ta.ichimoku(df['high_price'], df['low_price'], df['close_price'], tenkan=9, kijun=26, senkou=52)
    ichimoku_df = ichimoku[0] 
    df['Ichimoku_Conversion'] = ichimoku_df['ISA_9']  # Ligne de conversion (Tenkan-sen)
    df['Ichimoku_Base'] = ichimoku_df['ISB_26']  # Ligne de base (Kijun-sen)
    df['Ichimoku_LeadingA'] = ichimoku_df['ITS_9']  # Ligne Senkou A
    df['Ichimoku_LeadingB'] = ichimoku_df['IKS_26']  # Ligne Senkou B
    df['Ichimoku_Lagging'] = ichimoku_df['ICS_26']  # Ligne retardée (Chikou Span)

    for index, row in df.iterrows():
        ichimoku_data = {
            "market": market,
            "interval_time": interval,
            "date": pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "Ichimoku_Conversion": row.get('Ichimoku_Conversion', None),
            "Ichimoku_Base": row.get('Ichimoku_Base', None),
            "Ichimoku_LeadingA": row.get('Ichimoku_LeadingA', None),
            "Ichimoku_LeadingB": row.get('Ichimoku_LeadingB', None),
            "Ichimoku_Lagging": row.get('Ichimoku_Lagging', None)
        }

        IndicatorIchimoku.save_ichimoku(ichimoku_data)

def calculate_stochastic(df, market, interval):
    # Calculate Stochastic indicators
    stoch = ta.stoch(df['high_price'], df['low_price'], df['close_price'], fast_k=14, slow_k=3, slow_d=3)
    df['Stochastic_K'] = stoch['STOCHk_14_3_3']  # Ligne %K
    df['Stochastic_D'] = stoch['STOCHd_14_3_3']  # Ligne %D

    for index, row in df.iterrows():
        stoch_data = {
            "market": market,
            "interval_time": interval,
            "date": pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "stochastic_k": row.get('Stochastic_K', None),
            "stochastic_d": row.get('Stochastic_D', None)
        }

        IndicatorStochastic.save_stochastic(stoch_data)

