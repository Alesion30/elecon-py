from controllers.elevator import ElevatorController
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from plugin.datetime import tz_jst, td_jst
import datetime
import math
import os
import numpy as np


class CountGraphController():
    def __init__(self, dir: str, start_at: datetime = None, end_at: datetime = None):
        """
        カウントのグラフを表示するためのコントローラー

        @params str dir エレベーター向き（left or right）
        """
        print("\n//////////////////////////////////////////////////")
        print('♪♪ CountGraphController Initialized ♪♪')
        print("//////////////////////////////////////////////////\n")

        self.controller: ElevatorController = ElevatorController(
            dir, start_at, end_at)  # デバイスコントローラー

    def show_graph(self):
        """
        グラフを生成・表示
        """

        # X軸とy軸データ
        value_list: list[int] = []
        created_list: list[datetime] = []

        data = self.controller.get_log_data()
        for v in data:
            value_list.append(v['people'])
            # TODO ここは+9時間とせずに、グラフ側の設定でなんとかしたい、、
            created_list.append(v['created'] + td_jst)

        x_list = np.array(created_list)
        y_list = np.array(value_list)

        # x軸 最大値・最小値
        if len(x_list) > 0:
            x_min = min(x_list)
            x_max = max(x_list)

        # x軸の間隔を設定
        diff_x_sec: int = (x_max - x_min).seconds
        diff_x_min: int = math.ceil(diff_x_sec / 60)
        diff_x_div: int = math.ceil(diff_x_min / 10)

        # グラフ作成
        plt.xlabel("time")
        plt.ylabel("people")

        ax = plt.subplot()
        ax.grid(True)
        # ax.bar(x_list, y_list, width=1/(diff_x_sec*60))
        ax.plot(x_list, y_list, marker='.', linewidth=0)

        # 軸の設定
        ax.xaxis.set_major_locator(mdates.MinuteLocator(
            range(60), diff_x_div, tz=tz_jst))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        plt.show()
