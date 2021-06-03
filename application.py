from flask import Flask
import datetime as dtm

import config
from Agents.timeline_agent import timeline
from DataOperations.SQLite import SQLiteFactory
from DataOperations.Event import EventTable


print('Starting ..')

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(timeline, url_prefix='/timeline')


## Global parameters
config.environment = 'LOCAL'      # 'LOCAL'  #'AZURE'
config.document_pathtype = 'PATH'  #  'PATH'   #'AZURE'

##  Get Tablea and view parameters
path = '//192.168.0.117/' + 'Stefan/DigitalImmortality/Document and Event Tables/'
config.start_interval = (dtm.datetime.strptime('2020-01-01 12:31:15', '%Y-%m-%d %H:%M:%S'),
                         dtm.datetime.now())
config.documenttable = SQLiteFactory.read_sqlite_table(path + 'stefan.db', 'photo') # photo iphone
config.documenttable.timesort()
#config.documenttable.add_timeinterval()  # TODO Used for anything?
config.eventtable = EventTable(SQLiteFactory.read_sqlite_table(path + 'stefan.db', 'events').data)
config.eventtable.create_timeinterval_simple()
config.eventtable.replace_NaT()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82)