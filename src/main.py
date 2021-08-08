from plugin.firebase import fb_initialize_app, db_client
from plugin.datetime import tz_jst
from controllers.device import DeviceController
from controllers.graph.ble import BleGraphController
from controllers.graph.pressure import PressureGraphController
from controllers.graph.count import CountGraphController
from controllers.graph.elevator import ElevatorGraphController
import datetime
import json


def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def main():
    # firebase 初期化
    fb_initialize_app()

    # 取得期間
    start_at = datetime.datetime(2021, 7, 29, 15, 5, 0, tzinfo=tz_jst)
    end_at = datetime.datetime(2021, 7, 29, 15, 30, 0, tzinfo=tz_jst)

    # 各種デバイスの設定
    # devices = ['0881269a1ac6746f', '6e90dd68ec031ce1', '4f3b8bb564a3203c']
    # labels = ['left', 'right', '9F']
    # colors = ['royalblue', 'orange', 'green']

    devices = ['6e90dd68ec031ce1', '4f3b8bb564a3203c']
    labels = ['right', '9F']
    colors = ['royalblue', 'orange']

    # グラフを表示
    d = BleGraphController(devices, start_at, end_at)
    devices = d.get_graph_data(labels, colors)
    now = datetime.datetime.now(tz_jst)
    for id in devices:
        print(id)

        if (id in ['03:42:2A:54:F7:10', '41:5B:0B:B6:4B:2F', '39:B7:BE:BB:29:1F', '57:ED:CA:45:33:7C']):
            # if (id in ['00:41:33:6E:F0:1E', '7B:81:4D:23:73:32', '3B:D1:FE:AC:2A:A0', '72:E6:E9:26:7C:A3', '62:EA:AB:74:5F:38']):
            device = devices[id]

            # jsonデータを出力
            data = dict()
            for index, item in enumerate(device):
                data[index] = item
            with open(f'data/{id}.json', mode='wt', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False,
                          indent=2, default=json_serial)

            # try:
            #     d.show_graph(f"{id}", devices[id], export=True, created=now)
            # except:
            #     print("timeout error")

        # device = devices[id]
        # max_y = -1000
        # for item in device:
        #     y: list = item["y"]
        #     if len(y) > 0 and max_y < max(y):
        #         max_y = max(y)

        # # 信号強度が-70dB以上のみのグラフを表示
        # print(f"max rssi: {max_y}")
        # if max_y > -70:
        #     try:
        #         d.show_graph(f"{id}", devices[id], export=True, created=now)
        #     except:
        #         print("timeout error")
        print("--------------------------------")

    # # 気圧
    # d = PressureGraphController('6e90dd68ec031ce1', start_at, end_at)
    # d.show_graph()

    # # カウント
    # d = CountGraphController('right', start_at, end_at)
    # d.show_graph()

    # # 気圧 + カウント
    # d = ElevatorGraphController('6e90dd68ec031ce1' ,'right', start_at, end_at)
    # d.show_graph()


main()
