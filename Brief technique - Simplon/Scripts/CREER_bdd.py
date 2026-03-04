import sqlite3

# Fonction de création de la base de données
def creation_base():
    try:
        # Connexion et/ou création de la base de données
        connexion = sqlite3.connect('../BDD/ventes_magasins.db')
        pointeur = connexion.cursor()

        # Création de la table produits
        pointeur.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id_ref_produit TEXT,
                nom TEXT NOT NULL,
                prix REAL NOT NULL,
                stock INTEGER NOT NULL,
                PRIMARY KEY (id_ref_produit)         
            )
        ''')

        # Création de la table magasins
        pointeur.execute('''
            CREATE TABLE IF NOT EXISTS magasins (
                id_magasin INTEGER,
                ville TEXT NOT NULL,
                nb_salaries INTEGER NOT NULL,
                PRIMARY KEY (id_magasin)
            )
        ''')

        # Création de la table ventes
        pointeur.execute('''
            CREATE TABLE IF NOT EXISTS ventes (
                id_ref_produit TEXT,
                id_magasin INTEGER,
                date TEXT,
                quantite INTEGER NOT NULL,
                PRIMARY KEY (id_ref_produit, id_magasin, date),
                FOREIGN KEY (id_ref_produit) REFERENCES produits (id_ref_produit),
                FOREIGN KEY (id_magasin) REFERENCES magasins (id_magasin)
            )
        ''')

        # Création de la table pour stocker l'analyse du CA TOTAL
        pointeur.execute('''
            CREATE TABLE IF NOT EXISTS analyse_ca (
                id_analyse_ca INTEGER PRIMARY KEY AUTOINCREMENT,
                CA_TOTAL REAL NOT NULL
            )
        ''')

        # Création de la table pour stocker l'analyse des ventes par produit
        pointeur.execute('''
            CREATE TABLE IF NOT EXISTS analyse_ventes_produits (
                id_analyse_ventes_produits INTEGER PRIMARY KEY AUTOINCREMENT,
                PRODUIT TEXT NOT NULL,
                QTE_VENDUE INTEGER NOT NULL,
                PRIX_UNITAIRE REAL NOT NULL,
                VENTES REAL NOT NULL
            )
        ''')

        # Création de la table pour stocker l'analyse des ventes par magasin
        pointeur.execute('''
            CREATE TABLE IF NOT EXISTS analyse_ventes_magasins (
                id_analyse_ventes_magasins INTEGER PRIMARY KEY AUTOINCREMENT,
                MAGASIN TEXT NOT NULL,
                VENTES REAL NOT NULL
            )
        ''')

        # Commit et fermeture de la connection à la base de données
        connexion.commit()
        print("\nProcessus de création de la base de données réalisé")
        connexion.close()

    except Exception as e:
        # Affichage des erreurs éventuelles
        print(f"Erreur lors de la création de la base de données : {e}")