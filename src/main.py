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
    start_at = datetime.datetime(2021, 7, 23, 17, 20, 0, tzinfo=tz_jst)
    end_at = datetime.datetime(2021, 7, 23, 17, 40, 0, tzinfo=tz_jst)

    # # 各種デバイスの設定
    # devices = ['0881269a1ac6746f', 'd742f58d5e3c5ef7', '4f3b8bb564a3203c']
    # labels = ['left', 'right', '9F']
    # colors = ['royalblue', 'orange', 'green']

    # # グラフを表示
    # d = BleGraphController(devices, start_at, end_at)
    # d.show_graph(labels, colors, is_save=True)

    d = PressureGraphController('6e90dd68ec031ce1', start_at, end_at)
    d.show_graph()

main()
