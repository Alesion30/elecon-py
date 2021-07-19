from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from controllers.firestore import FirestoreController
from plugin.datetime import tz_jst, to_datetime
import datetime


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

    def get_ble_docs(self, start_at: datetime = None, end_at: datetime = None) -> list[DocumentSnapshot]:
        """
        BLEコレクションのデータを取得

        @return list[DocumentSnapshot]
        """
        if (start_at == None):
            start_at = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=tz_jst)

        if (end_at == None):
            end_at = datetime.datetime.now(
                tz=tz_jst) + datetime.timedelta(days=1)

        docs = self.ble_collection.where('created', '>=', start_at).where(
            'created', '<=', end_at).get()
        return docs

    def get_ble_docs_data(self, start_at: datetime = None, end_at: datetime = None) -> list[dict]:
        """
        BLEデータを配列として返す
        """
        docs = self.get_ble_docs(start_at, end_at)
        data = []
        for doc in docs:
            data += doc.get('data')

        data = list(map(self._cast, data))
        return data

    def get_device_id_data(self, start_at: datetime = None, end_at: datetime = None) -> dict:
        """
        id毎にデータを取得する
        """
        device = {}
        data = self.get_ble_docs_data(start_at, end_at)
        for item in data:
            id = item['id']
            rssi = item['rssi']
            created = item['created']
            obj = {'rssi': rssi, 'created': created}

            if (id in device):
                device[id].append(obj)
            else:
                device[id] = [obj]

        return device

    def _cast(self, data: dict) -> dict:
        """
        BLE/{docId}/dataを変換
        """
        id: str = data.get('id')
        rssi: int = data.get('rssi')
        created_timestamp: DatetimeWithNanoseconds = data.get('created')
        created = to_datetime(created_timestamp)
        return {'id': id, 'rssi': rssi, 'created': created}
