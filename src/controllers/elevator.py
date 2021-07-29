from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from controllers.firestore import FirestoreController
from plugin.datetime import tz_jst, to_datetime
import datetime


class ElevatorController(FirestoreController):
    def __init__(self, dir: str, start_at: datetime, end_at: datetime):
        """
        エレベーター情報コントローラー(elevatorsコレクションを扱う)

        @params str dir エレベーター向き（left or right）
        """
        super().__init__('elevators')
        self.document = self.collection.document(dir)
        self.log_collection = self.document.collection('log')

        # 取得期間をセット
        self.start_at = start_at
        self.end_at = end_at

    def get_doc(self) -> DocumentSnapshot:
        """
        ドキュメントフィールドを取得
        """
        doc = self.document.get()
        return doc

    def _get_log_docs(self) -> list[DocumentSnapshot]:
        """
        logコレクションのデータを取得
        """
        docs = self.log_collection.where('created', '>=', self.start_at).where(
            'created', '<=', self.end_at).get()
        return docs

    def get_log_data(self) -> list[dict]:
        """
        ログを取得
        """
        docs = self._get_log_docs()
        data = []
        for doc in docs:
            data += doc.get('data')

        data = list(map(self._log_cast, data))
        return data

    def _log_cast(self, data: dict) -> dict:
        """
        log/{docId}/dataを変換
        """
        people = data.get('people')
        created_timestamp: DatetimeWithNanoseconds = data.get('created')
        created = to_datetime(created_timestamp)
        return {'people': people, 'created': created}
