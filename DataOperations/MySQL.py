import pandas as pd
from sqlalchemy import ForeignKey, Table, Column, insert,  text
from sqlalchemy.types import Text, DateTime, Integer, Boolean


def create_table(db_engine, metadata, table_name, table_dct, foreign_table=None):
    table = Table(
        table_name,
        metadata,
        Column(
            table_dct["PrimaryKey"], Integer, primary_key=True
        ),
        *[
            Column(key, value["sqlalchemytype"]) for (key, value) in table_dct["Columns"].items()
        ]
    )
    if foreign_table:
        fk = table_dct["ForeignKey"]
        table.append_column(
            Column(fk, Integer, ForeignKey(f"{foreign_table}.{fk}"))
        )
    metadata.create_all(db_engine)
    # table.create(db_engine)

def create_table_mysql(conn, mycursor, table_name, table_dct, foreign_table_name=None, foreign_table_dct=None):
    query = f'CREATE TABLE {table_name} ('
    for k, v in table_dct["Columns"].items():
        query = query + " " + k + " " + v["mysqltype"] + ","
    query = query + " " + table_dct["PrimaryKey"] + " int AUTO_INCREMENT PRIMARY KEY"
    # TODO Foreign KEy addition not working?
    if foreign_table_name is not None:
        query = query + ", " + table_dct["ForeignKey"] + " int,"
        query = query + " FOREIGN KEY (" + table_dct["ForeignKey"] + ") REFERENCES " + foreign_table_name + "(" + foreign_table_dct["PrimaryKey"] + ")"
    query = query + ");"
    mycursor.execute(query)
    conn.commit()

def table_insert(metadata, db_conn, table_name, table):
    query = insert(metadata.tables[table_name])
    db_conn.execute(query, table.to_dict(orient='records'))
    db_conn.commit()

def table_insert_mysql(conn, mycursor, table_name, table):
    query = "INSERT INTO " + table_name + " ("
    for col in table.columns:
        query = query + " " + col + ","
    query = query[:-1] + ") VALUES ("  # Remove last comma
    for i in range(table.shape[1]):
        query = query + " %s,"
    query = query[:-1] + ");"
    data = [tuple(row) for row in table.values]
    mycursor.executemany(query, data)
    conn.commit()

def table_fetch(metadata, db_conn, table_name):
    table = metadata.tables[table_name]
    query = table.select()
    query_result = db_conn.execute(query)
    table_df = pd.DataFrame(query_result.fetchall())
    return table_df

# TODO Now metadata of sqlalchemy incorrect
# TODO Can add "DEFAULT NULL", "AFTER"
def add_columns(conn, mycursor, table_name, column_dct):
    for (column_name, column_type) in column_dct.items():
        query = f'ALTER TABLE {table_name} ADD  COLUMN {column_name} {column_type}'
        mycursor.execute(query)
    conn.commit()

def add_foreign_key():
    pass
    # - Create INT column NOT NULL
    # - ALTER TABLE CONSTRAINT name ADD FOREIGN KEY ({column_name_id}) REFERENCES ..
