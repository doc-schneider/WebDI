import pandas as pd
from sqlalchemy import ForeignKey, Table, Column, insert,  text
from sqlalchemy.types import Text, DateTime, Integer, Boolean

from DataStructures.TableTypes import table_types


# TODO Table Type should not appear here. Go through TableFactory
def create_table(db_engine, metadata, table_name, table_type, parent_table=None):
    table = Table(
        table_name,
        metadata,
        Column(
            table_types[table_type.name]["PrimaryKey"], Integer, primary_key=True
        ),
        *[
            Column(key, value["sqlalchemytype"]) for (key, value) in table_types[table_type.name]["Columns"].items()
        ]
    )
    if "ForeignKey" in table_types[table_type.name].keys():
        fk = table_types[table_type.name]["ForeignKey"]
        table.append_column(
            Column(fk, Integer, ForeignKey(f"{parent_table}.{fk}"))
        )
    metadata.create_all(db_engine)
    # table.create(db_engine)

# Reflect Table from database
def init_table(db_engine, metadata, table_name):
    return Table(
        table_name,
        metadata,
        autoload_with=db_engine
    )

def table_insert(db_conn, table_mysql, table_df):
    query = insert(table_mysql)
    Result = db_conn.execute(query, table_df.to_dict(orient='records'))
    db_conn.commit()

def table_fetch(db_conn, table_mysql):
    # TODO Why do I need db_conn if table is already reflected?
    query = table_mysql.select()
    query_result = db_conn.execute(query)
    table_df = pd.DataFrame(query_result.fetchall())
    return table_df


def create_database(db_connection, db_name):
    query = 'CREATE DATABASE ' + db_name
    # TODO engine.connect() method
    con = db_connection.connect()
    con.execute(text(query))

def drop_table(db_connection, table_name):
    query = "DROP TABLE IF EXISTS {0}".format(table_name)
    db_connection.execute(text(query))

def write_table(db_connection, table_name, table, if_exists="replace"):
    table.to_sql(
        table_name,
        db_connection,
        if_exists=if_exists,
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
    #  Document Group etc
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
