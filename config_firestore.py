import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

# Check if the script is running as a bundled app
if getattr(sys, 'frozen', False):
    # If the app is bundled with PyInstaller
    app_path = sys._MEIPASS
else:
    # If running in a development environment
    app_path = os.path.dirname(__file__)

# Define the path to the credentials file
cred_path = os.path.join(app_path, 'keys/cs-fair-panic-firebase-adminsdk-ua0sv-2afc4b9471.json')

# Initialize Firebase using the credentials file
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)  # Ensure Firebase is initialized

# Now we can use Firestore
db = firestore.client()

# Initializing database if empty

db_empty = False

scores_collection = db.collection('scores')

scores_docs = list(scores_collection.stream())

if len(scores_docs < 5):
    for _ in range(5):
        doc_ref = db.collection('scores').document('Player' + str(time.time()))
        doc_ref.set({'username': 'JDH', 'stage': 2, 'score': 50})

