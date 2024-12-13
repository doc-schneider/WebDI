import pandas as pd
import numpy as np

from DataStructures.TableTypes import TableType
from Views.View_Factory import ViewFactory


class CollectionViewer():
    def __init__(self, datatable_initial, filter_table=None):
        self.datatable = datatable_initial.filter(filter_table)
        self.table_type = datatable_initial.table_type
        self.collection = {
            "N_ELEMENTS":  self.datatable.table.shape[0]
        }

    def sort(self, column=None):
        if column:
            self.datatable.sort(column)
        else:
            if self.table_type == TableType.ALBUM or self.table_type == TableType.NOTEBOOK:
                self.datatable.sort("DATE_FROM")
            elif self.table_type == TableType.NOTE:
                self.datatable.sort("DATE_TIME")

    def view(self):
        # Raw content
        boxes = ViewFactory.view(self.datatable, view_mode="COLLECTION")
        if self.table_type == TableType.ALBUM:
            boxes['DATE_TIME_0'] = boxes.pop('DATE_FROM')
            boxes['DATE_TIME_1'] = boxes.pop('DATE_TO')
            boxes['TITLE'] = boxes.pop('PHOTO_ALBUM')
            boxes['TEXT'] = boxes.pop('DESCRIPTION')
        elif self.table_type == TableType.NOTEBOOK:
            boxes['DATE_TIME_0'] = boxes.pop('DATE_FROM')
            boxes['DATE_TIME_1'] = boxes.pop('DATE_TO')
            boxes['TITLE'] = boxes.pop('NOTEBOOK')
            boxes['TEXT'] = boxes.pop('NOTEBOOK_COLLECTION')
        elif self.table_type == TableType.NOTE:
            boxes['DATE_TIME_0'] = boxes.pop('DATE_TIME')
            boxes['DATE_TIME_1'] = boxes.pop('DATE_TIME')
            boxes['TITLE'] = boxes.pop('TITLE')
            boxes['TEXT'] = boxes.pop('NOTEBOOK')
        return boxes
