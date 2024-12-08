from django.core.management.base import BaseCommand
from trading_back_app_v2.models import Market
from trading_back_app_v2.services_yf import download_and_process_data, create_market_price
from trading_back_app_v2.indicators import *
from trading_back_app_v2.strategies import *
import time
import datetime

# python manage.py run_back "1d"
# python manage.py run_back "1h"
# python manage.py run_back "30min"
# python manage.py run_back "15min"

class Command(BaseCommand):
    help = 'Télécharge les données et exécute le backtest'

    def add_arguments(self, parser):
        parser.add_argument('interval', type=str, help='Intervalle pour les données (ex: 1h, 1d)')

    def handle(self, *args, **kwargs):
        start_time = time.time()
        interval = kwargs['interval']
        print('interval ' + interval)
        markets = Market.objects.all() # Récupérer toutes les actions du modèle Market

        # Itérer sur chaque action
        for market in markets:
            print(str(market.name))
            start_time2 = time.time()
            #Telecharger les données de yfinance
            data = download_and_process_data(market.name, interval)
            print("1.download_data  " + str((time.time() - start_time2) / 60))

            start_time2 = time.time()
            create_market_price(data, market.name, interval)
            print("  1.create_market_price  " + str((time.time() - start_time2) / 60))

            start_time2 = time.time()
            calculate_indicators(market.name, interval)
            print("  1.calculate_indicators  " + str((time.time() - start_time2) / 60))

            start_time2 = time.time()
            execute_trading(market.name, interval)
            print("  1.execute_trading  " + str((time.time() - start_time2) / 60))

            # #Seulement les samedi
            # if datetime.datetime.today().weekday() == 5:
            #     start_time2 = time.time()
            #     execute_backtest(market, interval)
            #     print("  2.execute_trading  " + str((time.time() - start_time2) / 60))

        self.stdout.write(self.style.SUCCESS(f'Données récupérées pour l\'intervalle: {interval}'))
        print("1.Total pgm  " + str((time.time() - start_time) / 60))
