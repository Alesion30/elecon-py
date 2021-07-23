from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from controllers.firestore import FirestoreController
from plugin.datetime import tz_jst, to_datetime
import datetime


class DeviceController(FirestoreController):
    def __init__(self, device_id: str, start_at: datetime, end_at: datetime):
        """
        端末情報コントローラー(devicesコレクションを扱う)

        @params str device_id デバイスID
        """
        super().__init__('devices')
        self.device_id = device_id
        self.document = self.collection.document(device_id)
        self.ble_collection = self.document.collection('ble')
        self.pressure_collection = self.document.collection('pressure')

        # 取得期間をセット
        self.start_at = start_at
        self.end_at = end_at

    def get_doc(self) -> DocumentSnapshot:
        """
        ドキュメントフィールドを取得

        @return DocumentSnapshot
        """
        doc = self.document.get()
        return doc

    def get_ble_docs(self) -> list[DocumentSnapshot]:
        """
        BLEコレクションのデータを取得

        @return list[DocumentSnapshot]
        """
        docs = self.ble_collection.where('created', '>=', self.start_at).where(
            'created', '<=', self.end_at).get()
        return docs

    def get_pressure_docs(self) -> list[DocumentSnapshot]:
        """
        PRESSUREコレクションのデータを取得

        @return list[DocumentSnapshot]
        """
        docs = self.pressure_collection.where('created', '>=', self.start_at).where(
            'created', '<=', self.end_at).get()
        return docs

    # //////////////////////////////////////////////////////////////////

    def get_device_id_data(self) -> dict:
        """
        id毎にCOCOAの信号データを取得する
        """
        device = {}
        data = self._get_ble_docs_data()
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

    def get_pressure_data(self) -> list[dict]:
        """
        気圧情報を取得
        """
        docs = self.get_pressure_docs()
        data = []
        for doc in docs:
            data += doc.get('data')

        data = list(map(self._pressure_cast, data))
        return data

    # //////////////////////////////////////////////////////////////////

    def _get_ble_docs_data(self) -> list[dict]:
        """
        BLEデータを配列として返す
        """
        docs = self.get_ble_docs()
        data = []
        for doc in docs:
            data += doc.get('data')

        data = list(map(self._ble_cast, data))
        return data

    def _ble_cast(self, data: dict) -> dict:
        """
        ble/{docId}/dataを変換
        """
        id: str = data.get('id')
        rssi: int = data.get('rssi')
        created_timestamp: DatetimeWithNanoseconds = data.get('created')
        created = to_datetime(created_timestamp)
        return {'id': id, 'rssi': rssi, 'created': created}

    def _pressure_cast(self, data: dict) -> dict:
        """
        pressure/{docId}/dataを変換
        """
        value = data.get('value')
        created_timestamp: DatetimeWithNanoseconds = data.get('created')
        created = to_datetime(created_timestamp)
        return {'value': value, 'created': created}
