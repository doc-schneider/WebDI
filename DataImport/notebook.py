from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataOperations.Notebook import NotebookFactory
from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.MySQL import table_insert
from Initialize.Initialize import initialize_MySQL
import config


config.environment_storage = "LOCAL"
initialize_MySQL()

# Script new notebook + entry in collection
#
# Raw table
note_table = NotebookFactory().table_from_folder(
    Path("W:/Biographie/Stefan/Logs&Blogs/Evernote/Biography/Mama/Mama.enex")
)
#
# Extract notebook data from a new photo dataframe
notebook = note_table.table["NOTEBOOK"].unique()[0]
d_t = note_table.table["DATE_TIME"]
date_from = d_t.min()
date_to = d_t.max()
cols = list(table_definitions[TableType.NOTEBOOK]["Columns"].keys())
notebook_table = pd.DataFrame(
    index=[0],
    data={
        cols[0]: notebook,
        cols[1]: "Biography",
        cols[2]: "Evernote",
        cols[3]: date_from,
        cols[4]: date_to,
    }
)
#
# Insert new album
table_insert(config.mysql["metadata"], config.mysql["conn"], "notebooks", notebook_table)
#
# Get the foreign key for the notes table
note_table.add_foreignkey("NOTEBOOK", "notebooks")
#
# Insert the new notes
table_insert(config.mysql["metadata"], config.mysql["conn"], "notes", note_table.table)

