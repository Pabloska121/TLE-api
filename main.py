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

@app.get("/tle-name/{object_name}")
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

@app.get("/tle/{id}")
async def get_tle_by_id(id: str):
    try:
        collections = ["stations", "visual", "active"]
        
        # Lista para almacenar los resultados
        all_tles = []

        # Iterar sobre las colecciones para obtener los satélites
        for col in collections:
            print(f"🔍 Obteniendo documentos de la colección {col}...")
            # Obtener todos los documentos de la colección
            docs = db.collection(col).stream()
            
            # Verificar si la colección tiene documentos
            doc_list = list(docs)
            if not doc_list:
                print(f"❌ No se encontraron documentos en la colección {col}")
            else:
                print(f"✔️ Se encontraron {len(doc_list)} documentos en la colección {col}")
                
            # Agregar todos los documentos a la lista all_tles
            for doc in doc_list:
                tle_data = doc.to_dict()
                tle_data["id"] = doc.id  # Guardamos el ID del documento
                all_tles.append(tle_data)
        
        print(f"📊 Se han agregado {len(all_tles)} TLEs a la lista")

        # Filtrar los TLEs por OBJECT_CAT_ID
        print(f"🔎 Buscando TLEs con OBJECT_CAT_ID = {id}")
        matched_tle = list(filter(lambda x: x.get("OBJECT_CAT_ID") == id, all_tles))

        # Si encontramos algún TLE, devolver el primero
        if matched_tle:
            print(f"✅ TLE encontrado: {matched_tle[0]}")
            return matched_tle[0]  # Devuelve el primer resultado
        else:
            print("❌ No se encontró ningún TLE con ese OBJECT_CAT_ID")
        
        # Si no se encuentra ningún TLE con el id proporcionado
        raise HTTPException(status_code=404, detail="TLE no encontrado con ese OBJECT_CAT_ID")
    
    except Exception as e:
        print(f"⚠️ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error buscando el TLE: {e}")

@app.post("/update-tles")
async def update_tles():
    await download_tles()
    return {"status": "TLEs actualizados en Firestore"}
