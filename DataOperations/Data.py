import pandas as pd
import numpy as np
from io import StringIO
from io import open
import datetime as dtm

from DataOperations.Utilities import str_to_list, list_to_str, strio_to_list
from DataOperations.Azure import AzureFactory


class DataTable:

    def __init__(self, table):
        self.data = table
        self.length = len(table)

    def append(self, mastertable):
        self.data = mastertable.data.append(self.data, ignore_index=True)

    def timesort(self):
        self.data.sort_values(by=['TIME_FROM'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def add_time_to(self):
        # If no end time (but only start time) add current time (for graphics depiction).
        for i in range(self.length):
            if not np.isnat(self.data['TIME_FROM'].iloc[i].to_datetime64()) and \
                    np.isnat(self.data['TIME_TO'].iloc[i].to_datetime64()):
                self.data.at[i, 'TIME_TO'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_timeinterval(self):
        dummy = []
        for i in range(self.length):
            dummy.append(pd.Interval(self.data['TIME_FROM'].iloc[i],
                                     self.data['TIME_TO'].iloc[i], closed='both'))
        self.data['TIME_INTERVAL'] = dummy

    def find_in_timeinterval(self, timeinterval):
        # Returns the index of all documents whose time_interval overlaps a requested time interval
        iix = pd.IntervalIndex.from_arrays(self.data['TIME_FROM'], self.data['TIME_TO'], closed='both')
        return self.data.index[iix.overlaps(timeinterval)].to_list()

    def document_groups(self):
        # TODO Takes very long
        # Add an index column for groups
        self.data['GROUP_INDEX'] = None
        groups = list(self.data['DOCUMENT_GROUP'].unique())
        ix_group = 0
        for g in groups:
            self.data.loc[self.data['DOCUMENT_GROUP'] == g, 'GROUP_INDEX'] = ix_group
            ix_group += 1

    def write_to_csv(self, pathname):
        table = self.data.copy()
        # TODO Inefficent
        for i in range(table.shape[0]):
            for h in list(table.columns.values):
                # Convert list to str?
                if DataTableFactory.list_key(h):
                    table.at[i,h] = list_to_str(table[h].iloc[i])
                    #table.at[i, h] = textlist_to_JSON(table[h].iloc[i])
        table.to_csv(pathname, index=False, sep=';', date_format='%d.%m.%Y %H:%M:%S')


class DataTableFactory:

    # Importing data
    @staticmethod
    def importFromAzure(container_name, blob_name, environment):
        downloaded_blob = AzureFactory.download_blob_single(container_name, blob_name, environment)
        buf = StringIO(downloaded_blob.content_as_text())
        return DataTableFactory.importHelper(buf)

    @staticmethod
    def importFromCsv(filename, encoding='utf8'):
        # TODO: newline=None instead of '' removes last character. Why?
        with open(filename, 'r', newline='', encoding=encoding) as csvfile:
            return DataTableFactory.importHelper(csvfile)

    @staticmethod
    def importHelper(text):
        # Returns the headers or `None` if the input is empty
        # TODO Complicated code
        headers = strio_to_list(next(text, None))
        n_headers = len(headers)
        datatable = {}
        col_time = []         #  Note where the date time information is.
        for i in range(n_headers):
            datatable[headers[i]] = []
            if DataTableFactory.time_keys(headers[i]):
                col_time.append(i)
        for r in text:
            row = strio_to_list(r)
            for i in range(n_headers):
                if i in col_time:
                    # TODO Unify
                    if not DataTableFactory.list_key(headers[i]):
                        if row[i]:
                            # TODO Excel / csv standard formats clips the seconds -> Format csv
                            try:
                                datatable[headers[i]].append(pd.to_datetime(row[i], format='%d.%m.%Y %H:%M:%S'))
                            except:
                                datatable[headers[i]].append(pd.to_datetime(row[i], format='%d.%m.%Y %H:%M'))
                        else:
                            datatable[headers[i]].append(pd.NaT)
                    else:
                        datatable[headers[i]].append([pd.to_datetime(d, format='%d.%m.%Y %H:%M:%S') if d
                                                      else pd.NaT
                                                      for d in str_to_list(row[i])])
                else:
                    if DataTableFactory.int_keys(headers[i]):
                        datatable[headers[i]].append(np.int(row[i]))
                    elif DataTableFactory.list_key(headers[i]):
                        datatable[headers[i]].append(str_to_list(row[i]))
                        #datatable[headers[i]].append(JSON_to_textlist(row[i]))
                    else:          # str. Can be empty.
                        datatable[headers[i]].append(row[i])
        df = pd.DataFrame(datatable)
        return df

    # Data types
    @staticmethod
    def list_key(column_name):
        # Datatable columns that are defined as list
        return column_name in ['DESCRIPTION', 'PARENT_DESCRIPTION', 'CATEGORY', 'PARENT_CATEGORY',
                               'EVENT_TIME_FROM', 'EVENT_TIME_TO',
                               'DOCUMENT_TABLE', 'DOCUMENT_TYPE', 'VIEW_TYPE', 'TAG']

    @staticmethod
    def time_keys(column_name):
        # Headers standing for date time information
        return column_name in ['TIME_FROM', 'TIME_TO', 'EVENT_TIME_FROM', 'EVENT_TIME_TO', 'DATE_BIRTH']

    @staticmethod
    def int_keys(column_name):
        # Integer information
        return column_name in ['EVENT_LEVEL']

    @staticmethod
    def key_types(value, column_name):
        # All allowed column names of DataTable and their types
        if column_name in ['TIME_FROM', 'TIME_TO']:
            # TODO: Timestpam? Chekc correct forma?
            result = isinstance(value, dtm.datetime)
        elif column_name in ['DESCRIPTION', 'CATEGORY']:
            # List of strings
            result = isinstance(value[0], str)  # Check first element only.
        # else:
            # error column is not allowed
        return result

