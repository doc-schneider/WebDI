import datetime as dtm
from flask import session
import uuid

from DataStructures.TableTypes import TableType


def session_manager(*args):
    new_user = check_user_id()  #TODO Not necessary, need no user id, just initial parameters for session?
    if new_user:
        # TODO Better store init values in config first
        session['user_id'] = str(uuid.uuid4())
        session['collection_type'] = TableType.ALBUM.name  # TODO Can store enum?
        session["collection"] = {"TAG": "Fotoalbum Stefan & Konstanze"}
        session["album"] = {'ID_ALBUM': 1}
        session["album_view"] = {"ID_PHOTO": [None]}
        session["photo"] = {"ID_PHOTO": 1}
        session["notebook"] = {"ID_NOTEBOOK": 1}
        session["note"] = {"ID_NOTE": 1}
        session["page"] = ""  # On which page is user?
    if args:
        for key, value in args[0].items():
            session[key] = value
    session["timestamp"] = dtm.datetime.now()

# Helper function to generate a unique session ID if it doesn't exist
def check_user_id():
    new_user = False
    if 'user_id' not in session:
        new_user = True
    return new_user

def show_session(label):
    print(label)
    for key in ["timestamp", 'user_id', 'collection_type', "collection", "album", "album_view", "photo", "notebook", "note", "page"]:
        if key in session.keys():
            print(session[key])
