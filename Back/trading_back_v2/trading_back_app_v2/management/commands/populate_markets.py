from django.core.management.base import BaseCommand
from trading_back_app_v2.models import Market

class Command(BaseCommand):
    help = 'Populate the Market table with initial data'

    def handle(self, *args, **kwargs):
        initial_markets = [
            'NVDA.NE',  # NVIDIA - Électronique et semi-conducteurs
            'PG.NE',  # The Procter & Gamble Company - Produits de consommation
            'AMZN.NE',  # Amazon.com, Inc - E-commerce et services cloud
            'JNJ.NE',  # Johnson & Johnson CDR - Pharmaceutique et dispositifs médicaux
            'AAPL.NE',  # Apple Inc. - Technologie et électronique grand public
            'MCDS.NE',  # McDonald's Corporation - Restauration rapide
            'MSFT.NE',  # Microsoft Corporation - Technologie et services logiciels
            'NFLX.NE',  # Netflix, Inc. - Streaming et production de contenu
            'COLA.NE',  # The Coca-Cola Company - Alimentaire et boissons
            'EBIT.TO',  # Bitcoin ETF CAD - Fonds négocié en bourse, crypto-monnaie
            'VFV.TO',  # Vanguard S&P 500 Index ETF - Fonds indiciel
            'BRK.NE',  # Berkshire Hathaway Inc. - Holding diversifiée
            'LLY.NE',  # Eli Lilly and Company - Pharmaceutique
            'BA.NE',  # The Boeing Company - Aéronautique et défense
            'RTX.NE',  # Raytheon Technologies Corporation - Aéronautique et défense
            'BBU-UN-TO',  # Brookfield Business Partners L.P. - Gestion d'actifs et infrastructures
        ]
        
        for market_name in initial_markets:
            market, created = Market.objects.get_or_create(name=market_name)
            if created:
                self.stdout.write(f"Added market: {market.name}")
            else:
                self.stdout.write(f"Market already exists: {market.name}")
