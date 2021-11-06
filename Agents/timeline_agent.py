from flask import render_template, request, Blueprint

import config
from Views.Parent import Viewer
from Views.Timeline import TimelineViewer
from Views.Utilities import timegrid


## Blueprint
timeline = Blueprint('timeline', __name__)


@timeline.route('/timeline', methods=["GET","POST"])
def show_timeline():

    def render_timeline():
        dct = config.TimelineView.view()

        dct = {
            'n_subboxes': config.TimelineView.n_subboxes,
            'data': config.TimelineView.data,
            'data_type': config.TimelineView.data_type,
            'description': config.TimelineView.descriptions,
            'timegrid': config.TimelineView.timestr,
            'markers': config.TimelineView.markers,
            'event_markers': config.TimelineView.event_markers,
            'event_labels': config.TimelineView.event_labels,
        }
        return dct

    if request.method == 'GET':
        # Initialize at first call
        if not hasattr(config, 'TimelineView'):
            View = Viewer(
                "photo",
                document_pathtype=config.document_pathtype,
                encode_type='base64',
                thumbnail=True
            )
            config.TimelineView = TimelineViewer(
                View,
                config.time_boxes,
                flag_single=False,
                documenttable=config.documenttable,
                eventtable=config.eventtable,
                markers=True,
            )

    elif request.method == 'POST':
        if request.form['submit'] == 'earlier':       # Navigate buttons
            config.TimelineView.earlier(config.documenttable, config.eventtable)
        elif request.form['submit'] == 'later':
            config.TimelineView.later(config.documenttable, config.eventtable)
        elif request.form['submit'] == 'zoom in':
            config.TimelineView.zoom_in(config.documenttable, config.eventtable)
        elif request.form['submit'] == 'zoom out':
            config.TimelineView.zoom_out(config.documenttable, config.eventtable)

    return render_template('/timeline/timeline.html', **render_timeline())

@timeline.route('/single', methods=["GET","POST"])
def show_single():

    def render_single():
        dct = {
            'n_subboxes': config.SingleView.n_subboxes,
            'data': config.SingleView.data,
            'data_type': config.SingleView.data_type,
            'description': config.SingleView.descriptions,
            'timegrid': config.SingleView.timestr,
            'markers': config.SingleView.markers,
            'marker_show': config.SingleView.marker_show,
            'event_markers': config.SingleView.event_markers,
            'event_labels': config.SingleView.event_labels,
        }
        return dct

    if request.method == 'POST':   # GET is only page refresh
        for key in request.form.keys():
            if key == 'submit':
                if request.form['submit'] == 'earlier':
                    config.SingleView.show_earlier(config.documenttable)
                else:
                    config.SingleView.show_later(config.documenttable)
            else:
                # First call of page.
                i = int(key)   # Box clicked
                timeinterval = config.TimelineView.BoxSeries[i].timeinterval
                timeinterval = timegrid(timeinterval.left,
                                        timeinterval.right, 1)
                config.SingleView = TimelineViewer(config.View, n_boxes=1, photos=True,
                                                   markers=True, marker_show=True, events=True)
                config.SingleView.init_photoTimeline(timeinterval.iloc[0], use_thumbnail=False)
                config.SingleView.update_Timeline(config.documenttable, config.eventtable)

    return render_template('/timeline/single.html', **render_single())
