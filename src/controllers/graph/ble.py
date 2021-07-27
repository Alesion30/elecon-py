from controllers.device import DeviceController
from controllers.graph.base import BaseController
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from plugin.datetime import tz_jst, td_jst
import datetime
import math
import os
import numpy as np


class BleGraphController(BaseController):
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
        self.deviceControllers: list[DeviceController] = list(map(lambda x: DeviceController(x, start_at, end_at), id_list))  # デバイスコントローラーリスト
        self.datas = list(map(lambda x: x.get_ble_graph_data(), self.deviceControllers))  # DBから取得したデータ

    def get_graph_data(self, labels: list[str], colors: list[str]):
        """
        グラフデータを生成

        {
            "デバイスID": [
                {
                    "x": [],
                    "y": [],
                    "color": "",
                    "label": ""
                },
            ]
        }
        """
        devices = {}

        id_list = self._get_id_list()
        for id in id_list:
            # plotするグラフのデータ（本数分）
            lines: list = []

            # グラフデータを取得
            for i, data in enumerate(self.datas):
                if(id in data):
                    item: dict = data[id]
                else:
                    item = {"x": [], "y": []}

                # グラフデータを用意
                line = {
                    "x": item["x"],
                    "y": item["y"],
                    "color": colors[i],
                    "label": labels[i]
                }

                # グラフに追加
                lines.append(line)

            devices[id] = lines

        return devices

    def _get_id_list(self):
        """
        idのリスト取得する

        ["", "", ...]
        """
        id_list = []
        for data in self.datas:
            for device_id in data:
                id_list.append(device_id)

        # 重複削除
        id_list = list(set(id_list))
        return id_list
