# Script principal
# Import des fonctions utiles des autres scripts
# Import de la fonction depuis le fichier CREER_bdd.py
from CREER_bdd import creation_base
from MAJ_magasins import maj_table_magasins
from MAJ_produits import maj_table_produits
from MAJ_ventes import maj_table_ventes
from analyses import calcul_ca_total, calcul_ventes_produits, calcul_ventes_magasin

# Executions des fonctions
# Création de la base
creation_base()

# Alimentation des tables via les CSV
maj_table_magasins()
maj_table_produits()
maj_table_ventes()

# Réalisation des analyses et stockage des résultats
print("Rapports des analyses\n")
calcul_ca_total()
calcul_ventes_produits()
calcul_ventes_magasin()
