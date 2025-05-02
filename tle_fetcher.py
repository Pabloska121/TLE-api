import requests
import json
from pathlib import Path

TLE_GROUPS = ["stations", "visual", "active"]
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
DATA_DIR = Path("data")

def download_tles():
    # Crear la carpeta si no existe
    DATA_DIR.mkdir(exist_ok=True)

    for group in TLE_GROUPS:
        print(f"📡 Iniciando descarga para el grupo: {group}")
        try:
            # Descargando los TLEs para el grupo
            response = requests.get(TLE_URL.format(group=group))
            response.raise_for_status()  # Verifica si la respuesta fue exitosa (código 200)
            tles = response.json()

            # Guardar los TLEs en un archivo
            group_file = DATA_DIR / f"{group}.json"
            with open(group_file, "w") as f:
                json.dump(tles, f)

            # Mensaje de éxito
            print(f"✅ Grupo {group} descargado y guardado en {group_file} ({len(tles)} satélites)")

        except Exception as e:
            print(f"❌ Error descargando el grupo {group}: {e}")
