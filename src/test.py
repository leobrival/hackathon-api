import pandas as pd
import os
import requests
from dotenv import load_dotenv
from recheche import rechercher_equipement

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
        print("Plusieurs équipements correspondent. Suggestions :")
        for i, row in result.iterrows():
            print(f"{i+1}. {row['Nom']}")
        print("Quel équipement voulez-vous intervenir ?") 
        equipement = input()
    else:
        print(f"Équipement sélectionné : {result['Nom'].iloc[0]}")
        break
