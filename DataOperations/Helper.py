import pandas as pd
from pathlib import Path

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.Files import read_table_from_csv
from DataOperations.Photo import PhotoFactory


allow_formats_image_JPEG = ["JPG", "JPEG"]
allow_formats_image_HEVC = ["HEIC"]
allow_formats_image = allow_formats_image_JPEG + allow_formats_image_HEVC
allow_formats_video = ["MOV", "MP4"]
allow_formats_document = ["PDF", "DOCX", "TXT", "XLS", "XLSX"]
allow_formats_html = ["HTML"]
allow_formats_all = allow_formats_image + allow_formats_video + allow_formats_document + allow_formats_html

date_format_German = '%d.%m.%Y %H:%M:%S'


def parse_datetime(df):
    cols = [k for k, v in table_columns_names_types.items() if v["mysqltype"] == "datetime" and k in df.columns]
    for c in cols:
        df[c] = pd.to_datetime(df[c], format=date_format_German)

def get_pretable(pretable_file, cols):
    # Additional columns
    if pretable_file:
        pretable = read_table_from_csv(
            pretable_file
        )
        parse_datetime(pretable)
        cols_add = list(set(pretable.columns) - set(cols))
        pretable_file_name = pretable_file.name
        if "DATE_TIME" in pretable.columns:
            pretable_datetime = pretable.loc[
                pretable["DATE_TIME"].notna(),
                ["FILE_NAME", "DATE_TIME"]
            ]
        else:
            pretable_datetime = None
    else:
        pretable = None
        cols_add = []
        pretable_file_name = None
        pretable_datetime = None

    return pretable, pretable_file_name, cols_add, pretable_datetime

def merge_pretable(pretable, table):
    if pretable is not None:
        table.set_index("FILE_NAME", inplace=True)
        pretable.set_index("FILE_NAME", inplace=True)

        # Drop entries from pretable with no entry in table
        pretable = pretable[pretable.index.isin(table.index)]

        # TODO More potential columns to drop?
        cols_drop = ["PATH", "DATE_TIME"]
        for c in list(set(cols_drop) & set(pretable.columns)):
            pretable.drop(columns=c, inplace=True)
        if "PATH" in pretable.columns:
            pretable.drop(columns=["PATH"], inplace=True)

        table.loc[
            pretable.index,
            pretable.columns
        ] = pretable
        table.reset_index(inplace=True)
