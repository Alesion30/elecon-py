import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def fb_initialize_app():
    """
    firebase 初期化
    """
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    print("//////////////////////////////////////////////////")
    print('♪♪ Firebase Initialized ♪♪')
    print("//////////////////////////////////////////////////\n")


def db_client():
    """
    firestore クライエント
    """
    return firestore.client()
