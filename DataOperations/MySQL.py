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

def table_insert(metadata, db_conn, table_name, table):
    query = insert(metadata.tables[table_name])
    Result = db_conn.execute(query, table.to_dict(orient='records'))
    db_conn.commit()

def table_fetch(metadata, db_conn, table_name):
    table = metadata.tables[table_name]
    query = table.select()
    query_result = db_conn.execute(query)
    table_df = pd.DataFrame(query_result.fetchall())
    return table_df
