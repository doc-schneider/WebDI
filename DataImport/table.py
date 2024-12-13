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

# Create table
create_table(db_engine, metadata, "documents", table_definitions[TableType.DOCUMENT], foreign_table="document_collections")

# Add column
table_name = "document_collections"
column_name = "TAG"
column_type = "TEXT"
after = "DESCRIPTION"
query = f'ALTER TABLE {table_name} ADD  COLUMN {column_name} {column_type} AFTER {after};'
mycursor.execute(query)
conn.commit()

# Delete column
table_name = "photos"
column_name = "TAG"
query = f'ALTER TABLE {table_name} DROP COLUMN {column_name};'
mycursor.execute(query)
conn.commit()

# Set column values
table_name = "albums"
column_set = "TAG"
column_if = "ID_ALBUM"
tag = 'Papas Kunst'
query = f"UPDATE {table_name} SET {column_set} =  CASE WHEN {column_if} = 12 THEN 'Papas Kunst' ELSE 'Fotoalbum Stefan & Konstanze' END;"
mycursor.execute(query)
conn.commit()







