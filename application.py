from flask import Flask, Blueprint
import datetime as dtm

import config
from Agents.start_agent import start
from Agents.list_agent import listen
from Agents.timeline_agent import timeline
from Agents.play_agent import play


## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

app.register_blueprint(start, url_prefix='/start')
app.register_blueprint(timeline, url_prefix='/timeline')
app.register_blueprint(listen, url_prefix='/listen')
app.register_blueprint(play, url_prefix='/play')

## Global parameters
# path: root path
#config.document_pathtype = 'PATH'
#config.path = '//192.168.178.53/Stefan/DigitalImmortality/Document and Event Tables/'
#config.starttable_name = 'Startliste_Papa_utf8.csv'
config.environment = 'AZURE'      # 'LOCAL'  #'AZURE'
config.document_pathtype = 'AZURE'  #
config.path = 'modest-di'   # container
config.starttable_name = 'tables/' + 'Startliste_Papa_utf8.csv'
config.use_thumbnail = True
config.start_interval = (dtm.datetime.strptime('2020-06-11 10:44:00', '%Y-%m-%d %H:%M:%S'),
                         dtm.datetime.strptime('2020-06-11 22:44:00', '%Y-%m-%d %H:%M:%S'))
    #(dtm.datetime.strptime('1969-03-18 00:44:00', '%Y-%m-%d %H:%M:%S'),
    #                     dtm.datetime.now())

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=82)