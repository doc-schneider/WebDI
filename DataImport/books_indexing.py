import pandas as pd
from sqlalchemy import create_engine

from DataOperations.Photos import PhotoFactory
from DataStructures.Document import DocumentTable
from DataStructures.TableTypes import column_types_table
from DataOperations.MySQL import (
    create_specific_table,
    drop_table,
    insert_specific_dataframe
)


make_booktable_from_folder = False
add_id_to_booktable = False
write_booktable_to_csv = False
make_from_csv = True
create_table_mysql = False
insert_table_mysql = True

path_root = 'Z:/'
path_book = "Biographie/Stefan/197x-1988_Schulzeit/Grundschule Beckeradstraße/Klassenheft_Ausgedachtes/" #'Biographie/Stefan/Tables/'
csv_table = "klassenheft_ausgedachtes"  # "books.csv"
path_full = path_root + path_book
mysql_table = "book_klassenheft_ausgedachtes"  # "books"

if make_booktable_from_folder:
    booktable = PhotoFactory.table_from_folder(path_full)
    booktable = booktable.data
    cols = set(booktable.columns)
    dct = column_types_table("book")
    dct.pop("primary_key")
    cols_all = set([value["alias"] for (key,value) in dct.items()])
    booktable.drop(columns=list(cols - cols_all), inplace=True)
    for c in list(cols_all - cols):
        booktable[c] = None

if add_id_to_booktable:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    books = pd.read_sql('books', con=db_connection)
    booktable["BOOK_ID"] = books.loc[books["BookTable"] == mysql_table.replace("book_", ""), "BookID"].values[0]

if write_booktable_to_csv:
    DocumentTable(booktable).to_csv(path_full, csv_table)

if make_from_csv:
    table = pd.read_csv(
        path_full + csv_table + ".csv",
        encoding='ANSI',
        sep=';',
        parse_dates=[],   # "DATE_CREATED"
        dayfirst=True
    )
    table = table.where(pd.notnull(table), None)

if create_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    #drop_table(db_connection, mysql_table)
    create_specific_table(db_connection, mysql_table, "book")

if insert_table_mysql:
    db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
    db_connection = create_engine(db_connection_str)
    insert_specific_dataframe(db_connection, mysql_table, "book", table)