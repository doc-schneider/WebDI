import pandas as pd

from Views.Box import BoxViewer
from Views.Utilities import timegrid
from DataStructures.Event import EventTable
from DataStructures.Document import DocumentTable


class TimelineViewer():
    def __init__(self, View, n_boxes, photos, markers, marker_show, events):
        # Not so pretty
        self.View = View
        self.n_boxes = n_boxes
        self.display_photos = photos
        self.display_markers = markers
        self.display_marker_show = marker_show
        self.markers = None
        self.marker_show = None
        self.display_events = events
        self.event_markers = None
        self.event_labels = None

    def init_photoTimeline(self, time_interval, use_thumbnail):
        self.timegrid = timegrid(time_interval['TIME_FROM'],
                                 time_interval['TIME_TO'], self.n_boxes
                                 )
        self.BoxSeries = pd.Series(data=[BoxViewer(self.View) for i in range(self.n_boxes)])
        for i in range(self.n_boxes):
            self.BoxSeries[i].init_photoTimeline(use_thumbnail=use_thumbnail)

    def update_photoTimeline(self, documenttable):
        for i in range(self.n_boxes):
            self.BoxSeries[i].update_photoTimeline(documenttable, self.timegrid.loc[i])

    def update_Timeline(self, documenttable, eventtable=None):
        if self.display_photos:
            self.update_photoTimeline(documenttable)

        # Lists for flask agent / Jinja
        self.update_boxdata()

        # Markers for documents
        if self.display_markers:
            self.markers = TimelineFactory.grid_markers(documenttable,
                                                        pd.Interval(
                                                            self.timegrid['TIME_FROM'].iloc[0],
                                                            self.timegrid['TIME_TO'].iloc[-1],
                                                            closed='left')
                                                        )

        # Highlight the markers of displayed documents
        if self.display_marker_show:
            # TODO: Box 0 for the the time being (it's only meant for Single Box View anyway)
            self.update_marker_show()

        # Event time lines
        if self.display_events:
            self.make_events(eventtable)

        # Time line
        self.timestr = [self.timegrid['TIME_FROM'].loc[i].strftime('%Y-%m-%d %H:%M')
                        for i in range(self.n_boxes)]

    def update_boxdata(self):
        # Lists for flask agent / Jinja
        # TODO Simplify
        self.n_subboxes = [Box.n_subboxes for Box in self.BoxSeries]
        self.descriptions = [Box.descriptions() for Box in self.BoxSeries]
        self.data_type = [Box.document_type() for Box in self.BoxSeries]
        self.data = [Box.get_data() for Box in self.BoxSeries]

    def update_marker_show(self):
        # TODO: Box 0 for the the time being (it's only meant for Single Box View anyway)
        Box = self.BoxSeries[0]
        self.marker_show = TimelineFactory.grid_markers(
            DocumentTable(Box.boxShow), Box.timeinterval
        )

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
        position, width = TimelineFactory.position_width(
            eventtable.data.loc[ix,:], time_interval
        )
        for i in range(len(ix)):
            # TODO Very short events: Tooltip?
            if width[i] > min_width:
                self.event_labels.append((position[i],
                                          eventtable.data['EVENT_NAME'].iloc[ix[i]]))

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

    def show_earlier(self, documenttable):
        # Shift within Box
        self.BoxSeries[0].update(documenttable, shift_show=-1)
        self.update_boxdata()
        self.update_marker_show()

    def show_later(self, documenttable):
        # TODO: Box 0 for the the time being (it's only meant for Single Box View anyway)
        self.BoxSeries[0].update(documenttable, shift_show=1)
        self.update_boxdata()
        self.update_marker_show()


# Timeline utilities
class TimelineFactory:
    rect_width_min = 0.5  # Percentage

    # Position and width of an event / time intervals
    # - As percentage
    @staticmethod
    def position_width(table, time_interval):
        left = 100.0 * (table['TIME_FROM'] - time_interval.left) / time_interval.length
        width = 100.0 * (table['TIME_TO'] - table['TIME_FROM']) / time_interval.length
        
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
