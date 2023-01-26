from sqlalchemy import create_engine

from DataStructures.TableTypes import find_optional_columns
from DataStructures.Document import DocumentTableFactory
from DataOperations.Music import MusicFactory
from DataOperations.TableOperations import make_metatable, update_metatable
from DataOperations.MySQL import (
    create_specific_table,
    insert_specific_dataframe,
    read_specific_dataframe
)


make_cdtable_fromfolder = False
exist_pretable = False
write_csv = False
read_csv = False
create_cdtable_mysql = False
insert_cdtable_mysql = False
read_cdtable_mysql = False

path_root = 'X:/'
path_cd = 'H-J Schneider/'
folder_cd = "MeinCembalo"
path_full = path_root + path_cd + folder_cd + "/"
mysql_table = "music_" + folder_cd.replace(" ", "_")

optional_columns = []

update_meta_table = True
exists_meta_table = False

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

# Pre-description
# TODO Document_Group is read as float (only if None present)
if exist_pretable:
    pretable = DocumentTableFactory.from_csv(
        "music",
        path_full,
        'PreDokumentliste'
    )
    pretable.format_to_category(optional_columns)
else:
    pretable = None

# Main table
if make_cdtable_fromfolder:
    musictable = MusicFactory.cd_from_path(
        path_root + path_cd,
        folder_cd,
        pretable=pretable
    )

# Write Tables
if write_csv:
    musictable.to_csv(path_full, mysql_table)

if create_cdtable_mysql:
    create_specific_table(
        db_connection,
        mysql_table,
        "music",
        find_optional_columns(musictable.data, "music")
    )

if insert_cdtable_mysql:
    insert_specific_dataframe(
        db_connection,
        mysql_table,
        "music",
        musictable.data,
        find_optional_columns(musictable.data, "music"),
    )

# Metatable
update_metatable(True, db_connection, "musics", "music")
