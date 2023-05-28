import pandas as pd
from sqlalchemy import create_engine

"""
Reads the root Topic file.
- Root topics 
- Sub-topics, indicating the next level tables

Creates: 
- Dataframes 
"""

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "stefan"
topics_filename = "Z:/Biographie/Stefan/Tables/Data_Stefan.xlsx"
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
table_topics["TABLE"] = person + "_" + "topic" + "_" + table_topics["TOPIC"]
if make_table_topics:
    table_topics.to_sql(
        topics_tablename.lower(),
        db_connection,
        if_exists="replace",
        index=False
    )

for t in table_topics["TOPIC"]:
    tp = pd.read_excel(
        topics_filename,
        sheet_name=t,
        engine="openpyxl"
    )
    tp["TABLE"] = person + "_" + "topic" + "_" + table_topics["TOPIC"]
    if make_tables_topic:
        tp.to_sql(
            (person + "_topic_" + t).lower(),
            db_connection,
            if_exists="replace",
            index=False
        )


