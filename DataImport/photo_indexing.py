import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

from DataStructures.Document import DocumentTable
from DataOperations.Photos import PhotoFactory
from DataOperations.MySQL import (
    create_phototable,
    insert_photo_dataframe,
    read_photo_dataframe,
)


make_phototable_fromfolder = True
exist_pretable = True
read_csv = False
write_csv = True
create_phototable_mysql = False
insert_phototable_mysql = False

path_root = 'Y:/'
path_photo = '2022/2022_02_15_Konstanze Geburtstag/'
path_full = path_root + path_photo
mysql_table = "20220215_Konstanze_Geburtstag"

# Pre-description
if exist_pretable:
    path_pre = path_root + path_photo + 'PreDokumentliste.csv'
    pretable = pd.read_csv(
        path_pre,
        encoding='ANSI',
        sep=';',
    )
    pretable = pretable.where(pd.notnull(pretable), None)
    pretable = DocumentTable(pretable)

# Main table
if make_phototable_fromfolder:
    phototable = PhotoFactory.table_from_folder(
        path_full,
        pretable=pretable,
    )

# Event extraction
#eventtable = EventFactory.extract_event_from_table(phototable)
# Tag extraction
#

# Write Tables
if write_csv:
    phototable.to_csv(path_full, "Dokumentliste")

# Read csv table
if read_csv:
    #phototable = DocumentTable(DataTableFactory.importFromCsv(path_table + filename, encoding='ANSI'))
    phototable = pd.read_csv(
        path_full + "Dokumentliste" + ".csv",
        encoding='ANSI',
        sep=';',
        parse_dates=['DATETIME'],
        dayfirst=True
    )
    phototable = phototable.where(pd.notnull(phototable), None)
    phototable = DocumentTable(phototable)

# MySQL
if create_phototable_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/photos'
    db_connection = create_engine(db_connection_str)
    create_phototable(db_connection, mysql_table)

if insert_phototable_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/photos'
    db_connection = create_engine(db_connection_str)
    insert_photo_dataframe(db_connection, mysql_table, phototable)

#  Read table from database
#phototable = read_photo_dataframe(db_connection, mysql_table)

