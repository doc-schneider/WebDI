import os
import pandas as pd
from sqlalchemy import create_engine

from DataOperations.Documents import DocumentFactory

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
sub_topic = "stefansfotoarchiv"

subtopic_table_name = person + "_" + topic + "_" + sub_topic
subtopic_table = pd.read_sql(
    subtopic_table_name,
    con=db_connection
)

# Loop over all low level tables
for i in range(subtopic_table.shape[0]):
    # Contains photos but no table written yet
    if (
            bool(subtopic_table.loc[i, "CONTAINS_PHOTOS"])
    ) & (
            subtopic_table.loc[i, "PHOTO_TABLE"] is None
    ):
        collection_name = subtopic_table.loc[i, "COLLECTION"]
        pth = subtopic_table.loc[i, "PATH"]

        # Check if pre-document list exists
        # TODO Move to Documents module
        if os.path.isfile(pth + "/" + "PreDokumentliste.csv"):
            pretable = pd.read_csv(
                pth + "/" + "PreDokumentliste.csv",
                encoding='ANSI',
                sep=';'
            )
        else:
            pretable = None

        # Read files info
        documenttable = DocumentFactory.table_from_folder(
            pth,
            "photo",
            pretable
        )

        # Output table
        documenttable.to_csv(
            pth + "/" + subtopic_table_name + "_" + collection_name + ".csv",
            sep=";",
            encoding='ANSI',
            index=False
        )

        table_name = subtopic_table_name + "_" + collection_name
        documenttable.to_sql(
            table_name,
            db_connection,
            if_exists="replace",
            index=False
        )

        # Update sub-topic table
        query = "UPDATE " + subtopic_table_name + \
                " SET PHOTO_TABLE = " + "\"" + table_name + "\"" + \
                " WHERE COLLECTION = " + "\"" + collection_name + "\"" + ";"
        db_connection.execute(query)

