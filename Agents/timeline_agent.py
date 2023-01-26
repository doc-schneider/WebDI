from flask import render_template, request, Blueprint

import config
from Views.View import MetaViewer
from Views.Timeline import TimelineViewer


## Blueprint
timeline = Blueprint('timeline', __name__)

@timeline.route('/timeline', methods=["GET","POST"])
def show_timeline():

    def render_timeline():
        return config.TimelineView.view()

    def init_TimelineView():
        # TODO Generalize View from photo
        MetaView = MetaViewer(
            config.document_category,
            document_pathtype=config.document_pathtype,
            database_connection=config.db_connection,
            thumbnail=True
        )
        config.TimelineView = TimelineViewer(
            MetaView,
            config.time_boxes,
            flag_single=False,
            tablecollection=config.tablecollection,
            eventtable=config.eventtable,
        )

    if request.method == 'GET':

        # Initialize at first call
        if not hasattr(config, 'TimelineView'):
            init_TimelineView()

    elif request.method == 'POST':

        # Coming back from SingleView
        if "back" in request.form:
            # Reload from database
            config.TimelineView.update(config.tablecollection, config.eventtable)

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

            elif key == 'back':
                # Back from Edit
                # Update SingleView from database
                index_show = config.SingleView.BoxSeries[0].index_show  # Re-instate old index_show
                config.SingleView.update(config.tablecollection, config.eventtable)
                config.SingleView.BoxSeries[0].update(
                    config.SingleView.documenttable,
                    shift_show=index_show
                )

            else:
                # First call of page from Timeline.
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
                )

    return render_template('/timeline/single.html', **render_single())
