from plugin.firebase import fb_initialize_app, db_client
from controller.firestore import DeviceController
import datetime


def main():
    fb_initialize_app()

    device_controller = DeviceController('d742f58d5e3c5ef7')

    start_at = datetime.datetime(2021, 7, 19, 20, 0, 0, 0)
    end_at = datetime.datetime(2021, 7, 19, 20, 1, 0, 0)

    docs = device_controller.get_ble_docs(start_at, end_at)
    for doc in docs:
        print(doc.to_dict())


main()
