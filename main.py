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

@app.get("/tle_name/{id}")
async def get_tle_by_id(id: str):
    try:
        collections = ["stations", "visual", "active"]
        
        # Lista para almacenar los resultados
        all_tles = []

        # Iterar sobre las colecciones para obtener los satélites
        for col in collections:
            # Obtener todos los documentos de la colección
            docs = db.collection(col).stream()

            # Agregar todos los documentos a la lista all_tles
            for doc in docs:
                tle_data = doc.to_dict()
                tle_data["id"] = doc.id  # Guardamos el ID del documento

                # Agregar a la lista de TLEs
                all_tles.append(tle_data)

        # Filtrar los TLEs por NORAD_CAT_ID
        matched_tle = list(filter(lambda x: x.get("OBJECT_NAME") == id, all_tles))

        # Si encontramos algún TLE, devolver el primero
        if matched_tle:
            return matched_tle[0]  # Devuelve el primer resultado

        # Si no se encuentra ningún TLE con el id proporcionado
        raise HTTPException(status_code=404, detail="TLE no encontrado con ese NORAD_CAT_ID")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error buscando el TLE: {e}")

@app.get("/tle/{id}")
async def get_tle_by_id(id: str):
    try:
        collections = ["stations", "visual", "active"]
        
        # Lista para almacenar los resultados
        all_tles = []

        # Iterar sobre las colecciones para obtener los satélites
        for col in collections:
            # Obtener todos los documentos de la colección
            docs = db.collection(col).stream()

            # Agregar todos los documentos a la lista all_tles
            for doc in docs:
                tle_data = doc.to_dict()
                tle_data["id"] = doc.id  # Guardamos el ID del documento

                # Agregar a la lista de TLEs
                all_tles.append(tle_data)

        # Filtrar los TLEs por NORAD_CAT_ID
        matched_tle = list(filter(lambda x: x.get("NORAD_CAT_ID") == id, all_tles))

        # Si encontramos algún TLE, devolver el primero
        if matched_tle:
            return matched_tle[0]  # Devuelve el primer resultado

        # Si no se encuentra ningún TLE con el id proporcionado
        raise HTTPException(status_code=404, detail="TLE no encontrado con ese NORAD_CAT_ID")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error buscando el TLE: {e}")

@app.post("/update-tles")
async def update_tles():
    await download_tles()
    return {"status": "TLEs actualizados en Firestore"}
