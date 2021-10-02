import pandas as pd
import datetime as dtm
import sqlalchemy as db

from DataStructures.Document import DocumentTable


def create_database(cursor, db_name):
    query = "CREATE DATABASE " + db_name + ";"
    cursor.execute(query)


def create_table(db, cursor, table_name, columns, types, primary_key):
    query = "CREATE TABLE {0} (".format(table_name)
    for x in zip(columns, types):
        query += x[0] + " " + x[1] + ", "
    query += primary_key + " int PRIMARY KEY AUTO_INCREMENT );"
    cursor.execute(query)
    db.commit()

def create_generictable(db, cursor, table_name, columns):
    dct = columns_diarytable()
    primary_key = dct["primary_key"]
    dct.pop("primary_key")
    create_table(
        db,
        cursor,
        table_name,
        tuple(dct.keys()),
        tuple([value["mysqltype"] for (key, value) in dct.items()]),
        primary_key
    )

def columns_generictable():
    return {
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

def create_phototable(db, cursor, table_name):
    dct = columns_phototable()
    primary_key = dct["primary_key"]
    dct.pop("primary_key")
    create_table(
        db,
        cursor,
        table_name,
        tuple(dct.keys()),
        tuple([value["mysqltype"] for (key, value) in dct.items()]),
        primary_key
    )

def columns_phototable():
    return {
        "PhotoName": {
            "mysqltype": "varchar(255)",
            "alias": "DOCUMENT_NAME"
        },
        "PhotoType": {
            "mysqltype": "varchar(255)",
            "alias": "DOCUMENT_TYPE"
        },
        "DateTime": {
            "mysqltype": "datetime",
            "alias": "DATETIME"
        },
        "Path": {
            "mysqltype": "varchar(255)",
            "alias": "PATH"
        },
        "Description": {
            "mysqltype": "varchar(255)",
            "alias": "DESCRIPTION"
        },
        "EVENT": {
            "mysqltype": "varchar(255)",
            "alias": "EVENT"
        },
        "primary_key": "PhotoID"
    }

def create_diarytable(db, cursor, table_name):
    dct = columns_diarytable()
    primary_key = dct["primary_key"]
    dct.pop("primary_key")
    create_table(
        db,
        cursor,
        table_name,
        tuple(dct.keys()),
        tuple([value["mysqltype"] for (key, value) in dct.items()]),
        primary_key
    )

def columns_diarytable():
    return {
        "NoteName": {
            "mysqltype": "varchar(255)",
            "alias": "DOCUMENT_NAME"
        },
        "NoteType": {
            "mysqltype": "varchar(255)",
            "alias": "DOCUMENT_TYPE"
        },
        "NoteTitle": {
            "mysqltype": "varchar(255)",
            "alias": "TITLE"
        },
        "NoteCategory": {
            "mysqltype": "varchar(255)",
            "alias": "CATEGORY"
        },
        "DateTime": {
            "mysqltype": "datetime",
            "alias": "DATETIME"
        },
        "Path": {
            "mysqltype": "varchar(255)",
            "alias": "PATH"
        },
        "Description": {
            "mysqltype": "varchar(255)",
            "alias": "DESCRIPTION"
        },
        "Attachment": {
            "mysqltype": "varchar(255)",
            "alias": "ATTACHMENT"
        },
        "Event": {
            "mysqltype": "varchar(255)",
            "alias": "EVENT"
        },
        "primary_key": "NoteID"
    }


def add_column(db, cursor, table_name, column_name, column_type):
    query = "ALTER TABLE %s ADD %s %s;" % (table_name, column_name, column_type)
    cursor.execute(query)
    db.commit()


## TODO Many values
def update(db_connection, metadata, table_name, set_column, where_column, value):
    table = db.Table(table_name, metadata, autoload=True, autoload_with=db_connection)
    query = db.update(table).values({set_column: value[0]})
    col = db.sql.column(where_column)
    query = query.where(col == value[1])
    result = db_connection.execute(query)

## TODO Escaping value strings
#def update(db, cursor, table_name, set_column, where_column, value):
#    query = "UPDATE %s SET %s = %s WHERE %s = %s;" % (
#        table_name, set_column, value[0], where_column, value[1]
#    )
#    cursor.execute(query)
#    db.commit()


def insert_photo_dataframe(db_connection, table_name, df, if_exists="append"):
    dct = columns_phototable()
    dct.pop("primary_key")
    df.data.rename(
        columns={value["alias"]: key for (key, value) in dct.items()},
        inplace=True
    )
    df.data.to_sql(table_name, db_connection, if_exists=if_exists, index=False)

def insert_diary_dataframe(db_connection, table_name, df, if_exists="append"):
    dct = columns_diarytable()
    dct.pop("primary_key")
    df.data.rename(
        columns={value["alias"]: key for (key, value) in dct.items()},
        inplace=True
    )
    df.data.to_sql(table_name, db_connection, if_exists=if_exists, index=False)

def insert_record(db, cursor, table_name, columns: tuple, values: tuple):
    query = "INSERT INTO {0} (".format(table_name)
    for x in columns:
        query += x + ", "
    query = query[:-2]
    query += ") VALUES ("
    for i in range(len(values)):
        query += "%s, "
    query = query[:-2]
    query += ");"
    cursor.execute(query, values)
    db.commit()

def insert_array(db, cursor, table_name, columns: tuple, values):
    query = "INSERT INTO {0} (".format(table_name)
    for x in columns:
        query += x + ", "
    query = query[:-2]
    query += ") VALUES ("
    for i in range(values.shape[1]):
        query += "%s, "
    query = query[:-2]
    query += ");"
    cursor.executemany(query, tuple(map(tuple, values)))
    db.commit()

def insert_photo_array(db, cursor, table_name, values):
    dct = columns_phototable()
    dct.pop("primary_key")
    # Convert timestamp to datetime
    values[:, 2] = list(map(lambda x: x.to_pydatetime(), values[:, 2]))
    insert_array(db, cursor, table_name, tuple(dct.keys()), values)


def read_photo_dataframe(db_connection, table_name):
    df = pd.read_sql("SELECT * FROM {0};".format(table_name)
                     , con=db_connection
                     )
    dct = columns_phototable()
    dct.pop("primary_key")
    df.rename(
        columns={key: value["alias"] for (key, value) in dct.items()},
        inplace=True
    )
    # TODO Not here
    df["TIME_FROM"] = df["DATETIME"]
    df = DocumentTable(df)
    df.add_timedelta(dtm.timedelta(seconds=1))
    return df

def read_diary_dataframe(db_connection, table_name):
    df = pd.read_sql("SELECT * FROM {0};".format(table_name)
                     , con=db_connection
                     )
    dct = columns_diarytable()
    dct.pop("primary_key")
    df.rename(
        columns={key: value["alias"] for (key, value) in dct.items()},
        inplace=True
    )
    df = DocumentTable(df)
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