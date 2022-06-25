import pandas as pd
from dateutil.relativedelta import relativedelta, MO, SU

from Views.Box import BoxViewer
from DataStructures.Event import EventTable
from DataStructures.Document import DocumentTable


# TODO:
#  - Get tables as reference
class TimelineViewer():
    def __init__(self,
                 View,
                 time_boxes,
                 flag_single,
                 tablecollection,
                 eventtable=None,
                 markers=True
                 ):
        self.View = View
        self.documenttable = None
        self.flag_single = flag_single    # TODO For the time bing
        self.display_markers = markers
        self.display_marker_show = markers  # TODO Should be convered by display_markers
        self.markers = None
        self.marker_show = None
        self.display_events = eventtable is not None
        #self.event_markers = None
        #self.event_labels = None

        if flag_single:
            self.n_boxes = 1
            self.granularity = None
            self.time_grid = pd.DataFrame(
                data={
                    "TIME_INTERVAL": [time_boxes],
                    "GRANULARITY": None
                }
            )
        else:
            # TODO: Do away granularity. Timeline shoudl figure out from time interval
            self.granularity, self.time_grid, self.n_boxes = TimelineFactory.time_boxes(
                time_boxes[0],
                time_boxes[1]
            )

        self.update(tablecollection, eventtable)

    def update(self, tablecollection, eventtable):
        # Assemble documenttables from meta-table
        self.documenttable = tablecollection.compound_table_from_timeinterval(
            pd.Interval(
                self.time_grid.loc[0, "TIME_INTERVAL"].left,
                self.time_grid.iloc[-1]["TIME_INTERVAL"].right,
                closed='left'
            ),
            self.View.database_connection
        )
        self.BoxSeries = pd.Series(data=[BoxViewer(self.View) for i in range(self.n_boxes)])
        # Find documents in each time box
        for i in range(self.n_boxes):
            self.BoxSeries[i].update_Timeline(
                self.documenttable,
                self.time_grid.loc[i, "TIME_INTERVAL"]
            )
        # TODO For timeline
        if self.display_markers and self.flag_single:
            self.markers = TimelineFactory.markers(self.documenttable, self.time_grid.loc[0, "TIME_INTERVAL"])
            self.update_marker_show()

    def update_marker_show(self):
        self.marker_show = TimelineFactory.markers(
            DocumentTable(self.BoxSeries[0].boxShow, self.View.document_category),
            self.time_grid.loc[0, "TIME_INTERVAL"]
        )

    def view(self):
        # List of dcts
        # TODO Date Time Interval information
        dct_lst = [Box.view() for Box in self.BoxSeries]
        # Bootstrap box size
        box_size, _ = self.View.boostrap_properties(self.granularity, self.time_grid)
        # Time line
        time_grid_str = [
            self.time_grid['TIME_INTERVAL'].loc[i].left.strftime('%Y-%m-%d %H:%M')
            for i in range(self.n_boxes)
        ]
        dct = {
            'boxes': dct_lst,
            "box_size": box_size,
            'timegrid': time_grid_str,
            'markers': self.markers,
            'marker_show': self.marker_show,
            'event_markers': None,
            'event_labels': None,
        }
        return dct


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
    def earlier(self, tablecollection, eventtable=None):
        # Shift one block
        _, self.time_grid, _ = TimelineFactory.time_boxes(
            None,
            self.granularity,
            change="earlier",
            time_grid=self.time_grid
        )
        self.update(tablecollection, eventtable)

    def later(self, tablecollection, eventtable=None):
        # Shift one block
        _, self.time_grid, _ = TimelineFactory.time_boxes(
            None,
            self.granularity,
            change="later",
            time_grid=self.time_grid
        )
        self.update(tablecollection, eventtable)

    def zoom_in(self, tablecollection, eventtable=None):
        self.granularity, self.time_grid, self.n_boxes = TimelineFactory.time_boxes(
            None,
            self.granularity,
            change="zoomin",
            time_grid=self.time_grid
        )
        self.update(tablecollection, eventtable)

    def zoom_out(self, tablecollection, eventtable=None):
        self.granularity, self.time_grid, self.n_boxes = TimelineFactory.time_boxes(
            None,
            self.granularity,
            change="zoomout",
            time_grid=self.time_grid
        )
        self.update(tablecollection, eventtable)

    # Shift within Box
    def show_earlier(self):
        self.BoxSeries[0].update(self.documenttable, shift_show=-1)
        self.update_marker_show()

    def show_later(self):
        self.BoxSeries[0].update(self.documenttable, shift_show=1)
        self.update_marker_show()


