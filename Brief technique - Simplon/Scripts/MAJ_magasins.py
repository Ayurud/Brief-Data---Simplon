import requests
import io
import pandas as pd
import sqlite3

def maj_table_magasins():
    # L'URL vers le CSV magasins
    # "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
    url_brief = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub"
    
    # Requête HTTP
    requete_http = requests.get(url_brief, params={"gid":"714623615", "single":"true", "output":"csv"})
    # Encodage (format du CSV pour les accents)
    requete_http.encoding = 'utf-8'
    # Transforme la réception de texte brut et simule un accès à un fichier
    fichier = io.StringIO(requete_http.text)

    try:
        # Lecture du fichier dans une data frame
        df_magasins = pd.read_csv(fichier)
        df_magasins = df_magasins.rename(columns={
            'ID Magasin': 'id_magasin',
            'Ville': 'ville',
            'Nombre de salariés': 'nb_salaries'
        })

        # Connexion à la base de données
        connexion = sqlite3.connect('../BDD/ventes_magasins.db')
        
        # Export de la data frame vers la base, on écrase les données si existantes
        df_magasins.to_sql('magasins', connexion, if_exists='replace', index=False)
        print("\nLa table 'magasins' a été mise à jour.")
        
        # Fermeture de la connection à la base de données
        connexion.close()

    except Exception as e:
        # Affichage des erreurs éventuelles
        print(f"Erreur lors de la mise à jour sur la table magasins : {e}")






