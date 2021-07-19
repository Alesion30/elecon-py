from google.cloud.firestore_v1.base_document import DocumentSnapshot
from plugin.firebase import fb_initialize_app, db_client
from plugin.datetime import tz_jst
import datetime


class FirestoreController():
    def __init__(self, collection_name: str):
        """
        Firestoreコントローラー

        @params str collection_name コレクション名
        """
        db = db_client()
        self.collection_name = collection_name
        self.collection = db.collection(self.collection_name)
