import json

def backtest_MM(symbols, cursor):
    def execute_strategy(symbol, short_mm, long_mm, cursor, strategy_type, take_profit=None, stop_loss=None):
        # Initialisation des variables
        trades_count = 0
        positive_trades = []
        negative_trades = []
        current_position = None
        entry_price = 0.0
        max_drawback = 0.0
        previous_entry_price = 0.0

        # Récupération des données de stratégie pour le symbole
        cursor.execute(f"""
            SELECT date, close_price, MM{short_mm}, MM{long_mm}
            FROM StrategyDataMM
            WHERE symbol = ?
            ORDER BY date
        """, (symbol,))
        data = cursor.fetchall()

        for i in range(len(data)):
            date, close_price, short_mm_value, long_mm_value = data[i]

            if short_mm_value is None or long_mm_value is None:
                continue
            
            # Signal d'achat basé sur les moyennes mobiles
            if strategy_type == "2MM+takeProfit/StopLoss":
                # Check for entry condition
                if (short_mm_value > long_mm_value) and previous_entry_price < close_price:
                    if current_position is None:
                        current_position = 'long'
                        entry_price = close_price

                # If position is open, check for exit conditions
                if current_position == 'long':
                    profit_percentage = (close_price - entry_price) / entry_price * 100

                    if take_profit is not None and profit_percentage >= take_profit:
                        trades_count += 1
                        positive_trades.append(close_price - entry_price)
                        current_position = None

                    elif stop_loss is not None and profit_percentage <= stop_loss:
                        trades_count += 1
                        negative_trades.append(close_price - entry_price)
                        max_drawback = min(max_drawback, close_price - entry_price)
                        current_position = None

                    elif short_mm_value < long_mm_value:
                        trades_count += 1
                        profit = close_price - entry_price
                        if profit > 0:
                            positive_trades.append(profit)
                        else:
                            negative_trades.append(profit)
                            max_drawback = min(max_drawback, profit)
                        current_position = None

                previous_entry_price = close_price

            else:  # "2MM"
                if short_mm_value > long_mm_value:
                    if current_position is None:
                        current_position = 'long'
                        entry_price = close_price

                elif short_mm_value < long_mm_value and current_position == 'long':
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

        return {
            "trades_count": trades_count,
            "worst_drawback": max_drawback,
            "average_positive_trade": average_positive_trade,
            "average_negative_trade": average_negative_trade,
            "strategy_parameter": json.dumps({"MMcourte": short_mm, "MMlongue": long_mm})
        }

    # Définition des valeurs de moyennes mobiles
    mm_values = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

    for symbol_row in symbols:
        symbol = symbol_row[0]
        results_mm = []
        results_mm_tp_sl = []
        
        for i in range(len(mm_values)):
            for j in range(i + 1, len(mm_values)):
                short_mm = mm_values[i]
                long_mm = mm_values[j]

                # Effectuer le backtesting pour la stratégie 2MM
                results_mm.append(execute_strategy(symbol, short_mm, long_mm, cursor, "2MM"))

                # Effectuer le backtesting pour la stratégie 2MM+TakeProfit/StopLoss
                results_mm_tp_sl.append(execute_strategy(symbol, short_mm, long_mm, cursor, 
                                                         "2MM+takeProfit/StopLoss", take_profit=12, stop_loss=-2))

        # Enregistrer les meilleurs résultats pour 2MM
        best_mm = max(results_mm, key=lambda res: res['average_positive_trade'])
        cursor.execute("""
            INSERT INTO Backtest (
                symbol,
                strategyName,
                tradesCount,
                worstDrawback,
                averagePositifTrade,
                averageNegativeTrade,
                strategyParameter
            ) VALUES (?, '2MM', ?, ?, ?, ?, ?)
        """, (
            symbol,
            best_mm["trades_count"],
            best_mm["worst_drawback"],
            best_mm["average_positive_trade"],
            best_mm["average_negative_trade"],
            best_mm["strategy_parameter"]
        ))

        # Enregistrer les meilleurs résultats pour 2MM+TakeProfit/StopLoss
        best_mm_tp_sl = max(results_mm_tp_sl, key=lambda res: res['average_positive_trade'])
        cursor.execute("""
            INSERT INTO Backtest (
                symbol,
                strategyName,
                tradesCount,
                worstDrawback,
                averagePositifTrade,
                averageNegativeTrade,
                strategyParameter
            ) VALUES (?, '2MM+takeProfit/StopLoss', ?, ?, ?, ?, ?)
        """, (
            symbol,
            best_mm_tp_sl["trades_count"],
            best_mm_tp_sl["worst_drawback"],
            best_mm_tp_sl["average_positive_trade"],
            best_mm_tp_sl["average_negative_trade"],
            best_mm_tp_sl["strategy_parameter"]
        ))
