from DataOperations.Data import DataTableFactory
from DataOperations.Document import DocumentTable
from DataOperations.iPhone import iPhoneFactory
from DataOperations.Photos import PhotoFactory
from DataOperations.SQLite import SQLiteFactory


path_root = '//192.168.178.53/'

# Make table from csv
#path = path_root + 'Stefan/Biographie/Stefan/iPhone/2020-12-28/'
#name = 'Konstanze Walther'
#iphonetable = iPhoneFactory.table_from_path(path, name)

# Make thumbnails
# TODO In the last run some error occurred
#PhotoFactory.table_thumbnails(iphonetable)

# Write to csv
#path = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
#filename = 'Dokumentliste_Konstanze SMS_iphone.csv'
#iphonetable.write_to_csv(path + filename)

# Read from csv table
#iphonetable = DocumentTable(DataTableFactory.importFromCsv(path + filename))

# Write a table into database
#SQLiteFactory.create_sqlite_table(iphonetable,
#                                  '//192.168.178.53/Stefan/DigitalImmortality/Document and Event Tables/stefan.db',
#                                  'iphone')

# Test: Read table from database
path = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
iphonetable = SQLiteFactory.read_sqlite_table(path + 'stefan.db', 'iphone')