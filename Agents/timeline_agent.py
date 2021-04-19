from flask import render_template, request, Blueprint

import config
from Views.Timeline import TimelineAllViewer, TimelineSingleViewer


## Parameters
n_boxes = 6

## Blueprint
timeline = Blueprint('timeline', __name__)

@timeline.route('/all', methods=["GET","POST"])
def show_timeline():

    def render_timeline():
        dct = {
            'n_boxes': config.timelineview.n_boxes,
            'usr_src': config.timelineview.data_for_view(),
            'img_format': config.timelineview.type_document,
            'usr_txt': config.timelineview.description_document,
            'usr_time': [config.timelineview.timegrid['TIME_FROM'].loc[i].strftime('%Y-%m-%d %H:%M')
                         for i in range(n_boxes)],
            'document_timeline_marker': config.timelineview.markers_time_documents
        }
        if config.eventtable is not None:
            dct.update(
                {
                    'event_timeline_marker': config.timelineview.markers_time_events,
                    'event_timeline_label': config.timelineview.labels_time_events
                 }
            )
        else:
            dct.update(
                {
                    'event_timeline_marker': None,
                    'event_timeline_label': None
                 }
            )
        return dct

    def init_timelineview():
        # Initialize at first call
        if not hasattr(config, 'timelineview'):
            # TODO Initialize general Viewer
            config.timelineview = TimelineAllViewer(n_boxes)
            config.timelineview.init_photo_timeline(config.documenttable, config.document_pathtype,
                                                    config.use_thumbnail, config.eventtable, config.start_interval)

    if request.method == 'GET':
        init_timelineview()

    elif request.method == 'POST':
        if request.form['submit'] == 'earlier':       # Navigate buttons
            config.timelineview.earlier(config.documenttable)
        elif request.form['submit'] == 'later':
            config.timelineview.later(config.documenttable)
        elif request.form['submit'] == 'zoom in':
            config.timelineview.zoom_in(config.documenttable)
        elif request.form['submit'] == 'zoom out':
            config.timelineview.zoom_out(config.documenttable)
        else:      # (First) call from start page
            init_timelineview()

    return render_template('/timeline/all.html', **render_timeline())

@timeline.route('/single', methods=["GET","POST"])
def show_single():

    def render_single():
        # TODO: End date
        return {
            'usr_src': config.timelinesingleview.data_for_view(),
            'usr_txt': config.timelinesingleview.description_document,
            'usr_time': [config.timelinesingleview.timegrid['TIME_FROM'].loc[0].strftime('%Y-%m-%d %H:%M')],
            'document_timeline_marker': config.timelinesingleview.markers_time_documents,
            'show_timeline_marker': config.timelinesingleview.markers_time_show
                }

    if request.method == 'POST':   # GET is only page refresh
        for key in request.form.keys():
            if key == 'submit':
                if request.form['submit'] == 'earlier':
                    config.timelinesingleview.earlier(config.documenttable)
                else:
                    config.timelinesingleview.later(config.documenttable)
            else:
                # First call of page.
                config.timelinesingleview = TimelineSingleViewer()
                i = int(key)
                config.timelinesingleview.init_photo_timeline(config.documenttable, config.document_pathtype,
                                                             config.timelineview.index_documents[i],
                                                             config.timelineview.index_show[i])

    return render_template('/timeline/single.html', **render_single())
