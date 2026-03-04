import requests
import io
import pandas as pd
import sqlite3

def maj_table_ventes():
    # L'URL vers le CSV ventes
    # "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
    url_brief = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub"

    # Requête HTTP
    requete_http = requests.get(url_brief, params={"gid":"760830694", "single":"true", "output":"csv"})
    # Transforme la réception de texte brut et simule un accès à un fichier
    fichier = io.StringIO(requete_http.text)

    try:
        # Lecture du fichier dans une data frame et on renomme les colonnes pour qu'elles correspondent exactement à notre base de données
        df_ventes = pd.read_csv(fichier)
        df_ventes = df_ventes.rename(columns={
            'ID RÃ©fÃ©rence produit': 'id_ref_produit',
            'ID Magasin': 'id_magasin',
            'Date': 'date',
            'QuantitÃ©': 'quantite'
        })

        # Connexion à la base de données
        connexion = sqlite3.connect('../BDD/ventes_magasins.db')
        pointeur = connexion.cursor()

        # Création d'une table temporaire 'ventes_temp' des ventes lues dans le CSV et qui sont potentiellement à ajouter
        df_ventes.to_sql('ventes_temp', connexion, if_exists='replace', index=False)

        # Requête SQL qui ajoute les ventes non existantes. 
        # Si existantes la quantité est mise à jour par sécurité en cas de mise à jour ultérieure de la quantité vendue
        requete_sql = '''
            INSERT INTO ventes (id_ref_produit, id_magasin, date, quantite)
            SELECT id_ref_produit, id_magasin, date, quantite FROM ventes_temp
            WHERE true
            ON CONFLICT(id_ref_produit, id_magasin, date) 
            DO UPDATE SET quantite = excluded.quantite
        '''

        # Execution de la requête
        pointeur.execute(requete_sql)

        # Suppression de la table temporaire
        pointeur.execute('DROP TABLE ventes_temp')

        print("La table 'ventes' a été mise à jour.\n")

        # Commit et fermeture de la connection à la base de données
        connexion.commit()
        connexion.close()

    except Exception as e:
        # Affichage des erreurs éventuelles
        print(f"Erreur lors de la mise à jour sur la table ventes : {e}")
