import pandas as pd
import plotly.graph_objs as go

def create_candlestick_chart(candlestick_df):
    df = pd.DataFrame(candlestick_df)
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open_price'],
        high=df['high_price'],
        low=df['low_price'],
        close=df['close_price'])])
    return fig


def generate_candle_html(symbol, graph_html):
    return f'''
    <html>
        <head>
            <title>Candlestick Chart - {symbol}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        </head>
        <body>
            <h1>Candlestick Chart for {symbol}</h1>
            <button onclick="location.href='/{symbol}/mm'">2MM</button>
            <div id="chart">{graph_html}</div>
        </body>
    </html>
    '''