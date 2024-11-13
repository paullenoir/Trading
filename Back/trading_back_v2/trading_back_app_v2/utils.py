# Fonctions utilitaires si nécessaire
import pandas as pd

# Fonction pour valider le DataFrame reçu
def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Vérification et correction des valeurs manquantes
    missing_values = df.isnull().sum()
    if missing_values.any():
        # Remplacer les valeurs manquantes par la valeur précédente
        df.fillna(method='ffill', inplace=True)
        print("Valeurs manquantes corrigées avec la valeur précédente.")
    
    # Vérification et correction des doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        # Supprimer les doublons
        df.drop_duplicates(inplace=True)
        print("Doublons supprimés.")

    return df

# Ajout des week end dans le Dataframe pour tester la fin de semaine
def transform_dataframe(df):
    # Ajoute les valeurs du vendredi pour le samedi et dimanche
    vendredi_indices = df.index[df.index.dayofweek == 4]   # 4 correspond à vendredi

    # Crée une liste pour stocker les nouvelles lignes
    new_rows = []

    for date in vendredi_indices:
        row = df.loc[date]  # Récupère la ligne correspondante
        # Crée une ligne pour samedi
        samedi = row.copy()
        samedi.name = pd.to_datetime(date) + pd.Timedelta(days=1)  # Met à jour la date pour samedi
        new_rows.append(samedi)

        # Crée une ligne pour dimanche
        dimanche = row.copy()
        dimanche.name = pd.to_datetime(date) + pd.Timedelta(days=2)  # Met à jour la date pour dimanche
        new_rows.append(dimanche)

    # Concatène les nouvelles lignes au DataFrame existant
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], axis=0)

    return df.sort_index()  # Trie le DataFrame par index

def alogorythm_smma(df, column_name, period):
    # Ensure the column is in float format
    df[column_name] = df[column_name].astype(float)

    # Calculate SMMA
    smma = df[column_name].rolling(window=period, min_periods=1).mean()
    
    for i in range(period, len(df)):
        smma.iloc[i] = (smma.iloc[i-1] * (period - 1) + df[column_name].iloc[i]) / period
    
    return smma

def determine_trend(slope):
    if slope > 0:
        return "increase"
    elif slope < 0:
        return "decrease"
    else:
        return "stable"
    
def all_increase(row):
    return str((
        row['tendance_EMA20'] == "increase" and 
        row['tendance_EMA50'] == "increase" and 
        row['tendance_EMA200'] == "increase"
    ))