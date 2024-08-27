from flask import Flask, jsonify, url_for, render_template_string, request
from data.database_handler import DatabaseHandler
from Application.methodeRouteHome import generate_table_html, render_html_page
from Application.methodeRouteCandle import create_candlestick_chart, generate_candle_html
from Application.methodeRouteMM import add_moving_averages_and_trades, determine_trade_color

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        db_handler = DatabaseHandler("database.db")
        df = db_handler.get_all_market()
        if df.empty:
            ticker_dict = {}
        else:
            ticker_dict = {'tickers': []}
            # Remplir la liste associée à la clé 'tickers'
            for ticker in df['symbol']:
                ticker_dict['tickers'].append(ticker)
        table_html = generate_table_html(db_handler,ticker_dict)
        return render_html_page(table_html)
    
    @app.route('/candle/<symbol>', methods=['GET'])
    def candle(symbol):
        db_handler = DatabaseHandler("database.db")
        
        # Récupérer les données candlestick
        candlestick_df = db_handler.get_marketPrice(symbol)
        fig = create_candlestick_chart(candlestick_df)

        # Convertir le graphique Plotly en HTML
        graph_html = fig.to_html(full_html=False)
        
        return render_template_string(generate_candle_html(symbol, graph_html))
    
    @app.route('/<symbol>/mm', methods=['GET'])
    def candle_mm(symbol):
        db_handler = DatabaseHandler("database.db")
        
        # Récupérer les données candlestick
        candlestick_df = db_handler.get_marketPrice(symbol)
        fig = create_candlestick_chart(candlestick_df)

        # Ajouter les moyennes mobiles et les annotations des trades
        add_moving_averages_and_trades(fig, db_handler, symbol)
        
        # Convertir le graphique Plotly en HTML
        graph_html = fig.to_html(full_html=False)

        return render_template_string(generate_candle_html(symbol, graph_html))
    
    return app