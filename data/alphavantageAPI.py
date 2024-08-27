import requests
import pandas as pd

api_key_symbol = 'OTDEESQFRM1HERGL' #25 call/jour
api_key_rsi = 'DA5UZ6XTPPO8IIL4' #25 call/jour
api_key_macd = '2FXHOQWJ7VIXQESN' #25 call/jour
symbol = ["NVDA","PG","AMZN","JNJ","AAPL","MSFT","NFLX","EBIT"] #8
no_symbol = ["BRK","MCDS","COLA","VFV"] #4

# Exemple de récupération des données quotidiennes
def fetch_daily_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key_symbol}&outputsize=full"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            market_data = []
            # Itérer à travers les données quotidiennes
            for date, values in data["Time Series (Daily)"].items():
                day_data = {
                    'date': date,
                    'low_price': values['3. low'],
                    'high_price': values['2. high'],
                    'open_price': values['1. open'],
                    'close_price': values['4. close']
                }
                market_data.append(day_data)
            df = pd.DataFrame(market_data)
            df = df.set_index("date")
            df = df.sort_index(ascending=True)  # ascending=True pour trier en ordre croissant
            return df
    else:
        print(f"Error: {response.status_code}")
    return None

# Exemple de récupération du RSI
def fetch_rsi(symbol, time_period=14):
    url = f"https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval=daily&time_period={time_period}&series_type=close&apikey={api_key_rsi}"
    response = requests.get(url)
    data = response.json()
    return data

# Exemple de récupération du MACD
def fetch_macd(symbol):
    url = f"https://www.alphavantage.co/query?function=MACDEXT&symbol={symbol}&interval=daily&series_type=close&apikey={api_key_macd}"
    response = requests.get(url)
    data = response.json()
    return data
