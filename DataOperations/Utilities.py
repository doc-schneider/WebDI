import pandas as pd
import datetime as dtm
import json
from pathlib import Path
import re
from os import path


#  Column properties of DataTable

# Datatable columns that are defined as list
def list_key(column_name):
    return column_name in ['DESCRIPTION', 'PARENT_DESCRIPTION', 'CATEGORY', 'PARENT_CATEGORY',
                           'EVENT_TIME_FROM', 'EVENT_TIME_TO',
                           'DOCUMENT_TABLE', 'DOCUMENT_TYPE', 'VIEW_TYPE', 'TAG']

def time_keys(column_name):   # Headers standing for date time information
    return column_name in ['TIME_FROM', 'TIME_TO', 'EVENT_TIME_FROM', 'EVENT_TIME_TO', 'DATE_BIRTH']

def int_keys(column_name):   # Integer information
    return column_name in ['EVENT_LEVEL']

# Conver column values to list
def list_column(df, col_name):
    if list_key(col_name):
        df[col_name] = df[col_name].apply(lambda x: [x])
    return df


def add_mintimedelta(list_time):
    return [t + dtm.timedelta(seconds=1) for t in list_time]

# List or datafram column of file path strings. Split into head, tail and type
def split_path_list(path_list):
    head = [path.split(p)[0] for p in path_list]
    tail = [path.split(p)[1] for p in path_list]
    extension = [path.splitext(p)[1][1:] for p in tail]
    return head, tail, extension

def get_files_info(pfad):
    PATH = list()
    DOCUMENT_NAME = list()
    DOCUMENT_TYPE = list()
    TIME_CREATED = list()
    # Get file names.
    files = list(pfad.glob('*'))
    for f in files:
        PATH.append(pfad)
        DOCUMENT_NAME.append(f.name)
        DOCUMENT_TYPE.append(f.suffix[1:])    #  Removes dot . from string.
        # st_ctime : creation time (of file on computer)
        # st_mtime : last content modification time (creation time of data, e,g time photo taken)
        TIME_CREATED.append(
            dtm.datetime.fromtimestamp(f.stat().st_mtime)   # .strftime('%d.%m.%Y %H:%M:%S')
        )
    return pd.DataFrame(data={'TIME_CREATED': TIME_CREATED, 'PATH': PATH,
                              'DOCUMENT_NAME': DOCUMENT_NAME, 'DOCUMENT_TYPE': DOCUMENT_TYPE})

# Csv row converted to list (with ; separator)
def strio_to_list(text):
    return [t for t in text[:-2].split(';')]   # Removing newline

def str_to_list(s):
    # From external (csv, ..) format to internal table format.
    # Internal format is always list (and list of lists).
    # External (csv) string can have no [] if only single item.
    # TODO: More levels of lists.
    if not s:
        result = ['']    # Empty string
    elif s[0]=='[' and s[-1]==']':
        s = s[1:-1]    # Remove brackets.
        result = [ss.strip() for ss in s.split('|')]
    else:
        # Exception case: single str can be without []
        result = [s]
    return result

def list_to_str(s, column_name):
    # For writing table to csv
    if list_key(column_name):
        if s is None:  # Todo: Where is this still needed?
            s = ''
        elif isinstance(s[0], list):  # Todo: only one inner list correct here
            # 2 nested lists
            s = s[0]
            # Assume only one inner list. Turn into string.
            u = '[' + s[0]
            for t in s[1:]:
                u = u + ', ' + t
            s = u + ']'
        else:
            # 1 list
            u = s[0]
            for i in range(1,len(s)):
                u = u + ', ' + s[i]
            s = u
    return s

def add_thumbnail_to_filename(DOCUMENT_NAME, DOCUMENT_TYPE):
    # Input needs to be of type str
    name = re.sub('\.' + DOCUMENT_TYPE + '$', '', DOCUMENT_NAME)
    return name + "_thumbnail.jpg"

def add_thumbnail_to_pathname(pathname):
    # Input needs to be of type Path
    p = pathname
    pp = list(pathname.parts)
    pp[-1] = p.stem + '_thumbnail' + p.suffix
    return Path(('/').join(pp))


# SQLite

def textlist_to_JSON(lst):
    return json.dumps(lst)

def JSON_to_textlist(jsn):
    return json.loads(jsn)

def timestamplist_to_JSON(lst):
    lstr = [l.strftime('%d.%m.%Y %H:%M:%S') for l in lst]
    return json.dumps(lstr)  #.encode('utf8')

def JSON_to_timestamplist(data):
    return [pd.to_datetime(d) for d in json.loads(data)]  #.decode('utf8')



