from DataOperations.SQLite import SQLiteFactory


path_root = '//192.168.178.53/'

path = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/'
iphonetable = SQLiteFactory.read_sqlite_table(path + 'stefan.db', 'iphone')

# Add column GROUP_INDEX
iphonetable.document_groups()

# Add column to sql table
SQLiteFactory.add_column(path + 'stefan.db', 'iphone', 'GROUP_INDEX', iphonetable)