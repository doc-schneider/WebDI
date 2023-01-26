import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta, MO, SU

from Views.View import Viewer
from Views.Box import BoxViewer
from DataStructures.Document import DocumentTable


class TimelineViewer():
    def __init__(self,
                 MetaView,
                 time_boxes,
                 flag_single,
                 tablecollection,
                 eventtable=None
                 ):
        self.MetaView = MetaView
        self.n_timelines = len(tablecollection)
        self.documenttable = list()
        self.flag_single = flag_single    # TODO For the time bing
        self.markers = list()
        self.marker_show = list()
        self.display_events = eventtable is not None
        self.event_markers = None
        self.event_labels = None
        self.event_descriptions = None

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
        for tc in tablecollection:
            self.documenttable.append(
                tc.compound_table_from_timeinterval(
                    pd.Interval(
                        self.time_grid.loc[0, "TIME_INTERVAL"].left,
                        self.time_grid.iloc[-1]["TIME_INTERVAL"].right,
                        closed='left'
                    ),
                    self.MetaView.database_connection
                )
            )
        self.BoxSeries = list()
        for i in range(self.n_timelines):
            self.BoxSeries.append(
                pd.Series(
                    data=[BoxViewer(Viewer(self.MetaView, i)) for j in range(self.n_boxes)]
                )
            )
        # Find documents in each time box
        for j in range(self.n_timelines):
            for i in range(self.n_boxes):
                self.BoxSeries[j][i].update_Timeline(
                    self.documenttable[j],
                    self.time_grid.loc[i, "TIME_INTERVAL"]
                )
        # Markers
        self.make_marker()
        # Show events?
        if self.display_events:
            self.make_events(eventtable)

    # Marker grid and indicator current document looked at
    def make_marker(self):
        for j in range(self.n_timelines):
            lst_m = list()
            lst_s = list()
            for i in range(self.n_boxes):
                lst_m.append(
                    TimelineFactory.markers(
                        self.documenttable[j], self.time_grid.loc[i, "TIME_INTERVAL"]
                    )
                )
                lst_s.append(
                    TimelineFactory.markers(
                        DocumentTable(
                            self.BoxSeries[j][i].boxShow,
                            self.BoxSeries[j][i].View.document_category
                        ),
                        self.time_grid.loc[i, "TIME_INTERVAL"]
                    )
                )
            self.markers.append(lst_m)
            self.marker_show.append(lst_s)

    def make_events(self, eventtable):
        # TODO
        #  Disjunct events for the time being
        #  Event container containing all items
        self.event_markers = list()
        self.event_labels = list()
        self.event_descriptions = list()
        # All events from all timelines
        # TODO Make this function in Event
        events = [
            eventtable.get_events(d) for d in self.documenttable
        ]
        events = pd.concat(events, ignore_index=True)
        events = events.sort_values(by="TIME_FROM").reset_index(drop=True)
        # Every box gets a (partial) event line
        flag_label = np.full(events.shape[0], False)  # Only one label per event over all boxes
        for i in range(self.n_boxes):
            event_markers = list()
            event_labels = list()
            event_descriptions = list()
            for j in range(events.shape[0]):
                position, width = TimelineFactory.position_width(
                    events.loc[j, ["TIME_FROM", "TIME_TO"]],
                    self.time_grid.loc[i, "TIME_INTERVAL"]
                )
                event_markers.append((position, width))
                if (position is not None) and (not flag_label[j]):
                    event_labels.append(
                        (position, events.loc[j, "EVENT_NAME"])
                    )
                    flag_label[j] = True
                    # Description only for Event in Box shown
                    for k in range(self.n_timelines):
                        if self.BoxSeries[k][i].boxShow["EVENT"].values[0] == events.loc[j, "EVENT_NAME"]:
                            event_descriptions.append(events.loc[j, "DESCRIPTION"])
                else:
                    event_labels.append((None, None))
            if len(event_descriptions) < len(event_labels):
                event_descriptions.append(None)
            self.event_markers.append(event_markers)
            self.event_labels.append(event_labels)
            self.event_descriptions.append(event_descriptions)

    def view(self):
        # List of dcts
        # TODO Make dicts with speaking names instead of tuples and lists
        # TODO All Event items put into one object
        # [Box.view() for Box in self.BoxSeries]
        dct_lst = [[BV.view() for BV in BS] for BS in self.BoxSeries]
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
            'display_events': self.display_events,
            'event_markers': self.event_markers,
            'event_labels': self.event_labels,
            'event_descriptions': self.event_descriptions
        }
        return dct

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

    # Shift within Single Box
    def show_earlier(self):
        self.BoxSeries[0].update(self.documenttable, shift_show=-1)
        self.make_marker()

    def show_later(self):
        self.BoxSeries[0].update(self.documenttable, shift_show=1)
        self.make_marker()


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
    # Full displayed timeinterval = 100% is partitioned into a grid and every grid bin overlapping a document is marked
    # TODO There is an issue for SingleView? Markers do no lie on real times?
    @staticmethod
    def markers(documenttable, time_interval):
        rect_width_min = 1.0  # Percentage
        markers = list()
        marker_grid = TimelineFactory.time_bins(
            time_interval.left, time_interval.right, int(100 / rect_width_min)
        )
        for i in range(int(100 / rect_width_min)):
            if documenttable.find_in_timeinterval(pd.Interval(
                    marker_grid['TIME_FROM'].iloc[i],
                    marker_grid['TIME_TO'].iloc[i], closed='left')):
                markers.append((i * rect_width_min, rect_width_min))
        return markers

    # TODO
    #  - Use Intervals?
    #  - Improve with linspace or so instead of loop
    # Partition full displayed timeinterval = 100% into a given number of bins
    @staticmethod
    def time_bins(t_start, t_end, n_t):
        t_delta = (t_end - t_start)
        dt = t_delta / n_t
        df = pd.DataFrame(columns=['TIME_FROM', 'TIME_TO'])
        for i in range(n_t):
            df.loc[i] = [t_start + i * dt, t_start + (i + 1) * dt]
        return df

    # Position and width of an event / time intervals
    # - As percentage
    # - If event extends beyond interval restrict
    @staticmethod
    def position_width(time_from_to, time_interval):
        if time_interval.overlaps(
                pd.Interval(time_from_to['TIME_FROM'], time_from_to['TIME_TO'])
        ):
            left = 100.0 * max(
                0.0,
                (time_from_to['TIME_FROM'] - time_interval.left) / time_interval.length
            )  # In case time_from is before left boundary
            right = 100.0 * min(
                1.0,
                (time_from_to['TIME_TO'] - time_interval.left) / time_interval.length
            )  # In case time_to is after right boundary
            width = right - left
            return (left, width)
        else:
            return (None, None)



