import pandas as pd
import datetime as dtm
from pathlib import Path
from sqlalchemy import create_engine

from DataOperations.Documents import DocumentFactory
from DataStructures.Data import DataTable
from DataOperations.MySQL import read_table, write_table


db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "stefan"
topic = "photo"
sub_topic = "mainphotoarchive"
subtopic_table_name = person + "_" + topic + "_" + sub_topic

single_table_list = [
    "2023_11_03_yabase_mehotels",
    "2023_11_01_radeln_areal_böhler",
    "2023_10_27_28_entrümpelung",
    "2023_07_19_2023_09_17"
]

# Concat tables
#
target_table = "2023_09_10_2023_11_03"
subtopic_table = read_table(db_connection, subtopic_table_name)
documenttable_all = pd.DataFrame()
for single_table_name in single_table_list:
    single_table_name_full = subtopic_table_name + "_" + single_table_name
    single_table = read_table(db_connection, single_table_name_full)
    documenttable_all = documenttable_all.append(single_table, ignore_index=True)
    query = "UPDATE " + subtopic_table_name + \
            " SET NAME_TABLE = " + "\"" + subtopic_table_name + "_" + target_table + "\"" + \
            " WHERE PATH = " + "\"" + single_table["PATH"].unique()[0][:-1] + "\"" + ";"
    db_connection.execute(query)
documenttable_all = documenttable_all.sort_values(by=['PATH'])
documenttable_all.reset_index(inplace=True, drop=True)
write_table(
    db_connection,
    subtopic_table_name + "_" +target_table,
    documenttable_all
)

# Add table name to meta table
#
subtopic_table = read_table(db_connection, subtopic_table_name)
for single_table_name in single_table_list:
    single_table_name_full = subtopic_table_name + "_" + single_table_name
    single_table = read_table(db_connection, single_table_name_full)
    # Match via path
    path_names = list(single_table["PATH"].unique())
    for p, t in zip(
            path_names,
            [single_table_name_full for i in range(len(path_names))]
    ):
        # TODO  Remove slash
        subtopic_table.loc[
            subtopic_table["PATH"] == p[:-1], "NAME_TABLE"
        ] = t
subtopic_table.to_csv(
    str(Path.joinpath(Path("Y:"), Path(subtopic_table_name + ".csv")).as_posix()),
    sep=";",
    encoding='ANSI',
    index=False
)
write_table(
    db_connection,
    subtopic_table_name,
    subtopic_table
)

# Add name column to table
#
for single_table_name in single_table_list:
    single_table_name_full = subtopic_table_name + "_" + single_table_name
    single_table = read_table(db_connection, single_table_name_full)
    single_table["NAME_TABLE"] = single_table_name_full
    write_table(db_connection, single_table_name_full, single_table)


