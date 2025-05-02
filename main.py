from fastapi import FastAPI
import json
from tle_fetcher import download_tles  # Importamos la función asincrónica desde tle_fetcher
from pathlib import Path

app = FastAPI()
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

@app.get("/satellites")
def get_satellite_list():
    return [{"name": sat["name"], "id": sat["id"]} for sat in tle_data]

@app.get("/tle/{id}")
def get_tle_by_id(id: str):
    for sat in tle_data:
        if sat["id"] == id:
            return sat
    return {"error": "Satélite no encontrado"}

@app.post("/update-tles")
async def update_tles():
    await download_tles()  # Usamos la versión asincrónica de download_tles
    return {"status": "TLEs actualizados"}
