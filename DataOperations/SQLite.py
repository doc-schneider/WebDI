import sqlite3
import datetime as dtm
import pandas as pd
import numpy as np
import json

from DataOperations.Utilities import textlist_to_JSON, JSON_to_textlist,\
    timelist_to_JSON, JSON_to_timelist
from DataOperations.Document import DocumentTable


# TODO Can use this instead of DataTable
# class SQLiteTable:
#


class SQLiteFactory:

    @staticmethod
    def create_sqlite_table(datatable, database_name, table_name):

        table_columns = list(datatable.data)
        n_columns = len(table_columns)

        # Convert to types understandable for SQlite
        for c in table_columns:
            if SQLiteFactory.map_keytypes(c) == 'json_str':
                datatable.data[c] = datatable.data[c].apply(TextList)
            elif SQLiteFactory.map_keytypes(c) == 'time':
                datatable.data[c] = datatable.data[c].apply(Time)
            elif SQLiteFactory.map_keytypes(c) == 'json_time':
                datatable.data[c] = datatable.data[c].apply(TimeList)

        # Adapters and converters
        sqlite3.register_adapter(TextList, adapt_textlist)
        sqlite3.register_converter("json_str", convert_textlist)
        sqlite3.register_adapter(Time, adapt_time)
        sqlite3.register_converter("time", convert_time)
        sqlite3.register_adapter(TimeList, adapt_timelist)
        sqlite3.register_converter("json_time", convert_timelist)

        # Open database
        conn = sqlite3.connect(database_name,
                               detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()

        # Remove old table if exists.
        c.execute("drop table if exists %s" % table_name)

        # Create table
        query = "CREATE TABLE " + table_name + " (" + table_columns[0] + " " + \
                SQLiteFactory.map_keytypes(table_columns[0])
        for tc in table_columns[1:]:
            query += "," + tc + " " + SQLiteFactory.map_keytypes(tc)
        query += ")"
        c.execute(query)

        # Insert rows
        query = "INSERT INTO " + table_name + " VALUES (?" + ''.join(',?' for i in range(n_columns-1)) + ')'
        for _, row in datatable.data.iterrows():
            # Convert timestamp to datetime
            c.execute(query, tuple(row))

        conn.commit()
        conn.close()

    @staticmethod
    def read_sqlite_table(database_name, table_name):

        # Adapters and converters
        # TODO Put into method
        sqlite3.register_adapter(TextList, adapt_textlist)
        sqlite3.register_converter("json_str", convert_textlist)
        sqlite3.register_adapter(Time, adapt_time)
        sqlite3.register_converter("time", convert_time)
        sqlite3.register_adapter(TimeList, adapt_timelist)
        sqlite3.register_converter("json_time", convert_timelist)

        # Open database
        conn = sqlite3.connect(database_name,
                               detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()

        # Get table description that is in the cursor object
        sql = "select * from %s;" % table_name
        c.execute(sql)
        table_columns = [d[0] for d in c.description]
        # TODO Shouldn't the table name appear here?
        df = pd.DataFrame.from_records(data=c.fetchall(), columns=table_columns)

        # Re-convert to types
        table_columns = list(df)
        for c in table_columns:
            if SQLiteFactory.map_keytypes(c) == 'json_str':
                df[c] = df[c].apply(adapt_textlist).apply(JSON_to_textlist)
            elif SQLiteFactory.map_keytypes(c) == 'time':
                df[c] = df[c].apply(adapt_time).apply(
                    lambda x: pd.NaT if x == 'NaT' else pd.to_datetime(x)
                )
            elif SQLiteFactory.map_keytypes(c) == 'json_time':
                df[c] = df[c].apply(adapt_timelist).apply(JSON_to_timelist)

        return DocumentTable(df)

    @staticmethod
    def add_column(database_name, table_name, column_name, df):

        # TODO Adapters and converters

        conn = sqlite3.connect(database_name,
                               detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()

        # TODO: Should insert column_name with ?, but doesn't work for me.
        sql = "ALTER TABLE %s ADD COLUMN %s %s;" \
              % (table_name, column_name, SQLiteFactory.map_keytypes(column_name))
        c.execute(sql)
        conn.commit()

        for i in range(1, df.data.shape[0]+1):
            df.data[column_name].iloc[i-1]
            c.execute("""UPDATE {} SET {}=? WHERE ROWID = ?""".format(table_name, column_name),
                        (int(df.data[column_name].iloc[i-1]), int(i)))
        conn.commit()
        conn.close()

    @staticmethod
    def map_keytypes(column_name):
        if column_name in ['TIME_FROM', 'TIME_TO']:
            return 'time'
        if column_name in ['DESCRIPTION', 'CATEGORY', 'DOCUMENT_TYPE']:
            return 'json_str'
        if column_name in ['EVENT_TIME_FROM', 'EVENT_TIME_TO']:
            return 'json_time'
        if column_name in ['GROUP_INDEX', 'EVENT_LEVEL']:
            return 'integer'
        else:
            return 'text'  # Default
        #['DOCUMENT_GROUP', 'EVENT', 'PATH', 'DOCUMENT_NAME', 'EVENT_NAME']:


# TODO: Do I need __repr__ ?
class TextList:
    def __init__(self, textlist):
        self.textlist = textlist

    def __repr__(self):
        return json.dumps(self.textlist)

def adapt_textlist(textlist):
    return json.dumps(textlist.textlist)

def convert_textlist(jsn):
    return TextList(json.loads(jsn))


# TODO: If-else makes it slow?
class Time:
    def __init__(self, time):
        self.time = time

    def __repr__(self):
        if isinstance(self.time, pd.Timestamp):
            lstr = self.time.strftime('%d.%m.%Y %H:%M:%S')
        else:
            lstr = 'NaT'
        return lstr

def adapt_time(time):
    if isinstance(time.time, pd.Timestamp):
        lstr = time.time.strftime('%d.%m.%Y %H:%M:%S')
    else:
        lstr = 'NaT'
    return lstr

def convert_time(strg):
    strg = strg.decode()
    if strg == 'NaT':
        return Time(pd.NaT)
    else:
        return Time(pd.to_datetime(strg))

class TimeList:
    def __init__(self, timelist):
        self.timelist = timelist

    def __repr__(self):
        lstr = [l.strftime('%d.%m.%Y %H:%M:%S') if isinstance(l, pd.Timestamp) else
                'NaT' for l in self.timelist]
        return json.dumps(lstr)

def adapt_timelist(timelist):
    lstr = [l.strftime('%d.%m.%Y %H:%M:%S') if isinstance(l, pd.Timestamp) else
            'NaT' for l in timelist.timelist]
    return json.dumps(lstr)

def convert_timelist(jsn):
    return TimeList([pd.NaT if d=='NaT' else pd.to_datetime(d) for d in json.loads(jsn)])
