import pandas as pd
from flask import Flask, render_template, request

import config
from DataOperations import Evernote, iPhone
from DataStructures import Data
from TimelineView import Timeline, Utilities, Single
import importlib
importlib.reload(Data)
importlib.reload(Evernote)
importlib.reload(iPhone)
importlib.reload(Timeline)
importlib.reload(Utilities)
importlib.reload(Single)

## Get documents and events

# Get document table
document_path = 'C:/Users/Stefan/Documents/DigitalImmortality/Document and Event Tables/'

# Photos:
#document_filename = 'Dokumentenliste_Weihnachten 2019.csv'
#documenttable = DataOperations.DataTableFactory().getFromCsv(document_path+document_filename)
# Evernote:
#document_filename = 'Dokumentliste_Mamas Sachen_Evernote.csv'
#documenttable = DataOperations.DataTableFactory().getFromCsv(document_path+document_filename)
# copy files to static, return new location
#documenttable = Evernote.EvernoteFactory.copy_html_to_static(documenttable,
#                                    Path('C:/Users/Stefan/PycharmProjects/WebDI/static/Evernote'))
# SMS iphone:
document_filename = 'Dokumentliste_Konstanze SMS_iphone.csv'
documenttable = Data.DataTableFactory().getFromCsv(document_path + document_filename)
# Remove entries without Event for the time being.
#documenttable.data['DESCRIPTION'].replace('', np.nan, inplace=True)
#documenttable.data.dropna(subset=['DESCRIPTION'], inplace=True)
#documenttable.data.reset_index(drop=True, inplace=True)
#documenttable.length = len(documenttable.data)
# Sort in TIME_FROM
documenttable.timesort()
# Add Durations
documenttable.add_timeinterval()

# Event table
event_path = 'C:/Users/Stefan/Documents/DigitalImmortality/Document and Event Tables/'
event_filename ="Eventliste.csv"
eventtable = Data.DataTableFactory().importFromCsv(event_path + event_filename, 'event')
# Close time interval with Now
eventtable.add_time_to()
# Add Event level
#eventtable.add_eventlevel()
# Drop some events for the time being
#eventtable.data['PARENT_EVENT'].replace('', np.nan, inplace=True)
#eventtable.data.dropna(subset=['PARENT_EVENT'], inplace=True)
#eventtable.data.reset_index(drop=True, inplace=True)
#eventtable.length = len(eventtable.data)

## Views definitions

# Define time axis (initial values)
t_start = pd.to_datetime('2019-12-01')
t_end = pd.to_datetime('2020-01-31')

## Make Views object

viewtype = 'jpeg_base64'   # 'html_path'
document_pathtype = 'PATH'     # 'STATIC_PATH'
timelineview = Timeline.TimelineAllViewer(documenttable, eventtable, t_start, t_end, viewtype, document_pathtype)
frameview = None

## Flask

app = Flask(__name__)

@app.route('/index', methods=["GET","POST"])
def show_index():
    global timelineview

    def render_index():
        return {'n_t': config.n_t, 'view_type': viewtype,'user_src': timelineview.data_for_view(),
                'user_text': timelineview.description_document.to_list(),
                'user_time': [timelineview.timegrid['TIME_FROM'].loc[i].strftime('%Y-%m-%d %H:%M')
                              for i in range(config.n_t)],
                'n_e': n_e, 'user_eventline': [[timelineview.eventlines['PIXEL_START'].loc[i],
                                                timelineview.eventlines['PIXEL_END'].loc[i]] for i in range(n_e)],
                'user_eventname': [timelineview.eventlines['EVENT_NAME'].loc[i] for i in range(n_e)],
                'n_a': n_a, 'user_atomarevents': [[timelineview.atomarevents['PIXEL_START'].loc[i],
                                                   timelineview.atomarevents['PIXEL_END'].loc[i]] for i in range(n_a)]
                   }

    if request.method == 'GET':
        n_e = timelineview.eventlines.shape[0]
        n_a = timelineview.atomarevents.shape[0]
        return render_template('index.html', **render_index())

    elif request.method == 'POST':
        for a in request.form:
            if a == 'zoom in':
                timelineview.zoom_in(documenttable,eventtable)
            elif a== 'zoom out':
                timelineview.zoom_out(documenttable, eventtable)
            elif a == 'earlier':
                timelineview.earlier(documenttable, eventtable)
            elif a == 'later':
                timelineview.later(documenttable, eventtable)
        n_e = timelineview.eventlines.shape[0]
        n_a = timelineview.atomarevents.shape[0]
        return render_template('index.html', **render_index())

@app.route('/view', methods=['GET', 'POST'])
def view():
    # - Need default if view page is viewed without clicking.
    # - Image be clickable and popping up in simple image view full size.
    global frameview                     # Stays unchanged for GET.

    def render_view():
        return {'n_t': config.n_t, 'view_type': viewtype,'user_src': frameview.data_for_view(),
                'description': frameview.description_document[0],
                'time': [frameview.timeinterval_document.left.strftime('%Y-%m-%d %H:%M'),
                         frameview.timeinterval_document.right.strftime('%Y-%m-%d %H:%M')],
                'user_time': [frameview.timegrid['TIME_FROM'].loc[i].strftime('%Y-%m-%d %H:%M')
                              for i in range(config.n_t)],
                'eventname': frameview.event_document,
                'parentevent': 'frameview.event_parent',
                'n_a':  n_a,
                'user_atomarevents': [[frameview.atomarevents['PIXEL_START'].loc[i],
                                       frameview.atomarevents['PIXEL_END'].loc[i]]
                                      for i in range(n_a)]
                }
    for a in request.form:               #  If user made a POST.
        if a == 'earlier':
            frameview.earlier(documenttable,eventtable)
        elif a == 'later':
            frameview.later(documenttable,eventtable)
        else:             #  User comes from "show_index" page, need to make new frameview.
            ix = int(list(request.form.keys())[0])  # button / time cell number as string
            t_1 = timelineview.timegrid['TIME_FROM'].iloc[ix]
            t_2 = timelineview.timegrid['TIME_TO'].iloc[ix]
            frameview = Single.FrameViewer(documenttable, eventtable, t_1, t_2, viewtype, document_pathtype,
                                           timelineview.index_documents[ix])
    n_a = frameview.atomarevents.shape[0]
    return render_template('view.html', **render_view())

app.run(host='0.0.0.0', port=82)

