import os
import json
from firebase_admin import credentials, firestore, initialize_app

# Obtener las credenciales de Firebase desde la variable de entorno
firebase_credentials = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))

# Crear las credenciales de Firebase a partir de las variables de entorno
cred = credentials.Certificate(firebase_credentials)

# Inicializar la aplicación de Firebase
initialize_app(cred)

# Crear una referencia a Firestore
db = firestore.client()
