import os
import json
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

def get_firestore_client():
    if not firebase_admin._apps:
        firebase_credentials = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))
        cred = credentials.Certificate(firebase_credentials)
        initialize_app(cred)
    return firestore.client()
