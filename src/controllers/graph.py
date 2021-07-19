from controllers.device import DeviceController
import datetime


class DeviceGraphController():
    def __init__(self, id_list: list[str], start_at: datetime = None, end_at: datetime = None):
        """
        id毎にBLE信号のグラフを生成するためのコントローラー

        @params list[str] id_list デバイスID
        """
        self.id_list = id_list
        self.devices: list[DeviceController] = list(map(lambda x: DeviceController(x), id_list)) # デバイスコントローラーリスト
        self.datas = list(map(lambda x: x.get_device_id_data(start_at, end_at), self.devices)) # DBから取得したデータ

    def get_id_list(self):
        """
        idのリスト取得する
        """
        id_list = []
        for data in self.datas:
            for device_id in data:
                id_list.append(device_id)

        # 重複削除
        list(set(id_list))
        return id_list
