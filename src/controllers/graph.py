from controllers.device import DeviceController
import matplotlib.pyplot as plt
import datetime


class DeviceGraphController():
    def __init__(self, id_list: list[str], start_at: datetime = None, end_at: datetime = None):
        """
        id毎にBLE信号のグラフを生成するためのコントローラー

        @params list[str] id_list デバイスID
        """
        self.id_list = id_list
        self.devices: list[DeviceController] = list(
            map(lambda x: DeviceController(x), id_list))  # デバイスコントローラーリスト
        self.datas = list(map(lambda x: x.get_device_id_data(
            start_at, end_at), self.devices))  # DBから取得したデータ

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

    def show_graph(self, labels: list[str], colors: list[str]):
        id_list = self.get_id_list()
        for id in id_list:
            # 各デバイスのグラフに必要なデータを格納
            l = []

            for data in self.datas:
                if(id in data):
                    item: list = data[id]
                else:
                    item = []

                # x軸とy軸データ
                rssi_list: list[int] = []
                created_list: list[datetime] = []
                for v in item:
                    rssi_list.append(v['rssi'])
                    created_list.append(v['created'])
                l.append({'rssi': rssi_list, 'created': created_list})

            # グラフ作成
            fig = plt.figure()
            plt.title(id)
            plt.xlabel("time")
            plt.ylabel("rssi")

            for i, j in enumerate(l):
                label = labels[i]
                color = colors[i]
                plt.plot(j['created'], j['rssi'], color=color, label=label)

            plt.grid(True)
            plt.legend()
            plt.show()
