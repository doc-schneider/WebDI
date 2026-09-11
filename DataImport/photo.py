from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from DataOperations.Photo import PhotoFactory
from DataOperations.MySQL import table_insert, table_insert_mysql, update_column
from Initialize.Initialize import initialize_MySQL
from DataOperations.Azure import AzureFactory
import config

load_dotenv()
config.environment_storage = "LOCAL"
config.environment_app = "LOCAL"
initialize_MySQL()

flag_add_to_azure = True
flag_add_photos = False
flag_add_event = False

# Add photo to existing album
if flag_add_photos:
    id_album = 282

    photo_table_old = DataTable.fetch_table(
        TableType.PHOTO,
        "photos"
    )
    photo_table_old = photo_table_old.match_foreignkey(id_album)

owner = "Stefan|Konstanze"  # "Stefan"  "Stefan|Konstanze"

# Raw photo table
album_name = "Zurheide"
chapters = [
    "Nach langer Pause wieder mal"
]
chapters_path = [
    Path("Y:/2026/2026_09_5_Zurheide"),
]
photo_table = PhotoFactory().table_from_folder(
    TableType.PHOTO,
    chapters_path,
    album_name,
    chapters,
    pretable_file=Path("Y:/2026/2026_09_5_Zurheide/PreDokumentliste.csv")
)
# Path("Y:/2016/2016_11_Australien/Australien_Auswahl/PreDokumentliste.csv")
# exif_key_time="DateTimeOriginal",
# timezone_default="America/Toronto",

if flag_add_photos:
    # Only keep new entries
    photo_table.table = photo_table.table[~photo_table.table["FILE_NAME"].isin(photo_table_old.table["FILE_NAME"])]
    photo_table.table["ID_ALBUM"] = id_album
    # TODO New DATE_FROM/TO for album

# Add Event
# Events from chapters
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

# Extract album data from a new photo dataframe
# TODO from - to not quite right for non CET time ?
if not flag_add_photos:
    owner = owner
    album_description = ""
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
            "DESCRIPTION": album_description,
            "OWNER": owner,
            "CONTENT_TYPE": "PHOTO"
        }
    )
    #
    # Insert new album
    table_insert(config.mysql["metadata"], config.mysql["conn"], "albums", album_table)
    #
    # Get the foreign key for the photo table
    photo_table.add_foreignkey("PHOTO_ALBUM", "albums", TableType.ALBUM)

# Insert the new photos
table_insert(config.mysql["metadata"], config.mysql["conn"], "photos", photo_table.table)

if flag_add_to_azure:
    # Add album entry
    #
    ID_ALBUM = photo_table.table["ID_ALBUM"].unique()[0]
    album_table_mysql = DataTable.fetch_table(
        TableType.ALBUM,
        "albums"
    ).filter({"ID_ALBUM": ID_ALBUM})
    config.environment_storage = "AZURE"
    album_table_azure = DataTable.fetch_table(
        TableType.ALBUM,
        "albums.csv"
    )
    album_table_azure_update = DataTable(
        pd.concat([album_table_mysql.table, album_table_azure.table], ignore_index=True),
        TableType.ALBUM
    )
    AzureFactory.write_table_to_blob("tables", "albums.csv", album_table_azure_update)
    # Get file table and upload
    #
    config.environment_storage = "LOCAL"
    photo_table_mysql = DataTable.fetch_table(
        TableType.PHOTO,
        "photos"
    ).filter({"ID_ALBUM": ID_ALBUM})
    # Add container name
    photo_table_mysql.table["AZURE_CONTAINER"] = "photo"
    # From Azure
    config.environment_storage = "AZURE"
    photo_table_azure = DataTable.fetch_table(
        TableType.PHOTO,
        "photos.csv"
    )
    # Upload files to blob
    PATH_AZURE_BLOB = AzureFactory.upload_from_table_to_blob("photo", "Y:/", photo_table_mysql)
    # Add Blob information
    photo_table_mysql.table["AZURE_BLOB"] = PATH_AZURE_BLOB
    # Append
    photo_table_azure_update = DataTable(
        pd.concat([photo_table_azure.table, photo_table_mysql.table], ignore_index=True),
        TableType.PHOTO,
    )
    # Upload table to blob
    AzureFactory.write_table_to_blob("tables", "photos.csv", photo_table_azure_update)
    # Write blob  names to MySQL table
    value_dct = dict(zip(photo_table_mysql.table["ID_PHOTO"], PATH_AZURE_BLOB))
    update_column(
        config.mysql["connector"], config.mysql["cursor"],
        "photos", "AZURE_BLOB", "ID_PHOTO", value_dct
    )
    value_dct = dict(zip(photo_table_mysql.table["ID_PHOTO"], ["photo"] * photo_table_mysql.table.shape[0]))
    update_column(
        config.mysql["connector"], config.mysql["cursor"],
        "photos", "AZURE_CONTAINER", "ID_PHOTO", value_dct
    )


print("done")

