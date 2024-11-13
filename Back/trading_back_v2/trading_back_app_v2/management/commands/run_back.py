from django.core.management.base import BaseCommand
import yfinance as yf
from trading_back_app_v2.models import Market
from trading_back_app_v2.services_data import download_and_process_data, process_market_data
import time
import pandas as pd

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
        markets = Market.objects.all() # Récupérer toutes les actions du modèle Market

        # Itérer sur chaque action
        for market in markets:
            print(str(market.name))
            start_time2 = time.time()
            data = download_and_process_data(market.name, interval)
            print("1.download_and_process_data  " + str((time.time() - start_time2) / 60))

            # data = pd.DataFrame() #Test
            start_time2 = time.time()
            process_market_data(data, market.name, interval)
            print("1.process_market_data  " + str((time.time() - start_time2) / 60))

        self.stdout.write(self.style.SUCCESS(f'Données récupérées pour l\'intervalle: {interval}'))
        print("1.Total pgm  " + str((time.time() - start_time) / 60))
