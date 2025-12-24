from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataOperations.Message import MessageFactory
from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.MySQL import table_insert
import config

config.environment_storage = "LOCAL"

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

# Script new message stream + entry in collection
#
message_collection = "iPhone Nachrichten Stefan Konstanze"
path_message_stream = Path("W:/Biographie/Stefan/iPhone/Nachrichten/Konstanze Walther/Nachrichten - Konstanze Walther.csv")
#
# Raw table
message_table = MessageFactory().table_from_folder(
    path_message_stream,
    message_collection=message_collection,
    attachments_folder="Messages - Konstanze Walther"
)
#
# Create Message Collection table
cols = list(table_definitions[TableType.MESSAGE_COLLECTION]["Columns"].keys())
collection_table = pd.DataFrame(columns=cols)
collection_table.loc[0, "MESSAGE_COLLECTION"] = message_collection
collection_table["OWNER"] = "Stefan"
collection_table["PARTICIPANT"] = "Konstanze"
d_t = message_table.table["DATE_TIME"]
date_from = d_t.min()
date_to = d_t.max()
collection_table["DATE_FROM"] = date_from
collection_table["DATE_TO"] = date_to
collection_table["PATH"] = str(path_message_stream.parent)  # TODO Process with Data class
collection_table["FILE_NAME"] = path_message_stream.name
collection_table["FILE_FORMAT"] = path_message_stream.suffix.lstrip(".").upper()
collection_table["DESCRIPTION"] = ""
table_insert(metadata, db_conn, "message_collections", collection_table)
#
# Get the foreign key
message_table.add_foreignkey("MESSAGE_COLLECTION", "message_collections", TableType.MESSAGE_COLLECTION)
#
# Insert the new messages
table_insert(metadata, db_conn, "messages", message_table.table)

print("done")
