import os
import pandas as pd
from sqlalchemy import create_engine

from DataOperations.Documents import DocumentFactory

"""
Walks through all folders indicated in a meta table
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
topic = "music"
sub_topic = "meinecds"

subtopic_table_name = person + "_" + topic + "_" + sub_topic
subtopic_table = pd.read_sql(
    subtopic_table_name,
    con=db_connection
)

# Loop over all low level tables
collections = []
documenttable = pd.DataFrame()
for i in range(subtopic_table.shape[0]):
    # Contains files but no table written yet
    if (
            subtopic_table.loc[i, "ALBUM"] is not None
    ) & (
            subtopic_table.loc[i, "TABLE"] is None
    ):
        collection_name = subtopic_table.loc[i, "COLLECTION"]
        pth = subtopic_table.loc[i, "PATH"]
        # Is it a multi album?
        flag_multi = subtopic_table.loc[i, "ALBUM"] == "MULTI"
        # Check if pre-document list exists
        pretable = DocumentFactory.read_pretable(pth)
        # List  belonging to multialbum
        if flag_multi:
            collections = list(
                subtopic_table.loc[
                    subtopic_table["PARENT_COLLECTION"] == collection_name,
                    "COLLECTION"
                ]
            ) + [collection_name]
            super_name = collection_name
            super_pth = pth
        elif not collections:
            # Start single CD
            collections = [collection_name]
            super_name = collection_name
            super_pth = pth
        else:
            pass
        # Read files info
        table = DocumentFactory.table_from_folder(
            pth,
            "music",
            pretable,
            ["DOCUMENT_TYPE"]
        )
        # Sub-collections
        if flag_multi:
            table["SUB_COLLECTION"] = None
        elif "SUB_COLLECTION" in documenttable.columns:
            table["SUB_COLLECTION"] = collection_name
        # Append
        documenttable = pd.concat(
            [documenttable, table]
        )
        # Job to be continued if multi
        collections.remove(collection_name)
        if not collections:
            # Output table
            documenttable.to_csv(
                super_pth + "/" + subtopic_table_name + "_" + super_name + ".csv",
                sep=";",
                encoding='ANSI',
                index=False
            )
            table_name = (subtopic_table_name + "_" + super_name).lower()
            documenttable.to_sql(
                table_name,
                db_connection,
                if_exists="replace",
                index=False
            )
            # Update sub-topic table
            query = "UPDATE " + subtopic_table_name + \
                    " SET `TABLE` = " + "\"" + table_name + "\"" + \
                    " WHERE COLLECTION = " + "\"" + super_name + "\"" + \
                    " OR PARENT_COLLECTION = " + "\"" + super_name + "\"" + ";"
            db_connection.execute(query)
            # Clear state
            documenttable = pd.DataFrame()
            collections = []
