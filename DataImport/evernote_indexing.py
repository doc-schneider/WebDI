from sqlalchemy import create_engine

from DataStructures.TableTypes import find_optional_columns
from DataOperations.Evernote import EvernoteFactory
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
)


make_notetable_fromfolder = True
exist_pretable = False
create_table_mysql = True
insert_table_mysql = True

mysql_table = "note_biography_papa"

# One path = one notebook.
path_root = "Z:/Biographie/Stefan/Logs&Blogs/Evernote/"
path_note = "Biography/Papa"

# Main table
if make_notetable_fromfolder:
    notetable = EvernoteFactory.table_from_path(path_root, path_note)

# MySQL
if create_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    create_specific_table(
        db_connection,
        mysql_table,
        "note",
        find_optional_columns(notetable.data, "note")
    )

if insert_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    insert_specific_dataframe(
        db_connection,
        mysql_table,
        "note",
        notetable.data,
        find_optional_columns(notetable.data, "note")
    )
