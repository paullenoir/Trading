import os
import sqlite3
import pandas as pd

class DatabaseHandler():
    def __init__(self, database_name:str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        
        #retourne un tableau key/value et non une liste
        self.con.row_factory = sqlite3.Row

    def create_market(self, symbol: str):
        cursor = self.con.cursor()
        
        # Vérifier si l'entrée existe déjà
        query_check = """SELECT COUNT(*) FROM Market WHERE symbol = ?"""
        cursor.execute(query_check, (symbol))
        existing_entries = cursor.fetchone()[0]

        if existing_entries == 0:
            # Insérer les nouvelles données
            query_insert = """INSERT INTO Market (symbol) VALUES (?);"""
            cursor.execute(query_insert, (symbol))
            self.con.commit()
        cursor.close()

    def get_all_market(self):
        cursor = self.con.cursor()
        query = """SELECT * FROM Market;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        
        # Create a DataFrame from the fetched data
        columns = ['id','symbol', 'yahooDownload']
        market_data_df = pd.DataFrame(rows, columns=columns)
        
        return market_data_df

    def create_marketPrices(self, symbol: str, low_price: float, high_price: float , open_price: float , close_price: float, interval_time : str, date: str ):
        cursor = self.con.cursor()

        # Vérifier si l'entrée existe déjà
        query_check = """SELECT COUNT(*) FROM MarketPrices WHERE symbol = ? AND date = ?"""
        cursor.execute(query_check, (symbol, date))
        existing_entries = cursor.fetchone()[0]

        if existing_entries == 0:
            # Insérer les nouvelles données
            query_insert = """INSERT INTO MarketPrices (symbol, low_price, high_price, open_price, close_price, interval_time, date) 
                            VALUES (?, ?, ?, ?, ?, ?, ?);"""
            cursor.execute(query_insert, (symbol, low_price, high_price, open_price, close_price, interval_time, date))
            self.con.commit()
            # print("Nouvel enregistrement inséré avec succès.")
        # else:
        #     print(f"Une entrée avec le symbol '{symbol}' et la date '{date}' existe déjà.")

        cursor.close()
    
    def get_marketPrice(self, symbol: str):
        cursor = self.con.cursor()

        # Récupérer les données pour le symbole spécifié
        query = """SELECT * FROM MarketPrices WHERE symbol = ?"""
        cursor.execute(query, (symbol,))
        results = cursor.fetchall()
        
        cursor.close()

        if results:
            # Récupérer les noms des colonnes
            column_names = [description[0] for description in cursor.description]

            # Créer un DataFrame avec les résultats
            df = pd.DataFrame(results, columns=column_names)
            return df

    def get_movingAverage(self, symbol: str, short_mm: int = None, long_mm: int = None):
        cursor = self.con.cursor()

        # Récupérer les données pour le symbole spécifié
        query = """SELECT * FROM StrategyDataMM WHERE symbol = ?"""
        cursor.execute(query, (symbol,))
        results = cursor.fetchall()
        
        if results:
            # Récupérer les noms des colonnes
            column_names = [description[0] for description in cursor.description]

            # Créer un DataFrame avec les résultats
            df = pd.DataFrame(results, columns=column_names)

            # If short_mm and long_mm are provided, filter the DataFrame to return only those columns
            if short_mm and long_mm:
                short_mm_col = f"MM{short_mm}"
                long_mm_col = f"MM{long_mm}"

                if short_mm_col in df.columns and long_mm_col in df.columns:
                    df = df[['date', 'close_price', short_mm_col, long_mm_col]]
                else:
                    print(f"One or both of the moving averages MM{short_mm} or MM{long_mm} do not exist in the DataFrame.")

            cursor.close()
            return df
        
        cursor.close()
        return None
        
    def get_backtest(self, symbol: str):
        cursor = self.con.cursor()
        # print(symbol["symbol"])
        # Récupérer les données pour le symbole spécifié
        query = """SELECT * FROM Backtest WHERE symbol = ?"""
        cursor.execute(query, (symbol,))
        results = cursor.fetchall()
        
        cursor.close()

        if results:
            # Récupérer les noms des colonnes
            column_names = [description[0] for description in cursor.description]

            # Créer un DataFrame avec les résultats
            df = pd.DataFrame(results, columns=column_names)
            return df
                
        return None

    def create_tradingResult(self, symbol: str, strategyName: str, strategyData: str):
        cursor = self.con.cursor()

        # Vérifier si l'entrée existe déjà
        query_check = """SELECT COUNT(*) FROM TradingResult WHERE symbol = ? AND strategyName = ?"""
        cursor.execute(query_check, (symbol, strategyName))
        existing_entries = cursor.fetchone()[0]

        if existing_entries == 0:
            # Insérer les nouvelles données
            query_insert = """INSERT INTO TradingResult (symbol, strategyName, strategyData) 
                            VALUES (?, ?, ?);"""
            cursor.execute(query_insert, (symbol, strategyName, strategyData))
            self.con.commit()

        cursor.close()

    def get_tradingResult(self, symbol: str, strategyName: str):
        cursor = self.con.cursor()
        # Récupérer les données pour le symbole spécifié
        query = """SELECT * FROM TradingResult WHERE symbol = ? AND strategyName = ?"""
        cursor.execute(query, (symbol, strategyName))
        results = cursor.fetchall()
        
        cursor.close()

        if results:
            # Récupérer les noms des colonnes
            column_names = [description[0] for description in cursor.description]

            # Créer un DataFrame avec les résultats
            df = pd.DataFrame(results, columns=column_names)
            return df
                
        return None

    def __del__(self):
        # Fermer la connexion à la base de données lors de la destruction de l'objet
        if self.con:
            self.con.close()