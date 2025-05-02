import requests
import json
from pathlib import Path

TLE_GROUPS = ["stations", "visual", "active"]
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"

def download_tles():
    for group in TLE_GROUPS:
        print(f"📡 Descargando grupo: {group}")
        try:
            response = requests.get(TLE_URL.format(group=group))
            response.raise_for_status()
            tles = response.json()

            # Guardar cada grupo en su propio archivo
            group_file = Path(f"{group}.json")
            with open(group_file, "w") as f:
                json.dump(tles, f)

            print(f"✅ Guardado en {group_file} ({len(tles)} satélites)")

        except Exception as e:
            print(f"❌ Error descargando grupo {group}: {e}")
