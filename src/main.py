import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from plugin.firebase import fb_initialize_app

def main():
    fb_initialize_app()
    print('hoge')

    db = firestore.client()
    docs = db.collection('floors').get()
    for doc in docs:
        print(doc.to_dict())

main()
