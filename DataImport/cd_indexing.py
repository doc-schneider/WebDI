from DataStructures.Data import DataTableFactory
from DataOperations.Music import MusicFactory


path_root = '//192.168.178.53/'

# pre-description
path_pre = path_root + 'Musik/H-J Schneider/MeinCembalo/' + 'PreDokumentliste_Cembalomusik Papa_cd.csv'
pretable = DataTableFactory.importFromCsv(path_pre)
# Main table.
path_main = path_root + 'Musik/H-J Schneider/MeinCembalo/'
cdtable = MusicFactory.cd_from_path(path_main, pretable, ['PreDokumentliste_Cembalomusik Papa_cd.csv'])

path_master = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/' + \
              'Dokumentliste_Cembalomusik Papa_cd.csv'
# Append to mastertable
mastertable = DataTableFactory.importFromCsv(path_master)
cdtable.append(mastertable)

# Write new Mastertable
#cdtable.write_to_csv(path_master)
