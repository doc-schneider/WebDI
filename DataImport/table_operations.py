import pandas as pd
from sqlalchemy import create_engine, inspect

from DataStructures.Document import DocumentTableFactory
from DataStructures.TableTypes import column_types_table
from DataOperations.MySQL import (
    drop_column,
    create_specific_table,
    read_specific_dataframe,
    insert_specific_dataframe,
    drop_table,
    export_table,
    alter_record
)


# TODO:
#  DocumentGroup: Extend attributes to all group members
#  Tag extraction

add_rows = False
delete_column = False
add_column = False
delete_table = True
interpolate_events = False
add_eventid = False
export_table_csv = False
alter_entry = False

if add_rows:
    table_type = "events"
    mysql_table = "events"
    file = "Z:/Biographie/Stefan/Timeline/EventListe.csv"

if delete_column:
    table_type = "notes"
    mysql_table = "notes"
    column = "TableName"

if delete_table:
    mysql_table = "note_diary_ideasscience_diary"

if export_table_csv:
    mysql_table = "notes"  # = csv_table
    pathname = "Z:/Biographie/Stefan/Tables/"

if interpolate_events:
    pass

if add_eventid:
    EventId = 31
    mysql_table = "photo_20220318_Geburtstag"
    PhotoId = range(2, 21+1)

if alter_entry:
    mysql_table = "note_energy_finance_energy_modelling"
    table_type = "note"
    where_tuple = None  # ("NOTE_TABLE", "note_energy_finance_energy_modelling")
    set_tuple = ("TAG", "Energy Modelling")

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)


if add_rows:
    # MySql table
    mysqltable = read_specific_dataframe(db_connection, mysql_table, table_type)
    # Remove non-defined columns
    documenttable = DocumentTableFactory.from_csv(
        table_type,
        file,
        parse_date=["TIME_FROM", "TIME_TO"]
    )
    # Compare on Event Name
    add_table = documenttable.data[
        documenttable.data["EVENT_NAME"].apply(
            lambda x: False if x in mysqltable["EVENT_NAME"].values else True
        )
    ]
    insert_specific_dataframe(db_connection, mysql_table, table_type, add_table)

if delete_column:
    drop_column(db_connection, mysql_table, table_type, column)

if delete_table:
    drop_table(db_connection, mysql_table)

if export_table_csv:
    export_table(db_connection, mysql_table, pathname)

if add_eventid:
    # Does column EventId exist?
    inspector = inspect(db_connection)
    result = inspector.get_columns(mysql_table)
    if not "EventID" in [res["name"] for res in result]:
        # Create column
        with db_connection.connect() as con:
            # TODO Combine into one statement
            rs = con.execute(
                "ALTER TABLE photo_20220318_Geburtstag ADD EventID integer;"
            )
            rs = con.execute(
                "ALTER TABLE photo_20220318_Geburtstag ADD FOREIGN KEY (EventID) REFERENCES events(EventID);"
            )
    # Add EventID
    with db_connection.connect() as con:
        for id in PhotoId:
            rs = con.execute(
                "UPDATE photo_20220318_Geburtstag SET EventID=" + str(EventId) + " WHERE PhotoID=" + str(id) + " ;"
            )

if alter_entry:
    alter_record(db_connection, mysql_table, table_type, set_tuple, where_tuple)