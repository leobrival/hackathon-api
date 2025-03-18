# utilise l'api de mistral pour répondre à la question en lui envoyant le prompt et les df triés

import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def get_response(prompt: str, id_equipement: str) -> dict:
    """
    Get AI response for a specific equipment based on prompt and equipment ID.
    
    Args:
        prompt (str): The user's question
        id_equipement (str): The equipment ID to get information about
        
    Returns:
        dict: The AI response
    """
    try:
        # Load data
        equipments_df = pd.read_csv("data/EQUIPMENTS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")
        interventions_df = pd.read_csv("data/INTERVENTIONS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")
        
        # Filter data for specific equipment
        equipment_info = equipments_df[equipments_df["ID équipement"] == id_equipement]
        intervention_info = interventions_df[interventions_df["ID"] == id_equipement]
        
        if equipment_info.empty:
            return {
                "choices": [{
                    "message": {
                        "content": f"Aucun équipement trouvé avec l'ID {id_equipement}"
                    }
                }]
            }
        
        # Prepare context for AI
        context = f"""
        Information sur l'équipement:
        {equipment_info.to_string()}
        
        Historique des interventions:
        {intervention_info.to_string()}
        """
        
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('api_key')}"
        }

        data = {
            "model": os.getenv("model"),
            "messages": [
                {
                    "role": "user",
                    "content": f"Réponds à la question suivante: {prompt}\n\nAvec ces informations:\n{context}"
                }
            ],
            "temperature": 0.2
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    except Exception as e:
        return {
            "choices": [{
                "message": {
                    "content": f"Erreur lors de la recherche: {str(e)}"
                }
            }]
        }

# if __name__ == "__main__":
#     print(get_response("Où se situe l'extincteur X45 ?"))

#test
# print(get_response("Ou est situé cet équipement?", "Mona 429"))