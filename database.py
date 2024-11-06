from config_firestore import db, firestore

def load_database(username, score):
    doc_ref = db.collection('scores').document(username)
    doc_ref.set({'score' : score})

def query_database():

    # Query the collection, sort by your integer field in descending order, and limit to top 5
    top_docs = (
        db.collection("yourCollection")
        .order_by("yourIntegerField", direction=firestore.Query.DESCENDING)
        .limit(5)
        .stream()
    )

    # Print the document ID and data for the top 5 documents
    for doc in top_docs:
        print(f'Document ID: {doc.id} => Data: {doc.to_dict()}')