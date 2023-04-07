import pandas as pd
from sqlalchemy import create_engine

from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
    read_specific_dataframe
)


db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "papa"
topics_filename = "Z:/Biographie/Papa/Tables/Data_Papa.xlsx"
read_topics_fromXLS = True
topics_tablename = person + "_" + "topics"
make_table_topics = True
make_tables_topic = True

# Read main topic page
if read_topics_fromXLS:
    table_topics = pd.read_excel(
        topics_filename,
        sheet_name="TOPICS",
        engine="openpyxl"
    )
if make_table_topics:
    table_topics.to_sql(
        topics_tablename.lower(),
        db_connection,
        if_exists="replace",
        index=False
    )

topics = list()
for t in table_topics["TOPIC"]:
    tp = pd.read_excel(
        topics_filename,
        sheet_name=t,
        engine="openpyxl"
    )
    topics.append(tp)
    if make_tables_topic:
        tp.to_sql(
            (person + "_topic_" + t).lower(),
            db_connection,
            if_exists="replace",
            index=False
        )


