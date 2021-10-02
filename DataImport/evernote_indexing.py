import mysql.connector
from sqlalchemy import create_engine

from DataOperations.Evernote import EvernoteFactory
from DataOperations.MySQL import (
    create_diarytable,
    insert_diary_dataframe,
    read_diary_dataframe
)

# One path = one notebook.
category = "personal diary"
descriptions = None
events = None
#path_root = 'C:/Users/Stefan/Documents/Writings & Web/Evernote/2020-01'
path_root = "//192.168.0.117/Stefan/Biographie/Stefan/Logs&Blogs/Evernote/"
#path_note = 'Familie/Mamas Sachen'
path_note = "Tagebuch & wissenschaftliche Ideen/Diary"

# Make table
#evernotetable = EvernoteFactory.table_from_path(path_root, path_note, category, events)

# Create table
#conn = mysql.connector.connect(
#    host="localhost",
#    user="Stefan",
#    passwd="Moppel3",
#    database="diaries",
#)
#mycursor = conn.cursor()
#create_diarytable(conn, mycursor, "Diary")

# Write a table into database
#db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/diaries'
#db_connection = create_engine(db_connection_str)
#insert_diary_dataframe(db_connection, "Diary", evernotetable)

# Write Table
#filename = 'Dokumentliste_Diary'
#evernotetable.to_csv(path_root + "/" + path_note, filename)

#  Read table from database
db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/diaries'
db_connection = create_engine(db_connection_str)
evernotetable = read_diary_dataframe(db_connection, "Diary")
