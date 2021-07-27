from plugin.firebase import fb_initialize_app, db_client
from plugin.datetime import tz_jst
from controllers.device import DeviceController
from controllers.graph.ble import BleGraphController
from controllers.graph.pressure import PressureGraphController
import datetime


def main():
    # firebase 初期化
    fb_initialize_app()

    # 取得期間
    start_at = datetime.datetime(2021, 7, 23, 17, 30, 0, tzinfo=tz_jst)
    end_at = datetime.datetime(2021, 7, 23, 17, 40, 0, tzinfo=tz_jst)

    # 各種デバイスの設定
    devices = ['0881269a1ac6746f', '6e90dd68ec031ce1', '4f3b8bb564a3203c']
    labels = ['left', 'right', '9F']
    colors = ['royalblue', 'orange', 'green']

    # グラフを表示
    d = BleGraphController(devices, start_at, end_at)
    devices = d.get_graph_data(labels, colors)
    now = datetime.datetime.now(tz_jst)
    for id in devices:
        print(id)
        d.show_graph(f"{id}", devices[id], export=False, created=now)

    # d = PressureGraphController('6e90dd68ec031ce1', start_at, end_at)
    # d.show_graph()

    # d = DeviceController('0881269a1ac6746f', start_at, end_at)
    # data = d.get_ble_graph_data()
    # print(data)

main()
