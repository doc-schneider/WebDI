from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from DataOperations.Photo import PhotoFactory
from DataOperations.MySQL import table_insert
from Initialize.Initialize import initialize_MySQL
import config


config.environment_storage = "LOCAL"
initialize_MySQL()

album_name = "Papas VHS-Filme"
flag_album_new = False

if flag_album_new:
    owner = "Papa"
    album_description = ""
    date_from = pd.Timestamp(1995, 10, 19)
    date_to = pd.Timestamp(1999, 4, 24)

    album_table = pd.DataFrame(
        index=[0],
        data={
            "PHOTO_ALBUM": album_name,
            "DATE_FROM": date_from,
            "DATE_TO": date_to,
            "DESCRIPTION": album_description,
            "OWNER": owner
        }
    )

    table_insert(config.mysql["metadata"], config.mysql["conn"], "albums", album_table)

# Add film to album
film_table = pd.DataFrame(
    index=[0],
    data={
        "FILE_NAME": "VHS_Papa_F 1997.mp4",
        "FILE_FORMAT": "MP4",
        "PATH": str(Path("Y:/Fotoalben Schneider/Papa VHS/F_1997")),
        "DATE_FROM": pd.Timestamp(1997, 7, 1),
        "DATE_TO": pd.Timestamp(1998, 7, 1),
        "DESCRIPTION": "",
        "CHAPTER": "Film F",
        "PHOTO_ALBUM": album_name,
        "ATTACHMENT": str(Path("Y:/Fotoalben Schneider/Papa VHS/F_1997/PreDokumentliste.csv"))
    }
)
film_table = DataTable(film_table, TableType.PHOTO)
film_table.add_foreignkey("PHOTO_ALBUM", "albums")

table_insert(config.mysql["metadata"], config.mysql["conn"], "photos", film_table.table)



