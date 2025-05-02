import httpx
import json
from pathlib import Path
from firebase_config import get_firestore_client  # Importamos la función en lugar de la variable

TLE_GROUPS = ["stations", "visual", "active"]
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"

# Descargar los TLEs de forma asincrónica
async def download_tles():
    db = get_firestore_client()  # Obtenemos la instancia de Firestore

    async with httpx.AsyncClient() as client:
        for group in TLE_GROUPS:
            print(f"📡 Iniciando descarga para el grupo: {group}")
            try:
                # Realizar la solicitud asincrónica
                response = await client.get(TLE_URL.format(group=group))
                response.raise_for_status()
                tles = response.json()

                # Guardar los TLEs en Firestore
                group_ref = db.collection(group)
                for tle in tles:
                    group_ref.add(tle)
                
                print(f"✅ Grupo {group} descargado y guardado en Firestore")
            except Exception as e:
                print(f"❌ Error descargando el grupo {group}: {e}")
