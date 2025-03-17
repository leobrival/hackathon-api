import pandas as pd
from difflib import get_close_matches

equipments_df = pd.read_csv("data/EQUIPMENTS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")

def rechercher_equipement(nom_recherche):
    """
    Recherche un équipement par nom et propose des suggestions si non trouvé.
    """
    nom_recherche = nom_recherche.lower() # Convertit la recherche en minuscules
    noms_existants = equipments_df["Nom"].str.lower().tolist() # Convertit les noms existants en minuscules pour la comparaison insensible à la casse

    if nom_recherche in noms_existants:
        print(f"Équipement trouvé : {nom_recherche}")
        return equipments_df[equipments_df["Nom"].str.lower() == nom_recherche]
    else:
        suggestions = get_close_matches(nom_recherche, noms_existants, n=5, cutoff=0.5) # Augmentez le cutoff pour des correspondances plus strictes
        if suggestions:
            print("Équipement non trouvé. Suggestions :")
            for suggestion in suggestions:
                print(suggestion)
            return equipments_df[equipments_df["Nom"].str.lower().isin(suggestions)]

        else:
            print("Équipement non trouvé. Aucune suggestion similaire.")
            return pd.DataFrame(columns=['Nom', 'ID équipement', 'Type', 'Secteur'])

# Exemple d'utilisation
# resultats = rechercher_equipement("nom de l'équipement recherché")
# resultats = input()

# print(rechercher_equipement(resultats))