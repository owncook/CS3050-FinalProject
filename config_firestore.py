import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Check if the script is running as a bundled app
if getattr(sys, 'frozen', False):
    # If the app is bundled with PyInstaller
    app_path = sys._MEIPASS
else:
    # If running in a development environment
    app_path = os.path.dirname(__file__)

# Define the path to the credentials file
cred_path = os.path.join(app_path, 'keys/cs-3050-final-project-538f66db8997.json')

# Initialize Firebase using the credentials file
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)  # Ensure Firebase is initialized

# Now we can use Firestore
db = firestore.client()
