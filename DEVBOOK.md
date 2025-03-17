# DEVBOOK : Chatbot intelligent pour techniciens du bâtiment

## 1. Introduction

Ce document décrit en détail la conception et la mise en œuvre d'un chatbot intelligent destiné aux techniciens du bâtiment. L'objectif est de fournir aux techniciens un assistant numérique capable de répondre à des questions en langage naturel sur les équipements de bâtiment et leurs interventions de maintenance.

Le chatbot s'appuie sur des données internes (fichiers CSV listant les équipements et les interventions) et utilise un modèle de langage avancé pour formuler des réponses claires et pertinentes.

### Contexte

Les techniciens du bâtiment doivent souvent consulter rapidement des informations techniques (caractéristiques d'un équipement, historique des interventions, procédures, etc.). Ce chatbot offre une interface conversationnelle simple où le technicien pose ses questions et obtient des réponses immédiates, sans avoir à parcourir manuellement des documents techniques ou bases de données.

### Fonctionnalités clés

- **Consultation des équipements** : interroger la base des équipements (par exemple connaître les caractéristiques d'un appareil ou son identifiant).
- **Consultation des interventions** : retrouver l'historique ou la date de la dernière intervention de maintenance sur un équipement donné.
- **Réponses en langage naturel** : le technicien pose des questions libres, le chatbot comprend la demande et y répond de façon contextuelle.
- **Modèle de langage local** : utilisation de Mistral 7B (un modèle de langage de Mistral AI) exécuté localement via Ollama, garantissant la confidentialité des données et une disponibilité sans dépendance à Internet.
- **Intégration des données internes** : le chatbot puise dans les fichiers CSV fournis (équipements et interventions) comme base de connaissances, pour fournir des réponses précises basées sur les données réelles de l'entreprise.

En résumé, ce DEVBOOK sert de référence technique complète pour développer ce chatbot, en couvrant son architecture, les choix technologiques, le code du backend et du frontend, ainsi que les instructions de déploiement et des pistes d'amélioration.

## 2. Architecture

L'architecture du système se décompose en plusieurs composants interconnectés. Chaque composant a un rôle défini, et l'ensemble forme une application chatbot cohérente :

- **Frontend (Next.js)** : Une interface web utilisateur où le technicien peut saisir ses questions et voir les réponses. Next.js est utilisé pour créer une application React moderne, offrant une zone de texte pour la question et une zone d'affichage pour la réponse du chatbot.

- **Backend (FastAPI)** : Un service web en Python qui sert d'intermédiaire entre le frontend, les données, et le modèle d'IA. Il expose des API REST permettant d'une part de requêter les données (équipements, interventions) et d'autre part d'obtenir une réponse du chatbot. C'est le cœur logique de l'application.

- **Modèle de langage (Mistral + Ollama)** : Le moteur d'IA qui génère les réponses en langage naturel. Mistral 7B est le modèle de langage utilisé, déployé localement à l'aide d'Ollama. Ollama agit comme serveur d'inférence local : il héberge le modèle Mistral et offre une API locale (HTTP) pour générer des réponses à partir de ce modèle.

- **Base de connaissances (CSV)** : Les données sur lesquelles le chatbot s'appuie – principalement deux fichiers CSV:

  - `equipements.csv` listant les équipements du bâtiment (avec des colonnes telles que identifiant, nom, type, localisation, date d'installation, etc.).
  - `interventions.csv` listant les interventions de maintenance (avec des colonnes comme identifiant de l'intervention, date, identifiant de l'équipement concerné, description de l'intervention, technicien responsable, etc.).

  Ces fichiers font office de base de données simplifiée. Le backend les charge en mémoire et peut effectuer des recherches dans ces données pour trouver l'information pertinente à la question posée.

### Schéma global d'interaction

Le technicien interagit avec l'interface Next.js (frontend), qui envoie la question au backend FastAPI. Le backend analyse la question : si nécessaire, il interroge les données CSV (par exemple pour trouver un équipement spécifique ou l'historique des interventions correspondantes).

Le backend construit ensuite une requête vers le modèle de langage Mistral (via l'API d'Ollama) en lui fournissant la question de l'utilisateur et éventuellement des informations contextuelles extraites des CSV. Le modèle génère une réponse en langage naturel, que le backend renvoie au frontend. Enfin, l'interface Next.js affiche cette réponse au technicien.

Le schéma suivant illustre ce flux :

```
Utilisateur (Technicien)
       ↓ (Question en langage naturel)
[ Frontend Next.js ] —→ (requête HTTP) —→ [ Backend FastAPI ]
       ↘︎                           ↙︎
        [ Fichiers CSV (Données) ]    [ Modèle Mistral via Ollama ]
```

Grâce à cette architecture modulaire, chaque composant peut être développé et testé indépendamment : l'interface utilisateur, l'API backend, le modèle d'IA, et la couche de données.

## 3. Backend (FastAPI)

Le backend est développé en Python en utilisant FastAPI, un framework web rapide et moderne bien adapté pour créer des APIs REST. Il remplit plusieurs fonctions : charger les données CSV, exposer des endpoints API pour accéder à ces données, et intégrer le modèle de langage pour générer les réponses du chatbot.

### Chargement des CSV avec Pandas

Au démarrage du backend, les fichiers CSV contenant les données d'équipements et d'interventions sont chargés en mémoire. Pour cela, on utilise la bibliothèque Pandas, qui permet de lire des fichiers CSV et de manipuler les données sous forme de DataFrame (tableaux structurés).

```python
import pandas as pd
from fastapi import FastAPI, HTTPException

# Chargement des données CSV dans des DataFrame pandas
try:
    df_equip = pd.read_csv("equipements.csv")  # Données des équipements
    df_int = pd.read_csv("interventions.csv")  # Données des interventions
except FileNotFoundError as e:
    raise RuntimeError(f"Erreur: fichier non trouvé - {e}")

# Optionnel: on peut vérifier quelques entrées
print(f"{len(df_equip)} équipements chargés, {len(df_int)} interventions chargées.")

app = FastAPI(title="Chatbot Technicien API")
```

Ce chargement initial permet d'avoir les données prêtes pour les requêtes API sans recharger les fichiers à chaque appel (améliorant les performances). Si les fichiers sont volumineux, cette approche reste viable tant que la taille tient en mémoire, sinon il faudrait envisager une base de données ou un chargement partiel.

### API pour requêter les équipements et interventions

Le backend expose des endpoints permettant de consulter les données brutes sur les équipements et interventions. Ces endpoints fournissent une sorte d'accès "lecture seule" à la base de connaissances CSV, utile pour des tests ou pour des fonctionnalités complémentaires.

Deux endpoints principaux sont définis :

- `GET /equipment/{id}` – Récupérer les informations d'un équipement donné par son identifiant (unique).
- `GET /equipment/{id}/interventions` – Obtenir la liste des interventions liées à un équipement spécifique.

```python
from typing import List

# Endpoint 1: Obtenir les informations d'un équipement par son ID
@app.get("/equipment/{equip_id}")
def get_equipment(equip_id: int):
    # Filtrer le DataFrame des équipements sur l'identifiant
    equip_data = df_equip[df_equip["id"] == equip_id]
    if equip_data.empty:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    # Convertir le résultat en dictionnaire (pour sérialisation JSON)
    record = equip_data.to_dict(orient="records")[0]
    return {"equipment": record}

# Endpoint 2: Obtenir la liste des interventions pour un équipement donné
@app.get("/equipment/{equip_id}/interventions")
def get_interventions_for_equipment(equip_id: int):
    # Vérifier d'abord que l'équipement existe
    equip_data = df_equip[df_equip["id"] == equip_id]
    if equip_data.empty:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    # Filtrer les interventions liées à cet équipement
    related_int = df_int[df_int["equip_id"] == equip_id]
    # Convertir en liste de dict (liste d'interventions)
    interventions_list = related_int.to_dict(orient="records")
    return {"equipment_id": equip_id, "interventions": interventions_list}
```

Ces endpoints permettent par exemple à un client (ou au frontend) de récupérer les données brutes. Exemples de requêtes possibles :

- `GET /equipment/42` pourrait retourner les détails de l'équipement d'ID 42 (par ex. son nom, type, etc.).
- `GET /equipment/42/interventions` retournerait toutes les interventions liées à l'équipement 42 (par ex. dates et descriptions des maintenances).

### Intégration d'Ollama et du modèle Mistral AI

Le cœur « intelligent » du backend réside dans l'appel au modèle de langage pour générer une réponse à partir de la question de l'utilisateur et des données contextuelles. Nous utilisons ici Mistral 7B, un modèle de langage développé par Mistral AI, que nous faisons tourner localement via Ollama.

Avant de pouvoir interroger Mistral, il faut s'assurer que Ollama est installé et que le modèle Mistral est disponible :

1. Installer Ollama sur la machine
2. Télécharger le modèle Mistral 7B via Ollama: `ollama pull mistral`
3. Lancer Ollama en s'assurant qu'il héberge le modèle (par défaut sur http://localhost:11434)

Définissons d'abord le modèle de données attendu en entrée avec Pydantic :

```python
from pydantic import BaseModel

class Question(BaseModel):
    question: str
```

Maintenant, le endpoint du chatbot lui-même :

```python
import requests

@app.post("/ask")
def ask_question(payload: Question):
    user_question = payload.question  # La question posée en texte naturel

    # 1. (Optionnel) Recherche de contexte dans les données internes
    contexte = ""
    # Par exemple, si la question contient un identifiant ou nom d'équipement, on peut extraire des infos
    for _, equip in df_equip.iterrows():
        name = str(equip.get("nom") or equip.get("name") or "")  # supposons colonne nom/name
        if name and name.lower() in user_question.lower():
            # On a trouvé un équipement dont le nom est mentionné dans la question
            equip_id = equip["id"]
            # Récupérer les interventions associées
            related_int = df_int[df_int["equip_id"] == equip_id]
            last_int_date = None
            if not related_int.empty:
                # trouver la dernière intervention (par date la plus récente)
                related_int = related_int.sort_values(by="date", ascending=False)
                last_int_date = related_int.iloc[0]["date"]
            # Construire une phrase de contexte avec ces infos
            contexte = f"Équipement {name} (ID {equip_id}). "
            if last_int_date:
                contexte += f"Dernière intervention le {last_int_date}. "
            contexte += "\n"
            break  # on prend le premier équipement correspondant pour le contexte

    # 2. Préparation du prompt pour le modèle Mistral
    if contexte:
        prompt = f"Contexte:\n{contexte}\nQuestion:\n{user_question}\nRéponse:"
    else:
        prompt = f"Question:\n{user_question}\nRéponse:"

    # 3. Appel au modèle Mistral via l'API d'Ollama
    ollama_url = "http://localhost:11434/api/generate"
    data = {
        "model": "mistral",   # nom du modèle tel que connu par Ollama
        "prompt": prompt,
        "stream": False       # on demande une réponse complète en une fois
    }
    try:
        res = requests.post(ollama_url, json=data, timeout=30)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'appel au modèle: {e}")
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Modèle IA a retourné une erreur {res.status_code}")
    # Analyser la réponse du modèle
    result_json = res.json()
    answer_text = result_json.get("response") or ""  # le texte de la réponse générée

    # 4. Renvoi de la réponse sous forme JSON
    return {"answer": answer_text.strip()}
```

Avec ce endpoint en place, le backend est capable de recevoir une question et de retourner une réponse générée par le modèle en tenant compte des données d'équipement. En quelque sorte, on a implémenté une forme simplifiée de RAG (Retrieval-Augmented Generation) où l'on fournit au modèle des informations supplémentaires issues d'une base de connaissances structurée.

## 4. Frontend (Next.js)

Le frontend de notre application est une interface web simple développée avec Next.js, framework React. Il offre une page unique permettant au technicien d'interagir avec le chatbot. L'accent est mis sur la simplicité d'utilisation : une zone de texte pour poser la question et une zone d'affichage de la réponse.

### Interface utilisateur

L'interface consiste en :

- Un champ de saisie (textarea) où l'utilisateur entre sa question
- Un bouton d'envoi pour déclencher la requête
- Une zone d'affichage de la réponse du chatbot

### Exemple de code Next.js (React)

```jsx
// pages/index.js (ou app/page.jsx dans Next 13+ avec app router)
import { useState } from "react";

export default function ChatbotPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return; // ne rien faire si la question est vide
    setLoading(true);
    setAnswer(""); // on réinitialise la réponse affichée
    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) {
        throw new Error(`Erreur ${res.status}`);
      }
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      console.error("Erreur lors de la requête:", err);
      setAnswer("Une erreur est survenue. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  // Permet d'envoyer la question avec Entrée
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div
      style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}
    >
      <h1>🤖 Assistant Technicien du Bâtiment</h1>
      <textarea
        rows={4}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Posez une question sur un équipement ou une intervention..."
        style={{ width: "100%", padding: "0.5rem" }}
      />
      <button
        onClick={handleAsk}
        disabled={loading}
        style={{ marginTop: "0.5rem", padding: "0.5rem 1rem" }}
      >
        {loading ? "Recherche..." : "Envoyer"}
      </button>
      <div style={{ marginTop: "1rem", whiteSpace: "pre-wrap" }}>
        {loading ? (
          <p>Réponse en cours...</p>
        ) : (
          <p>
            <strong>Réponse: </strong>
            {answer}
          </p>
        )}
      </div>
    </div>
  );
}
```

## 5. Déploiement et Tests

### Pré-requis et configuration

1. **Modèle Mistral via Ollama** :

   - Installer Ollama sur la machine de production
   - Télécharger le modèle: `ollama pull mistral`
   - Lancer le service Ollama

2. **Backend FastAPI** :

   - Préparer un environnement Python avec les dépendances nécessaires
   - Fichier requirements.txt: `fastapi`, `uvicorn`, `pandas`, `requests`
   - Lancer avec: `uvicorn main:app --reload --port 8000` (dev) ou sans `--reload` en production

3. **Frontend Next.js** :

   - Installer les dépendances Node (`npm install` ou `yarn`)
   - Configurer l'URL du backend (variable d'environnement `NEXT_PUBLIC_API_URL`)
   - Lancer avec: `npm run dev` (dev) ou `npm run build && npm run start` (prod)

4. **Communication entre frontend et backend** :
   - Configurer CORS si nécessaire:

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Tests manuels de l'API backend

FastAPI fournit une interface Swagger accessible à `/docs` (ex: http://localhost:8000/docs) pour tester les endpoints:

- `GET /equipment/1` - infos d'un équipement
- `GET /equipment/1/interventions` - liste des interventions
- `POST /ask` avec JSON `{"question": "Ma question?"}` - test du chatbot

Exemple avec curl:

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Quand a eu lieu la dernière intervention sur le Générateur A ?"}'
```

### Bonnes pratiques de déploiement

- **Journalisation** : Logguer les interactions importantes côté backend
- **Surveillance** : Surveiller l'utilisation CPU/Mémoire du modèle Mistral
- **Sécurité** : Valider/limiter la taille des questions reçues
- **Dockerisation** (optionnel) : Faciliter le déploiement avec Docker
- **Documentation utilisateur** : Rédiger un guide pour les techniciens

## 6. Améliorations possibles

Plusieurs améliorations peuvent être envisagées:

1. **Reconnaissance vocale** : Intégrer un système STT pour que les techniciens puissent parler leurs questions

2. **Suggestions automatiques** : Proposer des questions types ou compléter la question en cours de frappe

3. **Conservation du contexte conversationnel** : Garder l'historique des échanges pour permettre des conversations plus naturelles

4. **Enrichissement de la base de connaissances** : Intégrer un moteur d'indexation pour interroger des documents plus divers (manuels PDF, schémas, etc.)

5. **Interface utilisateur améliorée** : Affiner le design pour une meilleure UX

6. **Multi-langue** : Permettre au chatbot de fonctionner en plusieurs langues

En conclusion, ce DEVBOOK a présenté une solution complète pour un chatbot technique, depuis l'architecture jusqu'au code et au déploiement. Cette base peut être enrichie avec les suggestions ci-dessus pour aller plus loin. En appliquant ces principes et en tirant parti de la puissance du modèle Mistral AI, les techniciens du bâtiment disposeront d'un outil innovant pour accéder rapidement à l'information et gagner en efficacité dans leurs tâches quotidiennes.
