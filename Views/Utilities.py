import pandas as pd
import numpy as np
import base64
from random import shuffle
from os import path

from DataOperations.Azure import AzureFactory


# TODO
#  - ( DataFrame to complicated? )
#  - Use Intervals?
#  - Improve with linspace or so instead of loop
def timegrid(t_start, t_end, n_t):
    t_delta = (t_end - t_start)
    dt = t_delta / n_t
    df = pd.DataFrame(columns=['TIME_FROM', 'TIME_TO'])
    for i in range(n_t):
        df.loc[i] = [t_start + i * dt, t_start + (i + 1) * dt]
    return df

# TODO Remove
# The indexes of all documents in timegrid.
def find_documents(documenttable, tg):
    index_documents = list()
    for i in range(len(tg)):
        # All documents have non 0 timedelta TIME_TO - TIME_FROM. So rightmost open interval doesn't exclude any document
        timeinterval = pd.Interval(tg['TIME_FROM'].iloc[i],
                                   tg['TIME_TO'].iloc[i], closed='left')
        index_documents.append(documenttable.find_in_timeinterval(timeinterval))
    return index_documents

# TODO: Should be part of Parent class. REMOVE
# Which document to show in each time cell. Default: first.
def show_documents(index_documents, which=0):
    index_show = list()
    for i in range(len(index_documents)):
        if not index_documents[i]:
            index_show.append(None)
        else:
            index_show.append(index_documents[i][which])
    return index_show

# Convert list of strings elements to string only.
# If empty string than convert to None
# TODO Move to Data Operations list_to_str
def list_column_to_str(x):
    # TODO List of multiple elements
    y = x[0]
    if y == '':
        y = None
    return y

# Converts a list of texts to text only
# - Separates list elements by large space
# TODO: Merge with above functions
def view_text(text_list):
    text = text_list[0]
    for c in text_list[1:]:
        text = text + '  ' + c
    return text

def view_data(location_document, encode_type, document_pathtype, environment):
    if encode_type == 'html_path':
        # data = path to html source
        data = location_document + '.html'
    elif encode_type == 'base64':
        if document_pathtype == 'AZURE':
            downloaded_blob = AzureFactory.download_blob_single(location_document[0],
                                                                location_document[1],
                                                                environment)
            data = base64.b64encode(downloaded_blob.readall()).decode('ascii')
        else:
            if (location_document is not None) and path.isfile(location_document):
                with open(location_document, "rb") as data_file:
                    data = base64.b64encode(data_file.read()).decode('ascii')
            else:
                data = None

    return data



