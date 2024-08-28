from data.database_handler import DatabaseHandler

def strategyMM():
    db_handler = DatabaseHandler("database.db")
    symbols = db_handler.get_all_market()

    for index, row in symbols.iterrows():
        current_position = None
        symbol = row["symbol"]
        data_strategy = {}

        # Récupérer les paramètres de la stratégie pour le symbole
        backtest_result = db_handler.get_backtest(symbol)

        if backtest_result is not None and "None" not in backtest_result:
            # Extraire les valeurs des moyennes mobiles de la meilleure stratégie `2MM`
            strategy_params = backtest_result[backtest_result['strategyName'] == '2MM']['strategyParameter'].values[0]
            strategy_params = eval(strategy_params)  # Convertir la chaîne JSON en dictionnaire
            mm_short = strategy_params.get('MMcourte')
            mm_long = strategy_params.get('MMlongue')
        
            data = db_handler.get_movingAverage(symbol, mm_short, mm_long)
            date_start = ""
            i = 0
            #Strategy
            for index, row in data.iterrows():
                date, close_price, short_mm_value, long_mm_value = row
                if short_mm_value is None or long_mm_value is None:
                    continue
                else:  # "2MM"
                    if short_mm_value > long_mm_value:
                        if current_position is None:
                            current_position = 'long'
                            date_start = date
                            data_strategy[i] = {
                                "strategyParameter": {"MMcourte": mm_short, "MMlongue": mm_long},
                                "tradeDateStart": date_start,
                                "buyPrice": close_price,
                                "trading": "achat",
                                "profitIsPositif": "InProgress",
                                "dollarProfit": "",
                                "percentProfit": ""
                            }

                    elif short_mm_value < long_mm_value and current_position == 'long':
                        profitIsPositif = "False"
                        if close_price > data_strategy[i]["buyPrice"]:
                            profitIsPositif = "True"
                        data_strategy[i].update({
                            "tradeDateEnd": date,
                            "sellPrice": close_price,
                            "profitIsPositif": profitIsPositif,
                            "trading": "vente",
                            "dollarProfit": round(close_price - data_strategy[i]["buyPrice"], 2),
                            "percentProfit": round(((close_price * 100 / data_strategy[i]["buyPrice"]) - 100), 2)
                        })
                        current_position = None
                        date_start = ""
                        i = i + 1        

        # Enregistrer les meilleurs résultats pour 2MM
        db_handler.create_tradingResult(symbol, "2MM" , str(data_strategy))