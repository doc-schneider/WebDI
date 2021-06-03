from DataOperations.Photos import PhotoFactory
from DataOperations.Data import DataTableFactory
from DataOperations.Document import DocumentTable
from DataOperations.Event import EventFactory
from DataOperations.SQLite import SQLiteFactory


path_root = '//192.168.0.117/'

# Pre-description
#path_pre = path_root + 'Fotos/2020/2020_06_11_Schloss Dyck/' + 'PreDokumentliste.csv'
#pretable = DocumentTable(DataTableFactory.importFromCsv(path_pre, encoding='ANSI'))

# Main table
#path_photo = path_root + 'Fotos/2020/2020_06_11_Schloss Dyck/'
#phototable = PhotoFactory.table_from_folder(path_photo, pretable)

# Event extraction
#eventtable = EventFactory.extract_event_from_table(phototable)
# TODO: Append to global EventTable

# Write Tables
path_table = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
filename = 'Dokumentliste_2020_06_11_Schloss Dyck_photo.csv'
#phototable.write_to_csv(path_table + filename)

# Generate a thumbnail
#PhotoFactory.make_thumbnail(path_root + '/' + 'Musik/H-J Schneider/MeinCembalo', 'MeinCembalo.JPG', 'JPG')

# Read csv table
# phototable = DocumentTable(DataTableFactory.importFromCsv(path_table + filename, encoding='ANSI'))

# Write a table into database
#SQLiteFactory.create_sqlite_table(phototable,
#                                  '//192.168.0.117/Stefan/DigitalImmortality/Document and Event Tables/stefan.db',
#                                  'photo')

#  Read table from database
phototable = SQLiteFactory.read_sqlite_table(path_table + 'stefan.db', 'photo')
