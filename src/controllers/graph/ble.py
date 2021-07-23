from controllers.device import DeviceController
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from plugin.datetime import tz_jst, td_jst
import datetime
import math
import os
import numpy as np


class BleGraphController():
    def __init__(self, id_list: list[str], start_at: datetime, end_at: datetime):
        """
        id毎にBLE信号のグラフを生成するためのコントローラー

        @params list[str] id_list デバイスID
        """
        print("\n//////////////////////////////////////////////////")
        print('♪♪ BleGraphController Initialized ♪♪\n')
        print("deviceID")
        for id in id_list:
            print(f" - {id}")
        print("//////////////////////////////////////////////////\n")

        self.id_list = id_list
        self.devices: list[DeviceController] = list(
            map(lambda x: DeviceController(x, start_at, end_at), id_list))  # デバイスコントローラーリスト
        self.datas = list(map(lambda x: x.get_device_id_data(), self.devices))  # DBから取得したデータ

    def get_id_list(self):
        """
        idのリスト取得する
        """
        id_list = []
        for data in self.datas:
            for device_id in data:
                id_list.append(device_id)

        # 重複削除
        id_list = list(set(id_list))
        return id_list

    def show_graph(self, labels: list[str], colors: list[str], is_save: bool = False):
        """
        グラフを生成・表示

        @params list[str] labels ラベル
        @params list[str] colors 色
        """
        id_list = self.get_id_list()
        now = datetime.datetime.now(tz_jst)
        nowstr = now.strftime("%Y年%m月%d日 %H時%M分%S秒")
        print(f"♫ Start show_graph() ♫  {nowstr}\n")
        for id in id_list:
            # 各デバイスのグラフに必要なデータを格納
            l = []

            # 強い信号を含むかどうか
            is_strong: list[bool] = []

            # created_list 最小・最大
            created_min_list = []
            created_max_list = []

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
                    # TODO ここは+9時間とせずに、グラフ側の設定でなんとかしたい、、
                    created_list.append(v['created'] + td_jst)
                x_list = np.array(created_list)
                y_list = np.array(rssi_list)

                # 移動平均
                num = 3
                if (len(y_list) >= num):
                    y_list = np.convolve(
                        y_list, np.ones(num) / num, mode='same')
                    y_list = np.delete(y_list, 0)
                    y_list = np.delete(y_list, len(y_list) - 1)
                    x_list = np.delete(x_list, 0)
                    x_list = np.delete(
                        x_list, len(x_list) - 1)

                # グラフにデータを追加
                l.append({'x': y_list, 'y': x_list})

                # 強い信号を含むかどうか
                if (len(y_list) == 0):
                    is_strong.append(False)
                else:
                    is_strong.append(max(y_list) > -70)

                # 最小値・最大値 セット
                if len(created_list) > 0:
                    created_min_list.append(min(x_list))
                    created_max_list.append(max(x_list))

            # x軸 最大値・最小値
            if len(created_min_list) > 0:
                created_min = min(created_min_list)
            if len(created_max_list) > 0:
                created_max = max(created_max_list)

            # x軸の間隔を設定
            diff_created_sec: int = (created_max - created_min).seconds
            diff_created_min: int = math.ceil(diff_created_sec / 60)
            diff_created_div: int = math.ceil(diff_created_min / 10)

            if (True in is_strong):
                # 画像
                if is_save:
                    fig = plt.figure()

                # グラフ作成
                plt.title(id)
                plt.xlabel("time")
                plt.ylabel("rssi")

                ax = plt.subplot()
                plt.ylim(-100, -20)  # y軸の範囲
                ax.xaxis.set_major_locator(
                    mdates.MinuteLocator(range(60), diff_created_div, tz=tz_jst))
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

                # 横線
                threshold = -70
                plt.plot([created_min, created_max], [threshold, threshold],
                         "red", linestyle='dashed')

                for i, j in enumerate(l):
                    label = labels[i]
                    color = colors[i]
                    ax.plot(j['x'], j['y'], color=color, label=label)

                ax.grid(True)
                ax.legend()

                if is_save:
                    nowstr = now.strftime("%Y%m%d%H%M%S")
                    path = f"img/{nowstr}"
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    fig.savefig(f"{path}/{id}.png")
                    print(f"saved♩♩ {path}/{id}.png")
                else:
                    plt.show()
