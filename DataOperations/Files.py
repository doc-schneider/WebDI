import pandas as pd
import datetime as dtm


def get_files_info(
        pfad,
        exclude_formats=[],
        allow_formats=[],
        exclude_files=[]
):
    '''
    Function retrieves file infos for all files
    inside the given directory

    '''

    info = {
        "FILE_NAME": [],
        "PATH": [],
        "FILE_FORMAT": [],
        "TIME_CREATED": [],
        "TIME_MODIFIED": [],
    }

    if allow_formats:
        files = [y for y in pfad.iterdir() if (
                y.is_file() and y.suffix[1:].upper() in allow_formats and not y.name in exclude_files
        )]
    else:
        files = [y for y in pfad.iterdir() if (
                y.is_file() and not y.name in exclude_files and not y.suffix in exclude_formats
        )]
    for f in files:
        info["PATH"].append(pfad)
        info["FILE_NAME"].append(f.name)
        info["FILE_FORMAT"].append(f.suffix[1:].upper())  #  Removes dot . from string.
        # st_ctime : creation time (of file on computer)
        # st_mtime : last content modification time
        # TODO Has this timestamp any use? Modification time seems to be sometimes right
        info["TIME_CREATED"].append(
            dtm.datetime.fromtimestamp(f.stat().st_ctime)
        )
        info["TIME_MODIFIED"].append(
            dtm.datetime.fromtimestamp(f.stat().st_mtime)
        )

    return pd.DataFrame(data=info)

# TODO Parallel function in Data?
def read_table_from_csv(file, encoding="utf-8"):
    return pd.read_csv(file, sep=";", encoding=encoding)

