import pandas as pd
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.types import Text, DateTime, Integer, Boolean

from DataStructures.TableTypes import column_types_table, find_optional_columns, columns_names_types

# TODO Move column definitions to DataStructures
#  Add / remove columns

def create_database(db_connection, db_name):
    query = "CREATE DATABASE " + db_name
    # TODO engine.connect() method
    db_connection.execute(query)


def drop_table(db_connection, table_name):
    query = "DROP TABLE IF EXISTS {0}".format(table_name)
    db_connection.execute(query)

def create_specific_table(db_connection, table_name, table_type, optional_columns=[], if_exist="drop"):
    # TODO Need query for existance of table
    if if_exist == "drop":
        drop_table(db_connection, table_name)
    dct = column_types_table(table_type, optional_columns=optional_columns)
    primary_key = dct["primary_key"]
    dct.pop("primary_key")
    metadata = MetaData()
    table_sql = Table(
        table_name,
        metadata,
        Column(primary_key, Integer, primary_key=True),
        *[Column(key, value["sqlalchemytype"]) for (key, value) in dct.items()]
    )
    metadata.create_all(db_connection)

def write_table(db_connection, table_name, table):
    table.to_sql(
        table_name,
        db_connection,
        if_exists="replace",
        index=True,
        index_label="ID",
        dtype={c: columns_names_types[c] for c in table.columns}
    )
    db_connection.execute(
        'ALTER TABLE ' + table_name + ' ADD PRIMARY KEY (ID);'
    )


# TODO Simplfy code with table type functions
def alter_record(db_connection, table_name, document_category, set_tuple, where_tuple):
    dct = column_types_table(document_category, optional_columns=[], remove_primarykey=True)
    where_clause = ""  #  Update all rows
    if where_tuple is not None:
        where_clause = " WHERE " + \
                       [key for (key, value) in dct.items() if value["alias"] == where_tuple[0]][0] + \
                       " = '" + where_tuple[1] + "' "
    if isinstance(set_tuple[1], pd.Timestamp):
        set_value = set_tuple[1].strftime('%Y-%m-%d %H:%M:%S')
    else:
        set_value = set_tuple[1]
    query = "UPDATE " + table_name + " SET " + \
            [key for (key, value) in dct.items() if value["alias"] == set_tuple[0]][0] + \
            " = '" + set_value + "' " + where_clause
    db_connection.execute(query)

def drop_column(db_connection, table_name, document_category, column_name):
    # TODO document_category
    query = "ALTER TABLE %s DROP COLUMN %s;" % (table_name, column_name)
    db_connection.execute(query)

def drop_row(db_connection, table_name, which="all"):
    # TODO document_category
    query = "DELETE FROM %s;" % (table_name,)
    db_connection.execute(query)


def insert_specific_dataframe(db_connection,
                              table_name,
                              table_type,
                              df,
                              optional_columns=[],
                              if_exists="append"
                              ):
    dct = column_types_table(
        table_type,
        optional_columns=optional_columns,
        remove_primarykey=True
    )
    df.rename(
        columns={value["alias"]: key for (key, value) in dct.items()},
        inplace=True
    )
    df.to_sql(table_name.lower(), db_connection, if_exists=if_exists, index=False)


def read_dataframe(db_connection, table_name):
    df = pd.read_sql(table_name, con=db_connection)
    return df

def read_specific_dataframe(db_connection, table_name, table_type):
    df = pd.read_sql(table_name, con=db_connection)
    primary_key = column_types_table(table_type)["primary_key"]
    df.drop(columns=[primary_key], inplace=True)
    optional_columns = find_optional_columns(df, table_type, aliasnames=False)
    dct = column_types_table(
        table_type,
        optional_columns=optional_columns,
        remove_primarykey=True
    )
    df.rename(
        columns={key: value["alias"] for (key, value) in dct.items()},
        inplace=True
    )
    return df

def read_table(db_connection, table_name):
    # TODO New Python version : dtype={"CONTAINS_FILES": bool}
    table = pd.read_sql(
        table_name,
        con=db_connection,
        index_col="ID"
    )
    # TODO Smart class check
    if "CONTAINS_FILES" in table.columns:
        table["CONTAINS_FILES"] = table["CONTAINS_FILES"].astype(bool)
    return table


def export_table(db_connection, table_name, pathname):
    df = pd.read_sql(
        "SELECT * FROM {0};".format(table_name)
        , con=db_connection
    )
    df.to_csv(
        pathname + table_name + '.csv',
        index=False,
        sep=';',
        date_format='%d.%m.%Y %H:%M:%S',
        encoding='ANSI'
    )


def get_columns(cursor, table_name, columns: tuple):
    query = "SELECT "
    for x in columns:
        query += x + ", "
    query = query[:-2]
    query += " FROM {0}".format(table_name)
    query += ";"
    cursor.execute(query)
    return cursor