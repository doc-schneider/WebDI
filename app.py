import dash
import pandas as pd
from dash import Dash, html, dcc
import dash_auth
from flask import session, send_file, request
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

if config.environment_app == "LOCAL":
    load_dotenv()

# with open("resources/auth.json", "r") as f:
#     VALID_USERNAME_PASSWORD_PAIRS = json.load(f)

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
# auth = dash_auth.BasicAuth(dash_app, VALID_USERNAME_PASSWORD_PAIRS)
app = dash_app.server

# TODO On Azure: redis, sqlite?
os.makedirs(os.path.join(os.getcwd(), 'sessions'), exist_ok=True)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'  # Use the filesystem for sessions
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'sessions')  # Directory to store session files
app.config['SESSION_PERMANENT'] = False  # Sessions will expire when the browser is closed
app.config['SESSION_USE_SIGNER'] = True  # Sign session cookies for security
Session(app)

@app.before_request
def ensure_session_initialized():
    # TODO Into Initialize module
    if 'initialized' not in session:
        session['ALBUM'] = {"ID_ALBUM": 7}
        session['MESSAGE_COLLECTION'] = {"ID_MESSAGE_COLLECTION": 1}
        session['NOTEBOOK'] = {"ID_NOTEBOOK": 2}
        session['album_view'] = {"IX_PHOTO": [None]}
        session['timeline_simple_content'] = TableType.MESSAGE.name  # TableType.NOTE.name   # TableType.MESSAGE.name
        session['timeline_simple_view'] = {"GRANULARITY": "Y", "DATETIME_START": pd.Timestamp(2024, 1, 1)}
        session['timeline_content'] = TableType.ALBUM.name
        session['timeline_view'] = {"GRANULARITY": "Y", "DATETIME_START": pd.Timestamp(2024, 1, 1), "n_rows": 10}
        session['content_content'] = None
        session['content_view'] = {}
        session['initialized'] = True

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




