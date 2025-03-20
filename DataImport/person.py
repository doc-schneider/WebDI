import pandas as pd
from sqlalchemy import create_engine, MetaData
import mysql.connector

from DataStructures.TableTypes import TableType, table_definitions, table_columns_names_types
from DataOperations.MySQL import create_table, create_table_mysql, table_insert_mysql, add_columns, add_foreign_key
import config


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Moppel3!",
    database="lives",
)
mycursor = conn.cursor()
#
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

person_table = pd.DataFrame(
    data={
        "PERSON": ["Stefan", "Konstanze"],
        "FIRST_NAME": ["Stefan", "Konstanze"],
        "LAST_NAME": ["Schneider", "Schneider"]
    }
)

table_insert_mysql(conn, mycursor, "persons", person_table)
