import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import sqlalchemy as db

from DataOperations.MySQL import (
    create_database,
    create_specifictable,
    insert_dataframe
)


open_connection = False
open_engine = True
make_database = False
make_table = False
read_csv = True
write_table = True

if open_connection:
    conn = mysql.connector.connect(
        host="localhost",
        user="Stefan",
        passwd="Moppel3",
    )

db_name = "portal"

# Create database
if make_database:
    mycursor = conn.cursor()
    create_database(mycursor, db_name=db_name)

if open_connection:
    conn.connect(database=db_name)
    mycursor = conn.cursor()

mysql_table = "portal"  # "KonstanzeStefan"

# Create table
if make_table:
    create_specifictable(conn, mycursor, mysql_table, "portal")

if open_connection:
    conn.close()

if open_engine:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/portal'
    db_connection = create_engine(db_connection_str)
    connection = db_connection.connect()
    metadata = db.MetaData()

# Read csv table
if read_csv:
    path = 'Z:/DigitalImmortality/Document and Event Tables/Portal/'
    table = pd.read_csv(
        path + "Tabelle_Portal.csv",
        encoding='ANSI',
        sep=';',
        dayfirst=True
    )

if write_table:
    insert_dataframe(db_connection, mysql_table, "portal", table, if_exists="append")