import json
import plotly.graph_objs as go
import re
from datetime import datetime, timedelta

def add_moving_averages_and_trades(fig, db_handler, symbol):
    best_2mm_strategy = db_handler.get_backtest(symbol).query("strategyName == '2MM'")
    strategy_param = json.loads(best_2mm_strategy.iloc[0]['strategyParameter'])
    short_mm = f"MM{strategy_param['MMcourte']}"
    long_mm = f"MM{strategy_param['MMlongue']}"
    
    moving_avg_df = db_handler.get_movingAverage(symbol)
    short_mm_values = moving_avg_df[short_mm]
    long_mm_values = moving_avg_df[long_mm]

    fig.add_trace(go.Scatter(x=moving_avg_df['date'], y=short_mm_values, mode='lines', name=f'{short_mm}'))
    fig.add_trace(go.Scatter(x=moving_avg_df['date'], y=long_mm_values, mode='lines', name=f'{long_mm}'))

    data_strategy = db_handler.get_tradingResult(symbol, "2MM")
    json_string = data_strategy['strategyData'].iloc[0].replace("'", '"')
    json_string = re.sub(r"(?<!\w)(\d+)(?!\w):", r'"\1":', json_string)
    data = json.loads(json_string)

    for trade in data.values():
        trade_date_start = trade['tradeDateStart']
        trade_date_end = trade.get('tradeDateEnd', (datetime.now() - timedelta(days=0)).strftime('%b %d, %Y')) 
        profit_is_positive = trade['profitIsPositif']

        color = determine_trade_color(profit_is_positive)

        fig.add_shape(
            type="rect",
            x0=trade_date_start,
            x1=trade_date_end,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            fillcolor=color,
            opacity=0.4,
            layer="below",
            line_width=0,
        )

        fig.add_annotation(
            x=trade_date_start,
            y=1,
            xref="x",
            yref="paper",
            text=trade['percentProfit'],
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center",
        )


def determine_trade_color(profit_is_positive):
    if profit_is_positive == "True":
        return "LightGreen"
    elif profit_is_positive == "False":
        return "LightCoral"
    elif profit_is_positive == "InProgress":
        return "#FFFF00"
    return ""