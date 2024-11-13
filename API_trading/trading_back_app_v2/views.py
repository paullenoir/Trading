# point d'entrée pour traiter les requêtes HTTP (GET, POST, PUT, DELETE, etc.) liées à un modèle.
# Gestion des requêtes HTTP : Le ViewSet fournit des méthodes pour gérer différentes opérations CRUD (Create, Read, Update, Delete) basées sur les requêtes HTTP. Par exemple, une requête GET renverra une liste d'objets ou un objet spécifique, tandis qu'une requête POST créera un nouvel objet.
# Intégration avec le queryset et le serializer : Le ViewSet utilise le queryset pour récupérer les données et le serializer pour valider et transformer les données d'entrée et de sortie. Cela facilite la gestion des données en suivant le principe DRY (Don't Repeat Yourself).
# Automatisation des endpoints : En utilisant un ViewSet avec un routeur, vous pouvez automatiquement créer des routes RESTful pour vos modèles sans avoir à définir chaque route manuellement.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import (
    Market, MarketPrice, MarketStrategyResult, IndicatorSMA, IndicatorEMA, IndicatorMACD,
    IndicatorRSI, IndicatorBollingerBand, IndicatorIchimoku, IndicatorStochastic,
    StrategyDataTendance, Backtest, TradingResult
)
from .serializers import (
    MarketSerializer, MarketPriceSerializer, MarketStrategyResultSerializer, IndicatorSMASerializer,
    IndicatorEMASerializer, IndicatorMACDSerializer, IndicatorRSISerializer,
    IndicatorBollingerBandSerializer, IndicatorIchimokuSerializer,
    IndicatorStochasticSerializer, StrategyDataTendanceSerializer,
    BacktestSerializer, TradingResultSerializer
)
class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

class MarketPriceViewSet(viewsets.ModelViewSet):
    queryset = MarketPrice.objects.all()
    serializer_class = MarketPriceSerializer

    def get_queryset(self):
        # Récupérer les paramètres de la requête
        market = self.request.query_params.get('market')
        interval_time = self.request.query_params.get('interval_time')
        
        queryset = self.queryset
        if market:
            queryset = queryset.filter(market=market)
        if interval_time:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class MarketStrategyResultViewSet(viewsets.ModelViewSet):
    queryset = MarketStrategyResult.objects.all()
    serializer_class = MarketStrategyResultSerializer

    # GET http://127.0.0.1:8000/api/marketstrategyresult/?name=NVDA.NE&interval_time=1d
    def get_queryset(self):
        queryset = super().get_queryset()
        # name = self.request.query_params.get('name', None)
        # interval_time = self.request.query_params.get('interval_time', None)

        # if name is not None:
        #     queryset = queryset.filter(name=name)

        # if interval_time is not None:
        #     queryset = queryset.filter(interval_time=interval_time)

        return queryset


class IndicatorSMAViewSet(viewsets.ModelViewSet):
    queryset = IndicatorSMA.objects.all()
    serializer_class = IndicatorSMASerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market', None)
        interval_time = self.request.query_params.get('interval_time', None)

        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class IndicatorEMAViewSet(viewsets.ModelViewSet):
    queryset = IndicatorEMA.objects.all()
    serializer_class = IndicatorEMASerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market', None)
        interval_time = self.request.query_params.get('interval_time', None)

        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class IndicatorMACDViewSet(viewsets.ModelViewSet):
    queryset = IndicatorMACD.objects.all()
    serializer_class = IndicatorMACDSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market')
        interval_time = self.request.query_params.get('interval_time')

        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class IndicatorRSIViewSet(viewsets.ModelViewSet):
    queryset = IndicatorRSI.objects.all()
    serializer_class = IndicatorRSISerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market')
        interval_time = self.request.query_params.get('interval_time')

        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class IndicatorBollingerBandViewSet(viewsets.ModelViewSet):
    queryset = IndicatorBollingerBand.objects.all()
    serializer_class = IndicatorBollingerBandSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market')
        interval_time = self.request.query_params.get('interval_time')

        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class IndicatorIchimokuViewSet(viewsets.ModelViewSet):
    queryset = IndicatorIchimoku.objects.all()
    serializer_class = IndicatorIchimokuSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market')
        interval_time = self.request.query_params.get('interval_time')

        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class IndicatorStochasticViewSet(viewsets.ModelViewSet):
    queryset = IndicatorStochastic.objects.all()
    serializer_class = IndicatorStochasticSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market', None)
        interval_time = self.request.query_params.get('interval_time', None)
        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset

class StrategyDataTendanceViewSet(viewsets.ModelViewSet):
    queryset = StrategyDataTendance.objects.all()
    serializer_class = StrategyDataTendanceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        market = self.request.query_params.get('market')
        interval_time = self.request.query_params.get('interval_time')

        if market is not None:
            queryset = queryset.filter(market=market)

        if interval_time is not None:
            queryset = queryset.filter(interval_time=interval_time)

        return queryset


class BacktestViewSet(viewsets.ModelViewSet):
    queryset = Backtest.objects.all()
    serializer_class = BacktestSerializer

class TradingResultViewSet(viewsets.ModelViewSet):
    queryset = TradingResult.objects.all()
    serializer_class = TradingResultSerializer

    def get_queryset(self):
        # Récupérer les paramètres de la requête
        market = self.request.query_params.get('market')
        interval_time = self.request.query_params.get('interval_time')
        strategyName = self.request.query_params.get('strategyName')
        
        queryset = self.queryset
        if market:
            queryset = queryset.filter(market=market)
        if interval_time:
            queryset = queryset.filter(interval_time=interval_time)
        if strategyName:
            queryset = queryset.filter(strategyName=strategyName)

        return queryset