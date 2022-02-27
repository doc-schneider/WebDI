import pandas as pd
import datetime as dtm
from pathlib import Path
from os import path
import base64


def get_files_info(pfad):
    '''
    Function retrieves file infos for all files
    inside the given directory

    :param pfad:
    :return:
    '''

    PATH = list()
    DOCUMENT_NAME = list()
    DOCUMENT_TYPE = list()
    TIME_CREATED = list()

    # Get file names.
    files = list(Path(pfad).glob('*'))
    # TODO No loop?
    for f in files:
        PATH.append(pfad)
        DOCUMENT_NAME.append(f.name)
        DOCUMENT_TYPE.append(f.suffix[1:])    #  Removes dot . from string.
        # st_ctime : creation time (of file on computer)
        # st_mtime : last content modification time (creation time of data, e,g time photo taken)
        TIME_CREATED.append(
            dtm.datetime.fromtimestamp(f.stat().st_mtime)
        )
    return pd.DataFrame(data={'TIME_CREATED': TIME_CREATED, 'PATH': PATH,
                              'DOCUMENT_NAME': DOCUMENT_NAME, 'DOCUMENT_TYPE': DOCUMENT_TYPE})


# Load data from file and return base64 for viewing in website
def encode_data(file, encode_type):
    if encode_type == 'base64':
        if (file is not None) and path.isfile(file):
            with open(file, "rb") as data_file:
                data = base64.b64encode(data_file.read()).decode('ascii')
        else:
            data = None
    return data