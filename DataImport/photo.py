from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.Photo import PhotoFactory
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

# Script new photo album + entry in collection
#
# Raw photo table
photo_table = PhotoFactory().table_from_folder(
    [
        Path("Y:/2025/2025_02_08_Manufactum"),
    ],
    "Manufactum: Neuer Trolley & Stulle",
    [
        "Stulle essen",
    ],
    pretable_file=Path("Y:/2025/2025_02_08_Manufactum/PreDokumentliste.csv")
)
# Add Event
photo_table.table["EVENT"] = ""
#
# Extract album data from a new photo dataframe
album = photo_table.table["PHOTO_ALBUM"].unique()[0]
d_t = photo_table.table["DATE_TIME"]
date_from = d_t.min()
date_to = d_t.max()
cols = list(table_definitions[TableType.ALBUM]["Columns"].keys())
album_table = pd.DataFrame(
    index=[0],
    data={
        cols[0]: album,
        cols[1]: date_from,
        cols[2]: date_to,
        cols[3]: ""
    }
)
album_table["DESCRIPTION"] = "Manufactum: Wir brauchen einen neuen Trolley"
album_table["TAG"] = "Fotoalbum Stefan & Konstanze;samstags"
# Add Event
#album_table["ID_EVENT"] = 6
#
# Insert new album
table_insert(metadata, db_conn, "albums", album_table)
#
# Get the foreign key for the photo table
photo_table.add_foreignkey("PHOTO_ALBUM", "albums")
#
# Insert the new photos
table_insert(metadata, db_conn, "photos", photo_table.table)

print("done")

