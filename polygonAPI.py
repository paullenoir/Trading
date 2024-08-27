import requests
import pandas as pd
from datetime import datetime

api_key = 'UDMm7_iFVCsWXpdyKizsKD575gDQAv5o'

######################################
## Liste des stocks dans polygon.io ##
######################################
def get_full_market_list():
    # URL de l'endpoint pour obtenir la liste des tickers
    url = 'https://api.polygon.io/v3/reference/tickers'

    # Paramètres de la requête
    params = {
        'market': 'stocks',
        'active': 'true',
        'apiKey': api_key,
        'limit': 1000
    }

    tickers_list = []

    while url:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            tickers_list.extend(data['results'])
            url = data.get('next_url')
        else:
            print(f'Erreur: {response.status_code}')
            break

    df = pd.DataFrame(tickers_list)

    # print(df)
    return df

def get_daily_market_data(symbol:str, from_date: str, to_date: str, interval_time: str):
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{from_date}/{to_date}'
    params = {
        'adjusted': 'true',
        'apiKey': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            market_data = []
            for result in data['results']:
                day_data = {
                    'date': datetime.fromtimestamp(result['t'] / 1000).strftime('%Y-%m-%d'),
                    'low_price': result['l'],
                    'high_price': result['h'],
                    'open_price': result['o'],
                    'close_price': result['c']
                }
                market_data.append(day_data)
            df = pd.DataFrame(market_data)
            df = df.set_index("date")
            return df
        else:
            print("No results found")
    else:
        print(f"Error: {response.status_code}")
    return None
