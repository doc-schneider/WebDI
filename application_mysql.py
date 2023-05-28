from flask import Flask
from mysql.connector import connect
from sqlalchemy import create_engine

import config
from Agents.mysql_agent_topics import mysql_topics


#  Database
db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
config.db_connection = create_engine(db_connection_str)

config.person = "stefan"
config.table = config.person + "_topics"  # start table
config.table_type = "meta"
config.table_previous = config.table

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(mysql_topics, url_prefix='/mysql_topics')

if __name__ == "__main__":
    app.run(host='0.0.0.0')