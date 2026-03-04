import sqlite3
import pandas as pd

def calcul_ca_total():
    try:
        # Connexion à la base de données
        connexion = sqlite3.connect('../BDD/ventes_magasins.db')
        
        # Requête SQL
        requete_sql = '''
            SELECT SUM(ventes.quantite * produits.prix) as CA_TOTAL
            FROM ventes, produits
            WHERE ventes.id_ref_produit = produits.id_ref_produit
        '''

        # Execution de la requête et stockage du résultat dans une dataframe
        df_ca_total = pd.read_sql_query(requete_sql, connexion)
        print("Chiffre d'affaires total :")
        print(df_ca_total)
        
        # On alimente le résultat de l'analyse dans la base
        df_ca_total.to_sql('analyse_ca', connexion, if_exists='replace', index=False)
        print("(analyse stockée)\n")

        # Fermeture de la connection à la base de données
        connexion.close()

    except Exception as e:
        print(f"Erreur lors du calcul du chiffre d'affaire total : {e}")


def calcul_ventes_produits():
    try:
        # Connexion à la base de données
        connexion = sqlite3.connect('../BDD/ventes_magasins.db')
        
        # Requête SQL
        requete_sql = '''
            SELECT
                produits.nom as PRODUIT,
                IFNULL(SUM(ventes.quantite), 0) as QTE_VENDUE,
                AVG(produits.prix) as PRIX_UNITAIRE,
                IFNULL(SUM(ventes.quantite * produits.prix), 0) as VENTES
            FROM produits
            LEFT JOIN ventes ON ventes.id_ref_produit = produits.id_ref_produit
            GROUP BY produits.nom
            ORDER BY VENTES DESC, produits.nom ASC
        '''

        # Execution de la requête et stockage du résultat dans une dataframe
        df_ventes_produit = pd.read_sql_query(requete_sql, connexion)
        print("Ventes par produit :")
        print(df_ventes_produit)

        # On alimente le résultat de l'analyse dans la base
        df_ventes_produit.to_sql('analyse_ventes_produits', connexion, if_exists='replace', index=False)
        print("(analyse stockée)\n")
        
        # Fermeture de la connection à la base de données
        connexion.close()

    except Exception as e:
        print(f"Erreur lors du calcul des ventes par produit : {e}")


def calcul_ventes_magasin():
    try:
        # Connexion à la base de données
        connexion = sqlite3.connect('../BDD/ventes_magasins.db')
        
        # Requête SQL
        requete_sql = '''
            SELECT
                magasins.ville as MAGASIN,
                IFNULL(SUM(ventes.quantite * produits.prix), 0) as VENTES
            FROM magasins
            LEFT JOIN ventes ON ventes.id_magasin = magasins.id_magasin
            LEFT JOIN produits ON produits.id_ref_produit = ventes.id_ref_produit
            GROUP BY magasins.ville
            ORDER BY VENTES DESC, magasins.ville ASC
        '''

        # Execution de la requête et stockage du résultat dans une dataframe
        df_ventes_magasin = pd.read_sql_query(requete_sql, connexion)
        print("Ventes par magasin :")
        print(df_ventes_magasin)

        # On alimente le résultat de l'analyse dans la base
        df_ventes_magasin.to_sql('analyse_ventes_magasins', connexion, if_exists='replace', index=False)
        print("(analyse stockée)\n")
        
        # Fermeture de la connection à la base de données
        connexion.close()

    except Exception as e:
        print(f"Erreur lors du calcul des ventes par magasin : {e}")


