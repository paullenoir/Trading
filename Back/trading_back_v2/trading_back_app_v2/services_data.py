# Logique de traitement et d'interaction avec yfinance
import pandas as pd
import yfinance as yf
from .utils import validate_dataframe
from datetime import datetime, timedelta
from trading_back_app_v2.utils import *
from trading_back_app_v2.models import MarketPrice
from trading_back_app_v2.indicators import *
from trading_back_app_v2.strategies import execute_trading
import time

# python manage.py run_back "1h"

# Fonction pour télécharger les données depuis yfinance
def download_and_process_data(market: str, interval: str) -> pd.DataFrame:
    print(f"Téléchargement des données pour : {market} avec intervalle {interval}") # Utilise market.symbol ou tout autre champ du modèle Market       
    if interval == "1d":
        data = yf.download(market, period="max", interval=interval) # Téléchargement des données via yfinance pour chaque action
    else:
        end_date = datetime.today()  # Date actuelle
        start_date = end_date - timedelta(days=729)  # 729 jours avant aujourd'hui
        data = yf.download(market, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval=interval)

    # Valider le DataFrame
    data = validate_dataframe(data)
    # data = transform_dataframe(data)

    return data

# Fonction pour traiter les données du marché
def process_market_data(df: pd.DataFrame, market: str, interval: str):
    start_time = time.time()
    create_market_price(df, market, interval)
    print("  2.create_market_price  " + str((time.time() - start_time) / 60))

    start_time = time.time()
    calculate_indicators(market, interval)
    print("  2.calculate_indicators  " + str((time.time() - start_time) / 60))

    start_time = time.time()
    execute_trading(market, interval)
    print("  2.execute_trading  " + str((time.time() - start_time) / 60))

def create_market_price(data, market, interval):
    # Traitement des données de marché pour chaque symbole
    for index, row in data.iterrows():
        market_price = {
            'market': market,
            'interval': interval,
            'date': pd.Timestamp(index).strftime('%Y-%m-%d %H:%M:%S'),
            'low_price': row['Low'],
            'high_price': row['High'],
            'open_price': row['Open'],
            'close_price': row['Close'],
            'adj_close': row['Adj Close'],
            'volume': row['Volume']
        }

        MarketPrice.save_market_price(market_price)
