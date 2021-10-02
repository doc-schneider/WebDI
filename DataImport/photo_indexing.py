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


path_root = '//192.168.0.117/'
#path_root = 'C:/Users/Stefan/Documents/Bilder/'

path_photo = 'Fotos/2021/2021_09_05_Sonntags Eltern/'

# Pre-description
path_pre = path_root + path_photo + 'PreDokumentliste.csv'
#pretable = DocumentTable(DataTableFactory.importFromCsv(path_pre, encoding='ANSI'))
#pretable = DocumentTable(pd.read_csv(path_pre, sep=';', encoding='ANSI'))

# Main table
path_full = path_root + path_photo
#phototable = PhotoFactory.table_from_folder(path_photo, pretable)
#phototable = PhotoFactory.table_from_folder(
#    path_full,
#    pretable=pretable,
#)

# Event extraction
#eventtable = EventFactory.extract_event_from_table(phototable)

# Write Tables
#path_table = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
#filename = 'Dokumentliste_2021_07-08_Schwarzwald_photo.csv'
#phototable.to_csv()

# Read csv table
#phototable = DocumentTable(DataTableFactory.importFromCsv(path_table + filename, encoding='ANSI'))
#phototable = pd.read_csv(
#    path_table + filename,
#    encoding='ANSI',
#    sep=';',
#    parse_dates=['DATETIME']
#)
#phototable = phototable.where(pd.notnull(phototable), None)

# MySQL
mysql_table = "2021_09_05_Sonntags_Eltern"

# Create table
#conn = mysql.connector.connect(
#    host="localhost",
#    user="Stefan",
#    passwd="Moppel3",
#    database="photos",
#)
#mycursor = conn.cursor()
#create_phototable(conn, mycursor, "2021_09_05_Sonntags_Eltern")

# Write a table into database
#db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/photos'
#db_connection = create_engine(db_connection_str)
#insert_photo_dataframe(db_connection, mysql_table, phototable)
#insert_photo_array(
#    conn, mycursor, "2021_0708_Schwarzwald",
#    phototable[['DOCUMENT_NAME', 'DOCUMENT_TYPE', 'DATETIME', 'PATH', 'DESCRIPTION']].values
#)

#  Read table from database
db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/photos'
db_connection = create_engine(db_connection_str)
phototable = read_photo_dataframe(db_connection, mysql_table)

#phototable.to_csv(path_full, mysql_table)

