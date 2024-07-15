from sqlalchemy import create_engine, MetaData
from pathlib import Path

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

photo_table = PhotoFactory().table_from_folder(
    [
        Path("Y:/2023/2023_09_30-10_3_Amsterdam/01_Ankunft"),
        Path("Y:/2023/2023_09_30-10_3_Amsterdam/02_Rijksmuseum"),
        Path("Y:/2023/2023_09_30-10_3_Amsterdam/03_Letzter Tag"),
    ],
    "Reise Amsterdam 2023",
    [
        "Ankunft",
        "Rijksmuseum",
        "Letzter Tag",
    ],
    Path("Y:/2023/2023_09_30-10_3_Amsterdam/PreDokumentliste.csv")
)

photo_table.add_foreignkey("PHOTO_ALBUM", "albums")

table_insert(metadata, db_conn, "photos", photo_table.table)

print("done")

