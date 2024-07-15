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
    # if "ForeignKey" in table_types[table_type.name].keys():
    #     fk = table_types[table_type.name]["ForeignKey"]
    #     table.append_column(
    #         Column(fk, Integer, ForeignKey(f"{foreign_table}.{fk}"))
    #     )
    metadata.create_all(db_engine)
    # table.create(db_engine)
#
#    create_table_query = '''
#    CREATE TABLE employees (
#        id INT AUTO_INCREMENT PRIMARY KEY,
#        first_name VARCHAR(50),
#        last_name VARCHAR(50),
#        hire_date DATE,
#        salary DECIMAL(10, 2)
#    )
#    '''
    # Execute the table creation query
#    cursor.execute(create_table_query)
# Closing the cursor and connection
#    cursor.close()
#    cnx.close()

def table_insert(metadata, db_conn, table_name, table):
    query = insert(metadata.tables[table_name])
    db_conn.execute(query, table.to_dict(orient='records'))
    db_conn.commit()
#
# See table.py

def table_fetch(metadata, db_conn, table_name):
    table = metadata.tables[table_name]
    query = table.select()
    query_result = db_conn.execute(query)
    table_df = pd.DataFrame(query_result.fetchall())
    return table_df

def add_columns(conn, mycursor, table_name, column_dct):
    for (column_name, column_type) in column_dct.items():
        query = f'ALTER TABLE {table_name} ADD  COLUMN {column_name} {column_type}'
        mycursor.execute(query)
    conn.commit()
    # TODO Now metadata of sqlalchemy incorrect

def add_foreign_key():
    pass
    # - Create INT column NOT NULL
    # - ALTER TABLE CONSTRAINT name ADD FOREIGN KEY ({column_name_id}) REFERENCES ..
