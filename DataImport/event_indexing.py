import pandas as pd
from sqlalchemy import create_engine

from DataOperations.Events import EventFactory
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
)


make_from_csv = True
create_table_mysql = False
insert_table_mysql = True

path_root = 'Z:/'
path_csv = "Biographie/Stefan/Timeline/"
csv_table = "EventListe.csv"
mysql_table = "events"

if make_from_csv:
    events_table = EventFactory.table_from_csv(path_root + path_csv + csv_table)

if create_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    create_specific_table(db_connection, mysql_table, "events")

if insert_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    insert_specific_dataframe(db_connection, mysql_table, "events", events_table.data)



