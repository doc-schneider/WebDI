from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.Document import DocumentFactory
from DataOperations.MySQL import table_insert
import config

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

# Script new document collection + entry in collection
#
# Raw  table
document_table = DocumentFactory().table_from_folder(
    [
        Path("X:/Wohnung/2024_Anstreichen/Vorab"),
        Path("X:/Wohnung/2024_Anstreichen/Abnahme"),
    ],
    "Wohnung streichen 2024",
    [
        "Vorab",
        "Abnahme"
    ],
    pretable_file=Path("X:/Wohnung/2024_Anstreichen/PreDokumentliste.csv")
)
#
# Extract album data from a new photo dataframe
document_collection = document_table.table[""].unique()[0]
d_t = document_table.table["DATE_TIME"]
date_from = d_t.min()
date_to = d_t.max()
cols = list(table_definitions[TableType.DOCUMENT_COLLECTION]["Columns"].keys())
document_collection_table = pd.DataFrame(
    index=[0],
    data={
        cols[0]: document_collection,
        cols[1]: date_from,
        cols[2]: date_to,
        cols[3]: ""
    }
)
document_collection_table["DESCRIPTION"] = "Nach meiner Strategie wähle ich einen Handwerker aus der Nachbarschaft." \
                             "Mit sehr guten Google Rezensionen"
#TODO Adding column doesn't work with metadata
document_collection_table["TAG"] = "Handwerker"
#
# Insert new album
table_insert(metadata, db_conn, "document_collections", document_collection_table)
#
# Get the foreign key for the  table
document_table.add_foreignkey("DOCUMENT_COLLECTION", "document_collections")
#
# Insert the new
table_insert(metadata, db_conn, "documents", document_table.table)

print("done")

