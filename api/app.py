import sys
from fastapi import FastAPI, HTTPException, Query
sys.path.append('..')
from utils.entities import Annonce
sys.path.pop()

# Initialize FastAPI app
app = FastAPI()


@app.get("/annonces/")
def get_all_annonces(offset: int = Query(0, description="Offset", ge=0), limit: int = Query(10, description="Limit", le=500)):
    annonces = Annonce.find_all(offset, limit)
    if len(annonces) == 0:
        raise HTTPException(status_code=404, detail="No annonce found")
    return annonces

@app.get("/annonces/{annonce_id}")
def get_annonce(annonce_id: int):
    annonce = Annonce.find(annonce_id)
    if annonce is None:
        raise HTTPException(status_code=404, detail="Annonce not found")
    return annonce

@app.get("/annonces/by-contract/{contract_id}")
def get_annonces_by_contract_type(contract_id: int):
    annonces = Annonce.query().filter(Annonce.contrat_id == contract_id).all()
    return annonces

@app.get("/annonces/by-source/{source_id}")
def get_annonces_by_source(source_id: int):
    annonces = Annonce.query().filter(Annonce.source_id == source_id).all()
    return annonces
