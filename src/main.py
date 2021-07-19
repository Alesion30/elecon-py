from plugin.firebase import fb_initialize_app, db_client
from plugin.datetime import tz_jst
from controllers.device import DeviceController
from controllers.graph import DeviceGraphController
import datetime


def main():
    fb_initialize_app()

    start_at = datetime.datetime(2021, 7, 19, 17, 50, 0, tzinfo=tz_jst)
    end_at = datetime.datetime(2021, 7, 19, 18, 0, 0, tzinfo=tz_jst)

    devices = ['0881269a1ac6746f', 'd742f58d5e3c5ef7']
    labels = ['left', 'right']
    colors = ['royalblue', 'orange']

    d = DeviceGraphController(devices, start_at, end_at)
    d.show_graph(labels, colors)


main()
