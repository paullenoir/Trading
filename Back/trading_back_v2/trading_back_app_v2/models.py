from django.db import models
from datetime import datetime
import pandas as pd
import json

# python manage.py makemigrations
# python manage.py migrate

class Market(models.Model):
    name = models.CharField(max_length=50)

class MarketPrice(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    low_price = models.FloatField()
    high_price = models.FloatField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    adj_close = models.FloatField()
    volume = models.BigIntegerField()
    
    class Meta:
        unique_together = ('market', 'interval_time', 'date')
        
    @classmethod
    def get_all_record(cls, market, interval_time):
        # Filtrer les enregistrements par marché et intervalle
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time
        }

        # Récupérer le QuerySet basé sur les critères
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas

        return df
    
    @staticmethod
    def save_market_price(market_price):
        # Vérifier si un enregistrement existe déjà
        existing_record = MarketPrice.objects.filter(
            market=market_price['market'],
            interval_time=market_price['interval'],
            date=market_price['date']
        ).first()

        if existing_record:
            # Mettre à jour les champs si l'enregistrement existe
            existing_record.low_price = market_price['low_price']
            existing_record.high_price = market_price['high_price']
            existing_record.open_price = market_price['open_price']
            existing_record.close_price = market_price['close_price']
            existing_record.adj_close = market_price['adj_close']
            existing_record.volume = market_price['volume']
            existing_record.save()
        else:
            # Créer un nouvel enregistrement
            MarketPrice.objects.create(
                market=market_price['market'],
                interval_time=market_price['interval'],
                date=market_price['date'],
                low_price=market_price['low_price'],
                high_price=market_price['high_price'],
                open_price=market_price['open_price'],
                close_price=market_price['close_price'],
                adj_close=market_price['adj_close'],
                volume=market_price['volume']
            )

class MarketStrategyResult(models.Model):
    name = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    strategy_tendance_color = models.CharField(max_length=10)
    strategy_macd_color = models.CharField(max_length=10)
    strategy_ichimoku_color = models.CharField(max_length=10)
    strategy_2sma_color = models.CharField(max_length=10)
    strategy_bb_color = models.CharField(max_length=10)
    strategy_rsi_color = models.CharField(max_length=10)
    strategy_stochastic_color = models.CharField(max_length=10)

    @staticmethod
    def save_market_strategy_result(strategy_data):
        # Vérifier s'il existe déjà un enregistrement avec le même name, interval_time et date
        existing_record = MarketStrategyResult.objects.filter(
            name=strategy_data['name'],
            interval_time=strategy_data['interval_time']
        ).first()

        # Si l'enregistrement existe, mettre à jour les champs
        if existing_record:
            existing_record.strategy_tendance_color = strategy_data.get('strategy_tendance_color', existing_record.strategy_tendance_color)
            existing_record.strategy_macd_color = strategy_data.get('strategy_macd_color', existing_record.strategy_macd_color)
            existing_record.strategy_ichimoku_color = strategy_data.get('strategy_ichimoku_color', existing_record.strategy_ichimoku_color)
            existing_record.strategy_2sma_color = strategy_data.get('strategy_2sma_color', existing_record.strategy_2sma_color)
            existing_record.strategy_bb_color = strategy_data.get('strategy_bb_color', existing_record.strategy_bb_color)
            existing_record.strategy_rsi_color = strategy_data.get('strategy_rsi_color', existing_record.strategy_rsi_color)
            existing_record.strategy_stochastic_color = strategy_data.get('strategy_stochastic_color', existing_record.strategy_stochastic_color)
            existing_record.save()
        # Sinon, créer un nouvel enregistrement
        else:
            MarketStrategyResult.objects.create(
                name=strategy_data['name'],
                date=strategy_data['date'],
                interval_time=strategy_data['interval_time'],
                strategy_tendance_color=strategy_data['strategy_tendance_color'],
                strategy_macd_color=strategy_data['strategy_macd_color'],
                strategy_ichimoku_color=strategy_data['strategy_ichimoku_color'],
                strategy_2sma_color=strategy_data['strategy_2sma_color'],
                strategy_bb_color=strategy_data['strategy_bb_color'],
                strategy_rsi_color=strategy_data['strategy_rsi_color'],
                strategy_stochastic_color=strategy_data['strategy_stochastic_color']
            )

