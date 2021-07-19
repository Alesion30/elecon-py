from google.cloud.firestore_v1.base_document import DocumentSnapshot
from plugin.firebase import fb_initialize_app, db_client
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


class DeviceController(FirestoreController):
    def __init__(self, device_id: str):
        """
        端末情報コントローラー

        @params str device_id デバイスID
        """
        super().__init__('devices')
        self.device_id = device_id
        self.document = self.collection.document(device_id)
        self.ble_collection = self.document.collection('ble')

    def get_doc(self) -> DocumentSnapshot:
        """
        ドキュメントフィールドを取得

        @return DocumentSnapshot
        """
        doc = self.document.get()
        return doc

    def get_ble_docs(self, start_at=None, end_at=None) -> list[DocumentSnapshot]:
        """
        BLEコレクションのデータを取得

        @return list[DocumentSnapshot]
        """
        if (start_at == None):
            start_at = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
        else:
            start_at -= datetime.timedelta(hours=9)

        if (end_at == None):
            end_at = datetime.datetime.now() + datetime.timedelta(days=1)
        else:
            end_at -= datetime.timedelta(hours=9)

        docs = self.ble_collection.where('created', '>=', start_at).where(
            'created', '<=', end_at).get()
        return docs
