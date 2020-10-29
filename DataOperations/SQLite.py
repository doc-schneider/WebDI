import sqlite3

from DataOperations.Event import EventTable
from DataOperations.Data import DataTableFactory
from DataOperations.Utilities import timestamplist_to_JSON, JSON_to_timestamplist

path_root = '//192.168.178.53/'

# Read EventTable from csv
event_file = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/' + 'EventListe.csv'
eventtable = EventTable(DataTableFactory.importFromCsv(event_file))
event_items = list(eventtable.data)

# Open database
conn = sqlite3.connect(path_root + 'Stefan/DigitalImmortality/Document and Event Tables/stefan.db')
c = conn.cursor()

# Python sqlite adapters
def adapt_timestamplist_to_JSON(lst):
    return timestamplist_to_JSON(lst)

def convert_JSON_to_timestamplist(data):
    return JSON_to_timestamplist(data)

sqlite3.register_adapter(list, adapt_timestamplist_to_JSON)
sqlite3.register_converter("json", convert_JSON_to_timestamplist)

# Create  table
#sqlite_items = sqlite_types(event_items)
# Cannot CREATE TABLE with substitution
#c.execute('''CREATE TABLE events (event_name text, parent_event text,
#                time_from text, time_to text, event_level integer)''')
#conn.commit()

# Get columns of table
sql = "select * from %s where 1=0;" % 'events'
c.execute(sql)
sqlite_cols = [d[0] for d in c.description]


# c.execute('''ALTER TABLE events ADD COLUMN event_time_from json''')

#lst = eventtable.data['EVENT_TIME_FROM'].iloc[14]
lst = ['a', 'b']
c.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", ('a','a','a','a',1,lst))
#conn.commit()


# Enter row to Event table
#time_from = dtm.datetime(2020,6,26,0,0,0).strftime('%d.%m.%Y %H:%M:%S')
#time_to = dtm.datetime(2020,6,26,23,59,59).strftime('%d.%m.%Y %H:%M:%S')
# TODO Use the ? tuple method
#c.execute("INSERT INTO events VALUES ('Urlaubstag Stefan', 'Stefans freier Tag für Projekte', '"
#          + time_from + "', '" + time_to + "', NULL)")
#conn.commit()

# See Event table
#for row in c.execute('SELECT * FROM events'):
#    print(row)

conn.close()