##
## Indicator
##
class IndicatorSMA(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    MM10 = models.FloatField(null=True, blank=True)
    MM15 = models.FloatField(null=True, blank=True)
    MM20 = models.FloatField(null=True, blank=True)
    MM25 = models.FloatField(null=True, blank=True)
    MM30 = models.FloatField(null=True, blank=True)
    MM35 = models.FloatField(null=True, blank=True)
    MM40 = models.FloatField(null=True, blank=True)
    MM45 = models.FloatField(null=True, blank=True)
    MM50 = models.FloatField(null=True, blank=True)
    MM55 = models.FloatField(null=True, blank=True)
    MM60 = models.FloatField(null=True, blank=True)
    MM65 = models.FloatField(null=True, blank=True)
    MM70 = models.FloatField(null=True, blank=True)
    MM75 = models.FloatField(null=True, blank=True)
    MM80 = models.FloatField(null=True, blank=True)
    MM85 = models.FloatField(null=True, blank=True)
    MM90 = models.FloatField(null=True, blank=True)
    MM95 = models.FloatField(null=True, blank=True)
    MM100 = models.FloatField(null=True, blank=True)
    MM200 = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('market', 'interval_time', 'date')

    @classmethod
    def get_record(cls, market, interval_time, date, mm1, mm2):    
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
            "date" : date,
        }
        
        # Ajout dynamique des moyennes mobiles au dictionnaire
        filter_kwargs[mm1 + '__isnull'] = False
        filter_kwargs[mm2 + '__isnull'] = False

                # Récupérer le QuerySet
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas

        return df
    
    @classmethod
    def get_all_record(cls, market, interval_time, mm1, mm2):
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
        }
        
        # Ajout dynamique des moyennes mobiles au dictionnaire
        filter_kwargs[mm1 + '__isnull'] = False
        filter_kwargs[mm2 + '__isnull'] = False

                # Récupérer le QuerySet
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas

        return df
        
    @staticmethod
    def save_sma(sma_data):
        # Vérifier si un enregistrement existe déjà
        existing_record = IndicatorSMA.objects.filter(
            market=sma_data['market'],
            interval_time=sma_data['interval_time'],
            date=sma_data['date']
        ).first()

        if existing_record:
            # Update existing record with new values
            existing_record.close_price = sma_data.get('close_price', existing_record.close_price)
            existing_record.MM10 = sma_data.get('MM10', existing_record.MM10)
            existing_record.MM15 = sma_data.get('MM15', existing_record.MM15)
            existing_record.MM20 = sma_data.get('MM20', existing_record.MM20)
            existing_record.MM25 = sma_data.get('MM25', existing_record.MM25)
            existing_record.MM30 = sma_data.get('MM30', existing_record.MM30)
            existing_record.MM35 = sma_data.get('MM35', existing_record.MM35)
            existing_record.MM40 = sma_data.get('MM40', existing_record.MM40)
            existing_record.MM45 = sma_data.get('MM45', existing_record.MM45)
            existing_record.MM50 = sma_data.get('MM50', existing_record.MM50)
            existing_record.MM55 = sma_data.get('MM55', existing_record.MM55)
            existing_record.MM60 = sma_data.get('MM60', existing_record.MM60)
            existing_record.MM65 = sma_data.get('MM65', existing_record.MM65)
            existing_record.MM70 = sma_data.get('MM70', existing_record.MM70)
            existing_record.MM75 = sma_data.get('MM75', existing_record.MM75)
            existing_record.MM80 = sma_data.get('MM80', existing_record.MM80)
            existing_record.MM85 = sma_data.get('MM85', existing_record.MM85)
            existing_record.MM90 = sma_data.get('MM90', existing_record.MM90)
            existing_record.MM95 = sma_data.get('MM95', existing_record.MM95)
            existing_record.MM100 = sma_data.get('MM100', existing_record.MM100)
            existing_record.MM200 = sma_data.get('MM200', existing_record.MM200)
            existing_record.save()
        else:
            # Create a new record if none exists
            IndicatorSMA.objects.create(
                market=sma_data['market'],
                interval_time=sma_data['interval_time'],
                date=sma_data['date'],
                close_price=sma_data['close_price'],
                MM10=sma_data.get('MM10'),
                MM15=sma_data.get('MM15'),
                MM20=sma_data.get('MM20'),
                MM25=sma_data.get('MM25'),
                MM30=sma_data.get('MM30'),
                MM35=sma_data.get('MM35'),
                MM40=sma_data.get('MM40'),
                MM45=sma_data.get('MM45'),
                MM50=sma_data.get('MM50'),
                MM55=sma_data.get('MM55'),
                MM60=sma_data.get('MM60'),
                MM65=sma_data.get('MM65'),
                MM70=sma_data.get('MM70'),
                MM75=sma_data.get('MM75'),
                MM80=sma_data.get('MM80'),
                MM85=sma_data.get('MM85'),
                MM90=sma_data.get('MM90'),
                MM95=sma_data.get('MM95'),
                MM100=sma_data.get('MM100'),
                MM200=sma_data.get('MM200')
            )

