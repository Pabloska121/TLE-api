import httpx
import json
from pathlib import Path
from firebase_config import db  # Importamos la configuración de Firebase

TLE_GROUPS = ["stations", "visual", "active"]
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"

# Descargar los TLEs de forma asincrónica
async def download_tles():
    async with httpx.AsyncClient() as client:
        for group in TLE_GROUPS:
            print(f"📡 Iniciando descarga para el grupo: {group}")
            try:
                # Realizar la solicitud asincrónica
                response = await client.get(TLE_URL.format(group=group))
                response.raise_for_status()  # Verifica si la respuesta fue exitosa (código 200)
                tles = response.json()

                # Guardar los TLEs en Firestore
                group_ref = db.collection(group)  # Creamos una colección para cada grupo
                for tle in tles:
                    # Añadir cada TLE como documento en la colección correspondiente
                    group_ref.add(tle)
                
                print(f"✅ Grupo {group} descargado y guardado en Firestore")
            except Exception as e:
                print(f"❌ Error descargando el grupo {group}: {e}")
