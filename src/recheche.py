import pandas as pd
from difflib import get_close_matches

equipments_df = pd.read_csv("data/EQUIPMENTS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")
equipments_df = equipments_df[['Nom', 'ID équipement']]
equipments_df_duplicates = equipments_df[equipments_df.duplicated(subset=['Nom'], keep=False)]

def rechercher_equipement(nom_recherche):
    """
    Recherche un équipement par nom et propose des suggestions si non trouvé.
    """
    nom_recherche = nom_recherche.lower()
    noms_existants = equipments_df["Nom"].str.lower().tolist()

    if nom_recherche in noms_existants:
        return equipments_df[equipments_df["Nom"].str.lower() == nom_recherche]
    
    else:
        suggestions = get_close_matches(nom_recherche, noms_existants, n=5, cutoff=0.5)
        if suggestions:
            return equipments_df[equipments_df["Nom"].str.lower().isin(suggestions)]

        else:
            return pd.DataFrame(columns=['Nom', 'ID équipement'])
        
def rechercher_ID(nom_ID):
    nom_ID = nom_ID.lower()
    ID_existants = equipments_df["ID équipement"].str.lower().tolist()
    if nom_ID in ID_existants:
        return equipments_df[equipments_df["ID équipement"].str.lower() == nom_ID]
    else:
        return pd.DataFrame(columns=['Nom', 'ID équipement'])