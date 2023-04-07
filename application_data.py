'''
Tool for data structure
'''

from flask import Flask
from sqlalchemy import create_engine

import config
from Agents.portal_agent import portal
from Agents.timeline_agent import timeline
from DataOperations.MySQL import (
    read_specific_dataframe,
)


#  Database
db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
config.db_connection = create_engine(db_connection_str)

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(portal, url_prefix='/xyz')

if __name__ == "__main__":
    app.run(host='0.0.0.0')