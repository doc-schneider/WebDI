'''
Top level / portal for entering into the system
'''

from flask import Flask
from sqlalchemy import create_engine

import config
from Agents.portal_agent import portal
from Agents.timeline_agent import timeline
from DataOperations.MySQL import (
    read_specific_dataframe,
)


## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(portal, url_prefix='/portal')
app.register_blueprint(timeline, url_prefix='/timeline')

#  Database for document table
#db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/portal'
config.connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/'
config.db_connection = create_engine(config.connection_str + "portal")
config.portaltable = read_specific_dataframe(config.db_connection, "portal", "portal")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82)