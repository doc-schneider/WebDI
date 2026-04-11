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
path_notebook = Path("W:/Biographie/Stefan/Logs&Blogs/Evernote/Biography/Mama/Mama.enex")
#
# Raw table
note_table = NotebookFactory().table_from_folder(path_notebook)
#
# Extract notebook data from a new photo dataframe
notebook = note_table.table["NOTEBOOK"].unique()[0]
d_t = note_table.table["DATE_TIME"]
date_from = d_t.min()
date_to = d_t.max()
notebook_table = pd.DataFrame(
    index=[0],
    data={
        "NOTEBOOK": notebook,
        "NOTEBOOK_COLLECTION": "Biography",
        "NOTEBOOK_TYPE": "Evernote",
        "DATE_FROM": date_from,
        "DATE_TO": date_to,
        "FILE_NAME": path_notebook.name,
        "FILE_FORMAT": path_notebook.suffix[1:],
        "PATH": str(path_notebook.parent),
    }
)
#
# Insert new album
table_insert(config.mysql["metadata"], config.mysql["conn"], "notebooks", notebook_table)
#
# Get the foreign key for the notes table
note_table.add_foreignkey("NOTEBOOK", "notebooks", TableType.NOTEBOOK)
#
# Insert the new notes
table_insert(config.mysql["metadata"], config.mysql["conn"], "notes", note_table.table)

