import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
#import sqlalchemy as db

from DataOperations.MySQL import (
    create_database,
)


# sqlalchemy

# Create database
flag_create_database = True
if flag_create_database:
    engine = create_engine('mysql+mysqlconnector://Stefan:Moppel3@localhost')
    create_database(engine, "di")

flag_continue = False
if flag_continue:

    # Connect to database
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    connection = db_connection.connect()
    metadata = db.MetaData()

    path_root = '//192.168.0.117/'
    path_photo = 'Fotos/2021/2021_09_05_Sonntags Eltern/'
    export_table(db_connection, "2021_09_05_Sonntags_Eltern", path_root + path_photo)

    df = pd.read_sql("SELECT * FROM 2021_0708_Schwarzwald", con=db_connection)
    phototable = read_photo_dataframe(db_connection, "2021_0708_Schwarzwald")

    photos = db.Table('2021_0708_Schwarzwald', metadata, autoload=True, autoload_with=db_connection)
    photos.columns.keys()
    repr(metadata.tables['2021_0708_Schwarzwald'])

    update(db_connection, metadata, '2021_0708_Schwarzwald', "EVENT", "PhotoName",
           ("P1100972.JPG", "Besuch Triberger Wasserfälle")
           )


    # connector

    # Create database
    conn = mysql.connector.connect(
        host="localhost",
        user="Stefan",
        passwd="Moppel3",
    )
    mycursor = conn.cursor()
    create_database(mycursor, db_name="photos")

    # Work on database
    db = mysql.connector.connect(
        host="localhost",
        user="Stefan",
        passwd="Moppel3",
        database="di",
    )
    mycursor = db.cursor()

    # add_column(db, mycursor, '2021_0708_Schwarzwald', "EVENT", "varchar(255)")

    #update(db, mycursor, '2021_0708_Schwarzwald', "EVENT", "PhotoName",
    #       ("P1100972.JPG", "Besuch Triberger Wasserfälle")
    #       )

    alter_column_str(phototable.data, "PATH", "//192.168.0.117/Fotos", "Y:")
    update_column(db, mycursor, '2021_0708_Schwarzwald', "PATH", phototable.data["PATH"])

    #values = ("test_name", "jpg",
    #          dtm.datetime(2020,6,17,15,30,0),
    #          "test_path", "test_description"
    #          )
    #insert_record(db, mycursor, table_name, columns, values)

    #values = phototable.data[['TIME_FROM', 'PATH']].copy()
    #columns_insert = ("DateTime", "Path")
    #insert_array(db, mycursor, table_name, columns_insert, values)

    #mycursor = get_columns(mycursor, table_name, columns)
    #for x in mycursor:
    #    print(x)

    #path_root = '//192.168.0.117/'
    #path_table = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
    #filename = 'Dokumentliste_2020_06_11_Schloss Dyck_photo.csv'
    #phototable = DocumentTable(DataTableFactory.importFromCsv(path_table + filename, encoding='ANSI'))
    #
    #phototable.convert_to_datetime()



