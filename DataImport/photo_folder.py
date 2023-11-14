from pathlib import Path
import pandas as pd
import datetime as dtm
from sqlalchemy import create_engine

from DataOperations.MySQL import write_table, read_table

"""
Finds all folders in a root folder.
- Folders can be bottom level, ie, containing a photo collection and no further sub-folders
- Folders can be meta-collections, ie, contain sub-forders (eg, "best of") and a photo collection.
All folders with their attributes are written into a table (csv, mysql)
"""

# TODO
#  - Album type information

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "stefan"
topic = "photo"
id = 1   # ID = index in topic table
flag_process = "folder"  # "folder", "all"
if flag_process == "folder":
    single_folder = "2023/2023_11_03_Yabase&MeHotels"
flag_add = True  # Add one row to subtopic table, don't destroy old entries "NAME_TABLE"

topic_table = read_table(db_connection, person + "_topic_" + topic)
sub_topic = topic_table.loc[id, "SUB_TOPIC"]
sub_topic_table = topic_table.loc[id, "NAME_TABLE"]
path_root = Path(topic_table.loc[id, "PATH"][0:-1])  # Removing slash

discard_paths = ["#recycle"]
discard_files = ["Thumbs", "PreDokumentliste"]

if flag_add:
    table_old = read_table(
        db_connection,
        sub_topic_table
    )

collections = {
    "PATH": [],
    "COLLECTION": [],
    "PARENT_COLLECTION": [],
    "CONTAINS_FILES": [],
    "TIME_FROM": [],
    "TIME_TO": [],
    "NAME_TABLE": [],
    "DESCRIPTION": []
}

# Go through the folder hierarchies
pp = [p for p in path_root.glob('**/')]

# Discard
pp.pop(0)  # First is root directory
pp = [p for p in pp if not [True for prt in p.parts if prt in discard_paths]]

if flag_process == "folder":
    pp = [p for p in pp if p == Path.joinpath(path_root, Path(single_folder))]

# Get path
for p in pp:
    collections["PATH"].append(p.as_posix())

# Time span
# TODO Times often not correct. Need additional mechanisms
for p in pp:
    dts = []
    for f in p.iterdir():
        if str(f.stem) not in discard_files:
            dts.append(
                dtm.datetime.fromtimestamp(f.stat().st_mtime)
            )
    if dts:
        collections["TIME_FROM"].append(min(dts))
        collections["TIME_TO"].append(max(dts))
    else:
        collections["TIME_FROM"].append(None)
        collections["TIME_TO"].append(None)

for p in pp:
    collections["COLLECTION"].append(p.name)  # str in case name is year / number
    collections["PARENT_COLLECTION"].append(p.parts[-2])
    if [y for y in p.iterdir() if y.is_file()]:
        collections["CONTAINS_FILES"].append(True)
    else:
        collections["CONTAINS_FILES"].append(False)
    # To be filled
    collections["NAME_TABLE"].append(None)
    collections["DESCRIPTION"].append(None)

table = pd.DataFrame(
    data=collections
)

# proper name root
table.loc[
    table["PARENT_COLLECTION"] == path_root.parts[-1],
    "PARENT_COLLECTION"
] = sub_topic

if flag_add:
    table = pd.concat([table_old, table], ignore_index=True)

table = table.sort_values(by=['PATH'])
table.reset_index(inplace=True, drop=True)

table.to_csv(
    str(Path.joinpath(path_root, Path(sub_topic_table + ".csv")).as_posix()),
    sep=";",
    encoding='ANSI',
    index=False
)

write_table(
    db_connection,
    sub_topic_table,
    table
)
