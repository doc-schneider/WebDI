import pandas as pd
import numpy as np
import datetime as dtm

from DataStructures.TableTypes import table_types


class DataTable:
    def __init__(self, table, table_type=None):
        self.table = table
        self.table_type = table_type

    # Add the Table Type specific Primary Key as a column if not existing. Use integer index
    def add_primary_key(self):
        if self.table_type is None:
            pass  # TODO Throw error
        else:
            id_name = table_types[self.table_type.name]["PrimaryKey"]
            if id_name in self.table.columns:
                pass  # TODO Throw error
            else:
                # TODO Check if index is ordered normally
                self.table[id_name] = self.table.index + 1  # Primary ID shoudl start with 1

    # Create a dummy value table with correct types. Required for Dash interface
    def create_dummy_table(self, n_rows):
        column_primary = table_types[self.table_type.name]["PrimaryKey"]
        if "ForeignKey" in table_types[self.table_type.name].keys():
            column_foreign = table_types[self.table_type.name]["ForeignKey"]
        else:
            column_foreign = None
        types = [v["mysqltype"] for (k, v) in table_types[self.table_type.name]["Columns"].items()]
        columns = list(table_types[self.table_type.name]["Columns"].keys())
        self.table = pd.DataFrame(
            columns=[column_primary] + columns + [column_foreign]
        )
        self.table[column_primary] = np.arange(1, n_rows+1)
        self.table[column_foreign] = np.arange(1, n_rows+1)
        for t, c in zip(types, columns):
            if t == "text":
                self.table[c] = "text"
            elif t == "datetime":
                self.table[c] = dtm.datetime(2000, 1, 1, 1, 1, 1)
            elif t == "integer":
                self.table[c] = 1


    def timesort(self):
        self.data.sort_values(by=['TIME_FROM'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def datetimesort(self):
        self.data.sort_values(by=['DATETIME'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def add_timefromto(self, timedelta):
        self.data["TIME_FROM"] = self.data["DATETIME"]
        self.add_timedelta(timedelta)

    def add_timedelta(self, timedelta):
        self.data["TIME_TO"] = self.data["TIME_FROM"].apply(lambda x: x + timedelta)

    def find_in_timeinterval(self, timeinterval):
        if "TIME_FROM" in self.data.columns:
            # Returns the index of all documents whose time_interval overlaps a requested time interval
            iix = pd.IntervalIndex.from_arrays(self.data['TIME_FROM'], self.data['TIME_TO'], closed='both')
            return self.data.index[iix.overlaps(timeinterval)].to_list(), DataTable(self.data[iix])
        elif "DATETIME" in self.data.columns:
            iix = (self.data["DATETIME"] >= timeinterval.left) & (self.data["DATETIME"] <= timeinterval.right)
            return self.data.index[iix].to_list(), DataTable(self.data[iix])

    def document_groups(self):
        # TODO Takes very long
        # Add an index column for groups
        self.data['GROUP_INDEX'] = None
        groups = list(self.data['DOCUMENT_GROUP'].unique())
        ix_group = 0
        for g in groups:
            self.data.loc[self.data['DOCUMENT_GROUP'] == g, 'GROUP_INDEX'] = ix_group
            ix_group += 1

    def to_csv(self, pathname, tablename):
        self.data.to_csv(
            pathname + tablename + '.csv',
            index=False,
            sep=';',
            date_format='%d.%m.%Y %H:%M:%S',
            encoding='ANSI'
        )
