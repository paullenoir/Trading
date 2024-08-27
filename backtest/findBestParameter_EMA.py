import json

def backtest_EMA(symbols, cursor):
    def calculate_metrics(trades):
        """Helper function to calculate metrics from trades."""
        average_positive_trade = sum(trade for trade in trades if trade > 0) / len([trade for trade in trades if trade > 0]) if any(trade > 0 for trade in trades) else 0.0
        average_negative_trade = sum(trade for trade in trades if trade < 0) / len([trade for trade in trades if trade < 0]) if any(trade < 0 for trade in trades) else 0.0
        worst_drawback = min(trades) if trades else 0.0
        trades_count = len(trades)
        return trades_count, worst_drawback, average_positive_trade, average_negative_trade


    def EMA_strategy(symbol, short_ema, long_ema, cursor):
        """Backtesting strategy using only two EMAs."""
        trades = []
        current_position = None
        entry_price = 0.0

        # Fetch data
        cursor.execute(f"""
            SELECT date, close_price, EMA{short_ema}, EMA{long_ema}
            FROM StrategyDataEMA
            WHERE symbol = ?
            ORDER BY date
        """, (symbol,))
        data = cursor.fetchall()

        for date, close_price, short_ema_value, long_ema_value in data:
            if short_ema_value is None or long_ema_value is None:
                continue

            if short_ema_value > long_ema_value and current_position is None:
                current_position = 'long'
                entry_price = close_price

            elif short_ema_value < long_ema_value and current_position == 'long':
                profit = close_price - entry_price
                trades.append(profit)
                current_position = None

        return calculate_metrics(trades), {"EMA_courte": short_ema, "EMA_longue": long_ema}

    def EMA_Tp_Sl_strategy(symbol, short_ema, long_ema, cursor):
        """Backtesting strategy using two EMAs with take profit and stop loss."""
        trades = []
        current_position = None
        entry_price = 0.0

        cursor.execute(f"""
            SELECT date, close_price, EMA{short_ema}, EMA{long_ema}
            FROM StrategyDataEMA
            WHERE symbol = ?
            ORDER BY date
        """, (symbol,))
        data = cursor.fetchall()

        for date, close_price, short_ema_value, long_ema_value in data:
            if short_ema_value is None or long_ema_value is None:
                continue

            if short_ema_value > long_ema_value and current_position is None:
                current_position = 'long'
                entry_price = close_price

            if current_position == 'long':
                profit_percentage = (close_price - entry_price) / entry_price * 100

                if profit_percentage >= 12:
                    trades.append(close_price - entry_price)
                    current_position = None
                elif profit_percentage <= -2:
                    trades.append(close_price - entry_price)
                    current_position = None
                elif short_ema_value < long_ema_value:
                    trades.append(close_price - entry_price)
                    current_position = None

        return calculate_metrics(trades), {"EMA_courte": short_ema, "EMA_longue": long_ema}

    
    # Définition des périodes d'EMA
    ema_periods = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

    # Itération sur chaque symbole et chaque paire d'EMA
    for symbol_row in symbols:
        symbol = symbol_row[0]
        best_result_ema = {"metrics": None, "params": None}
        best_result_ema_tp_sl = {"metrics": None, "params": None}

        for i in range(len(ema_periods)):
            for j in range(i + 1, len(ema_periods)):
                short_ema_period = ema_periods[i]
                long_ema_period = ema_periods[j]

                # Effectuer le backtesting
                # resultTemps.append(perform_backtest_for_pair(symbol, short_ema_period, long_ema_period, cursor))

                # Backtest with EMA strategy
                metrics, params = EMA_strategy(symbol, short_ema_period, long_ema_period, cursor)
                if best_result_ema["metrics"] is None or metrics[2] > best_result_ema["metrics"][2]:
                    best_result_ema = {"metrics": metrics, "params": params}

                # Backtest with EMA + Tp/Sl strategy
                metrics, params = EMA_Tp_Sl_strategy(symbol, short_ema_period, long_ema_period, cursor)
                if best_result_ema_tp_sl["metrics"] is None or metrics[2] > best_result_ema_tp_sl["metrics"][2]:
                    best_result_ema_tp_sl = {"metrics": metrics, "params": params}

        # max_avg_positive_trade_index = max(range(len(resultTemps)), key=lambda i: resultTemps[i]['average_positive_trade'])

        # Save results for EMA strategy
        cursor.execute("""
            INSERT INTO Backtest (
                symbol,
                strategyName,
                tradesCount,
                worstDrawback,
                averagePositifTrade,
                averageNegativeTrade,
                strategyParameter
            ) VALUES (?, '2EMA', ?, ?, ?, ?, ?)
        """, (
            symbol,
            best_result_ema["metrics"][0],
            best_result_ema["metrics"][1],
            best_result_ema["metrics"][2],
            best_result_ema["metrics"][3],
            json.dumps(best_result_ema["params"])
        ))

        # Save results for EMA + Tp/Sl strategy
        cursor.execute("""
            INSERT INTO Backtest (
                symbol,
                strategyName,
                tradesCount,
                worstDrawback,
                averagePositifTrade,
                averageNegativeTrade,
                strategyParameter
            ) VALUES (?, '2EMA+TakeProfit/StopLoss', ?, ?, ?, ?, ?)
        """, (
            symbol,
            best_result_ema_tp_sl["metrics"][0],
            best_result_ema_tp_sl["metrics"][1],
            best_result_ema_tp_sl["metrics"][2],
            best_result_ema_tp_sl["metrics"][3],
            json.dumps(best_result_ema_tp_sl["params"])
        ))