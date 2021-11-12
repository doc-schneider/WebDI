from flask import Flask
import datetime as dtm
from mysql.connector import connect, Error
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
connection = connect(
    host="localhost",
    user="Stefan",
    passwd="Moppel3",
)
mycursor = connection.cursor()
config.connection = connection
config.cursor = mycursor

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82, debug=True)