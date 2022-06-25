import pandas as pd
from sqlalchemy import create_engine

from DataStructures.Event import EventTable
from DataStructures.TableTypes import column_types_table
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
)


make_from_csv = True
create_table_mysql = False
insert_table_mysql = True

path_root = 'Z:/'
path_csv = "Biographie/Stefan/Timeline/"
csv_table = "EventListe"
path_full = path_root + path_csv
mysql_table = "events"

if make_from_csv:
    table = pd.read_csv(
        path_full + csv_table + ".csv",
        encoding='ANSI',
        sep=';',
        parse_dates=["TIME_FROM", "TIME_TO"],
        dayfirst=True
    )
    table = table.where(pd.notnull(table), None)

    # Remove non-defined columns
    cols = set(table.columns)
    dct = column_types_table("events")
    dct.pop("primary_key")
    cols_all = set([value["alias"] for (key,value) in dct.items()])
    table.drop(columns=list(cols - cols_all), inplace=True)
    for c in list(cols_all - cols):
        table[c] = None

    # TODO: Fill ParentEventId

if create_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    create_specific_table(db_connection, mysql_table, "events")

if insert_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    insert_specific_dataframe(db_connection, mysql_table, "events", table)



