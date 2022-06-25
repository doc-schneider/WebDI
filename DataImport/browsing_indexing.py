import pandas as pd
from sqlalchemy import create_engine

from DataStructures.Document import DocumentTable
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
)


make_browsing_from_csv = True
create_browsingtable_mysql = False
insert_browsingtable_mysql = True

date = "2022-02-27"
path_root = 'Z:/'
path_browse = 'Biographie/Stefan/Timeline/'
path_full = path_root + path_browse
mysql_table = "browsing_20220227"  # TODO Is "20220227" a problem

# TODO Move that to Browsing and Data
if make_browsing_from_csv:
    table = pd.read_csv(
        path_full + date + "/" + 'browsing.csv',
        encoding='ANSI',
        sep=';',
        parse_dates=["DATETIME"],
        dayfirst=True
    )
    # TODO What to do with NaT?
    table = table.where(pd.notnull(table), None)
    table = DocumentTable(table)

# MySQL
if create_browsingtable_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/browsing'
    db_connection = create_engine(db_connection_str)
    create_specific_table(db_connection, mysql_table, "browsing")

if insert_browsingtable_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/browsing'
    db_connection = create_engine(db_connection_str)
    insert_specific_dataframe(db_connection, mysql_table, "browsing", table.data)

#  Read table from database
#phototable = read_photo_dataframe(db_connection, mysql_table)

