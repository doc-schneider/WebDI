import numpy as np
import pandas as pd
from pathlib import Path
from dateutil.relativedelta import relativedelta, MO, SU

from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory


granularities = ["10Y", "Y", "Q", "M", "W", "D", "6H"]

class TimelineViewer():
    def __init__(self, datatable_initial, message_collection, message_view):
        self.datatable = None
        self.datatable_show = None
        self.table_type = datatable_initial.table_type

        # Which out of the total collection?
        id_collection = message_collection['ID_MESSAGE_COLLECTION']
        self.datatable = datatable_initial.match_foreignkey(id_collection)
        self.datatable.sort()

        # TODO Pre-processing ATTACHMENT

        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            pd.Timestamp(message_view["DATETIME_START"]), granularity=message_view["GRANULARITY"], change=None,
        )

        self.update()

    def update(self):
        # TODO Marks for all Message time points

        # Get the first entry for each time box (if it exists, else nan)
        self.datatable_show = pd.DataFrame(columns=self.datatable.table.columns)
        for i in range(self.n_grid):
            t = self.datatable.find_in_timeinterval(self.time_grid[i]).table
            if t.shape[0] == 0:
                self.datatable_show.loc[i, :] = None  # np.nan
            else:
                self.datatable_show.loc[i, :] = t.iloc[[0]].values
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
        self.datatable_show.table["FILE_NAME"] = None
        self.datatable_show.table["PATH"] = None
        self.datatable_show.table["FILE_FORMAT"] = None
        for i in range(len(self.datatable_show.table)):
            if self.datatable_show.table.loc[i, "ATTACHMENT"]:
                file_pth = Path(self.datatable_show.table.loc[i, "ATTACHMENT"])
                self.datatable_show.table.loc[i, "FILE_NAME"] = file_pth.name
                self.datatable_show.table.loc[i, "PATH"] = file_pth.parent
                self.datatable_show.table.loc[i, "FILE_FORMAT"] = file_pth.suffix[1:].upper()

        # Raw content
        dct = ViewFactory.view(self.datatable_show)

        dct["TIME_GRID"] = pd.Series([t.left for t in self.time_grid])

        # Dimension information for viewing  # TODO Should be in pages and config
        dct["N_BOXES"] = self.n_grid

        return dct

# Timeline utilities
class TimelineFactory:

    # Returns time interval and number of boxes
    # - change: earlier, later, zoomin, zoomout
    # - If no "change" is indicated it returns number of boxes and box boundaries
    @staticmethod
    def timegrid(datetime_start, granularity, change=None):
        #TODO  50 Y granulairty, fine granularity

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
