from flask import url_for
import json
import re

def generate_table_html(db_handler, ticker_dict):
    # Commencer par l'en-tête des colonnes avec "2MM" en première colonne
    row_thead = "<thead><tr><th>Stock</th><th>2MM</th></tr></thead>"
    rows_tbody = "<tbody>"
    
    for letter, symbols in ticker_dict.items():
        for symbol in symbols:
            # Créer une ligne pour chaque stock
            row_html = f"<tr><th><button onclick=\"location.href='{url_for('candle', symbol=symbol)}'\">{symbol}</button></th>"
            # Ajouter la cellule pour la stratégie 2MM
            row_html += generate_strategy1_cell(db_handler, symbol)
            row_html += "</tr>"
            rows_tbody += row_html
    
    rows_tbody += "</tbody>"
    return row_thead + rows_tbody

def generate_strategy1_cell(db_handler, symbol):
    data_strategy = db_handler.get_tradingResult(symbol, "2MM")
    json_string = data_strategy['strategyData'].iloc[0]
    json_string = json_string.replace("'", '"')
    json_string = re.sub(r"(?<!\w)(\d+)(?!\w):", r'"\1":', json_string)
    data = json.loads(json_string)
    last_trade_key = list(data.keys())[-1]
    last_trade = str(data[last_trade_key]['trading'])
    cell_style = 'style="background-color: green; color: white;"' if last_trade == "achat" else 'style="background-color: red; color: white;"'
    trade_details = format_trade_details(data[last_trade_key], symbol)
    return f'<td {cell_style}>{last_trade}<br><small>{trade_details}</small></td>'




def format_trade_details(trade_data,symbol):
    return f"""
    MMcourte: {trade_data['strategyParameter']['MMcourte']}<br>
    MMlongue: {trade_data['strategyParameter']['MMlongue']}<br>
    tradeDateStart: {trade_data['tradeDateStart']}<br>
    buyPrice: {trade_data['buyPrice']}<br>
    <button onclick="location.href='/{symbol}/mm?MM=true'">2MM</button>
    """


def render_html_page(inner_table):
    return f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                table {{
                    border-collapse: collapse;
                    table-layout: auto;  /* Laisse les colonnes s'ajuster automatiquement */
                }}
                th, td {{
                    padding: 5px;  /* Réduire le padding pour économiser de l'espace */
                    border: 1px solid #ddd;
                    white-space: nowrap;  /* Empêche le contenu de s'étendre sur plusieurs lignes */
                }}
                button {{
                    margin-left: 5px;
                    padding: 2px 5px;  /* Réduire la taille des boutons */
                    font-size: 12px;  /* Réduire la taille de la police des boutons */
                }}
                small {{
                    font-size: 10px;  /* Réduire la taille de la police des détails */
                }}
            </style>
        </head>
        <body>
            <table>
                {inner_table}
            </table>
        </body>
        </html>
    '''