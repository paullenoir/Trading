from django.core.management.base import BaseCommand
from trading_back_app_v2.models import Market

class Command(BaseCommand):
    help = 'Populate the Market table with initial data'

    def handle(self, *args, **kwargs):
        initial_markets = [
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
        
        for market_name in initial_markets:
            market, created = Market.objects.get_or_create(name=market_name)
            if created:
                self.stdout.write(f"Added market: {market.name}")
            else:
                self.stdout.write(f"Market already exists: {market.name}")
