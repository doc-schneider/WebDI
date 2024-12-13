import dash
from dash import Dash, html, dcc
from sqlalchemy import create_engine, MetaData
import mysql.connector
import os
from flask_session import Session
import redis

from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
import config


# Settings
config.environment = "local"   # "azure"

if config.environment == "local":
    # MySQL
    db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
    db_engine = create_engine(db_connection_str)
    db_conn = db_engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=db_engine)
    config.mysql = {
        "engine": db_engine,
        "conn": db_conn,
        "metadata": metadata,
    }
    # Simple connector
    db_connector = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Moppel3!",
        database="lives",
    )
    db_cursor = db_connector.cursor()
    config.mysql["connector"] = db_connector
    config.mysql["cursor"] = db_cursor

    # Tables
    config.table = {
        TableType.TAG: {
            "mysql_name": "tags",
            "mysql_table": None,
            "data_table": None
        },
        TableType.ALBUM: {
            "mysql_name": "albums",
            "mysql_table": None,
            "data_table": None
        },
        TableType.PHOTO: {
            "mysql_name": "photos",
            "mysql_table": None,
            "data_table": None
        },
        TableType.NOTE: {
            "mysql_name": "notes",
            "mysql_table": None,
            "data_table": None
        },
        TableType.NOTEBOOK: {
            "mysql_name": "notebooks",
            "mysql_table": None,
            "data_table": None
        }
    }
    for key in config.table.keys():
        config.table[key]["data_table"] = DataTable.fetch_table(
            key,
            config.table[key]["mysql_name"]
        )
    config.collection_types = [TableType.ALBUM, TableType.NOTE, TableType.NOTEBOOK]

dash_app = Dash(__name__, use_pages=True)
server = dash_app.server

# Configure server-side session
server.config['SECRET_KEY'] = 'supersecretkey'
server.config['SESSION_TYPE'] = 'filesystem'  # Use the filesystem for sessions
server.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'sessions')  # Directory to store session files
server.config['SESSION_PERMANENT'] = False  # Sessions will expire when the browser is closed
server.config['SESSION_USE_SIGNER'] = True  # Sign session cookies for security
# Redis Configuration
# server.config["SESSION_TYPE"] = "redis"
# server.config["SESSION_PERMANENT"] = False
# server.config["SESSION_USE_SIGNER"] = True  # For added security
# server.config["SESSION_KEY_PREFIX"] = "dash_session:"
# server.config["SESSION_REDIS"] = redis.StrictRedis(host="localhost", port=6379, db=0)
#
Session(server)

# TODO get rid of store (or redo)
dash_app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dcc.Store(id='initial-call', data=True),
    dash.page_container,
])

if __name__ == '__main__':
    dash_app.run(host='192.168.0.225', port=5000, debug=True)  # (debug=True)   (host='192.168.0.225', port=5000, debug=True)



