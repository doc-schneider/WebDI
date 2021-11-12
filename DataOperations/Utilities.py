import pandas as pd
import datetime as dtm
from pathlib import Path
import re
from os import path
import json


##  Conversions

# SQL utilities

def textlist_to_JSON(lst):
    # TODO text converted into strange format.
    return json.dumps(lst)

def JSON_to_textlist(jsn):
    return json.loads(jsn)

def timelist_to_JSON(lst):
    lstr = [l.strftime('%d.%m.%Y %H:%M:%S') for l in lst]
    return json.dumps(lstr)  #.encode('utf8')

def JSON_to_timelist(data):
    return [pd.to_datetime(d) for d in json.loads(data)]  #.decode('utf8')

# csv utilties

# Csv row converted to list (with ; separator)
def strio_to_list(text):
    return [t for t in text[:-2].split(';')]   # Removing newline

def str_to_list(s):
    # From external (csv, ..) format to internal table format.
    # Internal format is always list (and list of lists).
    # External (csv) string can have no [] if only single item.
    # TODO: More levels of lists.
    # TODo Switch to json?
    if not s:
        result = ['']    # Empty string
    elif s[0]=='[' and s[-1]==']':
        s = s[1:-1]    # Remove brackets.
        result = [ss.strip() for ss in s.split('|')]
    else:
        # Exception case: single str can be without []
        result = [s]
    return result

def list_to_str(s):
    # For writing table to csv
    # Only a single list level
    if s is None:  # TODO: Where is this still needed?
        result = ''
    else:
        result = '[' + s[0]
        for ss in s[1:]:
            result += ' | ' + ss
        result += ']'
    return result


# Convert column values to list
def list_column(df, col_name):
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

def add_thumbnail_to_filename(DOCUMENT_NAME, DOCUMENT_TYPE):
    # Input needs to be of type str
    name = re.sub('\.' + DOCUMENT_TYPE + '$', '', DOCUMENT_NAME)
    return name + "_thumbnail.jpg"

# TODO Remove
def add_thumbnail_to_pathname(pathname):
    # Input needs to be of type Path
    p = pathname
    pp = list(pathname.parts)
    pp[-1] = p.stem + '_thumbnail' + p.suffix
    return Path(('/').join(pp))

# Alters a DataFrame str column
def alter_column_str(table, column, str_old, str_new):
    table[column] = table[column].map(lambda x: x.replace(str_old, str_new))

