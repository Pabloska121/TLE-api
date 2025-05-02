import requests
import json
from pathlib import Path

TLE_GROUPS = ["stations", "visual", "active"]
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
DATA_FILE = Path("tle_data.json")

def download_tles():
    all_tles = []

    for group in TLE_GROUPS:
        print(f"📡 Descargando grupo: {group}")
        try:
            response = requests.get(TLE_URL.format(group=group))
            response.raise_for_status()
            tles = response.json()
            all_tles.extend(tles)
        except Exception as e:
            print(f"❌ Error descargando grupo {group}: {e}")

    # Guardar en archivo local
    with open(DATA_FILE, "w") as f:
        json.dump(all_tles, f)

    print(f"✅ TLEs guardados: {len(all_tles)} satélites.")
