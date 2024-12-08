from django.db import models
import json

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

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
    
    @staticmethod
    def get_all_record(market, interval_time):
        query = MarketPrice.objects.filter(
            market=market,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query

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
    def get_all_record(name, interval_time):
        query = MarketStrategyResult.objects.filter(
            name=name,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query

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
    
    @staticmethod
    def get_all_record(market, interval_time, mm1, mm2):
        filter_kwargs = {
            'market': market,
            'interval_time': interval_time,
        }
        
        # Ajout dynamique des moyennes mobiles au dictionnaire
        filter_kwargs[mm1 + '__isnull'] = False
        filter_kwargs[mm2 + '__isnull'] = False


        query = IndicatorSMA.objects.filter(**filter_kwargs)

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query
    
    # @classmethod
    # def get_all_record(cls, market, interval_time, mm1, mm2):
    #     filter_kwargs = {
    #         'market': market,
    #         'interval_time': interval_time,
    #     }
        
    #     # Ajout dynamique des moyennes mobiles au dictionnaire
    #     filter_kwargs[mm1 + '__isnull'] = False
    #     filter_kwargs[mm2 + '__isnull'] = False

    #             # Récupérer le QuerySet
    #     queryset = cls.objects.filter(**filter_kwargs)

    #     # Convertir le QuerySet en DataFrame pandas
    #     data = list(queryset.values())  # Convertir en liste de dictionnaires
    #     df = pd.DataFrame(data)  # Créer un DataFrame pandas

    #     return df
        
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
    def get_all_record(market, interval_time):
        query = IndicatorEMA.objects.filter(
            market=market,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query

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

    @staticmethod
    def get_all_record(market, interval_time):
        query = IndicatorMACD.objects.filter(
            market=market,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query

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
        
    @staticmethod
    def get_all_record(market, interval_time):
        query = IndicatorRSI.objects.filter(
            market=market,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query

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

    @staticmethod
    def get_all_record(market, interval_time):
        query = IndicatorBollingerBand.objects.filter(
            market=market,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query
        
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

    @staticmethod
    def get_all_record(market, interval_time):
        query = IndicatorIchimoku.objects.filter(
            market=market,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query

class IndicatorStochastic(models.Model):
    market = models.CharField(max_length=50)
    interval_time = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    stochastic_k = models.FloatField()
    stochastic_d = models.FloatField()
    close_price = models.FloatField()

    @staticmethod
    def get_all_record(market, interval_time):
        query = IndicatorStochastic.objects.filter(
            market=market,
            interval_time=interval_time
        )
        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query

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

    @staticmethod
    def get_all_record(market, interval_time):
        query = StrategyDataTendance.objects.filter(
            market=market,
            interval_time=interval_time
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query


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
    def get_all_record(market, interval_time, strategyName):
        # Filtre les enregistrements selon 'market', 'interval_time', et 'strategyName'
        query = TradingResult.objects.filter(
            market=market,
            interval_time=interval_time,
            strategyName=strategyName
        )

        # Retourne le dernier enregistrement trouvé ou None s'il n'y a aucun résultat
        return query