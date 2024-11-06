from config_firestore import db

def load_database(username, score):
    doc_ref = db.collection('scores').document(username)
    doc_ref.set({'score' : score})