import pandas as pd
from sqlalchemy import create_engine, MetaData
import mysql.connector

from Initialize.Initialize import initialize_MySQL
from DataStructures.TableTypes import TableType, table_definitions, table_columns_names_types
from DataOperations.MySQL import create_table, create_table_mysql, table_insert, add_columns, add_foreign_key, update_column
import config

initialize_MySQL()

# Create table
# create_table(db_engine, metadata, "documents", table_definitions[TableType.DOCUMENT], foreign_table="document_collections")
create_table_mysql(
    config.mysql["connector"], config.mysql["cursor"],
    "messages",
    table_definitions[TableType.MESSAGE],
    foreign_table_name="message_collections",
    foreign_table_dct=table_definitions[TableType.MESSAGE_COLLECTION],
)
# foreign_table_dct=table_definitions[TableType.MESSAGE_COLLECTION]

# Add foreign key column
foreign_table = "events"
foreign_column = table_definitions[TableType.EVENT]["PrimaryKey"]
add_foreign_key(conn, mycursor, "photos", foreign_column, foreign_table)

# Add column
table_name = "photos"
column_name = "AZURE_BLOB"
add_columns(
    config.mysql["connector"], config.mysql["cursor"],
    table_name, {column_name: table_columns_names_types[column_name]["mysqltype"]}
)

# Delete column
table_name = "albums"
column_name = "TAG"
query = f'ALTER TABLE {table_name} DROP COLUMN {column_name};'
mycursor.execute(query)
conn.commit()

# Set column values
table_name = "photos"
column_set = "AZURE_BLOB"
update_column()
# query = f"UPDATE {table_name} SET {column_set} =  %s"
# column_if = "ID_EVENT"
# query = f"UPDATE {table_name} SET {column_set} =  CASE WHEN {column_if} = 24 THEN 5 END;"
#config.mysql["cursor"].execute(query, ("photo", ))
#config.mysql["connector"].commit()

# Fetch table subset (where)
table_name = "albums"
column_name = "ID_ALBUM"
value = 6
query = f"SELECT * FROM {table_name} WHERE {column_name} = {value}"
tbl = pd.read_sql(query, con=conn)






