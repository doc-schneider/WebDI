from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

from DataOperations.Documents import DocumentFactory
from DataOperations.Files import get_files_info

"""
...
"""

# TODO
#  - What to do with non-photo documents?

file_types_music = ["m4a"]

db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/di'
db_connection = create_engine(db_connection_str)

person = "stefan"
topic = "music"
type = "TITLE_LIST"
write_csv = True
write_mysql = True

# TODO Read parameters from topic table

if type == "CD_COLLECTION":
    path_root = Path('X:/Meine CDs/')
    name_root = "Meine CDs"

elif type == "TITLE_LIST":
    path_root = "Z:/Biographie/Stefan/Musik/Lieblingstitel.csv"
    name_root = "Lieblingstitel"

name_output = person + "_" + topic + "_" + name_root.replace(" ", "").lower()

if type == "CD_COLLECTION":
    collections = {
        "PATH": [],
        "COLLECTION": [],
        "PARENT_COLLECTION": [],
        "ALBUM": [],
        "TABLE": [],
        "DESCRIPTION": []
    }

    # Go through the folder hierarchies
    pp = [p for p in path_root.glob('**/')]
    pp.pop(0)  # First is root directory
    for p in pp:
        collections["PATH"].append(p.as_posix())
        collections["COLLECTION"].append(p.name)  # str in case name is year / number
        collections["PARENT_COLLECTION"].append(p.parts[-2])
        f = get_files_info(p.as_posix())
        if f.shape[0] > 0:
            # Cases:
            # - Plain album -> Files are audio tracks, cover (optional), pre-table (optional)
            # - Mult-album in sub-folders -> Files: Cover (optional), pre-table (required)
            pretable = DocumentFactory.read_pretable(str(p.as_posix()))
            if pretable is not None and "PATH" in pretable.columns:
                collections["ALBUM"].append("MULTI")
            else:
                collections["ALBUM"].append("SINGLE")
        else:
            collections["ALBUM"].append(None)
        collections["TABLE"].append(None)
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
        table.to_sql(
            name_output,
            db_connection,
            if_exists="replace",
            index=False
        )

elif type == "TITLE_LIST":
    table = pd.read_csv(
        path_root,
        encoding='ANSI',
        sep=';',
        parse_dates=['Hinzugefügt'],
        dayfirst=True
    )
    if write_mysql:
        table.to_sql(
            name_output,
            db_connection,
            if_exists="replace",
            index=False
        )