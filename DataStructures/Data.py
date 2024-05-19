import pandas as pd
import numpy as np
import datetime as dtm


class DataTable:
    def __init__(self, table):
        self.table = table

    def find_in_timeinterval(self, timeinterval):
        # Returns the index of all documents whose time_interval overlaps a requested time interval
        iix = (self.table["DATE_TIME"] >= timeinterval.left) & (self.table["DATE_TIME"] <= timeinterval.right)
        return DataTable(self.table[iix].reset_index(drop=True))
