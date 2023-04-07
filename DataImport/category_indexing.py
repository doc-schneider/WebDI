import pandas as pd
from sqlalchemy import create_engine

from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
    read_specific_dataframe
)


datatable_filename = "Z:/Biographie/Stefan/Tables/Data_Stefan.xlsx"
read_categories_fromCSV = False
read_categories = True
create_categories = False
insert_categories = False

read_category_fromCSV = True

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)


if read_categories_fromCSV:
    categories = pd.read_excel(
        datatable_filename,
        sheet_name="CATEGORY",
        engine="openpyxl"
    )
if read_categories:
    categories = read_specific_dataframe(db_connection, "categories", "categories")

# Store in database
if create_categories:
    create_specific_table(
        db_connection,
        "categories",
        "categories"
    )
if insert_categories:
    insert_specific_dataframe(
        db_connection,
        "categories",
        "categories",
        categories
    )


if read_category_fromCSV:
    category = list()
    for cat in categories["CATEGORY"]:
        df = pd.read_excel(
            datatable_filename,
            sheet_name=cat,
            engine="openpyxl"
        )
