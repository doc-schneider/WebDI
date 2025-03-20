from sqlalchemy import create_engine, MetaData
import mysql.connector
import config


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
