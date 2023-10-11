import os
import pandas as pd
import datetime as dtm
from sqlalchemy import create_engine

from DataOperations.Documents import DocumentFactory
from DataStructures.Data import DataTable
from DataOperations.MySQL import read_table, write_table

"""
Walks through all folders indicated in a topic table
- Records files in folder
- Reads accompanying csv with descriptions
- Outputs to csv and mysql

Creates: 
- Dataframes, csv, mysql
"""

# TODO Pretable with information about non-photo files

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "stefan"
topic = "photo"
sub_topic = "mainphotoarchive"
subtopic_table_name = person + "_" + topic + "_" + sub_topic

# Read only part of the whole, or all?
flag_all = "dateinterval"   # single, all, part
if flag_all == "all":
    multi_table_name = subtopic_table_name + "_all"
elif flag_all == "dateinterval":
    date_from = dtm.date(2023, 7, 19)
    date_to = dtm.date(2023, 9, 17)
    multi_table_name = subtopic_table_name + "_" + date_from.strftime("%Y_%m_%d") + "_" + date_to.strftime("%Y_%m_%d")

if (flag_all == "all") | (flag_all == "dateinterval"):
    documenttable_all = pd.DataFrame()

subtopic_table = read_table(db_connection, subtopic_table_name)

# Combine with events and tags
event_table = read_table(db_connection, person + "_event_" + "stefanseventliste")
# TODO Tags

# Filter parts
if flag_all == "dateinterval":
    subtopic_table = subtopic_table[
        pd.IntervalIndex.from_arrays(
            subtopic_table['TIME_FROM'],
            subtopic_table['TIME_TO'], closed='both'
        ).overlaps(
            pd.Interval(pd.Timestamp(date_from), pd.Timestamp(date_to), closed="both")
        )
    ]
# TODO Contains Files / Name Table etc

# Loop over all low level tables
for _, row in subtopic_table.iterrows():
    row = subtopic_table.loc[1672, :]
    if row["CONTAINS_FILES"]:
        collection_name = row["COLLECTION"]
        pth = row["PATH"]

        # Check if pre-document list exists
        pretable = DocumentFactory.read_pretable(pth)

        # Read files info
        documenttable = DocumentFactory.table_from_folder(
            pth,
            pretable_matching={
                "pretable": pretable,
                "match_columns": ["DESCRIPTION"]
            },
            eventtable_matching={
                "matching": "name",
                "eventtable": event_table,
                "eventname": "Tag des Offenen Denkmals 2023"
            }
        )

        # Output table
        single_table_name = subtopic_table_name + "_" + collection_name
        documenttable.to_csv(
            pth + "/" + single_table_name + ".csv",
            sep=";",
            encoding='ANSI',
            index=False
        )

        if (flag_all == "all") | (flag_all == "dateinterval"):
            documenttable["NAME_TABLE"] = single_table_name
            documenttable_all = documenttable_all.append(documenttable, ignore_index=True)
        else:
            write_table(
                db_connection,
                single_table_name .lower(),
                documenttable
            )

        # Update higher-level table
        if (flag_all == "all") | (flag_all == "dateinterval"):
            query = "UPDATE " + subtopic_table_name + \
                    " SET NAME_TABLE = " + "\"" + multi_table_name + "\"" + \
                    " WHERE COLLECTION = " + "\"" + collection_name + "\"" + ";"
        else:
            query = "UPDATE " + subtopic_table_name + \
                    " SET NAME_TABLE = " + "\"" + single_table_name + "\"" + \
                    " WHERE COLLECTION = " + "\"" + collection_name + "\"" + ";"
        db_connection.execute(query)

if (flag_all == "all") | (flag_all == "dateinterval"):
    write_table(
        db_connection,
        multi_table_name,
        documenttable_all
    )
