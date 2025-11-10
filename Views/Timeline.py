import pandas as pd
from dateutil.relativedelta import relativedelta, MO, SU

from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory


granularities = ["10Y", "Y", "Q", "M", "W", "D", "6H"]

class TimelineViewer():
    def __init__(self, datatable_initial, timeline_view):
        self.datatable = datatable_initial
        self.table_type = datatable_initial.table_type
        if self.table_type.name == "ALBUM":
            self.time_column = "DATE_FROM"
        else:  # MESSAGE, NOTE
            self.time_column = "DATE_TIME"
        if self.table_type.name == "NOTE":
            self.load_media = False
        else:
            self.load_media = True
        self.datatable.sort(self.time_column)
        self.datatable.sort(self.time_column)
        self.n_rows = timeline_view["n_rows"]
        self.n_dim = None
        self.datatable_show = None
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            pd.Timestamp(timeline_view["DATETIME_START"]), granularity=timeline_view["GRANULARITY"], change=None,
        )

        self.update()

    def update(self):
        # Get the entries for each time box (if it exists, else None)
        dct_table = {i: None for i in range(self.n_grid)}
        for i in range(self.n_grid):
            t = self.datatable.find_in_timeinterval(self.time_grid[i], self.time_column).table
            if t.shape[0] > 0:
                dct_table[i] = t
        # Size of 2-dim table to vizualize
        r = [dct_table[i].shape[0] for i in range(self.n_grid) if dct_table[i] is not None]
        if r:  # Any content at all?
            self.n_dim = (
                min(
                    max(r),
                    self.n_rows
                ),
                self.n_grid
            )
        else:
            self.n_dim = (0, self.n_grid)
        # Serial Dataframe, going line-wise left-right
        self.datatable_show = pd.DataFrame(
            columns=self.datatable.table.columns
        )
        if r:
            self.datatable_show = pd.DataFrame(
                [[None] * len(self.datatable.table.columns) for _ in range(self.n_dim[0] * self.n_dim[1])],
                columns=self.datatable_show.columns
            )
        for i in range(self.n_dim[0]):
            for j in range(self.n_dim[1]):
                if dct_table[j] is not None:
                    if dct_table[j].shape[0] > i:
                        self.datatable_show.loc[i * self.n_dim[1] + j, :] = dct_table[j].iloc[[i]].values
                    else:
                        pass
                else:
                    pass
        self.datatable_show = DataTable(
            self.datatable_show,
            self.table_type
        )

    def earlier(self):
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            self.time_grid[0].left,
            granularity=self.granularity,
            change="earlier"
        )
        self.update()

    def later(self):
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            self.time_grid[0].left,
            granularity=self.granularity,
            change="later"
        )
        self.update()

    def zoom_in(self):
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            self.time_grid[0].left,
            granularity=self.granularity,
            change="zoomin"
        )
        self.update()

    def zoom_out(self):
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            self.time_grid[0].left,
            granularity=self.granularity,
            change="zoomout"
        )
        self.update()

    def view(self):
        # Raw content
        boxes = ViewFactory.view(self.datatable_show, self.load_media)

        boxes["TIME_GRID"] = pd.Series([t for t in self.time_grid])
        boxes["N_DIM"] = self.n_dim

        return boxes

# Timeline utilities
class TimelineFactory:

    # Returns time interval and number of boxes
    # - change: earlier, later, zoomin, zoomout
    # - If no "change" is indicated it returns number of boxes and box boundaries
    @staticmethod
    def timegrid(datetime_start, granularity, change=None):
        # TODO Some kind of error with Yearly / zoom (beginning of year)?
        # TODO  50 Y granulairty, fine granularity

        # New granularity
        if change == "zoomin":
            granularity_new = TimelineFactory.iterate_granularities(granularity, 1)
        elif change == "zoomout":
            granularity_new = TimelineFactory.iterate_granularities(granularity, -1)
        else:
            granularity_new = granularity

        # Grid granularity inside larger granularity
        if granularity_new == "10Y":
            n_boxes = 10
            relative_delta = relativedelta(years=1)
        elif granularity_new == "Y":
            n_boxes = 4
            relative_delta = relativedelta(months=3)
        elif granularity_new == "Q":
            n_boxes = 3
            relative_delta = relativedelta(months=1)
            if change == "zoomout":
                # Coming from Month with start on Monday
                datetime_start = pd.Timestamp(year=datetime_start.year, month=(datetime_start.quarter - 1) * 3 + 1, day=1)
        elif granularity_new == "M":
            relative_delta = relativedelta(days=7)
            n_boxes = 4
            if change == "zoomin":
                # Go back to next Monday
                datetime_start = datetime_start + relativedelta(weekday=MO(-1))
            elif change == "zoomout":
                # Coming from Week (D)
                # Normalize to a Monday (Should go to first Monday)
                datetime_start = datetime_start + relativedelta(weekday=MO(-1))
        elif granularity_new == "W":
            n_boxes = 7
            relative_delta = relativedelta(days=1)
            if change == "zoomout":
                # Coming from Day (6H)
                # Go back to next Monday (Could also go to beginning of day)
                datetime_start = datetime_start + relativedelta(weekday=MO(-1))
        elif granularity_new == "D":
            n_boxes = 4
            relative_delta = relativedelta(hours=6)
            if change == "zoomout":
                # Coming from 6H (H)
                # Go back to beginning of day (Could also go to nearest 6H block)
                datetime_start = datetime_start.normalize()
        elif granularity_new == "6H":
            # finest granularity H
            n_boxes = 6
            relative_delta = relativedelta(hours=1)

        # Grid
        # TODO Series?
        time_grid = list()
        time_l = datetime_start
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

        # Shift action
        if change == "earlier":
            for i in range(n_boxes):
                time_grid[i] = pd.Interval(
                    time_grid[i].left - relative_delta,
                    time_grid[i].right - relative_delta,
                    closed='left'
                )
        elif change == "later":
            for i in range(n_boxes):
                time_grid[i] = pd.Interval(
                    time_grid[i].left + relative_delta,
                    time_grid[i].right + relative_delta,
                    closed='left'
                )

        return granularity_new, time_grid, n_boxes

    @staticmethod
    def iterate_granularities(granularity, step):
        ix_granularity = granularities.index(granularity)
        len_granularity = len(granularities)
        ix_granularity_new = max(min(ix_granularity + step, len_granularity - 1), 0)
        return granularities[ix_granularity_new]
