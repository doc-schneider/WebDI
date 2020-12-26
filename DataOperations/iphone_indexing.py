from DataOperations.iPhone import iPhoneFactory
from DataOperations.SQLite import SQLiteFactory


path_root = '//192.168.178.53/'


path = path_root + 'Stefan/Biographie/Stefan/iPhone/2020-12-01/'
name = 'Konstanze Walther'
# Make table
iphonetable = iPhoneFactory.table_from_path(path, name)

#path_table = 'C:/Users/Stefan/Documents/DigitalImmortality/Document and Event Tables/'
#filename = 'Dokumentliste_Konstanze SMS_iphone'
#iphonetable.write_to_csv(path_table, filename)


# Write a table into database
SQLiteFactory.create_sqlite_table(iphonetable, 'stefan', 'iphone')