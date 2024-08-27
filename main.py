import multiprocessing
from data.yahoo import get_all_new_marketprice, testGetData
from time import sleep
from Application.visualisation import *
import webbrowser
from data.database_handler import DatabaseHandler

def run_flask_app():
    app = create_app()
    def open_browser():
        sleep(1)  # Attendre une seconde pour que le serveur Flask démarre
        webbrowser.open('http://127.0.0.1:5000')

    # Ouvrir le navigateur dans le même processus que Flask
    open_browser()
    app.run(port=5000)

if __name__ == "__main__":
    # Créer des processus pour chaque partie
    database_handler = DatabaseHandler("database.db")
    processes = [
        #1. Store Stock Data In BD + datastrategy + strategy
        # multiprocessing.Process(target=get_all_new_marketprice(database_handler))
        # multiprocessing.Process(target=testGetData(database_handler))

        #2. Visualisation
        multiprocessing.Process(target=run_flask_app)
    ]

    # Démarrer les processus
    for process in processes:
        process.start()

    # Assurer que le programme principal attend la fin des processus (ce qui n'arrive jamais ici)
    for process in processes:
        process.join()