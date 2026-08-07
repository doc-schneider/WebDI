from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataOperations.Message import MessageFactory
from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.MySQL import table_insert
from Initialize.Initialize import initialize_MySQL
import config

config.environment_storage = "LOCAL"
initialize_MySQL()

# Script new message stream + entry in collection
#
message_type = "WhatsApp"
participant = "Konstanze"
# message_collection = "iPhone Nachrichten Stefan Konstanze"
message_collection = "iPhone WhatsApp Stefan Konstanze"
# path_message_stream = Path("W:/Biographie/Stefan/iPhone/Nachrichten/Konstanze Walther/Nachrichten - Konstanze Walther.csv")
path_message_stream = Path("W:/Biographie/Stefan/iPhone/WhatsApp/Konstanze Walther/WhatsApp - Konstanze Walther.csv")
#
# Raw table
message_table = MessageFactory().table_from_folder(
    path_message_stream,
    message_type=message_type,
    message_collection=message_collection,
    attachments_folder="WhatsApp - Konstanze Walther"
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
# Insert new collection
table_insert(config.mysql["metadata"], config.mysql["conn"], "message_collections", collection_table)
#
# Get the foreign key
message_table.add_foreignkey("MESSAGE_COLLECTION", "message_collections", TableType.MESSAGE_COLLECTION)
#
# Insert the new messages
table_insert(config.mysql["metadata"], config.mysql["conn"], "messages", message_table.table)

print("done")
