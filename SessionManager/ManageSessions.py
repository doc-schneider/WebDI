import datetime as dtm
from flask import session
import uuid


def session_manager(*args):
    new_user = check_user_id()  #TODO Not necessary, need no user id, just initial parameters for session
    if new_user:
        session['user_id'] = str(uuid.uuid4())
        session["album"] = {'ID_ALBUM': 1}
        session["album_view"] = {"ID_PHOTO": [None]}
        session["photo"] = {"ID_PHOTO": 1}
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
    for key in ["timestamp", 'user_id', "album", "album_view", "photo"]:
        if key in session.keys():
            print(session[key])
