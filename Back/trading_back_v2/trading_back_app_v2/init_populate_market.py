from trading_back_v2.trading_back_app_v2.models import Market # type: ignore

def populate_market():
    markets = [
        'NVDA.NE',  # NVIDIA 
        'PG.NE',  # The Procter & Gamble Company
        'AMZN.NE',  # Amazon.com, Inc
        'JNJ.NE',  # JOHNSON & JOHNSON CDR
        'AAPL.NE',  # Apple Inc.
        'MCDS.NE',  # McDonald's Corporation
        'MSFT.NE',  # Microsoft Corporation 
        'NFLX.NE',  # Netflix, Inc.
        'COLA.NE',  # The Coca-Cola Company
        'EBIT.TO',  # Bitcoin ETF CAD
        'VFV.TO',  # Vanguard S&P 500 Index ETF 
        'BRK.NE'  # Berkshire Hathaway Inc.
    ]

    for market_name in markets:
        # Utilise get_or_create pour éviter d'ajouter des doublons
        Market.objects.get_or_create(name=market_name)

    print("Market data has been populated.")


# python manage.py shell
# from trading_back_app_v2.init_populate_market import populate_market
populate_market()


# from myapp.models import Market
# Market.objects.all()  # Cela affichera toutes les actions stockées
# exit()
