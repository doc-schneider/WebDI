from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.Photo import PhotoFactory
from DataOperations.MySQL import table_insert
from Initialize.Initialize import initialize_MySQL
import config


config.environment_storage = "LOCAL"
initialize_MySQL()

# Script new photo album + entry in collection
#
# Raw photo table
chapters = ["Es schmeckt!"]
photo_table = PhotoFactory().table_from_folder(
    [
        Path("Y:/2025/2025_03_20_Bull Steak"),
    ],
    "Geburtstag mit Steak",
    chapters,
    pretable_file=Path("Y:/2025/2025_03_20_Bull Steak/PreDokumentliste.csv")
)
#
# Add Event
# Events from chapters
flag_add_event = False
if flag_add_event:
    photo_table.table["EVENT"] = photo_table.table["CHAPTER"]
    events_dct = {c: {"EVENT": c,
                      "DATE_FROM": photo_table.table.loc[photo_table.table["CHAPTER"] == c, "DATE_TIME"].min(),
                      "DATE_TO": photo_table.table.loc[photo_table.table["CHAPTER"] == c, "DATE_TIME"].max(),
                      "DESCRIPTION": "",
                      "PARENT_EVENT": "Reise nach Indien 2024"
                      } for c in chapters}
    events_dct["Delhi"]["DESCRIPTION"] = "Bei der ersten Fahrt mit Führer in die Stadt denke ich, dass Indien mir wenig Spaß machen wird. Soviel Vermüllung habe ich noch nie gesehen. Die extreme Huperei. Die Menschenmassen. Die furchtbaren, verfallen Betongrotten der Häuser. Allerdings gewöhnt man sich. Am letzten Reisetag kommt mir Delhi sogar überdurchschnittlich vor. Fairerweise muss man sagen, dass man auf solchen Reisen eben auch kaum bürgerliches Leben sieht, Apartments etc. Immer die unterste Ebene."
    foreign_key = table_definitions[TableType.EVENT]["ForeignKey"]
    for c in chapters:
        event_table = pd.DataFrame(
            index=[0],
            data={
                "EVENT": c,
                "DATE_FROM": events_dct[c]["DATE_FROM"],
                "DATE_TO": events_dct[c]["DATE_TO"],
                "PARENT_EVENT": events_dct[c]["PARENT_EVENT"],
                "DESCRIPTION": events_dct[c]["DESCRIPTION"],
            }
        )
        event_table[foreign_key] = 8
        table_insert_mysql(conn, mycursor, "events", event_table)
    # plain
    # photo_table.table["ID_EVENT"] = 7
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
        "PHOTO_ALBUM": album,
        "DATE_FROM": date_from,
        "DATE_TO": date_to,
        "DESCRIPTION": "",
        "OWNER": "Stefan|Konstanze"
    }
)  # "OWNER": "Stefan|Konstanze"
#
# Insert new album
table_insert(config.mysql["metadata"], config.mysql["conn"], "albums", album_table)
#
# Get the foreign key for the photo table
photo_table.add_foreignkey("PHOTO_ALBUM", "albums")
#
# Insert the new photos
table_insert(config.mysql["metadata"], config.mysql["conn"], "photos", photo_table.table)

print("done")

