import pandas as pd
import os
import requests
from dotenv import load_dotenv

load_dotenv()

equipments_df = pd.read_csv("data/EQUIPMENTS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")
equipments_df = equipments_df[['Nom']]

def get_keywords(prompt):
    api_key = os.getenv("api_key")
    model = os.getenv("model")

    def make_mistral_request(prompt):
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "donne moi, sans aucun autre mot, les mots composant le sujet de ce texte: " + prompt
                }
            ],
            "temperature": 0.2
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    response = make_mistral_request(prompt)
    print(prompt)
    print(response)
    return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    prompt = "Où se situe l'extincteur X45 ?"
    keywords = get_keywords(prompt)
    print(keywords)

# equipments_df = pd.read_csv("data/EQUIPMENTS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")
# interventions_df = pd.read_csv("data/INTERVENTIONS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")

# equipments_df_output = pd.DataFrame()

# for keyword in keywords:
#     #chercher dans equipments_df
#     equipment = equipments_df[equipments_df['Nom'].str.contains(keyword, case=False, na=False)]
#     if not equipment.empty:
#         equipments_df_output = pd.concat([equipments_df_output, equipment])
#     else:
#         print("aucun équipement trouvé")
#     #chercher dans interventions_df
#     # intervention = interventions_df[interventions_df['name'].str.contains(keyword)]
#     # if not intervention.empty:
#     #     print(intervention)
#     # else:
#     #     print("aucune intervention trouvée")

# #show infos about equipments_df_output
# print(equipments_df_output.info())