from config_firestore import db, firestore
import constant


# Creates a score 'document' in the firestore database
# username: name inputted by user
# score: score of user
def load_database(username, score):
    doc_ref = db.collection('scores').document(username)
    doc_ref.set({'score' : score})

# Gets top 5 scores from database
# returns: list of tuples where
# tuple[0] is username
# tuple[1] is score
def query_database():
    top_scores = []

    # Gets top 5 scores descending order
    top_docs = (
        db.collection("scores")
        .order_by("score", direction=firestore.Query.DESCENDING)
        .limit(constant.NUM_HIGHSCORES)
        .stream()
    )

    # Add 5 tuples of format (username, score)
    for doc in top_docs:
        data = doc.to_dict()
        top_scores.append((doc.id, data['score']))
    
    return top_scores