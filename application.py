from flask import Flask
import datetime as dtm
import mysql.connector
from sqlalchemy import create_engine

import config
from Agents.timeline_agent import timeline
from DataOperations.SQLite import SQLiteFactory
from DataOperations.MySQL import read_photo_dataframe
from DataStructures.Event import EventTable


print('Starting ..')

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(timeline, url_prefix='/timeline')


## Global parameters
config.environment = 'LOCAL'      # 'LOCAL'  #'AZURE'
config.document_pathtype = 'PATH'  #  'PATH'   #'AZURE'

##  Get Table and view parameters
#path = '//192.168.0.117/' + 'Stefan/DigitalImmortality/Document and Event Tables/'
config.start_interval = (dtm.datetime.strptime('2021-07-01 12:31:15', '%Y-%m-%d %H:%M:%S'),
                         dtm.datetime.strptime('2021-09-01 12:31:15', '%Y-%m-%d %H:%M:%S'))

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/photos'
db_connection = create_engine(db_connection_str)
config.documenttable = read_photo_dataframe(db_connection, "2021_0708_Schwarzwald")
#config.documenttable = SQLiteFactory.read_sqlite_table(path + 'stefan.db', 'photo') # photo iphone
config.documenttable.timesort()

config.eventtable = None
#config.eventtable = EventTable(SQLiteFactory.read_sqlite_table(path + 'stefan.db', 'events').data)
#config.eventtable.create_timeinterval_simple()
#config.eventtable.replace_NaT()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82)