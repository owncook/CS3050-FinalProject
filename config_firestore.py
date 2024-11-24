import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

'''
config_firestore.py locates our firebase key and initializes the firebase application and database objects which are imported into database.py
'''

# Use a service account.
cred = credentials.Certificate('keys/cs-3050-final-project-538f66db8997.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()