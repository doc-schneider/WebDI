import pandas as pd
from sqlalchemy import create_engine, MetaData
import mysql.connector

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.MySQL import create_table, table_insert, add_columns
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


# Add column
table_name = "photos"
column_name = "TAG"
column_type = "TEXT"
after = "CHAPTER"
query = f'ALTER TABLE {table_name} ADD  COLUMN {column_name} {column_type} AFTER {after};'
mycursor.execute(query)
conn.commit()

# Delete column
table_name = "photos"
column_name = "TAG"
query = f'ALTER TABLE {table_name} DROP COLUMN {column_name};'
mycursor.execute(query)
conn.commit()







