import pandas as pd
from sqlalchemy import MetaData, Table, Column, Text, DateTime, Integer

from DataStructures.TableTypes import column_types_table, find_optional_columns


# TODO Move column definitions to DataStructures
#  Add / remove columns

def create_database(db_connection, db_name):
    query = "CREATE DATABASE " + db_name
    # TODO engine.connect() method
    db_connection.execute(query)


def drop_table(db_connection, table_name):
    query = "DROP TABLE " + table_name
    #query = "DROP TABLE IF EXISTS {0}".format(table_name)
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

# Various DataFrame column names and their MySQL correspondence
def columns_generictable():
    return {
        "NAME": {
            "mysqltype": "text",
            "alias": "NAME"
        },
        "DOCUMENT_NAME": {
            "mysqltype": "varchar(255)",
            "alias": "DOCUMENT_NAME"
        },
        "DOCUMENT_TYPE": {
            "mysqltype": "varchar(255)",
            "alias": "DOCUMENT_TYPE"
        },
        "DATETIME": {
            "mysqltype": "datetime",
            "alias": "DATETIME"
        },
        "PATH": {
            "mysqltype": "varchar(255)",
            "alias": "PATH"
        },
        "DESCRIPTION": {
            "mysqltype": "varchar(255)",
            "alias": "DESCRIPTION"
        },
        "EVENT": {
            "mysqltype": "varchar(255)",
            "alias": "EVENT"
        },
        "primary_key": "ID"
    }

def columns_portaltable():
    return {
        "NAME": {
            "mysqltype": "text",
            "alias": "NAME"
        },
        "SUB_PORTAL": {
            "mysqltype": "text",
            "alias": "SUB_PORTAL"
        },
        "DATABASE_NAME": {
            "mysqltype": "text",
            "alias": "DATABASE"
        },
        "TABLE_NAME": {
            "mysqltype": "text",
            "alias": "TABLE"
        },
        "DOCUMENT_CATEGORY": {
            "mysqltype": "text",
            "alias": "DOCUMENT_CATEGORY"
        },
        "VIEW_TYPE": {
            "mysqltype": "text",
            "alias": "VIEW_TYPE"
        },
        "primary_key": "PortalID"
    }

def alter_record(db_connection, table_name, document_category, set_tuple, where_tuple):
    dct = column_types_table(document_category, optional_columns=[], remove_primarykey=True)
    query = "UPDATE " + table_name + " SET " + \
            [key for (key, value) in dct.items() if value["alias"] == set_tuple[0]][0] + \
            " = '" + set_tuple[1] + "' " + " WHERE " + \
            [key for (key, value) in dct.items() if value["alias"] == where_tuple[0]][0] + \
            " = '" + where_tuple[1] + "' "
    db_connection.execute(query)

#def add_column(db, cursor, table_name, column_name, column_type):
#    query = "ALTER TABLE %s ADD %s %s;" % (table_name, column_name, column_type)
#    cursor.execute(query)
#    db.commit()

#def update_column(db, mycursor, table_name, column_name, new_column, primary_key):
#    mycursor.execute("SELECT %s FROM " % (primary_key) + table_name)
#    id_column = mycursor.fetchall()
#    # TODO
#    #  Execute many
#    #  Other than str
#    for id in id_column:
#        query = "UPDATE %s SET %s = \" %s \" WHERE %s = %s;" % (
#            table_name, column_name, new_column[0], primary_key, id[0]
#        )
#        mycursor.execute(query)
#    db.commit()


def insert_specific_dataframe(db_connection,
                              table_name,
                              table_type,
                              df,
                              optional_columns=[],
                              if_exists="append"
                              ):
    dct = column_types_table(table_type, optional_columns=optional_columns)
    dct.pop("primary_key")
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
    # Any optional columns?
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