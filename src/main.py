from plugin.firebase import fb_initialize_app, db_client
from plugin.datetime import tz_jst
from controllers.device import DeviceController
from controllers.graph.ble import BleGraphController
from controllers.graph.pressure import PressureGraphController
from controllers.graph.count import CountGraphController
import datetime


def main():
    # firebase 初期化
    fb_initialize_app()

    # 取得期間
    start_at = datetime.datetime(2021, 7, 27, 15, 30, 0, tzinfo=tz_jst)
    end_at = datetime.datetime(2021, 7, 27, 16, 30, 0, tzinfo=tz_jst)

    # 各種デバイスの設定
    devices = ['0881269a1ac6746f', '6e90dd68ec031ce1', '4f3b8bb564a3203c']
    labels = ['left', 'right', '9F']
    colors = ['royalblue', 'orange', 'green']

    # グラフを表示
    # d = BleGraphController(devices, start_at, end_at)
    # devices = d.get_graph_data(labels, colors)
    # now = datetime.datetime.now(tz_jst)
    # for id in devices:
    #     print(id)
    #     device = devices[id]
    #     max_y = -1000
    #     for item in device:
    #         y: list = item["y"]
    #         if len(y) > 0 and max_y < max(y):
    #             max_y = max(y)

    #     # 信号強度が-70dB以上のみのグラフを表示
    #     print(f"max rssi: {max_y}")
    #     if max_y > -70:
    #         try:
    #             d.show_graph(f"{id}", devices[id], export=True, created=now)
    #         except:
    #             print("timeout error")
    #     print("--------------------------------")

    # # グラフを表示（エレベーター右）
    # d = PressureGraphController('6e90dd68ec031ce1', start_at, end_at)
    # d.show_graph()

    d = CountGraphController('right', start_at, end_at)
    d.show_graph()

main()
