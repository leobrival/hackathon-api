import pandas as pd
import os
import requests
from dotenv import load_dotenv
from recheche import rechercher_equipement, rechercher_ID

load_dotenv()

print("Quel équipement voulez-vous intervenir ?")
equipement = input()

while True:
    result = rechercher_equipement(equipement)

    if len(result) == 0:
        print("Aucun équipement trouvé. Veuillez réessayer.")
        print("Quel équipement voulez-vous intervenir ?")
        equipement = input()

    elif len(result) > 1:
        #check si les "Nom" sont identiques
        if result['Nom'].str.lower().nunique() != 1:
            print("Plusieurs équipements correspondent. Suggestions :")
            for i, row in result.iterrows():
                print(f"{i+1}. {row['Nom']}")
            print("Quel équipement voulez-vous intervenir ?")
            equipement = input()
        else:
            print(f"Plusieurs éléments avec le même nom, veuillez entrer l'ID de l'équipement: {result['ID équipement']}")
            id_equipement = input()
            
            while True:
                result = rechercher_ID(id_equipement)
                
                if len(result) == 0:
                    print("Aucun équipement trouvé. Veuillez réessayer.")
                    print("Quel équipement voulez-vous intervenir ?")
                    id_equipement = input()
                else:
                    print(f"Équipement sélectionné : {result['Nom'].iloc[0]}")
                    break
            break
    else:
        print(f"Équipement sélectionné : {result['Nom'].iloc[0]}")
        break