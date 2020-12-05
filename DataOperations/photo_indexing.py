from pathlib import Path
from DataOperations.Photos import PhotoFactory
from DataOperations.Data import DataTableFactory
from DataOperations.Document import DocumentTable
from DataOperations.Event import EventFactory


path_root = '//192.168.178.53/'


# Pre-description
path_pre = path_root + 'Fotos/2020/2020_11_23_Stefan Urlaubstag/' + 'PreDokumentliste.csv'
pretable = DocumentTable(DataTableFactory.importFromCsv(path_pre))

# Main table
path_photo = Path(path_root + 'Fotos/2020/2020_11_23_Stefan Urlaubstag/')
phototable = PhotoFactory.table_from_folder(path_photo, pretable)

# Event extraction
#eventtable = EventFactory.extract_event_from_table(phototable)
# TODO: Append to global EventTable

# Write Tables
path_table = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
filename = 'Dokumentliste_2020_11_23_Stefan Urlaubstag_photo.csv'
#phototable.write_to_csv(path_table + filename)


# Generate a thumbnail
#PhotoFactory.make_thumbnail(path_root + '/' + 'Musik/H-J Schneider/MeinCembalo', 'MeinCembalo.JPG', 'JPG')
