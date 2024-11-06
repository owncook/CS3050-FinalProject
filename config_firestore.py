import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('keys/cs-3050-final-project-firebase-adminsdk-x0odc-9b2aebb467.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()