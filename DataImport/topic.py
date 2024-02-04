import pandas as pd
from sqlalchemy import create_engine, MetaData

from DataStructures.Topic import TopicTable
from DataOperations import TableOperations
from DataStructures.TableTypes import TableType, table_types
from DataOperations.MySQL import create_table, init_table
import config


db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
db_engine = create_engine(db_connection_str)
db_conn = db_engine.connect()
metadata = MetaData()
metadata.reflect(bind=db_engine)
config.mysql = {
    "engine": db_engine,
    "conn": db_conn,
    "metadata": metadata
}

person = "stefan"

table_type = TableType["SUBTOPIC"]
table_name = person + "_" + table_type.name.lower()

table = TableOperations.create_table(table_type, person, 1)



topics_filename = "W:/Biographie/Stefan/Tables/Topics.xlsx"
# read_topics_fromXLS = True
# topics_tablename = person + "_" + "topics"
# make_table_topics = False
# make_tables_topic = ["tag"]  # "all"

# TODO Read from Database
def read_topics(topics_filename):
    return TopicTable(
        pd.read_excel(
            topics_filename,
            sheet_name="TOPICS",
            engine="openpyxl"
        )
    )

table_topics = read_topics(topics_filename)
table_topics.add_primary_key()

create_table(db_engine, metadata, "stefan_topics", TableType.TOPIC)



table_insert(db_conn, stefan_topics, table_topics.table)


# Read main topic page
# if read_topics_fromXLS:
#     table_topics = read_topics(topics_filename)
#
# table_topics["NAME_TABLE"] = person + "_" + "topic" + "_" + table_topics["TOPIC"]
#
# if make_table_topics:
#     write_table(
#         db_connection,
#         topics_tablename.lower(),
#         table_topics
#     )
# for t in table_topics["TOPIC"]:
#     tp = pd.read_excel(
#         topics_filename,
#         sheet_name=t,
#         engine="openpyxl"
#     )
#     if (all in make_tables_topic) | (t in make_tables_topic):
#         write_table(
#             db_connection,
#             (person + "_topic_" + t).lower(),
#             tp
#         )