# Timeline utilities
class TimelineFactory:

    # Returns time interval and number of boxes
    # - change: earlier, later, zoomin, zoomout
    # - If no "change" is indicated it returns number of boxes and box boundaries
    @staticmethod
    def time_boxes(time_interval, granularity, change=None, time_grid=None):
        #TODO:
        # 50 Y granulairty, fine granularity
        # List for cycling through granularities

        # New granularity
        if change == "zoomin":
            granularity_new = time_grid.loc[0, "GRANULARITY"]
        elif change == "zoomout":
            if granularity == "10Y":
                # coarsest granularity
                granularity_new = "10Y"
            elif granularity == "Y":
                granularity_new = "10Y"
            elif granularity == "Q":
                granularity_new = "Y"
            elif granularity == "M":
                granularity_new = "Q"
            elif granularity == "W":
                granularity_new = "M"
            elif granularity == "D":
                granularity_new = "W"
            elif granularity == "6H":
                granularity_new = "D"
        else:
            granularity_new = granularity

        # n_boxes, ..
        # Main problem is with granularity_new == "M": How many weeks / boxes? Starting where?
        if granularity_new == "10Y":
            n_boxes = 10
            relative_delta = relativedelta(years=1)
            granularity_smaller = "Y"
        elif granularity_new == "Y":
            n_boxes = 4
            relative_delta = relativedelta(months=3)
            granularity_smaller = "Q"
        elif granularity_new == "Q":
            n_boxes = 3
            relative_delta = relativedelta(months=1)
            granularity_smaller = "M"
        elif granularity_new == "M":
            relative_delta = relativedelta(days=7)
            granularity_smaller = "W"
            # n_boxes depend on case
            if change in ["earlier", "later"]:
                # Keep 4 or 5 boxes
                n_boxes = time_grid.shape[0]
        elif granularity_new == "W":
            n_boxes = 7
            relative_delta = relativedelta(days=1)
            granularity_smaller = "D"
        elif granularity_new == "D":
            n_boxes = 4
            relative_delta = relativedelta(hours=6)
            granularity_smaller = "6H"
        elif granularity_new == "6H":
            # finest granularity H
            n_boxes = 6
            relative_delta = relativedelta(hours=1)
            granularity_smaller = "6H"

        # Left boundary
        if change is None:
            # TODO Find nearest defined time interval
            time_l = time_interval.left
            if granularity_new == "M":
                time_l = time_interval.left + relativedelta(weekday=MO(-1))
                time_r = time_interval.right + relativedelta(weekday=SU(+1))
        elif change == "earlier":
            time_l = time_grid.loc[0, "TIME_INTERVAL"].left - relative_delta
        elif change == "later":
            time_l = time_grid.loc[0, "TIME_INTERVAL"].left + relative_delta
        elif change == "zoomin":
            if granularity_new == "M":
                # Overlapping complete weeks of first grid slot
                time_l = time_grid.loc[0, "TIME_INTERVAL"].left + relativedelta(weekday=MO(-1))
                time_r = time_grid.loc[0, "TIME_INTERVAL"].right + relativedelta(weekday=SU(+1))
            else:
                # Expand first grid slot
                time_l = time_grid.loc[0, "TIME_INTERVAL"].left
        elif change == "zoomout":
            # Nearest boundary to the left
            time_l_pre = time_grid.loc[0, "TIME_INTERVAL"].left
            if granularity_new == "10Y":
                time_l = pd.Timestamp(year=time_l_pre.year - (time_l_pre.year % 10), month=1, day=1)
            elif granularity_new == "Y":
                time_l = pd.Timestamp(year=time_l_pre.year, month=1, day=1)
            elif granularity_new == "Q":
                time_l = pd.Timestamp(year=time_l_pre.year, month=(time_l_pre.quarter - 1) * 3 + 1, day=1)
            elif granularity_new == "M":
                #TODO Better find nearest month
                time_l = pd.Timestamp(year=time_l_pre.year, month=time_l_pre.month, day=1) + relativedelta(weekday=MO(-1))
                time_r = pd.Timestamp(year=time_l_pre.year, month=time_l_pre.month, day=1) + relativedelta(months=+1, days=-1) + relativedelta(weekday=SU(+1))
            elif granularity_new == "W":
                # Start with Monday
                time_l = time_l_pre + relativedelta(weekday=MO(-1), hour=0)
            elif granularity_new == "D":
                # Start with 00:00 time
                time_l = time_l_pre + relativedelta(hour=0)
        if granularity_new == "M" and change not in ("earlier", "later"):
            # How many weeks / boxes?
            n_boxes = round(
                ((time_r + relativedelta(days=1)) - time_l) / pd.Timedelta("7 days")
            )

        # Construct new time grid
        # TODO Common time grid function?
        time_grid = list()
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

        return granularity_new, time_grid, n_boxes

    # Marker for marking existing documents / time intervals on a grid.
    @staticmethod
    def markers(documenttable, time_interval):
        rect_width_min = 0.5  # Percentage
        markers = list()
        marker_grid = TimelineFactory.timegrid(time_interval.left, time_interval.right, int(100 / rect_width_min))
        for i in range(int(100 / rect_width_min)):
            if documenttable.find_in_timeinterval(pd.Interval(
                    marker_grid['TIME_FROM'].iloc[i],
                    marker_grid['TIME_TO'].iloc[i], closed='left')):
                markers.append((i * rect_width_min, rect_width_min))
        return markers

    # TODO
    #  - Use Intervals?
    #  - Improve with linspace or so instead of loop
    @staticmethod
    def timegrid(t_start, t_end, n_t):
        t_delta = (t_end - t_start)
        dt = t_delta / n_t
        df = pd.DataFrame(columns=['TIME_FROM', 'TIME_TO'])
        for i in range(n_t):
            df.loc[i] = [t_start + i * dt, t_start + (i + 1) * dt]
        return df


    # Position and width of an event / time intervals
    # - As percentage
    @staticmethod
    def position_width(table, time_interval):
        left = 100.0 * (table['TIME_FROM'] - time_interval.left) / time_interval.length
        width = 100.0 * (table['TIME_TO'] - table['TIME_FROM']) / time_interval.length
        
        return left.tolist(), width.tolist()


