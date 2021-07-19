import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def fb_initialize_app():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    print('♪♪ Firebase Initialized ♪♪')
