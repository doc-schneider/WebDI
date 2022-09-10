from flask import render_template, request, Blueprint

import config
#from Views.View import Viewer
#from Views.Box import BoxViewer
#from Views.Timeline import TimelineViewer
#from Views.Utilities import timegrid


## Blueprint
test = Blueprint('test', __name__)


@test.route('/timeline', methods=["GET","POST"])
def show_timeline():

    def render_timeline():
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

    def init_timelineview():
        # Initialize at first call
        if not hasattr(config, 'TimelineView'):
            start_interval = timegrid(config.start_interval[0], config.start_interval[1], 1)
            config.View = Viewer(document_pathtype=config.document_pathtype, encode_type='base64')
            config.TimelineView = TimelineViewer(config.View, n_boxes=6, photos=True,
                                                 markers=True, marker_show=False, events=True)
            config.TimelineView.init_photoTimeline(start_interval.iloc[0], use_thumbnail=True)
            config.TimelineView.update_Timeline(config.documenttable, config.eventtable)

    if request.method == 'GET':
        init_timelineview()

    elif request.method == 'POST':
        if request.form['submit'] == 'earlier':       # Navigate buttons
            config.TimelineView.earlier(config.documenttable, config.eventtable)
        elif request.form['submit'] == 'later':
            config.TimelineView.later(config.documenttable, config.eventtable)
        elif request.form['submit'] == 'zoom in':
            config.TimelineView.zoom_in(config.documenttable, config.eventtable)
        elif request.form['submit'] == 'zoom out':
            config.TimelineView.zoom_out(config.documenttable, config.eventtable)

    return render_template('/test/timeline.html', **render_timeline())

@test.route('/single', methods=["GET","POST"])
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

    return render_template('/test/single.html', **render_single())

@test.route('/box', methods=["GET","POST"])
def show_box():

    def render_box():
        n_subboxes = config.BoxView.boxShow.shape[0]
        data_type = config.BoxView.boxShow['DOCUMENT_TYPE'].tolist()  # TODO Like data as method in BoxViewer
        descriptions = config.BoxView.descriptions()
        data = config.BoxView.encode_data()
        dct = {
            'n_subboxes': n_subboxes,
            'data': data,
            'data_type': data_type,
            'description': descriptions
        }
        return dct

    def init_boxview():
        # Initialize at first call
        if not hasattr(config, 'BoxView'):
            start_interval = timegrid(config.start_interval[0], config.start_interval[1], 1)
            config.View = Viewer(document_pathtype=config.document_pathtype, encode_type='base64')
            config.BoxView = BoxViewer(config.View)
            config.BoxView.init_photoTimeline(use_thumbnail=config.use_thumbnail)
            config.BoxView.update_photoTimeline(
                config.documenttable, start_interval.iloc[0]
            )

    if request.method == 'GET':
        init_boxview()

    return render_template('/test/box.html', **render_box())

@test.route('/iframe', methods=["GET","POST"])
def show_iframe():

    return render_template('/test/iframe.html')