class IndicatorEMA(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    EMA20 = models.FloatField(null=True, blank=True)
    EMA50 = models.FloatField(null=True, blank=True)
    EMA200 = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('market', 'interval_time', 'date')
    
    @staticmethod
    def save_ema(smma_data):
        # Vérifier si un enregistrement existe déjà avec le même marché, intervalle et date
        existing_record = IndicatorEMA.objects.filter(
            market=smma_data['market'],
            interval_time=smma_data['interval_time'],
            date=smma_data['date']
        ).first()

        if existing_record:
            # Mettre à jour l'enregistrement existant avec les nouvelles valeurs
            existing_record.close_price = smma_data.get('close_price', existing_record.close_price)
            existing_record.EMA20 = smma_data.get('EMA20', existing_record.EMA20)
            existing_record.EMA50 = smma_data.get('EMA50', existing_record.EMA50)
            existing_record.EMA200 = smma_data.get('EMA200', existing_record.EMA200)
            existing_record.save()
        else:
            # Créer un nouvel enregistrement si aucun n'existe
            IndicatorEMA.objects.create(
                market=smma_data['market'],
                interval_time=smma_data['interval_time'],
                date=smma_data['date'],
                close_price=smma_data['close_price'],
                EMA20=smma_data.get('EMA20'),
                EMA50=smma_data.get('EMA50'),
                EMA200=smma_data.get('EMA200')
            )

class IndicatorMACD(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    macd = models.FloatField()
    macd_signal = models.FloatField()
    macd_histogram = models.FloatField()

    class Meta:
        unique_together = ('market', 'interval_time', 'date')

    @classmethod
    def get_record_by_market_interval_date(cls, market, interval_time, date):
        # Filtrer les enregistrements par marché et intervalle
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
            "date": date
        }

        # Récupérer le QuerySet basé sur les critères
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas
        return df
    
    @staticmethod
    def save_macd(macd_data):
        existing_record = IndicatorMACD.objects.filter(
            market=macd_data['market'],
            interval_time=macd_data['interval_time'],
            date=macd_data['date']
        ).first()

        if existing_record:
            existing_record.close_price = macd_data.get('close_price', existing_record.close_price)
            existing_record.macd = macd_data.get('macd', existing_record.macd)
            existing_record.macd_signal = macd_data.get('macd_signal', existing_record.macd_signal)
            existing_record.macd_histogram = macd_data.get('macd_histogram', existing_record.macd_histogram)
            existing_record.save()
        else:
            IndicatorMACD.objects.create(
                market=macd_data['market'],
                interval_time=macd_data['interval_time'],
                date=macd_data['date'],
                close_price=macd_data['close_price'],
                macd=macd_data['macd'],
                macd_signal=macd_data['macd_signal'],
                macd_histogram=macd_data['macd_histogram']
            )

class IndicatorRSI(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    rsi_7 = models.FloatField()
    rsi_14 = models.FloatField()
    rsi_21 = models.FloatField()

    class Meta:
        unique_together = ('market', 'interval_time', 'date')
        
    @classmethod
    def get_record_by_market_interval_date(cls, market, interval_time, date):
        # Filtrer les enregistrements par marché et intervalle
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
            "date": date
        }

        # Récupérer le QuerySet basé sur les critères
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas
        return df
    
    @staticmethod
    def save_rsi(rsi_data):
        existing_record = IndicatorRSI.objects.filter(
            market=rsi_data['market'],
            interval_time=rsi_data['interval_time'],
            date=rsi_data['date']
        ).first()

        if existing_record:
            existing_record.close_price = rsi_data.get('close_price', existing_record.close_price)
            existing_record.rsi_7 = rsi_data.get('rsi_7', existing_record.rsi_7)
            existing_record.rsi_14 = rsi_data.get('rsi_14', existing_record.rsi_14)
            existing_record.rsi_21 = rsi_data.get('rsi_21', existing_record.rsi_21)
            existing_record.save()
        else:
            IndicatorRSI.objects.create(
                market=rsi_data['market'],
                interval_time=rsi_data['interval_time'],
                date=rsi_data['date'],
                close_price=rsi_data['close_price'],
                rsi_7=rsi_data['rsi_7'],
                rsi_14=rsi_data['rsi_14'],
                rsi_21=rsi_data['rsi_21']
            )

class IndicatorBollingerBand(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    BB_Lower = models.FloatField()
    BB_Middle = models.FloatField()
    BB_Upper = models.FloatField()
    BB_Bandwidth = models.FloatField()
    BB_Percent = models.FloatField()

    class Meta:
        unique_together = ('market', 'interval_time', 'date')

    @classmethod
    def get_record_by_market_interval_date(cls, market, interval_time, date):
        # Filtrer les enregistrements par marché et intervalle
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
            "date": date
        }

        # Récupérer le QuerySet basé sur les critères
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas
        return df
    
    @classmethod
    def get_all_record(cls, market, interval_time):
        # Query the database for the matching record
        queryset = cls.objects.get(
            market=market,
            interval_time=interval_time
        )

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas
        return df
        
    @staticmethod
    def save_bollinger_band(bollinger_data):
        existing_record = IndicatorBollingerBand.objects.filter(
            market=bollinger_data['market'],
            interval_time=bollinger_data['interval_time'],
            date=bollinger_data['date']
        ).first()

        if existing_record:
            existing_record.close_price = bollinger_data.get('close_price', existing_record.close_price)
            existing_record.BB_Lower = bollinger_data.get('BB_Lower', existing_record.BB_Lower)
            existing_record.BB_Middle = bollinger_data.get('BB_Middle', existing_record.BB_Middle)
            existing_record.BB_Upper = bollinger_data.get('BB_Upper', existing_record.BB_Upper)
            existing_record.BB_Bandwidth = bollinger_data.get('BB_Bandwidth', existing_record.BB_Bandwidth)
            existing_record.BB_Percent = bollinger_data.get('BB_Percent', existing_record.BB_Percent)
            existing_record.save()
        else:
            IndicatorBollingerBand.objects.create(
                market=bollinger_data['market'],
                interval_time=bollinger_data['interval_time'],
                date=bollinger_data['date'],
                close_price=bollinger_data['close_price'],
                BB_Lower=bollinger_data['BB_Lower'],
                BB_Middle=bollinger_data['BB_Middle'],
                BB_Upper=bollinger_data['BB_Upper'],
                BB_Bandwidth=bollinger_data['BB_Bandwidth'],
                BB_Percent=bollinger_data['BB_Percent']
            )

class IndicatorIchimoku(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    Ichimoku_Conversion = models.FloatField()
    Ichimoku_Base = models.FloatField()
    Ichimoku_LeadingA = models.FloatField()
    Ichimoku_LeadingB = models.FloatField()
    Ichimoku_Lagging = models.FloatField()

    class Meta:
        unique_together = ('market', 'interval_time', 'date')

    @classmethod
    def get_record_by_market_interval_date(cls, market, interval_time, date):
        # Filtrer les enregistrements par marché et intervalle
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
            "date": date
        }

        # Récupérer le QuerySet basé sur les critères
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas
        return df
    
    @staticmethod
    def save_ichimoku(ichimoku_data):
        existing_record = IndicatorIchimoku.objects.filter(
            market=ichimoku_data['market'],
            interval_time=ichimoku_data['interval_time'],
            date=ichimoku_data['date']
        ).first()

        if existing_record:
            existing_record.close_price = ichimoku_data.get('close_price', existing_record.close_price)
            existing_record.Ichimoku_Conversion = ichimoku_data.get('Ichimoku_Conversion', existing_record.Ichimoku_Conversion)
            existing_record.Ichimoku_Base = ichimoku_data.get('Ichimoku_Base', existing_record.Ichimoku_Base)
            existing_record.Ichimoku_LeadingA = ichimoku_data.get('Ichimoku_LeadingA', existing_record.Ichimoku_LeadingA)
            existing_record.Ichimoku_LeadingB = ichimoku_data.get('Ichimoku_LeadingB', existing_record.Ichimoku_LeadingB)
            existing_record.Ichimoku_Lagging = ichimoku_data.get('Ichimoku_Lagging', existing_record.Ichimoku_Lagging)
            existing_record.save()
        else:
            IndicatorIchimoku.objects.create(
                market=ichimoku_data['market'],
                interval_time=ichimoku_data['interval_time'],
                date=ichimoku_data['date'],
                close_price=ichimoku_data['close_price'],
                Ichimoku_Conversion=ichimoku_data['Ichimoku_Conversion'],
                Ichimoku_Base=ichimoku_data['Ichimoku_Base'],
                Ichimoku_LeadingA=ichimoku_data['Ichimoku_LeadingA'],
                Ichimoku_LeadingB=ichimoku_data['Ichimoku_LeadingB'],
                Ichimoku_Lagging=ichimoku_data['Ichimoku_Lagging']
            )

class IndicatorStochastic(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    stochastic_k = models.FloatField()
    stochastic_d = models.FloatField()

    class Meta:
        unique_together = ('market', 'interval_time', 'date')

    @classmethod
    def get_record_by_market_interval_date(cls, market, interval_time, date):
        # Filtrer les enregistrements par marché et intervalle
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
            "date": date
        }

        # Récupérer le QuerySet basé sur les critères
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas
        return df
    
    @staticmethod
    def save_stochastic(stoch_data):
        existing_record = IndicatorStochastic.objects.filter(
            market=stoch_data['market'],
            interval_time=stoch_data['interval_time'],
            date=stoch_data['date']
        ).first()

        if existing_record:
            existing_record.close_price = stoch_data.get('close_price', existing_record.close_price)
            existing_record.stochastic_k = stoch_data.get('stochastic_k', existing_record.stochastic_k)
            existing_record.stochastic_d = stoch_data.get('stochastic_d', existing_record.stochastic_d)
            existing_record.save()
        else:
            IndicatorStochastic.objects.create(
                market=stoch_data['market'],
                interval_time=stoch_data['interval_time'],
                date=stoch_data['date'],
                close_price=stoch_data['close_price'],
                stochastic_k=stoch_data['stochastic_k'],
                stochastic_d=stoch_data['stochastic_d']
            )


##
## Strategies Data
##
class StrategyDataTendance(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    close_price = models.FloatField()
    pente_EMA20 = models.FloatField()  # Changement de SMMA à EMA
    pente_EMA50 = models.FloatField()  # Changement de SMMA à EMA
    pente_EMA200 = models.FloatField()  # Changement de SMMA à EMA
    tendance_EMA20 = models.CharField(max_length=50)  # Changement de SMMA à EMA
    tendance_EMA50 = models.CharField(max_length=50)  # Changement de SMMA à EMA
    tendance_EMA200 = models.CharField(max_length=50)  # Changement de SMMA à EMA
    tendance_all = models.CharField(max_length=50)

    class Meta:
        unique_together = ('market', 'interval_time', 'date')

    @classmethod
    def get_record(cls, market, interval_time, date):
            # Filtrer les enregistrements par marché et intervalle
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
            "date": date
        }

        # Récupérer le QuerySet basé sur les critères
        queryset = cls.objects.filter(**filter_kwargs)

        # Convertir le QuerySet en DataFrame pandas
        data = list(queryset.values())  # Convertir en liste de dictionnaires
        df = pd.DataFrame(data)  # Créer un DataFrame pandas
        return df
        
    @staticmethod
    def save_tendance(tendance_data):
        # Rechercher un enregistrement existant
        existing_record = StrategyDataTendance.objects.filter(
            market=tendance_data['market'],
            interval_time=tendance_data['interval_time'],
            date=tendance_data['date']
        ).first()

        if existing_record:
            # Mise à jour des champs si l'enregistrement existe
            existing_record.close_price = tendance_data.get('close_price', existing_record.close_price)
            existing_record.pente_EMA20 = tendance_data.get('pente_EMA20', existing_record.pente_EMA20)
            existing_record.pente_EMA50 = tendance_data.get('pente_EMA50', existing_record.pente_EMA50)
            existing_record.pente_EMA200 = tendance_data.get('pente_EMA200', existing_record.pente_EMA200)
            existing_record.tendance_EMA20 = tendance_data.get('tendance_EMA20', existing_record.tendance_EMA20)
            existing_record.tendance_EMA50 = tendance_data.get('tendance_EMA50', existing_record.tendance_EMA50)
            existing_record.tendance_EMA200 = tendance_data.get('tendance_EMA200', existing_record.tendance_EMA200)
            existing_record.tendance_all = tendance_data.get('tendance_all', existing_record.tendance_all)
            existing_record.save()
        else:
            # Création d'un nouvel enregistrement
            StrategyDataTendance.objects.create(
                market=tendance_data['market'],
                interval_time=tendance_data['interval_time'],
                date=tendance_data['date'],
                close_price=tendance_data['close_price'],
                pente_EMA20=tendance_data['pente_EMA20'],
                pente_EMA50=tendance_data['pente_EMA50'],
                pente_EMA200=tendance_data['pente_EMA200'],
                tendance_EMA20=tendance_data['tendance_EMA20'],
                tendance_EMA50=tendance_data['tendance_EMA50'],
                tendance_EMA200=tendance_data['tendance_EMA200'],
                tendance_all=tendance_data['tendance_all']
            )


class Backtest(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    strategyName = models.CharField(max_length=100)
    tradesCount = models.FloatField()
    worstDrawback = models.FloatField()
    averagePositifTrade = models.FloatField()
    averageNegativeTrade = models.FloatField()
    strategyParameter = models.TextField()

    class Meta:
        unique_together = ('market', 'interval_time', 'strategyName')

    @classmethod
    def get_strategy_params(cls, market, interval_time, strategy_name):
        try:
            # Récupérer l'instance du backtest correspondant aux critères
            backtest_instance = cls.objects.get(
                market=market,
                interval_time=interval_time,
                strategyName=strategy_name
            )
            # Convertir les paramètres de stratégie en dictionnaire
            return json.loads(backtest_instance.strategyParameter)
        except cls.DoesNotExist:
            # Aucun enregistrement trouvé, retourner None
            return None
        except json.JSONDecodeError:
            # Gérer le cas où le JSON est mal formé
            return None

    @staticmethod
    def save_backtest(backtest_data):
        # Chercher un enregistrement existant pour ce marché et intervalle
        existing_record = Backtest.objects.filter(
            market=backtest_data['market'],
            interval_time=backtest_data['interval_time'],
            strategyName = backtest_data['strategyName']
        ).first()

        if existing_record:
            # Mise à jour des champs si l'enregistrement existe
            existing_record.tradesCount = backtest_data.get('tradesCount', existing_record.tradesCount)
            existing_record.worstDrawback = backtest_data.get('worstDrawback', existing_record.worstDrawback)
            existing_record.averagePositifTrade = backtest_data.get('averagePositifTrade', existing_record.averagePositifTrade)
            existing_record.averageNegativeTrade = backtest_data.get('averageNegativeTrade', existing_record.averageNegativeTrade)
            existing_record.strategyParameter = backtest_data.get('strategyParameter', existing_record.strategyParameter)
            existing_record.save()
        else:
            # Créer un nouvel enregistrement si aucun n'existe
            Backtest.objects.create(
                market=backtest_data['market'],
                interval_time=backtest_data['interval_time'],
                strategyName=backtest_data['strategyName'],
                tradesCount=backtest_data['tradesCount'],
                worstDrawback=backtest_data['worstDrawback'],
                averagePositifTrade=backtest_data['averagePositifTrade'],
                averageNegativeTrade=backtest_data['averageNegativeTrade'],
                strategyParameter=backtest_data['strategyParameter']
            )

class TradingResult(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date_start = models.CharField(max_length=50)
    date_end = models.CharField(max_length=50)
    strategyName = models.CharField(max_length=100)
    strategyParameter = models.TextField()
    buy_price = models.CharField(max_length=100)
    sell_price = models.CharField(max_length=100)
    dollars_profit = models.CharField(max_length=100)
    percent_profit = models.CharField(max_length=100)

    class Meta:
        unique_together = ('market', 'interval_time', 'date_start', "strategyName")

    @staticmethod
    def save_tradingresult(result_data):
        existing_record = TradingResult.objects.filter(
            market=result_data['market'],
            interval_time=result_data['interval_time'],
            date_start=result_data['date_start'],
            strategyName = result_data['strategyName']
        ).first()

        if existing_record:
            if existing_record.date_end:  # Si date_end n'est pas vide, ne rien faire
                return  # Sortir de la fonction ou passer à la prochaine logique
            else:
                # Mettre à jour les champs de l'enregistrement existant
                existing_record.date_end = result_data.get('date_end', existing_record.date_end)
                # existing_record.strategyParameter = result_data.get('strategyParameter', existing_record.strategyParameter)
                # existing_record.buy_price = result_data.get('buy_price', existing_record.buy_price)
                existing_record.sell_price = result_data.get('sell_price', existing_record.sell_price)
                existing_record.dollars_profit = result_data.get('dollars_profit', existing_record.dollars_profit)
                existing_record.percent_profit = result_data.get('percent_profit', existing_record.percent_profit)
                existing_record.save()
        else:
            TradingResult.objects.create(
                market=result_data['market'],
                interval_time=result_data['interval_time'],
                date_start=result_data['date_start'],
                date_end=result_data['date_end'],
                strategyName=result_data['strategyName'],
                strategyParameter=result_data['strategyParameter'],
                buy_price=result_data['buy_price'],  
                sell_price=result_data['sell_price'],
                dollars_profit=result_data['dollars_profit'],
                percent_profit=result_data['percent_profit']
            )
    
    @staticmethod
    def get_record(market, interval_time, strategyName):
        # Filtre les enregistrements selon 'market', 'interval_time', et 'strategyName'
        query = TradingResult.objects.filter(
            market=market,
            interval_time=interval_time,
            strategyName=strategyName
        ).order_by('-date_start')  # Trie par 'date_start' décroissant pour obtenir le plus récent

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query.first()
    
    @staticmethod
    def apply_strategies_and_save(market, interval_time, signal, strategy, row):
        strategy_name = strategy.get_name()
        strategy_params = strategy.get_params()  # On suppose que chaque stratégie a cette méthode
        row_date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
        existing_trade = TradingResult.get_record(market, interval_time, strategy_name)

        if existing_trade is None:
            if signal == 'buy':
                TradingResult.save_tradingresult(
                    {
                        "market":market,
                        "interval_time":interval_time,
                        "date_start":row['date'],
                        "date_end":"",
                        "strategyName":strategy_name,
                        "strategyParameter":strategy_params,
                        "buy_price":row['close_price'],  # On suppose qu'on achète au prix de clôture
                        "sell_price":'',
                        "dollars_profit":'',
                        "percent_profit":''
                    }
                )
        elif existing_trade is None or (existing_trade.date_end != "" and row_date > datetime.strptime(existing_trade.date_end, '%Y-%m-%d %H:%M:%S')) and signal == 'buy':  #buy
            TradingResult.save_tradingresult(
                {
                    "market":market,
                    "interval_time":interval_time,
                    "date_start":row['date'],
                    "date_end":"",
                    "strategyName":strategy_name,
                    "strategyParameter":strategy_params,
                    "buy_price":row['close_price'],  # On suppose qu'on achète au prix de clôture
                    "sell_price":'',
                    "dollars_profit":'',
                    "percent_profit":''
                }
            )

        # Condition de vente
        elif row_date >= datetime.strptime(existing_trade.date_start, '%Y-%m-%d %H:%M:%S') and (existing_trade.date_end is None or existing_trade.date_end == "") and signal == 'sell':
            # Compléter le trade en ajoutant le prix de vente et en calculant les profits
            existing_trade.sell_price = row['close_price']  # On suppose qu'on vend au prix de clôture
            existing_trade.date_end = row['date']

            # Calcul du profit en dollars et en pourcentage
            buy_price = float(existing_trade.buy_price)
            sell_price = float(existing_trade.sell_price)
            existing_trade.dollars_profit = str(sell_price - buy_price)
            existing_trade.percent_profit = str(((sell_price - buy_price) / buy_price) * 100)

            # Sauvegarder le trade complété
            TradingResult.save_tradingresult(
                {
                    "market": market,
                    "interval_time": interval_time,
                    "date_start": existing_trade.date_start,
                    "date_end": existing_trade.date_end,
                    "strategyName": strategy_name,
                    "strategyParameter": strategy_params,
                    "buy_price": existing_trade.buy_price,
                    "sell_price": existing_trade.sell_price,
                    "dollars_profit": str(existing_trade.dollars_profit),
                    "percent_profit": str(existing_trade.percent_profit)
                }
            )