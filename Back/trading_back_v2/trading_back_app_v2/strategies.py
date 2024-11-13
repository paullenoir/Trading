from trading_back_app_v2.models import *
import pandas as pd
from trading_back_app_v2.utils import determine_trend, all_increase
import numpy as np
import time
import ast
from trading_back_app_v2.backtest import apply_backtest_for_get_params

class StrategyBase:
    def __init__(self, market, interval, df, name="Unnamed Strategy"):
        self.market = market
        self.interval = interval
        self.params = []
        self.paramsBacktest = []
        self.name = name
        self.df = df

    def initialize(self):
        raise NotImplementedError("Subclasses must implement this method!")

    def get_params(self):
        return self.params  # Retourne les paramètres de la stratégie
    
    def get_paramsBacktest(self):
        return self.paramsBacktest  # Retourne les paramètres de la stratégie

    def get_name(self):
        return self.name  # Retourne le nom de la stratégie

    def apply_strategy_for_a_row(self, row):
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes.")

#Without Backtest

class StrategyTendance(StrategyBase):
    def __init__(self, market, interval, df):
        super().__init__(market, interval, df, name="tendance")
        # Calculer les données de tendance lors de l'instanciation
        self.prepare_tendance_data()

    def prepare_tendance_data(self):
        # Calculer les données de tendance avec la fonction data_tendance
        data_tendance(self.df, self.market, self.interval)

    def apply_strategy_for_a_row(self, marketPrice_row):
        date = marketPrice_row['date']
        #chercher l<enregistrement precedent et si = True wait, aller chercher le dernier enregistrement dans tradingresult pour date_end
        dataTendance_row = StrategyDataTendance.get_record(self.market, self.interval, date)
        # Exemple de logique de stratégie
        if str(dataTendance_row["tendance_all"].tolist()[0]) == "True":
            return "buy"
        elif str(dataTendance_row["tendance_all"].tolist()[0]) == "False":
            return "sell"
        else:
            return "wait"

