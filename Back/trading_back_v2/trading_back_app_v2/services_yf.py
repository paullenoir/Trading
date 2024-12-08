import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from trading_back_app_v2.models import MarketPrice

# Télécharger les données depuis api de yfinance
def download_and_process_data(market: str, interval: str) -> pd.DataFrame:
    print(f"Téléchargement des données pour : {market} avec intervalle {interval}")       
    if interval == "1d":
        data = yf.download(market, period="max", interval=interval) # Téléchargement des données via yfinance pour chaque action
        data = validate_dataframe(data)
    else:
        end_date = datetime.today()  # Date actuelle
        start_date = end_date - timedelta(days=729)  # 729 jours avant aujourd'hui
        data = yf.download(market, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval=interval)
        data = validate_dataframe(data)

    return data


# Fonction pour valider le DataFrame reçu
def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Vérification et correction des valeurs manquantes
    missing_values = df.isnull().sum()
    if missing_values.any():
        # Remplacer les valeurs manquantes par la valeur précédente
        df.fillna(method='ffill', inplace=True)
        print("Valeurs manquantes corrigées avec la valeur précédente.")
    
    # Vérification et correction des doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        # Supprimer les doublons
        df.drop_duplicates(inplace=True)
        print("Doublons supprimés.")

    return df

def create_market_price(data, market, interval):
    # Traitement des données de marché pour chaque symbole
    for index, row in data.iterrows():
        market_price = {
            'market': market,
            'interval': interval,
            'date': pd.Timestamp(index).strftime('%Y-%m-%d %H:%M:%S'),
            'low_price': round(row['Low'], 4),
            'high_price': round(row['High'], 4),
            'open_price': round(row['Open'], 4),
            'close_price': round(row['Close'], 4),
            'adj_close': round(row['Adj Close'], 4),
            'volume': row['Volume']
        }

        MarketPrice.save_market_price(market_price)