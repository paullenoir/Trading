from trading_back_app_v2.strategies import *
from trading_back_app_v2.models import Backtest

def apply_backtest_for_get_params(df, strategy, market, interval):
        """Méthode générique pour l'optimisation des paramètres"""
        results = []  # contient le profit obtenu pour chaque combinaison
        # df = MarketPrice.get_all_record(market, interval)

        params = strategy.get_paramsBacktest()
        param_1 = params[0]
        param_2 = params[1] if len(params) > 1 else [None]  # Si pas de second paramètre, on met [None]

        for i in range(len(param_1)):
            if param_2[0] is None:  # Si seulement un paramètre
                param1 = param_1[i]
                strategy.params[0] = param1
                results.append(execute_strategy_for_backtest(strategy, market, interval,df))
            else:  # Si deux paramètres
                for j in range(len(param_2)):
                    param1 = param_1[i]
                    param2 = param_2[j]
                    if param1 != param2:
                        strategy.params[0] = param1
                        strategy.params[1] = param2
                        results.append(execute_strategy_for_backtest(strategy, market, interval, df))

        # Sélectionner les meilleurs résultats basés sur un critère (ex: averagePositifTrade)
        best_result = max(results, key=lambda res: res['averagePositifTrade'])
        Backtest.save_backtest(best_result)  # sauvegarder l'enregistrement avec le meilleur profit

def execute_strategy_for_backtest(strategy, market, interval, df):
    # Initialisation des variables
    trades_count = 0
    positive_trades = []
    negative_trades = []
    current_position = None
    entry_price = 0.0
    max_drawback = 0.0

    for index, row in df.iterrows():
        close_price = row['close_price']
        action = strategy.apply_strategy_for_a_row(row)

        if action == "buy":
            if current_position is None:
                current_position = 'long'
                entry_price = close_price

        elif action == "sell":
            trades_count += 1
            profit = close_price - entry_price
            if profit > 0:
                positive_trades.append(profit)
            else:
                negative_trades.append(profit)
                max_drawback = min(max_drawback, profit)
            current_position = None

    # Calcul des métriques
    average_positive_trade = sum(positive_trades) / len(positive_trades) if positive_trades else 0.0
    average_negative_trade = sum(negative_trades) / len(negative_trades) if negative_trades else 0.0

    result = {
        'market': market,
        'interval_time': interval,
        'strategyName': strategy.get_name(),
        'tradesCount': trades_count,
        'worstDrawback': max_drawback,
        'averagePositifTrade': average_positive_trade,
        'averageNegativeTrade': average_negative_trade,
    }

    # Ajoute param1 et param2 si param2 n'est pas None
    if len(strategy.params) > 1 and strategy.params[1] is not None:
        result['strategyParameter'] = str([strategy.params[0], strategy.params[1]])
    else:
        result['strategyParameter'] = str([strategy.params[0]])  # Ajoute seulement param1

    return result