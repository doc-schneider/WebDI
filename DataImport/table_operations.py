import pandas as pd
from sqlalchemy import create_engine, inspect

from DataStructures.Document import DocumentTableFactory
from DataStructures.TableTypes import column_types_table
from DataOperations.MySQL import (
    create_specific_table,
    read_specific_dataframe,
    insert_specific_dataframe,
    drop_table,
    export_table
)

# TODO:
#  DocumentGroup: Extend attributes to all group members
#  Tag extraction

add_rows = False
delete_table = False
interpolate_events = False
add_eventid = False
make_metatable = False
update_metatable = True
exists_metatable = False
export_table_csv = False

if add_rows:
    table_type = "events"
    mysql_table = "events"
    file = "Z:/Biographie/Stefan/Timeline/EventListe.csv"

if delete_table:
    mysql_table = "photos"

if export_table_csv:
    mysql_table = "photos"  # = csv_table
    pathname = "Z:/Biographie/Stefan/Tables/"

if interpolate_events:
    pass

if add_eventid:
    EventId = 31
    mysql_table = "photo_20220318_Geburtstag"
    PhotoId = range(2, 21+1)

if make_metatable or update_metatable:
    category = "note"
    meta_category = "notes"

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

# TODO Specifc to each catoegory module
if make_metatable:
    create_specific_table(db_connection, meta_category, meta_category)

# TODO
#  Time sort
if update_metatable:
    if exists_metatable:
        metatable = read_specific_dataframe(db_connection, meta_category, meta_category)
        tables_existing = set(metatable["PHOTO_TABLE"])
    else:
        tables_existing = set()

    dct = column_types_table(meta_category)
    dct.pop("primary_key")
    meta_table_add = {value["alias"]: [] for (key, value) in dct.items()}
    columns = list(meta_table_add.keys())

    # Find table of category
    table_names = db_connection.table_names()
    table_names = [tn for tn in table_names if category + "_" in tn]
    for tn in list(set(table_names) - tables_existing):
        # TODO - Transfer tags and events
        # Assume first column is table name
        meta_table_add[columns[0]].append(tn)  # TODO bad style
        table = read_specific_dataframe(db_connection, tn, category)
        if "TIME_FROM" in columns:
            meta_table_add["TIME_FROM"].append(table["DATETIME"].min())
            meta_table_add["TIME_TO"].append(table["DATETIME"].max())
        for item in set(columns[1:]) - set(["TIME_FROM", "TIME_TO", 'TABLE_NAME']):
            meta_table_add[item].append(None)
        meta_table_add['TABLE_NAME'].append(meta_category)  # TODO Useful?

    insert_specific_dataframe(
        db_connection,
        meta_category,
        meta_category,
        pd.DataFrame(meta_table_add)
    )




