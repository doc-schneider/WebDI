import pandas as pd

from Views.View import Viewer, ViewerFactory
from Views.Box import BoxViewer
from Views.Timeline_Factory import TimelineFactory
from DataStructures.Document import DocumentTable
from DataStructures.Event import EventTable


class TimelineViewer():
    def __init__(self,
                 MetaView,
                 time_boxes,
                 flag_single,
                 tablecollection,
                 eventtable=None
                 ):
        self.MetaView = MetaView
        self.n_timelines = 1  # TODO For the time being
        self.documenttable = list()
        self.eventtable = None  # TODO List of timelines
        self.flag_single = flag_single    # TODO For the time bing
        self.marker = {
            "markers": None,
            "marker_show": None
        }
        self.display_events = False  # eventtable is not None
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
        # Time filtering documents
        for tc in tablecollection:
            self.documenttable.append(
                tc.find_in_timeinterval(
                    pd.Interval(
                        self.time_grid.loc[0, "TIME_INTERVAL"].left,
                        self.time_grid.iloc[-1]["TIME_INTERVAL"].right,
                        closed='left'
                    )
                )[1]
            )
        # Time filtering all events from all timelines
        self.eventtable = pd.concat(
            [eventtable.get_events(d) for d in self.documenttable],
            ignore_index=True
        )
        self.eventtable.drop_duplicates(
            subset=["EVENT_NAME"], inplace=True
        )
        self.eventtable = EventTable(
            self.eventtable.sort_values(by="TIME_FROM").reset_index(drop=True)
        )
        # Series of Boxes
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
                    self.eventtable,
                    self.time_grid.loc[i, "TIME_INTERVAL"]
                )
        # Markers
        self.make_marker()
        # Show events?
        if self.display_events:
            self.make_events(eventtable)

    # Marker grid and indicator current document looked at
    def make_marker(self):
        self.marker["markers"] = list()
        self.marker["marker_show"] = list()
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
            self.marker["markers"].append(lst_m)
            self.marker["marker_show"].append(lst_s)

    def view(self):
        # List of dcts
        # TODO Make dicts with speaking names instead of tuples and lists
        # [Box.view() for Box in self.BoxSeries]
        dct_lst = [[BV.view() for BV in BS] for BS in self.BoxSeries]
        # Bootstrap box size
        box_size, _ = ViewerFactory.bootstrap_properties(self.granularity, self.time_grid)
        # Time line
        time_grid_str = [
            self.time_grid['TIME_INTERVAL'].loc[i].left.strftime('%Y-%m-%d %H:%M')
            for i in range(self.n_boxes)
        ]
        dct = {
            'boxes': dct_lst,
            "box_size": box_size,
            'timegrid': time_grid_str,
            'marker': self.marker,
            'display_events': self.display_events
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

    # Shift within Single Box mode
    # TODO Correct for Event
    def show_earlier(self, eventtable=None):
        self.BoxSeries[0][0].update(self.documenttable[0], shift_show=-1)
        self.make_marker()
        if self.display_events:
            self.make_events(eventtable)

    def show_later(self, eventtable=None):
        self.BoxSeries[0][0].update(self.documenttable[0], shift_show=1)
        self.make_marker()
        if self.display_events:
            self.make_events(eventtable)
