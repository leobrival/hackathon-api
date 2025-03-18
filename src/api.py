from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from keywords import get_keywords
from recheche import rechercher_equipement, rechercher_ID

app = FastAPI()

class SearchResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None

class SearchRequest(BaseModel):
    query: str

@app.post("/get_nom", response_model=SearchResponse)
async def search_equipment(request: SearchRequest):
    # Get keywords from the query
    keywords = get_keywords(request.query)
    
    # Search for equipment using the first keyword
    result = rechercher_equipement(keywords)
    
    # Case 1: No matches
    if result.empty:
        return SearchResponse(
            code=1,
            message="Pas de correspondances",
            data=None
        )
    
    # Case 2: Approximate matches
    if len(result) > 1 and result['Nom'].str.lower().nunique() != 1:
        return SearchResponse(
            code=2,
            message="Plusieurs équipements correspondent. Vouliez vous dire :",
            data={"suggestions": result['Nom'].tolist()}
        )
    
    # Case 3: Duplicates (same name, different IDs)
    if len(result) > 1 and result['Nom'].str.lower().nunique() == 1:
        return SearchResponse(
            code=3,
            message="Plusieurs éléments avec le même nom, veuillez entrer l'ID de l'équipement :",
            data={"ids": result['ID équipement'].tolist()}
        )
    
    # Case 4: Exact match
    return SearchResponse(
        code=4,
        message="Equipement trouvé, que souhaitez vous savoir dessus?",
        data={"id": result['ID équipement'].iloc[0]}
    )

@app.post("/get_id", response_model=SearchResponse)
async def search_by_id(id: str):
    result = rechercher_ID(id)
    
    if result.empty:
        return SearchResponse(
            code=1,
            message="Pas de correspondances",
            data=None
        )
    
    return SearchResponse(
        code=4,
        message="Equipement trouvé, que souhaitez vous savoir dessus?",
        data={
            "nom": result['Nom'].iloc[0],
            "id": result['ID équipement'].iloc[0]
            }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 