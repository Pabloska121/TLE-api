from fastapi import FastAPI, HTTPException
import json
from tle_fetcher import download_tles  # Importamos la función asincrónica desde tle_fetcher
from pathlib import Path
from firebase_config import get_firestore_client

app = FastAPI()
db = get_firestore_client()
DATA_FILE = Path("tle_data.json")

# Cargar datos al iniciar
@app.on_event("startup")
async def load_data():
    if not DATA_FILE.exists():
        await download_tles()  # Llamamos a la función asincrónica para descargar los TLEs
    global tle_data
    with open(DATA_FILE, "r") as f:
        tle_data = json.load(f)

@app.get("/")
def root():
    return {"message": "API de TLE en funcionamiento 🚀"}

@app.get("/tle/{object_name}")
async def get_tle_by_name(object_name: str):
    try:
        # Buscar documentos en la colección "tles" donde OBJECT_NAME coincida
        query = db.collection("tles").where("OBJECT_NAME", "==", object_name).limit(1)
        results = query.stream()
        
        for doc in results:
            tle_data = doc.to_dict()
            return {"id": doc.id, "data": tle_data}

        # Si no se encontró nada
        raise HTTPException(status_code=404, detail="TLE no encontrado")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error buscando el TLE: {e}")

@app.get("/tle-id/{id}")
def get_tle_by_id(id: str):
    for sat in tle_data:
        if sat["id"] == id:
            return sat
    return {"error": "Satélite no encontrado"}

@app.post("/update-tles")
async def update_tles():
    await download_tles()  # Usamos la versión asincrónica de download_tles
    return {"status": "TLEs actualizados"}
