import httpx
import json
from pathlib import Path
import git
import os

TLE_GROUPS = ["stations", "visual", "active"]
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
DATA_DIR = Path("data")

# Configura el repositorio Git
repo_dir = Path("/path/to/your/repo")  # Ruta al directorio donde está tu repositorio clonado
repo = git.Repo(repo_dir)

# Descargar los TLEs de forma asincrónica
async def download_tles():
    # Crear la carpeta si no existe
    DATA_DIR.mkdir(exist_ok=True)

    async with httpx.AsyncClient() as client:
        for group in TLE_GROUPS:
            print(f"📡 Iniciando descarga para el grupo: {group}")
            try:
                # Realizar la solicitud asincrónica
                response = await client.get(TLE_URL.format(group=group))
                response.raise_for_status()
                tles = response.json()

                # Guardar los TLEs en un archivo
                group_file = DATA_DIR / f"{group}.json"
                with open(group_file, "w") as f:
                    json.dump(tles, f)

                print(f"✅ Grupo {group} descargado y guardado en {group_file}")

                # Realizar commit y push de los cambios
                repo.git.add(str(group_file))  # Añadir el archivo al commit
                repo.index.commit(f"Update TLEs for {group}")  # Hacer el commit
                origin = repo.remotes.origin
                origin.push()  # Hacer el push a GitHub

            except Exception as e:
                print(f"❌ Error descargando el grupo {group}: {e}")

