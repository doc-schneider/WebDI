import pandas as pd
from sqlalchemy import create_engine

from DataOperations.MySQL import write_table

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
make_table_topics = False
make_tables_topic = ["tag"]  # "all"

# Read main topic page
if read_topics_fromXLS:
    table_topics = pd.read_excel(
        topics_filename,
        sheet_name="TOPICS",
        engine="openpyxl"
    )
table_topics["NAME_TABLE"] = person + "_" + "topic" + "_" + table_topics["TOPIC"]
if make_table_topics:
    write_table(
        db_connection,
        topics_tablename.lower(),
        table_topics
    )
for t in table_topics["TOPIC"]:
    tp = pd.read_excel(
        topics_filename,
        sheet_name=t,
        engine="openpyxl"
    )
    if (all in make_tables_topic) | (t in make_tables_topic):
        write_table(
            db_connection,
            (person + "_topic_" + t).lower(),
            tp
        )



