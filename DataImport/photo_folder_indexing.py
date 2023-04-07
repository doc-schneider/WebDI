import os
from sqlalchemy import create_engine

from DataStructures.TableTypes import find_optional_columns
from DataStructures.Document import DocumentTableFactory
from DataOperations.Photos import PhotoFactory
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
    read_specific_dataframe
)
from DataOperations.TableOperations import update_metatable


make_phototable_fromfolder = True
# exist_pretable = False  # Automize by looking into folder
write_csv = True
read_csv = False
create_phototable_mysql = True
insert_phototable_mysql = True
read_phototable_mysql = False
update_meta_table = True

path_root = 'Y:/'
path_photo = '2023/'
folder_photo = "2023_03_03"
path_full = path_root + path_photo + folder_photo + "/"
mysql_table = "photo_" + folder_photo.replace(
    " ", "_"
).replace(
    "/", "_"
).replace(
    "-", "_"
)
# mysql_table = "photo_2022_08_28_sonntagsradeln_botanischer_garten"  # Use this as default table name
optional_columns = []  # ["DOCUMENT_GROUP", "LOCATION"]
additional = None  # {"EVENT": "Samstagseinkauf 07.01.2023"}

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

# Pre-description
# TODO Document_Group is read as float (only if None present)
if os.path.isfile(path_full + "PreDokumentliste.csv"):
# if exist_pretable:
    pretable = DocumentTableFactory.from_csv(
        "photo",
        path_full,
        'PreDokumentliste'
    )
    pretable.format_to_category(optional_columns)
else:
    pretable = None

# Main table
if make_phototable_fromfolder:
    phototable = PhotoFactory.table_from_folder(
        path_root + path_photo,
        folder_photo,
        pretable=pretable,
        transfer_events=False,
        additional=additional
    )

# Write Tables
if write_csv:
    phototable.to_csv(path_full, mysql_table)

# Read csv table
if read_csv:
    phototable = DocumentTableFactory.from_csv(
        "photo",
        path_full,
        mysql_table,
        parse_date=['DATETIME']
    )

# MySQL
if create_phototable_mysql:
    create_specific_table(
        db_connection,
        mysql_table,
        "photo",
        find_optional_columns(phototable.data, "photo")
    )

if insert_phototable_mysql:
    insert_specific_dataframe(
        db_connection,
        mysql_table,
        "photo",
        phototable.data,
        find_optional_columns(phototable.data, "photo"),
    )

#  Read table from database
if read_phototable_mysql:
    phototable = read_specific_dataframe(db_connection, mysql_table, "photo")

if update_meta_table:
    update_metatable(db_connection, "photos", "photo")
