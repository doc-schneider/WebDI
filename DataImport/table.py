from sqlalchemy import create_engine, MetaData
import mysql.connector

from DataStructures.TableTypes import TableType, table_definitions, table_columns_names_types
from DataOperations.MySQL import create_table, create_table_mysql, table_insert, add_columns, add_foreign_key
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

# Add foreign key column
foreign_table = "events"
foreign_column = table_definitions[TableType.EVENT]["PrimaryKey"]
add_foreign_key(conn, mycursor, "albums", foreign_column, foreign_table)

# Add column
table_name = "document_collections"
column_name = "EVENT"
#column_type = "TEXT"
add_columns(conn, mycursor, table_name, {column_name: table_columns_names_types[column_name]["mysqltype"]})
#query = f'ALTER TABLE {table_name} ADD  COLUMN {column_name} {column_type};'  # AFTER {after};'
#mycursor.execute(query)
#conn.commit()

# Create table
# create_table(db_engine, metadata, "documents", table_definitions[TableType.DOCUMENT], foreign_table="document_collections")
create_table_mysql(
    conn, mycursor,
    "events",
    table_definitions[TableType.EVENT],
    foreign_table_name="events",
    foreign_table_dct=table_definitions[TableType.EVENT],
)

# Delete column
table_name = "photos"
column_name = "TAG"
query = f'ALTER TABLE {table_name} DROP COLUMN {column_name};'
mycursor.execute(query)
conn.commit()

# Set column values
table_name = "albums"
column_set = "ID_EVENT"
column_if = "ID_ALBUM"
query = f"UPDATE {table_name} SET {column_set} =  CASE WHEN {column_if} = 23 THEN 1 END;"
mycursor.execute(query)
conn.commit()







