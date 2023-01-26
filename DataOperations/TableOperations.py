import pandas as pd

from DataStructures.TableTypes import column_types_table
from DataOperations.MySQL import (
    create_specific_table,
    read_specific_dataframe,
    insert_specific_dataframe,
    alter_record
)


# TODO Specifc to each catoegory module
def make_metatable(db_connection, meta_category):
    create_specific_table(db_connection, meta_category, meta_category)

def update_metatable(db_connection, meta_category, category):
    metatable = read_specific_dataframe(db_connection, meta_category, meta_category)
    tables_existing = set(metatable[category.upper() + "_TABLE"])
    columns = column_types_table(
        meta_category,
        optional_columns=[],
        remove_primarykey=True,
        return_aliasnames=True
    )
    # Find tables of category
    table_names = db_connection.table_names()
    table_names = [tn for tn in table_names if category + "_" in tn]

    # Make new table
    metatable_new = {value: [] for value in columns}

    for tn in table_names:
        table = read_specific_dataframe(db_connection, tn, category)
        t_min = table["DATETIME"].min()
        t_max = table["DATETIME"].max()
        if tn in list(set(table_names) - tables_existing):  # New entry?
            # Assume first column is table name
            metatable_new[columns[0]].append(tn)  # TODO bad style
            # Update times to latest entries
            # if "TIME_FROM" in columns:
            metatable_new["TIME_FROM"].append(t_min)
            metatable_new["TIME_TO"].append(t_max)
            for item in set(columns[1:]) - set(["TIME_FROM", "TIME_TO", columns[0]]):
                metatable_new[item].append(None)
        else:
            alter_record(
                db_connection,
                meta_category,
                meta_category,
                ("TIME_FROM", t_min),
                (columns[0], tn)
            )
            alter_record(
                db_connection,
                meta_category,
                meta_category,
                ("TIME_TO", t_max),
                (columns[0], tn)
            )

    if metatable_new[columns[0]]:  # Empty?
        insert_specific_dataframe(
            db_connection,
            meta_category,
            meta_category,
            pd.DataFrame(metatable_new)
        )




