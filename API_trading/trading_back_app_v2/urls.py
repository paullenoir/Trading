from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MarketViewSet, MarketPriceViewSet, MarketStrategyResultViewSet, IndicatorSMAViewSet, IndicatorEMAViewSet,
    IndicatorMACDViewSet, IndicatorRSIViewSet, IndicatorBollingerBandViewSet,
    IndicatorIchimokuViewSet, IndicatorStochasticViewSet, StrategyDataTendanceViewSet,
    BacktestViewSet, TradingResultViewSet
)
# Création du routeur pour l'API
router = DefaultRouter()
router.register(r'markets', MarketViewSet)
router.register(r'marketprices', MarketPriceViewSet)
router.register(r'marketstrategyresult', MarketStrategyResultViewSet)
router.register(r'indicatorsma', IndicatorSMAViewSet)
router.register(r'indicatorema', IndicatorEMAViewSet)
router.register(r'indicatormacd', IndicatorMACDViewSet)
router.register(r'indicatorrsi', IndicatorRSIViewSet)
router.register(r'indicatorbollingerband', IndicatorBollingerBandViewSet)
router.register(r'indicatorichimoku', IndicatorIchimokuViewSet)
router.register(r'indicatorstochastic', IndicatorStochasticViewSet)
router.register(r'strategytendances', StrategyDataTendanceViewSet)
router.register(r'backtests', BacktestViewSet)
router.register(r'tradingresults', TradingResultViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclut toutes les routes
]
