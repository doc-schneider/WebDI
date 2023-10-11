import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

from DataOperations.MySQL import (
    read_table,
    write_table
)

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "stefan"
topic = "event"   # "tag"
id = 0   # ID = index in topic table

topic_table = read_table(db_connection, person + "_topic_" + topic)
sub_topic = topic_table.loc[id, "SUB_TOPIC"]
pth = topic_table.loc[id, "PATH"]
document = topic_table.loc[id, "DOCUMENT_NAME"]

sub_topic_table = person + "_" + topic + "_" + sub_topic.replace(" ", "").lower()
# Leave out intermediate sub-topic (meta) table, because only a single Excel list document
output_table_name = sub_topic_table

table = pd.read_excel(
    pth + "/" + document,
    sheet_name=0,
    engine="openpyxl"
)

write_table(
    db_connection,
    output_table_name,
    table
)

table.to_csv(
    str(Path.joinpath(Path(pth), Path(Path(document).stem + ".csv")).as_posix()),
    sep=";",
    encoding='ANSI',
    index=False
)

