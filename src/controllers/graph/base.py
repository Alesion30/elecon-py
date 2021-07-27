import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from plugin.datetime import tz_jst
import timeout_decorator
import datetime
import math
import os
import numpy as np

class BaseController():
    @timeout_decorator.timeout(5)
    def show_graph(self, title: str, graphs: list, export: bool = False, created: datetime = datetime.datetime.now(tz_jst)):
        # 画像
        if export:
            fig = plt.figure()

        # データ 最大値・最小値
        min_x = None
        max_x = None
        min_y = None
        max_y = None

        for graph in graphs:
            x: list = np.array(graph["x"])
            y: list = np.array(graph["y"])
            color: str = graph["color"]
            label: str = graph["label"]

            if (len(x) > 0):
                if (min_x == None or min(x) < min_x):
                    min_x = min(x)
                if (max_x == None or  max(x) > max_x):
                    max_x = max(x)

            if (len(y) > 0):
                if (min_y == None or  min(y) < min_y):
                    min_y = min(y)
                if (max_y == None or  max(y) > max_y):
                    max_y = max(y)

            # 移動平均を算出
            num = 3
            if (len(x) >= num):
                x = np.delete(x, 0)
                x = np.delete(x, len(x) - 1)
                y = np.convolve(y, np.ones(num) / num, mode='same')
                y = np.delete(y, 0)
                y = np.delete(y, len(y) - 1)

            # 線 追加
            if (len(x) > 2):
                plt.plot(x, y, color=color, label=label)
            else:
                plt.plot(x, y, color=color, label=label, marker="o")

        # グラフ設定
        plt.title(title)
        plt.xlabel("time")
        plt.ylabel("rssi")
        ax = plt.subplot()

        # x軸の設定
        diff_x_sec: int = (max_x - min_x).seconds
        diff_x_min: int = math.ceil(diff_x_sec / 60)
        diff_x: int = math.ceil(diff_x_min / 10)
        ax.xaxis.set_major_locator(mdates.MinuteLocator(range(60), diff_x, tz=tz_jst))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        # y軸の設定
        plt.ylim(-100, -20)

        # 凡例の表示・グリッド表示
        ax.legend()
        ax.grid(True)

        # グラフの表示 or 保存
        if export:
            created_str = created.strftime("%Y%m%d%H%M%S")
            path = f"img/{created_str}"
            if not os.path.isdir(path):
                os.makedirs(path)
            fig.savefig(f"{path}/{title}.png")
            print(f"saved♩♩ {path}/{title}.png")
        else:
            plt.show()
