import dash
import pandas as pd
from dash import Dash, html, dcc
from flask import session
from flask_session import Session
from sqlalchemy import create_engine, MetaData
import mysql.connector
import os
from dotenv import load_dotenv

from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
from Initialize.Initialize import initialize_MySQL
import config

config.environment_app = "LOCAL"  # AZURE
config.environment_storage = "LOCAL"  # "AZURE"  # LOCAL

if config.environment_app == "LOCAL":
    load_dotenv()

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

app = dash_app.server
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
        session['album'] = {"ID_ALBUM": 14}
        session['album_view'] = {"IX_PHOTO": [None]}
        session['message_collection'] = {"ID_MESSAGE_COLLECTION": 1}
        session['message_view'] = {"GRANULARITY": "W", "DATETIME_START": pd.Timestamp(2024, 12, 23)}
        session['initialized'] = True

dash_app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
])

if __name__ == '__main__':
    if config.environment_app == "LOCAL":
        dash_app.run(host='192.168.0.225', port=5000, debug=False)
    elif config.environment_app == "AZURE":
        dash_app.run(debug=False)




