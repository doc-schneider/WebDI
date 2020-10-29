from pathlib import Path

from DataOperations.Data import DataTableFactory
from DataOperations.Event import EventTable, EventFactory


path_root = '//192.168.178.53/'

# Test: Loading an Event Table
event_file = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/' + \
           'EventListe.csv'
eventtable = EventTable(DataTableFactory.importFromCsv(event_file))

# Event extraction
#eventtable = EventFactory.extract_event_from_table(phototable)

# Append to global EventTable
# ..
