from sqlalchemy import create_engine, MetaData
from pathlib import Path
import pandas as pd

from DataOperations.Files import read_table_from_csv
from DataOperations.Helper import parse_datetime
from DataOperations.MySQL import table_insert
from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
from Initialize.Initialize import initialize_MySQL
import config


config.environment_storage = "LOCAL"
initialize_MySQL()

flag_add_film = False
flag_add_content = True

# Add new film
if flag_add_film:
    film_table = pd.DataFrame(
        index=[0],
        data={
            "TITLE": "VHS Papa A 1995",
            "FILE_NAME": "VHS_Papa_A 1995.mp4",
            "FILE_FORMAT": "MP4",
            "PATH": str(Path("Y:/Fotoalben Schneider/Papa VHS/A_1995")),
            "DATE_FROM": pd.Timestamp(1995, 10, 19, 19, 0, 0),
            "DATE_TO": pd.Timestamp(1995, 12, 31, 23, 59, 59),
            "DESCRIPTION": "Papas erster VHS-Film",
            "OWNER": "Papa"
        }
    )
    table_insert(config.mysql["metadata"], config.mysql["conn"], "films", film_table)

if flag_add_content:
    pretable_file = Path("Y:/Fotoalben Schneider/Papa VHS/A_1995/PreDokumentliste.csv")
    #
    pretable = read_table_from_csv(pretable_file)
    # Uhrzeiten  # TODO Into Helper, but only for Dash
    # pretable['TIME_FROM'] = pd.to_timedelta(pretable['TIME_FROM'])
    # pretable['TIME_TO'] = pd.to_timedelta(pretable['TIME_TO'])
    # Datetime
    parse_datetime(pretable)
    content_table = DataTable(pretable, TableType.FILM_CONTENT)
    content_table.replace_nan()

    title = "VHS Papa A 1995"
    #
    content_table.table["TITLE"] = title
    content_table.add_foreignkey("TITLE", "films", TableType.FILM)
    table_insert(config.mysql["metadata"], config.mysql["conn"], "film_contents", content_table.table)



