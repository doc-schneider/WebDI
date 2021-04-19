import pandas as pd
import numpy as np

from Views.Box import BoxViewer
from Views.Utilities import timegrid
from DataOperations.Event import EventTable


class TimelineViewer():
    def __init__(self, View, n_boxes, photos, markers, events):
        # Not so pretty
        self.View = View
        self.n_boxes = n_boxes
        self.display_photos = photos
        self.display_markers = markers
        self.markers = None
        self.display_events = events
        self.event_markers = None
        self.event_labels = None

    def init_photoTimeline(self, time_interval):
        self.timegrid = timegrid(time_interval['TIME_FROM'],
                                 time_interval['TIME_TO'], self.n_boxes
                                 )
        self.BoxSeries = pd.Series(data=[BoxViewer(self.View) for i in range(self.n_boxes)])
        for i in range(self.n_boxes):
            self.BoxSeries[i].init_photoTimeline(use_thumbnail=True)

    def update_photoTimeline(self, documenttable):
        for i in range(self.n_boxes):
            self.BoxSeries[i].update_photoTimeline(documenttable, self.timegrid.loc[i])

    def update_Timeline(self, documenttable, eventtable=None):
        if self.display_photos:
            self.update_photoTimeline(documenttable)

        # Lists for flask agent / Jinja
        # TODO Simplify
        self.n_subboxes = [Box.n_subboxes for Box in self.BoxSeries]
        self.descriptions = [Box.descriptions() for Box in self.BoxSeries]
        self.data_type = [Box.document_type() for Box in self.BoxSeries]
        self.data = [Box.encode_data() for Box in self.BoxSeries]

        # Markers for documents
        if self.display_markers:
            self.markers = TimelineFactory.grid_markers(documenttable,
                                                        pd.Interval(
                                                            self.timegrid['TIME_FROM'].iloc[0],
                                                            self.timegrid['TIME_TO'].iloc[-1],
                                                            closed='left')
                                                        )

        # Event time lines
        if self.display_events:
            self.make_events(eventtable)

        # Time line
        self.timestr = [self.timegrid['TIME_FROM'].loc[i].strftime('%Y-%m-%d %H:%M')
                        for i in range(self.n_boxes)]

    # Time buttons
    def earlier(self, documenttable, eventtable=None):
        # Shift one block
        t_start = self.timegrid['TIME_FROM'].iloc[0]
        t_end = self.timegrid['TIME_TO'].iloc[-1]
        time_delta = (t_end - t_start) / self.n_boxes
        t_start = t_start - time_delta
        t_end = t_end - time_delta
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update_Timeline(documenttable, eventtable)

    def later(self, documenttable, eventtable=None):
        # Shift one block
        t_start = self.timegrid['TIME_FROM'].iloc[0]
        t_end = self.timegrid['TIME_TO'].iloc[-1]
        time_delta = (t_end - t_start) / self.n_boxes
        t_start = t_start + time_delta
        t_end = t_end + time_delta
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update_Timeline(documenttable, eventtable)

    def zoom_in(self, documenttable, eventtable=None):
        # Make 2 middle blocks new total time interval
        t_start = self.timegrid['TIME_FROM'].iloc[2]   # TODO: make general
        t_end = self.timegrid['TIME_TO'].iloc[3]
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update_Timeline(documenttable, eventtable)

    def zoom_out(self, documenttable, eventtable=None):
        # Make all blocks into the 2 middle blocks
        t_1 = self.timegrid['TIME_FROM'].iloc[0]
        t_2 = self.timegrid['TIME_TO'].iloc[-1]
        t_start = t_1 - (t_2 - t_1)  # 2 blocks to start   # TODO: make general
        t_end = t_2 + (t_2 - t_1)
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update_Timeline(documenttable, eventtable)

    def make_events(self, eventtable):
        min_width = 1.0    # Percentage

        self.event_markers = list()
        self.event_labels = list()
        time_interval = pd.Interval(self.timegrid['TIME_FROM'].iloc[0],
                                    self.timegrid['TIME_TO'].iloc[-1],
                                    closed='left')
        # TODO Only level 0 elements for the time being
        ix = list(
            set(eventtable.find_in_timeinterval(time_interval)) &
            set(eventtable.find_eventlevel(0))
        )
        self.event_markers = TimelineFactory.grid_markers(
            EventTable(eventtable.data.loc[ix,:]), time_interval
        )
        # Label for events, but require minimum length
        position, width = TimelineFactory.position_width(
            EventTable(eventtable.data.loc[ix,:]), time_interval
        )
        for i in range(len(ix)):
            # TODO Very short events: Tooltip?
            if width[i] > min_width:
                self.event_labels.append((position[i],
                                          eventtable.data['EVENT_NAME'].iloc[ix[i]]))


# Timeline utilities
class TimelineFactory:
    # TODO rect_width_min

    # Position and width of an event / time intervals
    # - As percentage
    @staticmethod
    def position_width(documenttable, time_interval):
        left = 100.0 * (documenttable.data['TIME_FROM'] - time_interval.left) / time_interval.length
        width = 100.0 * (documenttable.data['TIME_TO'] - documenttable.data['TIME_FROM']) / time_interval.length
        
        return left.tolist(), width.tolist()

    # Marker for marking existing documents / time intervals on a grid.
    @staticmethod
    def grid_markers(documenttable, time_interval):
        rect_width_min = 0.5  # Percentage

        markers = list()
        marker_grid = timegrid(time_interval.left, time_interval.right, int(100 / rect_width_min))
        for i in range(int(100 / rect_width_min)):
            if documenttable.find_in_timeinterval(pd.Interval(
                    marker_grid['TIME_FROM'].iloc[i],
                    marker_grid['TIME_TO'].iloc[i], closed='left')):
                markers.append((i * rect_width_min, rect_width_min))

        return markers




# Single frame view on documents within one time interval (index_documents)
class TimelineSingleViewer(TimelineViewer):
    def __init__(self):
        super().__init__(n_boxes=1)

    def init_photo_timeline(self, documenttable, document_pathtype, index_documents, index_show):
        super().init_photo_timeline(document_pathtype)
        self.index_documents = index_documents
        self.index_show = [index_show]
        self.index = 0    # Initially show first document
        self.n_documents = len(index_documents)
        self.timegrid = timegrid(documenttable.data['TIME_FROM'].iloc[self.index_documents[0]],
                                 documenttable.data['TIME_TO'].iloc[self.index_documents[-1]], 1)
        self.markers_time_documents = graphics_markers_time(documenttable.data, [self.index_documents],
                                                            (self.timegrid['TIME_FROM'].iloc[0],
                                                             self.timegrid['TIME_TO'].iloc[-1]))
        self.update(documenttable)

    def update(self, documenttable):
        self.location_document = self.document_location(documenttable)
        self.description_document = self.document_description(documenttable, 'DESCRIPTION')
        # Emphasize mark for currently viewed document
        self.markers_time_show = graphics_markers_time(documenttable.data, [self.index_show],
                                                            (self.timegrid['TIME_FROM'].iloc[0],
                                                             self.timegrid['TIME_TO'].iloc[-1]))

    def earlier(self, documenttable):
        # Shift one
        if self.index > 0:
            self.index = self.index - 1
            self.index_show = [self.index_documents[self.index]]
        self.update(documenttable)

    def later(self, documenttable):
        if self.index < self.n_documents - 1:
            self.index = self.index + 1
            self.index_show = [self.index_documents[self.index]]
        self.update(documenttable)

