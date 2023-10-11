from flask import Flask
import pandas as pd
from sqlalchemy import create_engine

import config
from Agents.timeline_agent import timeline
from DataStructures.Data import DataTable
from DataOperations.MySQL import read_table


#  Database
db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
config.db_connection = create_engine(db_connection_str)

config.document_pathtype = 'PATH'

config.person = "stefan"

# Which document categories
config.document_category = [
    "photo"
]  #   TODO document_type seems better

# Starting time interval
config.time_boxes = (
    pd.Interval(
        pd.Timestamp('2022-01-01 00:00:00'),
        pd.Timestamp('2022-12-31 00:00:00'),
        closed='left'
    ),
    "Y"
)

config.tablecollection = list()
table = read_table(
    config.db_connection,
    config.person + "_photo_stefansfotoarchiv_all"
)
table["DATETIME"] = table["TIME_CREATED"]  # TODO For the tim ebing
config.tablecollection.append(
    DataTable(
        table
    )
)

config.eventtable = None

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(timeline, url_prefix='/timeline')

if __name__ == "__main__":
    app.run(host='0.0.0.0')