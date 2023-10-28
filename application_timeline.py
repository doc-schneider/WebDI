from flask import Flask
import pandas as pd
from sqlalchemy import create_engine

import config
from Agents.timeline import timeline
from DataStructures.Data import DataTable
from DataStructures.Collection import TableCollectionFactory
from DataOperations.MySQL import read_table


#  Database
db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
config.db_connection = create_engine(db_connection_str)

config.document_pathtype = 'PATH'

person = "stefan"
# Which document categories
config.document_category = [
    "photo"
]  #   TODO document_type seems better

config.tablecollection = list()
config.tablecollection.append(
    TableCollectionFactory.create_compoundtable(
        config.db_connection,
        person,
        "photo",
        "main photo archive",
        "photo"
    )
)

# Starting time interval
config.time_boxes = (
    pd.Interval(
        pd.Timestamp('2023-01-01 00:00:00'),
        pd.Timestamp('2023-12-31 00:00:00'),
        closed='left'
    ),
    "Y"
)

config.eventtable = TableCollectionFactory.create_compoundtable(
    config.db_connection,
    person,
    "event",
    "Stefans Eventliste",
    "event"
)

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(timeline, url_prefix='/timeline')

if __name__ == "__main__":
    app.run(host='0.0.0.0')