#convertir les instances de modèles en données JSON (ou d'autres formats) et inversement.
# Validation des données : Avant de créer ou de mettre à jour des objets, le serializer vérifie que les données reçues sont valides. Il s'assure que les champs requis sont fournis et que les données respectent les types spécifiés
# Conversion : Il transforme les objets du modèle en représentations de données plus simples, généralement en JSON. Cela permet de renvoyer des réponses aux clients sous forme de données exploitables.
# Gestion des relations : Si votre modèle a des relations (comme des clés étrangères), le serializer peut gérer ces relations, en incluant des données de modèles liés ou en acceptant des identifiants pour les relations.
# Personnalisation : Vous pouvez personnaliser le comportement du serializer en ajoutant des méthodes pour la validation ou en définissant des champs dérivés.
from rest_framework import serializers
from .models import (
    Market, MarketPrice, MarketStrategyResult, IndicatorSMA, IndicatorEMA, IndicatorMACD,
    IndicatorRSI, IndicatorBollingerBand, IndicatorIchimoku, IndicatorStochastic,
    StrategyDataTendance, Backtest, TradingResult
)
import numpy as np


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = '__all__'

class MarketStrategyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketStrategyResult
        fields = '__all__'

##
## Indicator
##
class IndicatorSMASerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorSMA
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remplace NaN par 0 ou une autre valeur par défaut
        for key, value in data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                data[key] = 0  # ou une autre valeur par défaut
        return data

class IndicatorEMASerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorEMA
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remplace NaN par 0 ou une autre valeur par défaut
        for key, value in data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                data[key] = 0  # ou une autre valeur par défaut
        return data

class IndicatorMACDSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorMACD
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remplace NaN par 0 ou une autre valeur par défaut
        for key, value in data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                data[key] = 0  # ou une autre valeur par défaut
        return data

class IndicatorRSISerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorRSI
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remplace NaN par 0 ou une autre valeur par défaut
        for key, value in data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                data[key] = 0  # ou une autre valeur par défaut
        return data

class IndicatorBollingerBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorBollingerBand
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remplace NaN par 0 ou une autre valeur par défaut
        for key, value in data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                data[key] = 0  # ou une autre valeur par défaut
        return data

class IndicatorIchimokuSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorIchimoku
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remplace NaN par 0 ou une autre valeur par défaut
        for key, value in data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                data[key] = 0  # ou une autre valeur par défaut
        return data

class IndicatorStochasticSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorStochastic
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remplace NaN par 0 ou une autre valeur par défaut
        for key, value in data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                data[key] = 0  # ou une autre valeur par défaut
        return data

##
## Strategies Data
##
class StrategyDataTendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyDataTendance
        fields = '__all__'
        
class BacktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backtest
        fields = '__all__'

class TradingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingResult
        fields = '__all__'
