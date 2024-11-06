from config_firestore import db, firestore

def load_database(username, score):
    doc_ref = db.collection('scores').document(username)
    doc_ref.set({'score' : score})

def query_database():
    top_scores = []

    # Gets top 5 scores descending order
    top_docs = (
        db.collection("scores")
        .order_by("score", direction=firestore.Query.DESCENDING)
        .limit(5)
        .stream()
    )

    # Add 5 tuples of format (username, score)
    for doc in top_docs:
        top_scores.append((doc.id, doc['score']))
    
    return top_scores
