from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import sqlite3
import os

def get_all_new_marketprice(database_handler):
    start_time = time.time()
    market_data_df = database_handler.get_all_market()
    for index, row in tqdm(market_data_df.iterrows(), total=market_data_df.shape[0]):
        if row['yahooDownload'] is not None and "None" not in row['yahooDownload']:
            symbol = row['symbol'] 
            # Configurer les options pour Firefox
            firefox_options = Options()
            firefox_options.add_argument("--headless")  # Exécuter Firefox en mode headless
            firefox_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU (optionnelle)
            firefox_options.add_argument("--window-size=1920x1080")  # Taille de la fenêtre (optionnelle)

            driver = webdriver.Firefox(options=firefox_options)
            print(row['yahooDownload'])
            driver.get(row['yahooDownload'])
            time.sleep(3)
            driver.find_element(By.ID, "scroll-down-btn").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[2]/button[1]").click()
            time.sleep(1)

            #new stock avoir tout l'historique
            # try:
            #     driver.find_element(By.XPATH, "//*[@id='nimbus-app']/section/section/section/article/div[1]/div[1]/div[1]/button").click()
            #     time.sleep(1)
            #     driver.find_element(By.XPATH, "//*[@id='menu-30']/div[2]/section/div[1]/button[8]").click()
            # except:
            #     driver.find_element(By.XPATH, "/html/body/div[1]/main/section/section/section/article/div[1]/div[1]/div[1]/button/span").click()
            #     time.sleep(1)
            #     driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/div[1]/div").click()
            
            time.sleep(5)
            elem = driver.find_element(By.XPATH, "//*[@id='nimbus-app']/section/section/section/article/div[1]/div[3]/table")
            time.sleep(5)
            rows = elem.find_elements("tag name", "tr")
            # Liste pour stocker les données
            data = []
            # Parcourez chaque ligne et récupérez les données
            for row in rows:
                cols = row.find_elements("tag name", "td")
                # Vérifiez que la ligne contient des colonnes (pour éviter les en-têtes vides)
                if len(cols) == 7:
                    row_data = {}
                    i = 0
                    for col in cols:
                        if i == 0:
                            row_data['date'] = col.text
                        elif i == 1:
                            row_data['open_price'] = col.text
                        elif i == 2:
                            row_data['high_price'] = col.text
                        elif i == 3:
                            row_data['low_price'] = col.text
                        elif i == 4:
                            row_data['close_price'] = col.text
                        elif i == 6:
                            row_data['volume'] = col.text
                        i += 1
                    data.append(row_data)

            # Créez un DataFrame à partir des données collectées
            df = pd.DataFrame(data)
            print(df)
            indices_sorted_desc = df.index.tolist()
            for index in reversed(indices_sorted_desc):
                row = df.loc[index]
                database_handler.create_marketPrices(
                    symbol,
                    row['low_price'],
                    row['high_price'],
                    row['open_price'],
                    row['close_price'],
                    'day',
                    row['date']
                )
            driver.close()
        time.sleep(5)

    # create MM data from fichier SQL
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/database.db'))
    cursor = conn.cursor()
    script_dir = os.path.dirname(__file__)  # Répertoire du script Python
    bourse_dir = os.path.abspath(os.path.join(script_dir, '..'))  # Aller au dossier parent (Bourse)
    sql_path = os.path.join(bourse_dir, 'SQL', 'createDataMM.sql')  # Construire le chemin complet vers le fichier SQL
    with open(sql_path, 'r') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

    #executer backtest
    from backtest.findBestParameter_MM import backtest_MM
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/database.db'))
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT symbol FROM StrategyDataMM")
    symbols = cursor.fetchall()
    backtest_MM(symbols, cursor)
    # backtest_EMA(symbols, cursor)
    conn.commit()
    conn.close()

    #executer strategy
    from Strategy.strategy_MM import strategyMM
    strategyMM()

    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print(elapsed_time)

def testGetData(database_handler):
    url = "https://finance.yahoo.com/quote/AAPL.NE/history/"

    # Configurer les options pour Firefox
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Exécuter Firefox en mode headless
    firefox_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU (optionnelle)
    firefox_options.add_argument("--window-size=1920x1080")  # Taille de la fenêtre (optionnelle)

    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.ID, "scroll-down-btn").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[2]/button[1]").click()
    time.sleep(5)
    elem = driver.find_element(By.XPATH, "//*[@id='nimbus-app']/section/section/section/article/div[1]/div[3]/table")
    time.sleep(5)
    time.sleep(5)
    rows = elem.find_elements("tag name", "tr")
    # Liste pour stocker les données
    data = []
    # Parcourez chaque ligne et récupérez les données
    for row in rows:
        cols = row.find_elements("tag name", "td")
        # Vérifiez que la ligne contient des colonnes (pour éviter les en-têtes vides)
        if len(cols) == 7:
            row_data = {}
            i = 0
            for col in cols:
                if i == 0:
                    row_data['date'] = col.text
                elif i == 1:
                    row_data['open_price'] = col.text
                elif i == 2:
                    row_data['high_price'] = col.text
                elif i == 3:
                    row_data['low_price'] = col.text
                elif i == 4:
                    row_data['close_price'] = col.text
                elif i == 6:
                    row_data['volume'] = col.text
                i += 1
            data.append(row_data)

    # Créez un DataFrame à partir des données collectées
    df = pd.DataFrame(data)
    print(df)