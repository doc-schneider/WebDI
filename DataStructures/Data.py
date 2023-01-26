import pandas as pd
import numpy as np
from io import StringIO
from io import open
import datetime as dtm

from DataOperations.Utilities import str_to_list, list_to_str, strio_to_list
from DataOperations.Azure import AzureFactory
from DataStructures.TableTypes import column_types_table


class DataTable:

    def __init__(self, table, document_category=None, table_name=None):
        self.data = table
        self.length = len(table)
        self.document_category = document_category
        self.table_name = table_name
        # Keep individual name?
        if table_name is not None:
            self.data["TABLE_NAME"] = table_name

    def append(self, mastertable):
        self.data = mastertable.data.append(self.data, ignore_index=True)

    # Remove columns not defined
    def format_to_category(self, optional_columns):
        cols = set(self.data.columns)
        cols_standard = column_types_table(
            self.document_category,
            optional_columns,
            remove_primarykey=True,
            return_aliasnames=True
        )
        self.data.drop(columns=list(cols - set(cols_standard)), inplace=True)

    def timesort(self):
        self.data.sort_values(by=['TIME_FROM'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def datetimesort(self):
        self.data.sort_values(by=['DATETIME'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    #def add_time_to(self):
    #    # If no end time (but only start time) add current time (for graphics depiction).
    #    for i in range(self.length):
    #        if not np.isnat(self.data['TIME_FROM'].iloc[i].to_datetime64()) and \
    #                np.isnat(self.data['TIME_TO'].iloc[i].to_datetime64()):
    #            self.data.at[i, 'TIME_TO'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    # TODO Remove ?
    #def replace_NaT(self):
    #    # Default: Replace by now
    #    ix = self.data['TIME_TO'].apply(lambda x: not isinstance(x, pd.Timestamp))
    #    self.data.loc[ix, 'TIME_TO'] = pd.Timestamp.now()

    def add_timefromto(self, timedelta):
        self.data["TIME_FROM"] = self.data["DATETIME"]
        self.add_timedelta(timedelta)

    def add_timedelta(self, timedelta):
        self.data["TIME_TO"] = self.data["TIME_FROM"].apply(lambda x: x + timedelta)

    def find_in_timeinterval(self, timeinterval):
        if "TIME_FROM" in self.data.columns:
            # Returns the index of all documents whose time_interval overlaps a requested time interval
            iix = pd.IntervalIndex.from_arrays(self.data['TIME_FROM'], self.data['TIME_TO'], closed='both')
            return self.data.index[iix.overlaps(timeinterval)].to_list()
        elif "DATETIME" in self.data.columns:
            iix = (self.data["DATETIME"] >= timeinterval.left) & (self.data["DATETIME"] <= timeinterval.right)
            return self.data.index[iix].to_list()

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


class DataTableFactory:

    # Importing data
    @staticmethod
    def from_csv(file, parse_date=[]):
        table = pd.read_csv(
            file,
            encoding='ANSI',
            sep=';',
            parse_dates=parse_date,
            dayfirst=True
        )
        table = table.where(pd.notnull(table), None)
        return table

    @staticmethod
    def importFromAzure(container_name, blob_name, environment):
        downloaded_blob = AzureFactory.download_blob_single(container_name, blob_name, environment)
        buf = StringIO(downloaded_blob.content_as_text())
        return DataTableFactory.importHelper(buf)

    # @staticmethod
    # def importFromCsv(filename, encoding='utf8'):
    #     # TODO: newline=None instead of '' removes last character. Why?
    #     with open(filename, 'r', newline='', encoding=encoding) as csvfile:
    #         return DataTableFactory.importHelper(csvfile)

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
                        if row[i]:
                            datatable[headers[i]].append(np.int(row[i]))
                        else:
                            datatable[headers[i]].append(None)
                    elif DataTableFactory.list_key(headers[i]):
                        datatable[headers[i]].append(str_to_list(row[i]))
                    else:          # str. Can be empty.
                        datatable[headers[i]].append(row[i])
        df = pd.DataFrame(datatable)
        return df

    # Data types
    # If not specified type is str
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

