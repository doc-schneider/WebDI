from flask import Flask
import pandas as pd
from sqlalchemy import create_engine

import config
from Agents.timeline_agent import timeline
from Agents.edit_agent import edit
from DataStructures.Data import DataTable
from DataStructures.Event import EventTable
from DataStructures.Collection import TableCollection
from DataOperations.MySQL import (
    read_specific_dataframe,
)


#  Database
db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
config.db_connection = create_engine(db_connection_str)

# TODO Functional?
# Files environment
config.environment = 'LOCAL'      # 'LOCAL'  #'AZURE'
config.document_pathtype = 'PATH'  #  'PATH'   #'AZURE'
config.table_source = 'MYSQL'

# Starting time interval
config.time_boxes = (
    pd.Interval(
        pd.Timestamp('2022-01-01 00:00:00'),
        pd.Timestamp('2022-12-31 00:00:00'),
        closed='left'
    ),
    "Y"
)

# Which document categories
config.document_category = [
    "photo",
    "note"
]

# Read meta-table and init TableCollection
metatable = list()
metatable.append(
    DataTable(
        read_specific_dataframe(config.db_connection, "notes", "notes"),
        "notes"
    )
)
metatable.append(
    DataTable(
        read_specific_dataframe(config.db_connection, "photos", "photos"),
        "photos"
    )
)
category = [
    "personal diary",
    None
]
# tags=["Energy Modelling"]
config.tablecollection = list()
for i in range(len(metatable)):
    config.tablecollection.append(
        TableCollection(
            config.document_category[i],
            config.table_source,
            metatable[i],
            category[i]
        )
    )

events_table = read_specific_dataframe(config.db_connection, "events", "events")
events_table = EventTable(events_table)
events_table.add_eventlevel()
# TODO Only level 0 for the time being
events_table.data = events_table.data[events_table.data["EVENT_LEVEL"] == 0]
config.eventtable = events_table

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(timeline, url_prefix='/timeline')
app.register_blueprint(edit, url_prefix='/edit')

if __name__ == "__main__":
    app.run(host='0.0.0.0')  # app.run(host='0.0.0.0', port=82)