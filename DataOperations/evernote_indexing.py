from DataOperations import Evernote
import importlib
importlib.reload(Evernote)

# One path = one notebook.
category = 'todo'
descriptions = None
events = None    # Every notebook entry could be associated with an event (or events).
path_root = 'C:/Users/Stefan/Documents/Writings & Web/Evernote/2020-01'
path_note = 'Familie/Mamas Sachen'
# Make table
evernotetable = Evernote.EvernoteFactory.table_from_path(path_root, path_note, category, descriptions, events)
# Write Table
path_table = 'C:/Users/Stefan/Documents/DigitalImmortality/Document and Event Tables/'
filename = 'Dokumentliste_Mamas Sachen_Evernote'
evernotetable.write_to_csv(path_table, filename)


