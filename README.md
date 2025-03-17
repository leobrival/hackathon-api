# Chatbot Intelligent pour les Techniciens du Bâtiment

## 💡 Contexte
Dans le secteur du bâtiment, les techniciens perdent souvent du temps à chercher des informations clés pour leurs interventions (localisation des équipements, historique, urgences). Pour optimiser leur efficacité, nous développons un **chatbot intelligent**, simple et connecté à une base de données interne, qui répond rapidement à leurs questions en langage naturel.

**Exemples de questions :**
- "Où se situe l’équipement extincteur X45 ?"
- "Quel est l’historique des interventions sur cet équipement ?"
- "Quel est le type de cet équipement ?"
- "Y a-t-il des interventions urgentes aujourd’hui ?"

## 🎯 Objectif
Créer un **assistant IA sous forme de chatbot** qui :
- Fournit des informations sur les équipements (localisation, état, type, etc.).
- Récupère l’historique des interventions.
- Décrit les pannes signalées.
- Résume les tâches à effectuer par le technicien.

## Besoins et Spécifications

### Fonctionnalités
1. **Interaction directe :**
   - Répond aux questions en langage naturel.
   - Analyse les demandes et recherche les données pertinentes.
2. **Connexion aux données :**
   - Accès à deux fichiers CSV :
     - `EQUIPMENTS_data_anonymized.csv` : Liste des équipements.
     - `INTERVENTIONS_data_anonymized.csv` : Historique des interventions.
3. **Gestion des échecs :**
   - Message clair si aucune donnée n’est trouvée :  
     _"Désolé, je n’ai pas trouvé d’information dans la base."_

### Architecture
- **Backend :** Gestion des CSV avec `pandas`, API Mistral pour l’IA.
- **Frontend :** Interface simple.
- **Flux :**
  1. L’utilisateur pose une question.
  2. Le backend interroge les CSV.
  3. Mistral analyse et génère une réponse.
  4. Réponse affichée dans l’interface.

## 📦 Ressources
- **Mistral AI :**  
  - [Documentation](https://docs.mistral.ai/getting-started/quickstart).  
  - Modèle : `mistral-large-latest`.
- **Bases de données :**  
  ```python
  import pandas as pd
  equipments_df = pd.read_csv("folder/EQUIPMENTS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")
  interventions_df = pd.read_csv("folder/INTERVENTIONS_data_anonymized.csv", sep=";", encoding="ISO-8859-1")```
 - **Interface :** Maquette simple (zone de texte + affichage).

 ## Rendu Attendu
 - Interface :
    - Zone de texte pour poser une question.
    - Bouton "Envoyer".
    - Affichage des réponses de l'ia.
- Exemples : "Où se situe l’extincteur X45 ?" → "Vous pouvez retrouver l’extincteur X45 au 2e étage, bâtiment A."

## Conseils de Développement
1. Backend :  
- Choix libre (Flask/FastAPI est pas mal pour une interface basique.)
- Charger les CSV avec pandas.
- Intégrer Mistral via API.
2. Frontend :
- Choix libre
3. Tests :
- Tester diverses questions.
- Vérifier les cas sans données.

- **Astuce :** Commencez par un prototype fonctionnel avec une seule fonctionnalité (ex. historique des interventions d'un équipement spécifique), puis ajoutez les autres progressivement.


## 🎁 Bonus (si temps disponible)
- Ajouter une reconnaissance vocale pour poser des questions (via une bibliothèque comme SpeechRecognition en Python).
- Proposer des suggestions automatiques si la question est ambiguë (ex. "Voulez-vous dire l’équipement X45 ou X46 ?").