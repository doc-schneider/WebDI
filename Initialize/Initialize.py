import pandas as pd
from sqlalchemy import create_engine, MetaData
import mysql.connector
from flask import session

from DataStructures.TableTypes import TableType
import config


def register_session_init(app):
    @app.before_request
    def ensure_session_initialized():
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
