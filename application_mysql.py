from flask import Flask
import datetime as dtm
from sqlalchemy import create_engine
import sqlalchemy as db

import config
from Agents.mysql_agent import mysql


print('Starting ..')

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(mysql, url_prefix='/mysql')

## Global parameters
conn = mysql.connector.connect(
    host="localhost",
    user="Stefan",
    passwd="Moppel3",
)
mycursor = conn.cursor()
config.connection = conn
config.cursor = mycursor
#config.environment = 'LOCAL'
#config.document_pathtype = 'PATH'

##  Start parameters
config.database = "photos"
config.table = "2021_0708_schwarzwald"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82)