def data_tendance(df, market, interval):
    # Calcul des EMA
    df['EMA20'] = df['close_price'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['close_price'].ewm(span=50, adjust=False).mean()
    df['EMA200'] = df['close_price'].ewm(span=200, adjust=False).mean()

    # Calcul des pentes pour chaque EMA
    df["pente_EMA20"] = np.gradient(np.array(df['EMA20']))
    df["pente_EMA50"] = np.gradient(np.array(df['EMA50']))
    df["pente_EMA200"] = np.gradient(np.array(df['EMA200']))

    # Déterminer les tendances basées sur les pentes
    df['tendance_EMA20'] = df['pente_EMA20'].apply(determine_trend)
    df['tendance_EMA50'] = df['pente_EMA50'].apply(determine_trend)
    df['tendance_EMA200'] = df['pente_EMA200'].apply(determine_trend)

    # Vérifier si toutes les EMA augmentent
    df['all_EMA_increase'] = df.apply(all_increase, axis=1)

    # Parcourir chaque ligne pour sauvegarder les données de tendance
    for index, row in df.iterrows():
        row = df.loc[index]
        tendance = {
            "market" : market,
            "interval_time" : interval,
            "date" : pd.Timestamp(row['date']).strftime('%Y-%m-%d %H:%M:%S'),
            "close_price" : row['close_price'],
            "pente_EMA20" : row.get('pente_EMA20', None),
            "pente_EMA50" : row.get('pente_EMA50', None),
            "pente_EMA200" : row.get('pente_EMA200', None),
            "tendance_EMA20" : row.get('tendance_EMA20', None),
            "tendance_EMA50" : row.get('tendance_EMA50', None),
            "tendance_EMA200" : row.get('tendance_EMA200', None),
            "tendance_all" : row.get('all_EMA_increase', None)
        }

        StrategyDataTendance.save_tendance(tendance)

class StrategyMACD(StrategyBase):
    def __init__(self, market, interval, df):
        super().__init__(market, interval, df, name="macd")

    def apply_strategy_for_a_row(self, marketPrice_row):
        macd_row = IndicatorMACD.get_record_by_market_interval_date(self.market, self.interval, marketPrice_row['date'])
        macd = macd_row['macd'].tolist()[0]
        macd_signal = macd_row['macd_signal'].tolist()[0]
        macd_histogram = macd_row['macd_histogram'].tolist()[0]

        # Exemple de logique de stratégie
        if macd > macd_signal and macd > macd_histogram:
            return "buy"
        elif macd < macd_signal:
            return "sell"
        else:
            return "wait"

class StrategyIchimoku(StrategyBase):
    def __init__(self, market, interval, df):
        super().__init__(market, interval, df, name="ichimoku")

    def apply_strategy_for_a_row(self, marketPrice_row):
        ichimoku_row = IndicatorIchimoku.get_record_by_market_interval_date(self.market, self.interval, marketPrice_row['date'])
        close_price = ichimoku_row['close_price'].tolist()[0]
        Ichimoku_Conversion = ichimoku_row['Ichimoku_Conversion'].tolist()[0]
        Ichimoku_Base = ichimoku_row['Ichimoku_Base'].tolist()[0]
        Ichimoku_LeadingA = ichimoku_row['Ichimoku_LeadingA'].tolist()[0]
        Ichimoku_LeadingB = ichimoku_row['Ichimoku_LeadingB'].tolist()[0]
        Ichimoku_Lagging = ichimoku_row['Ichimoku_Lagging'].tolist()[0]

        # Exemple de logique de stratégie
        if Ichimoku_Conversion > Ichimoku_Base and close_price > Ichimoku_LeadingA and close_price > Ichimoku_LeadingB:
            return "buy"
        elif Ichimoku_Conversion < Ichimoku_Base and close_price < Ichimoku_LeadingA and close_price < Ichimoku_LeadingB:
            return "sell"
        else:
            return "wait"


#With Backtest
class Strategy2SMA(StrategyBase):
    def __init__(self, market, interval, df):
        super().__init__(market, interval, df, name="2sma")
        self.paramsBacktest = [[10, 15, 20], [50, 100, 200]]
        self.params = Backtest.get_strategy_params(self.market, self.interval, self.name)
        if self.params is None:
            self.params = [10, 50]

    def apply_strategy_for_a_row(self, marketPrice_row):
        row = IndicatorSMA.get_record(marketPrice_row["market"], marketPrice_row["interval_time"], marketPrice_row["date"], "MM" + str(self.params[0]), "MM" + str(self.params[1]))
        short_mm_value = row["MM" + str(self.params[0])]
        long_mm_value = row["MM" + str(self.params[1])]

        if short_mm_value is None or long_mm_value is None:
            return "wait"
        elif float(short_mm_value) > float(long_mm_value):
            return "buy"
        else:
            return "sell"

class StrategyBollingerBand(StrategyBase):
    def __init__(self, market, interval, df):
        super().__init__(market, interval, df, name="bollingerband")
        self.paramsBacktest = [[0.05, 0.1, 0.15, 0.2], [0.80, 0.85, 0.9, 0.95]]
        self.params = Backtest.get_strategy_params(self.market, self.interval, self.name)
        if self.params is None:
            self.params = [0.2, 0.8]

    def apply_strategy_for_a_row(self, marketPrice_row):
        close_price = marketPrice_row['close_price']

        bb_row = IndicatorBollingerBand.get_record_by_market_interval_date(self.market, self.interval, marketPrice_row['date'])
        bb_lower = bb_row['BB_Lower'].tolist()[0]
        bb_upper = bb_row['BB_Upper'].tolist()[0]
        bb_percent = bb_row['BB_Percent'].tolist()[0]
        bb_middle = bb_row['BB_Middle'].tolist()[0]
        bb_bandwidth = bb_row['BB_Bandwidth'].tolist()[0]

        #A faire varier
        # Seuils pour la stratégie Bollinger
        percent_threshold_buy = self.params[0]  # Acheter si bb_percent est proche de 0%
        percent_threshold_sell = self.params[1]  # Vendre si bb_percent est proche de 100%

        # Si les données sont absentes, passer à la prochaine itération
        if bb_lower is None or bb_upper is None or bb_percent is None:
            return "wait"
        elif float(close_price) <= float(bb_lower) and float(bb_percent) < float(percent_threshold_buy):
            return "buy"
        elif float(close_price) >= float(bb_upper) and float(bb_percent) > float(percent_threshold_sell):
            return "sell"

class StrategyRSI(StrategyBase):
    def __init__(self, market, interval, df):
        super().__init__(market, interval, df, name="rsi")
        self.paramsBacktest = [[7,14,21]]
        self.params = Backtest.get_strategy_params(self.market, self.interval, self.name)
        if self.params is None:
            self.params = [14]

    def apply_strategy_for_a_row(self, marketPrice_row):
        rsi_row = IndicatorRSI.get_record_by_market_interval_date(self.market, self.interval, marketPrice_row['date'])
        rsi = rsi_row['rsi_' + str(self.params[0])].tolist()[0]

        if rsi < 30:
            return "buy"
        elif rsi > 70:
            return "sell"
        else:
            return 'wait'

class StrategyStochastique(StrategyBase):
    def __init__(self, market, interval, df):
        super().__init__(market, interval, df, name="stochastic")
        self.paramsBacktest = [[5, 10, 15, 20], [80, 85, 90, 95]]
        self.params = Backtest.get_strategy_params(self.market, self.interval, self.name)
        if self.params is None:
            self.params = [20, 80]

    def apply_strategy_for_a_row(self, marketPrice_row):
        sto_row = IndicatorStochastic.get_record_by_market_interval_date(self.market, self.interval, marketPrice_row['date'])
        close_price = sto_row['close_price'].tolist()[0]
        stochastic_k = sto_row['stochastic_k'].tolist()[0]
        stochastic_d = sto_row['stochastic_d'].tolist()[0]

        # Seuils pour la stratégie Bollinger
        oversold_threshold = self.params[0]  # Acheter si bb_percent est proche de 0%
        overbought_threshold = self.params[1]  # Vendre si bb_percent est proche de 100%

        # Exemple de logique de stratégie
        if stochastic_k < oversold_threshold and stochastic_k > stochastic_d:
            return "buy"
        elif stochastic_k > overbought_threshold and stochastic_k < stochastic_d:
            return "sell"
        else:
            return "wait"





def execute_trading(market, interval):
    market_price_qs = MarketPrice.objects.filter(market=market, interval_time=interval).order_by('date')
    df = pd.DataFrame(list(market_price_qs.values()))
    # Ensure the 'close_price' column is in float format
    df['close_price'] = df['close_price'].astype(float)

    start_time = time.time()
    
    #Without Backtest
    start_time2 = time.time()
    strategy_tendance = StrategyTendance(market, interval, df)
    print("    3.StrategyTendance  " + str((time.time() - start_time2) / 60))

    start_time2 = time.time()
    strategy_macd = StrategyMACD(market, interval, df)
    print("    3.StrategyMACD  " + str((time.time() - start_time2) / 60))

    start_time2 = time.time()
    strategy_ichimoku = StrategyIchimoku(market, interval, df)
    print("    3.StrategyIchimoku  " + str((time.time() - start_time2) / 60))

    #With Backtest
    start_time2 = time.time()
    strategy_2sma = Strategy2SMA(market, interval, df)
    apply_backtest_for_get_params(df, strategy_2sma, market, interval)
    print("    3.Strategy2SMA  " + str((time.time() - start_time2) / 60))

    start_time2 = time.time()
    strategy_bb = StrategyBollingerBand(market, interval, df)
    apply_backtest_for_get_params(df, strategy_bb, market, interval)
    print("    3.StrategyBollingerBand  " + str((time.time() - start_time2) / 60))

    start_time2 = time.time()
    strategy_rsi = StrategyRSI(market, interval, df)
    apply_backtest_for_get_params(df, strategy_rsi, market, interval)
    print("    3.StrategyRSI  " + str((time.time() - start_time2) / 60))

    start_time2 = time.time()
    strategy_stochastic = StrategyStochastique(market, interval, df)
    apply_backtest_for_get_params(df, strategy_stochastic, market, interval)
    print("    3.StrategyStochastic  " + str((time.time() - start_time2) / 60))

    strategies = [strategy_tendance, strategy_macd, strategy_ichimoku, strategy_2sma, strategy_bb, strategy_rsi, strategy_stochastic]
    # strategies = [strategy_rsi]
    print("    3.create_strategies  " + str((time.time() - start_time) / 60))

    marketstrategyresult = {
        "name": market,
        "date": None,
        "interval_time": interval,
        "strategy_tendance_color": 'red',
        "strategy_macd_color": 'red',
        "strategy_ichimoku_color": 'red',
        "strategy_2sma_color": 'red',
        "strategy_bb_color": 'red',
        "strategy_rsi_color": 'red',
        "strategy_stochastic_color": 'red'
    }

    for strategy in strategies:
        for index, row in df.iterrows():
            action = strategy.apply_strategy_for_a_row(row)  # Exécuter la stratégie
            TradingResult.apply_strategies_and_save(market, interval, action, strategy, row)  # Enregistrer le résultat
            if index == df.index[-1]:
                existing_trade = TradingResult.get_record(market, interval, strategy.get_name())
                if existing_trade is not None and existing_trade.date_end == "":
                    if strategy.get_name() == "Tendance":
                        marketstrategyresult["strategy_tendance_color"] = "green" 
                    if strategy.get_name() == "BollingerBand":
                        marketstrategyresult["strategy_bb_color"] = "green"
                    if strategy.get_name() == "RSI":
                        marketstrategyresult["strategy_rsi_color"] = "green"
                    if strategy.get_name() == "MACD":
                        marketstrategyresult["strategy_macd_color"] = "green"
                    if strategy.get_name() == "2MM":
                        marketstrategyresult["strategy_2sma_color"] = "green"
                    if strategy.get_name() == "Ichimoku":
                        marketstrategyresult["strategy_ichimoku_color"] = "green"
                    if strategy.get_name() == "Stochastic":
                        marketstrategyresult["strategy_stochastic_color"] = "green"
                    marketstrategyresult["date"] = row['date']
                
    print(marketstrategyresult)
    MarketStrategyResult.save_market_strategy_result(marketstrategyresult)