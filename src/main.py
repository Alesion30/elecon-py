from plugin.firebase import fb_initialize_app, db_client
from plugin.datetime import tz_jst
from controllers.device import DeviceController
import datetime


def main():
    fb_initialize_app()

    device_controller = DeviceController('d742f58d5e3c5ef7')

    start_at = datetime.datetime(2021, 7, 19, 17, 0, 0, tzinfo=tz_jst)
    end_at = datetime.datetime(2021, 7, 19, 17, 1, 0, tzinfo=tz_jst)

    docs = device_controller.get_ble_docs_data(start_at, end_at)
    for doc in docs:
        print(doc)


main()
