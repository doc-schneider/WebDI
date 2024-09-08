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
#
# Raw photo table
photo_table = PhotoFactory().table_from_folder(
    [
        Path("Y:/2024/2024_09_07_Igudesman & Joo"),
    ],
    "Konzert Tonhalle 7. Sep 2024",
    [
        "Igudesman & Joo & Gäste"
    ],
    pretable_file=None
)

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
album_table["DESCRIPTION"] = "Igudesman & Joo kannte ich über YouTube. War überrascht, dass sie in Düsseldorf auftreten. Sehr gut, sehr unterhaltsam. Man merkt, dass es alles Musiker von Weltniveau sind. Sehr gekonnter Bogen von den Blödel-Barden Ass-Dur bis zu dem ernsthaften iranischen Lautenisten, der Woody Woodpecker vertont. Ein origineller Zugang zu klassicher Musik"
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

