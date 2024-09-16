import pandas as pd
import numpy as np

from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory


class CollectionViewer():
    def __init__(self, datatable_initial, filter_table):
        self.datatable = datatable_initial.filter(filter_table)
        self.table_type = datatable_initial.table_type
        self.collection = {
            "N_ELEMENTS":  self.datatable.table.shape[0]
        }

    def sort(self, column):
        self.datatable.sort(column)

    def view(self):
        # Raw content
        boxes = ViewFactory.view(self.datatable, view_mode="COLLECTION")

        return boxes
