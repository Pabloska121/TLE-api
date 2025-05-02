from fastapi import FastAPI, HTTPException
from tle_fetcher import download_tles
from firebase_config import get_firestore_client

app = FastAPI()
db = None  # Se inicializa en el startup

@app.on_event("startup")
async def startup_event():
    global db
    db = get_firestore_client()  # Solo ahora, cuando todo está disponible

@app.get("/")
def root():
    return {"message": "API de TLE en funcionamiento 🚀"}

@app.get("/tle/{object_name}")
async def get_tle_by_name(object_name: str):
    try:
        # Buscar en todas las colecciones (por ejemplo, "stations", "visual", "active")
        collections = ["stations", "visual", "active"]
        for col in collections:
            query = db.collection(col).where("OBJECT_NAME", "==", object_name).limit(1)
            results = query.stream()

            for doc in results:
                tle_data = doc.to_dict()
                return {"id": doc.id, "collection": col, "data": tle_data}

        raise HTTPException(status_code=404, detail="TLE no encontrado")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error buscando el TLE: {e}")

@app.get("/tle-id/{collection}/{id}")
def get_tle_by_id(collection: str, id: str):
    try:
        doc_ref = db.collection(collection).document(id)
        doc = doc_ref.get()
        if doc.exists:
            return {"id": doc.id, "collection": collection, "data": doc.to_dict()}
        else:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error buscando el documento: {e}")

@app.post("/update-tles")
async def update_tles():
    await download_tles()
    return {"status": "TLEs actualizados en Firestore"}
