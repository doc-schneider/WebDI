from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

from DataOperations.MySQL import write_table

"""
Finds all folders in a root folder.
- Folders can be bottom level, ie, containing a photo collection and no further sub-folders
- Folders can be meta-collections, ie, contain sub-forders (eg, "best of") and a photo collection.
All folders with their attributes are written into a table (csv, mysql)

Creates: 
- Dataframe 
"""

# TODO
#  - Album type information

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "stefan"
write_csv = True
write_mysql = True
path_root = Path('Z:/Bilder/')
name_root = "Stefans Fotoarchiv"

# TODO Can read these from main photo table
name_output = person + "_" + "photo" + "_" + name_root.replace(" ", "").lower()

collections = {
    "PATH": [],
    "COLLECTION": [],
    "PARENT_COLLECTION": [],
    "CONTAINS_FILES": [],
    "NAME_TABLE": [],
    "DESCRIPTION": []
}

# Go through the folder hierarchies
pp = [p for p in path_root.glob('**/')]
pp.pop(0)  # First is root directory
for p in pp:
    collections["PATH"].append(p.as_posix())
for p in pp:
    collections["COLLECTION"].append(p.name)  # str in case name is year / number
    collections["PARENT_COLLECTION"].append(p.parts[-2])
    if [y for y in p.iterdir() if y.is_file()]:
        collections["CONTAINS_FILES"].append(True)
    else:
        collections["CONTAINS_FILES"].append(False)
    # TODO To be filled
    collections["NAME_TABLE"].append(None)
    collections["DESCRIPTION"].append(None)

table = pd.DataFrame(
    data=collections
)

table.loc[
    table["PARENT_COLLECTION"] == path_root.parts[-1],
    "PARENT_COLLECTION"
] = name_root

if write_csv:
    table.to_csv(
        str(Path.joinpath(path_root, Path(name_output + ".csv")).as_posix()),
        sep=";",
        encoding='ANSI',
        index=False
    )

if write_mysql:
    write_table(
        db_connection,
        name_output,
        table
    )
