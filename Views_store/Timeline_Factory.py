import pandas as pd
from dateutil.relativedelta import relativedelta, MO, SU


# Timeline utilities
class TimelineFactory:

    # Returns time interval and number of boxes
    # - change: earlier, later, zoomin, zoomout
    # - If no "change" is indicated it returns number of boxes and box boundaries
    @staticmethod
    def timegrid(time_interval, granularity=None, change=None, time_grid=None):
        #TODO
        # - 50 Y granulairty, fine granularity
        # - List for cycling through granularities

        # Find a starting granularity (and time_interval) from raw data
        if granularity is None:
            if time_interval.left.year < time_interval.right.year:
                granularity = "10Y"
                relative_delta = relativedelta(years=10)
            else:
                granularity = "Y"
                relative_delta = relativedelta(years=1)
            time_interval = pd.Interval(
                pd.Timestamp(time_interval.left.year, 1, 1),
                pd.Timestamp(time_interval.left.year, 1, 1) + relative_delta, closed="left"
            )

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

