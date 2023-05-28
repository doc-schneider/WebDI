from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

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

photocollections = {
    "PATH": [],
    "COLLECTION": [],
    "PARENT_COLLECTION": [],
    "CONTAINS_PHOTOS": [],
    "PHOTO_TABLE": [],
    "DESCRIPTION": []
}

# Go through the folder hierarchies
pp = [p for p in path_root.glob('**/')]
pp.pop(0)  # First is root directory
for p in pp:
    photocollections["PATH"].append(p.as_posix())
for p in pp:
    photocollections["COLLECTION"].append(p.name)  # str in case name is year / number
    photocollections["PARENT_COLLECTION"].append(p.parts[-2])
    if [y for y in p.iterdir() if y.is_file()]:
        photocollections["CONTAINS_PHOTOS"].append(True)
    else:
        photocollections["CONTAINS_PHOTOS"].append(False)
    # TODO To be filled
    photocollections["PHOTO_TABLE"].append(None)
    photocollections["DESCRIPTION"].append(None)

phototable = pd.DataFrame(
    data=photocollections
)

phototable.loc[
    phototable["PARENT_COLLECTION"] == path_root.parts[-1],
    "PARENT_COLLECTION"
] = name_root

if write_csv:
    phototable.to_csv(
        str(Path.joinpath(path_root, Path(name_output + ".csv")).as_posix()),
        sep=";",
        encoding='ANSI',
        index=False
    )

if write_mysql:
    phototable.to_sql(
        name_output,
        db_connection,
        if_exists="replace",
        index=False
    )