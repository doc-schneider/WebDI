import pandas as pd
from sqlalchemy import create_engine

from DataOperations.Photos import PhotoFactory
from DataStructures.Document import DocumentTable
from DataStructures.TableTypes import column_types_table
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe
)


make_booktable_from_folder = True
add_id_to_booktable = False
write_booktable_to_csv = True
make_from_csv = False
create_table_mysql = False
insert_table_mysql = False

path_root = 'Z:/'
path_book = "Biographie/Stefan/Bücher&Magazine/Science Fiction/"
folder = "Star Wars - Das Erwachen der Macht/"  # 'Biographie/Stefan/Tables/'
csv_table = "star_wars_das_erwachen_der_macht"  # "books.csv"
path_full = path_root + path_book
mysql_table = "book_star_wars _das_erwachen_der_macht"  # "books"

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

if make_booktable_from_folder:
    booktable = PhotoFactory.table_from_folder(
        path_root + path_book,
        folder
    )
    booktable = booktable.data
    cols = set(booktable.columns)
    dct = column_types_table("book")
    dct.pop("primary_key")
    cols_all = set([value["alias"] for (key,value) in dct.items()])
    booktable.drop(columns=list(cols - cols_all), inplace=True)
    for c in list(cols_all - cols):
        booktable[c] = None

if add_id_to_booktable:
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
    #drop_table(db_connection, mysql_table)
    create_specific_table(db_connection, mysql_table, "book")

if insert_table_mysql:
    insert_specific_dataframe(db_connection, mysql_table, "book", table)