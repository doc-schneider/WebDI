import sqlite3
import datetime as dtm
import pandas as pd
import numpy as np
import json


#class SQLiteTable:
#

class SQLiteFactory:

    @staticmethod
    def create_sqlite_table(datatable, database_name, table_name):

        # Adapters and converters
        # TODO Need different list-derived types
        sqlite3.register_adapter(list, textlist_to_JSON)
        sqlite3.register_converter("json_str", JSON_to_textlist)

        # Open database
        conn = sqlite3.connect('//192.168.178.53/Stefan/DigitalImmortality/Document and Event Tables/' +
                               database_name + '.db',
                               detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()

        # Remove old table if exists.
        c.execute("drop table if exists %s" % table_name)

        # Define columns
        table_columns = list(datatable.data)
        n_columns = len(table_columns)

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
            c.execute(query, tuple([x.to_pydatetime() if isinstance(x, pd.Timestamp) else x
                                    for x in row]))

        conn.commit()
        conn.close()

        #def read_sqlite_table
        #    # Check
        #    c.execute('SELECT * FROM ' + table_name)
        #    row = c.fetchone()
    #
    #        # Get columns of table
    #        sql = "select * from %s where 1=0;" % 'events'
    #        c.execute(sql)
     #       sqlite_cols = [d[0] for d in c.description]

    @staticmethod
    def map_keytypes(column_name):
        if column_name in ['TIME_FROM', 'TIME_TO']:
            return 'timestamp'
        if column_name in ['DESCRIPTION', 'CATEGORY', 'DOCUMENT_TYPE']:
            return 'json_str'
        if column_name in ['DOCUMENT_GROUP', 'EVENT', 'PATH', 'DOCUMENT_NAME']:
            return 'text'


def textlist_to_JSON(lst):
    # TODO text converted into strange format.
    return json.dumps(lst)

def JSON_to_textlist(jsn):
    return json.loads(jsn)

#def timestamplist_to_JSON(lst):
#    lstr = [l.strftime('%d.%m.%Y %H:%M:%S') for l in lst]
#    return json.dumps(lstr)  #.encode('utf8')
#
#def JSON_to_timestamplist(data):
#    return [pd.to_datetime(d) for d in json.loads(data)]  #.decode('utf8')

