import sqlite3
import datetime as dtm
import pandas as pd
import numpy as np

from DataOperations import iPhone
from DataOperations.Utilities import textlist_to_JSON, JSON_to_textlist


path_root = '//192.168.178.53/'


path = path_root + 'Stefan/Biographie/Stefan/iPhone/2020-12-01/'
name = 'Konstanze Walther'
# Make table
iphonetable = iPhone.iPhoneFactory.table_from_path(path, name)
#path_table = 'C:/Users/Stefan/Documents/DigitalImmortality/Document and Event Tables/'
#filename = 'Dokumentliste_Konstanze SMS_iphone'
#iphonetable.write_to_csv(path_table, filename)


# Write into sqlite database
# - TODO Mapping column name - type (adapters)
# - TODO utf8 problem when writing to database or back?

# Adapters and converters
sqlite3.register_adapter(list, textlist_to_JSON)
sqlite3.register_converter("json", JSON_to_textlist)

# Open database
conn = sqlite3.connect(path_root + 'Stefan/DigitalImmortality/Document and Event Tables/stefan.db',
                       detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()

# Define columns
table_columns = list(iphonetable.data)

# Doping  table if already exists
c.execute("DROP TABLE test")

# Create table
c.execute('''CREATE TABLE test
             (TIME_FROM timestamp, PATH text, DESCRIPTION json)''')

ix = 0
description = iphonetable.data['DESCRIPTION'].iloc[ix]
time_from = iphonetable.data['TIME_FROM'].iloc[ix].to_pydatetime()
pth = iphonetable.data['PATH'].iloc[ix]

# Insert a row of data
c.execute("INSERT INTO test VALUES (?,?,?)", (time_from, pth, description))

c.execute('SELECT * FROM test')
row = c.fetchone()

conn.commit()
conn.close()



# Get columns of table
sql = "select * from %s where 1=0;" % 'events'
c.execute(sql)
sqlite_cols = [d[0] for d in c.description]

# c.execute('''ALTER TABLE events ADD COLUMN event_time_from json''')

#lst = eventtable.data['EVENT_TIME_FROM'].iloc[14]
lst = ['a', 'b']
c.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", ('a','a','a','a',1,lst))

