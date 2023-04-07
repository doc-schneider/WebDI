from sqlalchemy import create_engine

from DataStructures.TableTypes import find_optional_columns
from DataStructures.Document import DocumentTableFactory
from DataOperations.Evernote import EvernoteFactory
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
)
from DataOperations.TableOperations import update_metatable


# TODO Additive mode for new notes. Not overwritign exisintg tables

make_notetable_fromfolder = True
pretable = None
optional_columns = ["Event"]
read_date_from_title = True
write_csv = True
read_csv = False
create_table_mysql = True
exists_table_mysql = False
insert_table_mysql = True
update_meta_table = False

mysql_table = "note_diary_ideasscience_diary"

# One path = one notebook.
path_root = "Z:/Biographie/Stefan/Logs&Blogs/Evernote/"
path_note = "Tagebuch & wissenschaftliche Ideen/Diary"
path_full = path_root + path_note + "/"

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

# Main table
if make_notetable_fromfolder:
    notetable = EvernoteFactory.table_from_path(
        path_root,
        path_note,
        pretable=pretable,
        optional_columns=optional_columns,
        read_date_from_title=read_date_from_title
    )

# Write Tables
if write_csv:
    notetable.to_csv(path_full, mysql_table)

# Read csv table
if read_csv:
    notetable = DocumentTableFactory.from_csv(
        "note",
        path_full,
        mysql_table,
        parse_date=['DATETIME']
    )

# MySQL
if create_table_mysql:
    create_specific_table(
        db_connection,
        mysql_table,
        "note",
        find_optional_columns(notetable.data, "note")
    )

if insert_table_mysql:
    if exists_table_mysql:
        # TODO Falsely removes NoteID (primary key)
        if_exists = "replace"
    else:
        if_exists = "append"

    insert_specific_dataframe(
        db_connection,
        mysql_table,
        "note",
        notetable.data,
        find_optional_columns(notetable.data, "note"),
        if_exists=if_exists
    )

# TODO Category for table
if update_meta_table:
    update_metatable(db_connection, "notes", "note")
