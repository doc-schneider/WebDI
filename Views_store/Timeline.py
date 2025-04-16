import pandas as pd

from Views_store.Timeline_Factory import TimelineFactory
from Views.View_Factory import ViewFactory


class TimelineViewer():
    def __init__(self, datatable_initial):
        # Get max interval from table to initialise
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            pd.Interval(datatable_initial.table["DATE_TIME"].min(), datatable_initial.table["DATE_TIME"].max(), closed="left")
        )
        self.datatable = None  # Clipped table
        self.table_type = datatable_initial.table_type
        self.update(datatable_initial)

    def update(self, datatable):
        # Time filtering documents
        self.datatable = datatable.find_in_timeinterval(
            pd.Interval(
                self.time_grid.loc[0, "TIME_INTERVAL"].left,
                self.time_grid.iloc[-1]["TIME_INTERVAL"].right,
                closed='left'
            )
        )

    def earlier(self, datatable):
        # Shift one block
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            None,
            self.granularity,
            change="earlier",
            time_grid=self.time_grid
        )
        self.update(datatable)

    def later(self, datatable):
        # Shift one block
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            None,
            self.granularity,
            change="later",
            time_grid=self.time_grid
        )
        self.update(datatable)

    def zoom_in(self, datatable):
        # Zoom into left-most block
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            None,
            self.granularity,
            change="zoomin",
            time_grid=self.time_grid
        )
        self.update(datatable)

    def zoom_out(self, datatable):
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            None,
            self.granularity,
            change="zoomout",
            time_grid=self.time_grid
        )
        self.update(datatable)

    def view(self):
        # Content
        boxes = ViewFactory.view(self.datatable, view_mode="TIMELINE")
        # Timeline
        boxes["N_BOXES"] = len(boxes["DATE_TIME"])
        boxes["TIME_GRID"] = [
            self.time_grid['TIME_INTERVAL'].loc[i].left for i in range(self.n_grid)
        ]
        boxes["TIME_INTERVAL"] = pd.Interval(
            self.time_grid.loc[0, "TIME_INTERVAL"].left,
            self.time_grid.iloc[-1]["TIME_INTERVAL"].right,
            closed='left'
        )
        boxes["N_GRID"] = self.n_grid
        return boxes
