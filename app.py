import dash
import pandas as pd
from datetime import datetime, timedelta
from dash import Dash, html, dcc
import bcrypt
from flask import session, send_file, request, redirect
from flask_session import Session
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import mimetypes

from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
from DataOperations.Photo import PhotoFactory
from Initialize.Initialize import initialize_MySQL
import config

config.environment_app = "LOCAL"   # "AZURE"  # LOCAL
config.environment_storage = "LOCAL"  # "AZURE"  # LOCAL

FAILED_LOGINS = {}
MAX_ATTEMPTS = 3
LOCK_TIME = timedelta(hours=24)

if config.environment_app == "LOCAL":
    load_dotenv()
    with open("resources/auth_hash.json", "r") as f:
        VALID_USERNAME_PASSWORD_PAIRS = json.load(f)
elif config.environment_app == "AZURE":
        VALID_USERNAME_PASSWORD_PAIRS = json.loads(os.environ["USERS_JSON"])

if config.environment_storage == "LOCAL":
    # MySQL
    initialize_MySQL()
    # Tables
    config.table = {
        TableType.ALBUM: {
            "storage_name": "albums",
            "data_table": None
        },
        TableType.PHOTO: {
            "storage_name": "photos",
            "data_table": None
        },
        TableType.FILM: {
            "storage_name": "films",
            "data_table": None
        },
        TableType.FILM_CONTENT: {
            "storage_name": "film_contents",
            "data_table": None
        },
        TableType.MESSAGE: {
            "storage_name": "messages",
            "data_table": None
        },
        TableType.MESSAGE_COLLECTION: {
            "storage_name": "message_collections",
            "data_table": None
        },
        TableType.NOTE: {
            "storage_name": "notes",
            "data_table": None
        },
        TableType.NOTEBOOK: {
            "storage_name": "notebooks",
            "data_table": None
        },
        TableType.DOCUMENT: {
            "storage_name": "documents",
            "data_table": None
        },
        TableType.DOCUMENT_COLLECTION: {
            "storage_name": "document_collections",
            "data_table": None
        },
        TableType.TAG: {
            "storage_name": "tags",
            "data_table": None
        },
        TableType.EVENT: {
            "storage_name": "events",
            "data_table": None
        },
    }
elif config.environment_storage == "AZURE":
    config.table = {
        TableType.ALBUM: {
            "storage_name": "albums.csv",
            "data_table": None
        },
        TableType.PHOTO: {
            "storage_name": "photos.csv",
            "data_table": None
        },
    }
for key in config.table.keys():
    config.table[key]["data_table"] = DataTable.fetch_table(
        key,
        config.table[key]["storage_name"]
    )

dash_app = Dash(__name__, use_pages=True)
app = dash_app.server

# TODO On Azure: redis, sqlite?
os.makedirs(os.path.join(os.getcwd(), 'sessions'), exist_ok=True)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'  # Use the filesystem for sessions
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'sessions')  # Directory to store session files
app.config['SESSION_PERMANENT'] = False  # Sessions will expire when the browser is closed
app.config['SESSION_USE_SIGNER'] = True  # Sign session cookies for security
Session(app)

if config.environment_app == "AZURE":
    @app.before_request
    def protect_dash():
        if request.path.startswith("/") and not request.path.startswith("/login"):
            if "user" not in session:
                return redirect("/login")

# TODO Into View Factory?
@app.before_request
def ensure_session_initialized():
    # TODO Into Initialize module
    if 'initialized' not in session:
        session['ALBUM'] = {"ID_ALBUM": 7}
        session['FILM'] = {"ID_FILM": 1}
        session['MESSAGE_COLLECTION'] = {"ID_MESSAGE_COLLECTION": 1}
        session['NOTEBOOK'] = {"ID_NOTEBOOK": 1}
        session['table_content'] = TableType.FILM.name
        session['album_view'] = {"IX_PHOTO": [None]}
        # session['timeline_content'] = TableType.MESSAGE.name
        # session['timeline_view'] = {"GRANULARITY": "Y", "DATETIME_START": pd.Timestamp(2024, 1, 1)}
        session['timeline_content'] = TableType.ALBUM.name
        session['timeline_view'] = {"GRANULARITY": "Y", "DATETIME_START": pd.Timestamp(2024, 1, 1), "n_rows": 10}
        # session['timeline_content'] = TableType.NOTE.name
        # session['timeline_view'] = {"GRANULARITY": "Y", "DATETIME_START": pd.Timestamp(2024, 1, 1), "n_rows": 10}
        session['content_content'] = TableType.PHOTO.name
        session['content_view'] = {"ID_PHOTO": 313}
        session['initialized'] = True

if config.environment_app == "AZURE":
    def is_locked(username):
        entry = FAILED_LOGINS.get(username)
        if not entry:
            return False
        locked_until = entry.get("locked_until")
        if locked_until and locked_until > datetime.utcnow():
            return True
        return False

    def register_failed_attempt(username):
        entry = FAILED_LOGINS.setdefault(
            username,
            {"count": 0, "locked_until": None}
        )
        entry["count"] += 1
        if entry["count"] >= MAX_ATTEMPTS:
            entry["locked_until"] = datetime.utcnow() + LOCK_TIME

    def reset_attempts(username):
        FAILED_LOGINS.pop(username, None)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if is_locked(username):
                return "Account für 24 Stunden gesperrt", 403

            stored_hash = VALID_USERNAME_PASSWORD_PAIRS.get(username)
            if stored_hash and bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            ):
                reset_attempts(username)
                session["user"] = username
                return redirect("/")

            register_failed_attempt(username)
            return "Login fehlgeschlagen", 401

        return """
        <form method="post">
          <input name="username" placeholder="Username">
          <input name="password" type="password" placeholder="Password">
          <button type="submit">Login</button>
        </form>
        """

# TODO Into View Factory?
@app.route("/video")
def stream_video():
    name = request.args.get("name")
    # TODO Common call, decoding in PhotoFactory
    if config.environment_storage == "LOCAL":
        stream = Path(name)
    elif config.environment_storage == "AZURE":
        stream = PhotoFactory.stream_image(
            pd.Series(data={'AZURE_CONTAINER': "photo", 'AZURE_BLOB': name}, index=['AZURE_CONTAINER', 'AZURE_BLOB']),
            "AZURE"
        )
    mimetype, _ = mimetypes.guess_type(name)
    if not mimetype:
        mimetype = "application/octet-stream"  # fallback
    return send_file(stream, mimetype=mimetype)

dash_app.layout = html.Div([
    dcc.Location(id="url-redirect"),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
])

import Views.Callbacks

if __name__ == '__main__':
    if config.environment_app == "LOCAL":
        dash_app.run(host='192.168.0.225', port=5000, debug=False)
    elif config.environment_app == "AZURE":
        dash_app.run(host='192.168.0.225', port=5000, debug=False)
        #dash_app.run(debug=False)




