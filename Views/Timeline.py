import numpy as np
import pandas as pd

from Views.Timeline_Factory import TimelineFactory
from Views.View_Factory import ViewFactory


class TimelineViewer():
    def __init__(self, datatable_initial):
        # Get max interval from table to initialise
        self.granularity, self.time_grid, self.n_grid = TimelineFactory.timegrid(
            pd.Interval(datatable_initial.table["DATE_TIME"].min(), datatable_initial.table["DATE_TIME"].max(), closed="left")
        )
        self.datatable = None  # Clipped table
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
        # Timeline
        time_grid = [
            self.time_grid['TIME_INTERVAL'].loc[i].left for i in range(self.n_grid)
        ]
        # Boxes
        boxes = ViewFactory.view(self.datatable)
        boxes["boxes_grid"] = self.datatable.table["DATE_TIME"]
        #
        return {
            "time_interval": pd.Interval(
                self.time_grid.loc[0, "TIME_INTERVAL"].left,
                self.time_grid.iloc[-1]["TIME_INTERVAL"].right,
                closed='left'
            ),
            "n_grid": self.n_grid,
            'time_grid': time_grid,
            "n_boxes": len(boxes["boxes_grid"]),
            "boxes_grid": boxes["boxes_grid"],
            "title_boxes": boxes["title_boxes"],
            "description_boxes": boxes["description_boxes"]
        }
