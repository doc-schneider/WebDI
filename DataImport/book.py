from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.Photo import PhotoFactory
from DataOperations.MySQL import table_insert
from Initialize.Initialize import initialize_MySQL
import config


config.environment_storage = "LOCAL"
initialize_MySQL()

root = Path("Y:/Fotoalben Schneider/06_März 1976 - August 1977")
chapter_dirs = [p.name for p in root.iterdir() if p.is_dir()]
chapters = [c[3:] for c in chapter_dirs]
#
book_name = "06_März 1976 - August 1977"
# chapters = [
# ]
book_table = PhotoFactory().table_from_folder(
    TableType.PHOTO_PAGE,
    [root / Path(c) for c in chapter_dirs],
    book_name,
    chapters,
    pretable_file=Path("Y:/Fotoalben Schneider/06_März 1976 - August 1977/PreDokumentliste.csv")
)

owner = "Schneider"
album_description = ""
album = book_table.table["PHOTO_ALBUM"].unique()[0]
date_from = pd.Timestamp(1976, 3, 1)
date_to = pd.Timestamp(1977, 9, 1)
cols = list(table_definitions[TableType.ALBUM]["Columns"].keys())
album_table = pd.DataFrame(
    index=[0],
    data={
        "PHOTO_ALBUM": album,
        "DATE_FROM": date_from,
        "DATE_TO": date_to,
        "DESCRIPTION": album_description,
        "OWNER": owner
    }
)
#
# Insert new album
table_insert(config.mysql["metadata"], config.mysql["conn"], "albums", album_table)

# Get the foreign key for the photo table
book_table.add_foreignkey("PHOTO_ALBUM", "albums", TableType.ALBUM)

# Insert the new photos
table_insert(config.mysql["metadata"], config.mysql["conn"], "photo_pages", book_table.table)
