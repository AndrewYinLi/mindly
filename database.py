import firebase_admin
from firebase_admin import credentials, firestore

# firebase credentials and database object
cred = credentials.Certificate("database-42a59-firebase-adminsdk-n5794-aeb3110aba.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def add_person(name, rel, contact):
    """ Add person to the database.

    :param name: str, person's name
    :param rel: str, person's relationship to the user
    :param contact: str, person's contact number
    """

    dataperson = {'name': name, 'relationship': rel, 'contact': contact}
    db.collection(u'people').document(name).set(dataperson)
    print('Person added.')


def get_person(name):
    """ Get person's information from the database.

    :param name: str, person's name stored in the database
    :return: False if person not in database, dictionary with person's parameters otherwise.
    """

    docs = db.collection(u'people').get()
    peoplein = {doc.id: doc.to_dict() for doc in docs}
    if name not in peoplein:
        return False
    else:
        return peoplein[name]