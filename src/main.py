from plugin.firebase import fb_initialize_app, db_client
from plugin.datetime import tz_jst
from controllers.device import DeviceController
from controllers.graph import DeviceGraphController
import datetime


def main():
    fb_initialize_app()

    start_at = datetime.datetime(2021, 7, 19, 17, 0, 0, tzinfo=tz_jst)
    end_at = datetime.datetime(2021, 7, 19, 17, 1, 0, tzinfo=tz_jst)

    controller = DeviceGraphController(['d742f58d5e3c5ef7'], start_at, end_at)

    data = controller.get_id_list()
    print(data)

main()
