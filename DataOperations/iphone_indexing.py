from DataOperations import iPhone
import importlib
importlib.reload(iPhone)


path_root = '//192.168.178.53/Stefan/Biographie/Stefan/iPhone/2020-02-23/SMS/'
name = 'Konstanze Walther'
# Make table
iphonetable = iPhone.iPhoneFactory.table_from_path(path_root, name)

path_table = 'C:/Users/Stefan/Documents/DigitalImmortality/Document and Event Tables/'
filename = 'Dokumentliste_Konstanze SMS_iphone'
iphonetable.write_to_csv(path_table, filename)
