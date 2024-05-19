from sqlalchemy import create_engine, MetaData
from pathlib import Path

from DataOperations.Photo import PhotoFactory


db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
db_engine = create_engine(db_connection_str)
db_conn = db_engine.connect()
metadata = MetaData()
metadata.reflect(bind=db_engine)

photo_table = PhotoFactory().table_from_folder(
    [
        Path("Y:/2024/2024_04_26-05_01_Paris/01_Ankunft"),
        Path("Y:/2024/2024_04_26-05_01_Paris/02_Ile & Marais"),
    ],
    "Reise Paris 2024",
    {
        "Ankunft": ("IMG_8570.HEIC", "IMG_8579.HEIC"),
        "Ile & Marais": ("IMG_8581.HEIC", "IMG_8645.HEIC"),
    },
    Path("Y:/2024/2024_04_26-05_01_Paris/PreDokumentliste.csv")
)

