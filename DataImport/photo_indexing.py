import pandas as pd
from sqlalchemy import create_engine

from DataStructures.TableTypes import find_optional_columns
from DataStructures.Document import DocumentTableFactory
from DataOperations.Photos import PhotoFactory
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
    read_specific_dataframe
)


make_phototable_fromfolder = False
exist_pretable = False
write_csv = False
read_csv = True
create_phototable_mysql = False
insert_phototable_mysql = False
read_phototable_mysql = False

path_root = 'Y:/'
path_photo = '2022/'
folder_photo = "2022_06_10_Wuppertal Konferenz"
path_full = path_root + path_photo + folder_photo + "/"
mysql_table = "photo_20220610_wuppertal_konferenz" # Use this as default table name

optional_columns = ["LOCATION"]

# Pre-description
if exist_pretable:
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
    )
    # Document Group
    pass

# Event extraction
#eventtable = EventFactory.extract_event_from_table(phototable)
# Tag extraction
#

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
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    create_specific_table(
        db_connection,
        mysql_table,
        "photo",
        find_optional_columns(phototable.data, "photo")
    )

if insert_phototable_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    insert_specific_dataframe(
        db_connection,
        mysql_table,
        "photo",
        phototable.data,
        find_optional_columns(phototable.data, "photo")
    )

#  Read table from database
if read_phototable_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    phototable = read_specific_dataframe(db_connection, mysql_table, "photo")

