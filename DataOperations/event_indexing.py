from DataOperations.SQLite import SQLiteFactory

path_root = '//192.168.178.53/'


# Make table from csv
#event_file = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/' + \
#             'EventListe.csv'
#eventtable = EventTable(DataTableFactory.importFromCsv(event_file, encoding='ANSI'))


# Write a table into database
#SQLiteFactory.create_sqlite_table(eventtable,
#                                  '//192.168.178.53/Stefan/DigitalImmortality/Document and Event Tables/stefan.db',
#                                  'events')

# Read table from database
path = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
eventtable = SQLiteFactory.read_sqlite_table(path + 'stefan.db', 'events')


# Event extraction
#eventtable = EventFactory.extract_event_from_table(phototable)


# Append to global EventTable
# ..
