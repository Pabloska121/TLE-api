import firebase_admin
from firebase_admin import credentials, firestore

# Ruta a tu archivo de credenciales
cred = credentials.Certificate("/Users/pabloasensfuentes/Downloads/tle-storage-firebase-adminsdk-fbsvc-3330726f25.json")
firebase_admin.initialize_app(cred)

# Inicializar Firestore
db = firestore.client()
