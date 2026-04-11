from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.Document import DocumentFactory
from DataOperations.MySQL import table_insert
from Initialize.Initialize import initialize_MySQL
import config


config.environment_storage = "LOCAL"
initialize_MySQL()

# Script new document collection + entry in collection
#
# Raw  table
collection_name = "Unterlagen Mama"
chapters = [
    "Geburturkunde Mama",
    "Taufschein Mama"
]
chapters_path = [
    Path("W:/Biographie/Schneider/Stammbuch/Geburtsurkunde Mama"),
    Path("W:/Biographie/Schneider/Stammbuch/Taufschein Mama"),
]
document_table = DocumentFactory().table_from_folder(
    chapters_path,
    collection_name,
    chapters,
    pretable_file=Path("W:/Biographie/Mama/TABLES/DOCUMENT_COLLECTION_Mama_Unterlagen.csv"),
)
#
# Extract album data from a new photo dataframe
document_collection = document_table.table["DOCUMENT_COLLECTION"].unique()[0]
d_t = document_table.table["DATE_TIME"]
date_from = d_t.min()
date_to = d_t.max()
cols = list(table_definitions[TableType.DOCUMENT_COLLECTION]["Columns"].keys())
document_collection_table = pd.DataFrame(
    index=[0],
    data={
        "DOCUMENT_COLLECTION": document_collection,
        "DATE_FROM": date_from,
        "DATE_TO": date_to,
        "DESCRIPTION": "",
        "OWNER": "Mama"
    }
)
#
# Insert new document collection
table_insert(config.mysql["metadata"], config.mysql["conn"], "document_collections", document_collection_table)
#
# Get the foreign key for the  table
document_table.add_foreignkey("DOCUMENT_COLLECTION", "document_collections", TableType.DOCUMENT_COLLECTION)
#
# Insert the new
table_insert(config.mysql["metadata"], config.mysql["conn"], "documents", document_table.table)

print("done")

