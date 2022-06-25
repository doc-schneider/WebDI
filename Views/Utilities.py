import pandas as pd
import numpy as np
import base64
from random import shuffle
from os import path

from DataOperations.Azure import AzureFactory


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

# TODO move
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



