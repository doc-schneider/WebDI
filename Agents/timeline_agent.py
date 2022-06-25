import pandas as pd
from flask import render_template, request, Blueprint
from sqlalchemy import create_engine

import config
from Views.View import Viewer
from Views.Timeline import TimelineViewer
#from DataOperations.MySQL import (
#    read_photo_dataframe,
#)


## Blueprint
timeline = Blueprint('timeline', __name__)

@timeline.route('/timeline', methods=["GET","POST"])
def show_timeline():

    def render_timeline():
        return config.TimelineView.view()

    def init_TimelineView():
        # TODO Generalize View from photo
        View = Viewer(
            config.document_category,
            document_pathtype=config.document_pathtype,
            database_connection=config.db_connection,
            thumbnail=True
        )
        config.TimelineView = TimelineViewer(
            View,
            config.time_boxes,
            flag_single=False,
            tablecollection=config.tablecollection,
            eventtable=config.eventtable,
            markers=True,
        )

    if request.method == 'GET':

        # Initialize at first call
        if not hasattr(config, 'TimelineView'):
            init_TimelineView()

    elif request.method == 'POST':

        # Coming from portal?
        if "portal" in request.form:
            row = int(request.form["portal"])
            db = config.portaltable.loc[row, "DATABASE"]
            table = config.portaltable.loc[row, "TABLE"]
            # Open database / table
            config.db_connection.dispose()  # TODO Close old database. Seems to have no effect
            config.db_connection = create_engine(config.connection_str + db)
            config.documenttable = read_photo_dataframe(
                config.db_connection, table
            )
            # Set starting parameters
            config.document_pathtype = 'PATH'
            config.documenttable.timesort()
            config.eventtable = None
            config.time_boxes = (
                pd.Interval(
                    pd.Timestamp('2021-01-01 00:00:00'),
                    pd.Timestamp('2022-01-01 00:00:00'),
                    closed='left'
                ),
                "Y"
            )
            init_TimelineView()

        # Navigation in timeline
        elif "submit" in request.form:
            if request.form['submit'] == 'earlier':       # Navigate buttons
                config.TimelineView.earlier(config.tablecollection, config.eventtable)
            elif request.form['submit'] == 'later':
                config.TimelineView.later(config.tablecollection, config.eventtable)
            elif request.form['submit'] == 'zoom in':
                config.TimelineView.zoom_in(config.tablecollection, config.eventtable)
            elif request.form['submit'] == 'zoom out':
                config.TimelineView.zoom_out(config.tablecollection, config.eventtable)

    return render_template('/timeline/timeline.html', **render_timeline())

@timeline.route('/single', methods=["GET","POST"])
def show_single():

    def render_single():
        return config.SingleView.view()

    if request.method == 'POST':   # GET is only page refresh
        for key in request.form.keys():

            if key == 'submit':
                # Flip within box
                if request.form['submit'] == 'earlier':
                    config.SingleView.show_earlier()
                else:
                    config.SingleView.show_later()

            else:
                # First call of page.
                i = int(key)
                time_interval = config.TimelineView.BoxSeries[i].time_interval # Box clicked
                View = Viewer(
                    config.document_category,
                    document_pathtype=config.document_pathtype,
                    database_connection=config.db_connection
                )
                config.SingleView = TimelineViewer(
                    View,
                    time_interval,
                    flag_single=True,
                    tablecollection=config.tablecollection,
                    eventtable=config.eventtable,
                    markers=True,
                )

    return render_template('/timeline/single.html', **render_single())
