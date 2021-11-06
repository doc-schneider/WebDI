import pandas as pd
from dateutil.relativedelta import relativedelta

from Views.Box import BoxViewer
from Views.Utilities import timegrid
from DataStructures.Event import EventTable
from DataStructures.Document import DocumentTable


# TODO:
#  - Get tables as reference
class TimelineViewer():
    def __init__(self,
                 View,
                 time_boxes,
                 flag_single,
                 documenttable,
                 eventtable=None,
                 markers=True
                 ):
        self.View = View
        #self.time_interval = time_interval
        self.display_markers = markers
        self.display_marker_show = markers  # TODO Should be convered by display_markers
        self.markers = None
        self.marker_show = None
        self.display_events = eventtable is not None
        self.event_markers = None
        self.event_labels = None

        if flag_single:
            self.n_boxes = 1
            self.time_grid = pd.DataFrame(
                data={
                    "TIME_INTERVAL": time_boxes[0],
                    "GRANULARITY": None
                }
            )
        else:
            # TODO: Do away granularity. Timeline shoudl figure out from time interval
            self.granularity, self.time_grid, self.n_boxes = TimelineFactory.time_boxes(
                time_boxes[0],
                time_boxes[1]
            )

        self.update(documenttable, eventtable)

    def update(self, documenttable, eventtable):
        self.BoxSeries = pd.Series(data=[BoxViewer(self.View) for i in range(self.n_boxes)])
        # Find documents in each time box
        for i in range(self.n_boxes):
            self.BoxSeries[i].update_Timeline(
                documenttable,
                self.time_grid.loc[i, "TIME_INTERVAL"]
            )
    # TODO Markers etc

    def view(self):
        # List of dcts
        dct_lst = [Box.view() for Box in self.BoxSeries]
        # enhance dct
        #dct = {
        #    'timegrid': config.TimelineView.timestr,
        #    'markers': config.TimelineView.markers,
        #    'event_markers': config.TimelineView.event_markers,
        #    'event_labels': config.TimelineView.event_labels,
        #}
        return dct_lst  # dict containing lists of lists


    def update_Timeline_old(self, documenttable, eventtable=None):
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

    # Time intervals and number of containig boxes that can be displayed
    # - Intervals are rolling, eg,Year spans 4 subsequent seasons
    # .. year multiples of 10?
    # year: 4 seasons
    # season: 3 months / Jan - Mar, Apr - Jun, Jul - Sep, Oct - Dec
    # month: 4 calendar weeks
    # week: 7 days
    # day
    # day phases 00:00 - 06:00, 06:00 - 12:00, 12:00 - 18:00, 18:00 - 24:00
    # hour
    # .. 10 minutes

    # Returns time interval and number of boxes
    # - change: shiftleft, shiftright, zoomin, zoomout
    # - If no "change" is indicated it returns number of boxes and box boundaries
    @staticmethod
    def time_boxes(time_interval, granularity, change=None):

        # TODO Find nearest defined time interval
        if change is None:
            time_grid = list()
            if granularity == "Y":
                n_boxes = 4
                relative_delta = relativedelta(months=3)
                granularity_smaller = "S"
            time_l = time_interval.left
            for i in range(n_boxes):
                time_r = time_l + relative_delta
                time_grid.append(
                    pd.Interval(
                        time_l,
                        time_r,
                        closed='left'
                    )
                )
                time_l = time_r
            # TODO Period Index?
            time_grid = pd.DataFrame(
                data={
                    "TIME_INTERVAL": time_grid,
                    "GRANULARITY": granularity_smaller
                }
            )

        else:
            pass

        return granularity, time_grid, n_boxes

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
