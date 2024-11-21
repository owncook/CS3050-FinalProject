from config_firestore import db, firestore
import constant
import time


# Creates a score 'document' in the firestore database
# username: name inputted by user
# score: score of user
def load_database(username, stage, score):
    doc_ref = db.collection('scores').document('Player' + str(time.time()))
    doc_ref.set({'username': username, 'stage': stage, 'score': score})


# Gets top 5 scores from database
# returns: list of tuples where
# tuple[0] is username
# tuple[1] is stage
# tuple[2] is score
def query_database():
    top_scores = []

    # Gets top 5 scores descending order
    top_docs = (
        db.collection("scores")
        .order_by("score", direction=firestore.Query.DESCENDING)
        .limit(constant.NUM_HIGHSCORES)
        .stream()
    )

    # Add 5 tuples of format (username, stage, score)
    for doc in top_docs:
        data = doc.to_dict()
        top_scores.append((data['username'], data['stage'], data['score']))

    return top_scores
