import pandas as pd
from sqlalchemy import create_engine, MetaData
import mysql.connector
from flask import session

from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
import config


def session_init(app):
    @app.before_request
    def ensure_session_initialized():
        init_session()

def init_session():
    if 'initialized' not in session:
        session['ALBUM'] = {"ID_ALBUM": 7}
        session['FILM'] = {"ID_FILM": 1}
        session['MESSAGE_COLLECTION'] = {"ID_MESSAGE_COLLECTION": 1}
        session['NOTEBOOK'] = {"ID_NOTEBOOK": 3}
        session['table_content'] = TableType.FILM.name
        session['album_content'] = TableType.PHOTO.name
        session['album_view'] = {"IX_PHOTO": [None], "IX_PHOTO_PAGE": [None]}
        session['timeline_content'] = TableType.ALBUM.name
        session['timeline_view'] = {"GRANULARITY": "Y", "DATETIME_START": pd.Timestamp(2024, 1, 1), "n_rows": 10}
        session['content_content'] = TableType.PHOTO.name
        session['content_view'] = {"ID_PHOTO": 313, "ID_PHOTO_PAGE": 1, "ID_NOTE": 1, "ID_MESSAGE": 1}  # TODO Necessary to pre-specify?
        session['initialized'] = True

def initialize_MySQL():
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

def init_tables(environment_storage):
    if environment_storage == "LOCAL":
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
            TableType.PHOTO_PAGE: {
                "storage_name": "photo_pages",
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
    elif environment_storage == "AZURE":
        config.table = {
            TableType.ALBUM: {
                "storage_name": "albums.csv",
                "data_table": None
            },
            TableType.PHOTO: {
                "storage_name": "photos.csv",
                "data_table": None
            },
            TableType.FILM: {
                "storage_name": "films.csv",
                "data_table": None
            },
            TableType.FILM_CONTENT: {
                "storage_name": "film_contents.csv",
                "data_table": None
            }
        }
    for key in config.table.keys():
        config.table[key]["data_table"] = DataTable.fetch_table(
            key,
            config.table[key]["storage_name"]
        )
