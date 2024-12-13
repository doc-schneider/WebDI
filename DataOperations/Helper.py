import pandas as pd
from pathlib import Path

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.Files import read_table_from_csv
from DataOperations.Photo import PhotoFactory


allow_formats_image_JPEG = ["JPG", "JPEG"]
allow_formats_image_HEVC = ["HEIC"]
allow_formats_image = allow_formats_image_JPEG + allow_formats_image_HEVC
allow_formats_video = ["MOV", "MP4"]
allow_formats_document = ["PDF"]
allow_formats_html = ["HTML"]
allow_formats_all = allow_formats_image + allow_formats_video + allow_formats_document + allow_formats_html

date_format_German = '%d.%m.%Y %H:%M:%S'


def parse_datetime(df):
    cols = [k for k, v in table_columns_names_types.items() if v["mysqltype"] == "datetime" and k in df.columns]
    for c in cols:
        df[c] = pd.to_datetime(df[c], format=date_format_German)

# File creation time
def get_creation_time(table, timezone_default="CET"):
    for i in range(table.shape[0]):
        # Get meta data (exif)
        # TODO Process exif data in function
        if table.loc[i, "FILE_FORMAT"] in allow_formats_image:
            exif_dct, exif_gps = PhotoFactory.get_exif_data(
                Path(table.loc[i, "PATH"], table.loc[i, "FILE_NAME"]),
                table.loc[i, "FILE_FORMAT"]
            )
            # Extracting local time when image was taken
            t = pd.to_datetime(exif_dct["DateTime"], format="%Y:%m:%d %H:%M:%S")
            if not exif_gps:
                # Eg, non Apple camera. Assuming that no GPS info means camera always records CET time
                t = t.tz_localize("CET")
                t = t.tz_convert(timezone_default)
                t = t.tz_localize(None)
        elif table.loc[i, "FILE_FORMAT"] in allow_formats_video:
            exif_dct = PhotoFactory.get_meta_data(Path(table.loc[i, "PATH"], table.loc[i, "FILE_NAME"]))
            if "comapplequicktimemake" in exif_dct.keys():  # Apple MOV
                t = pd.Timestamp(exif_dct["comapplequicktimecreationdate"])  # includes local tz
                t = t.tz_localize(None)
            elif "recorded_date" in exif_dct.keys():  # Apple MP4
                t = pd.Timestamp(exif_dct["recorded_date"])
                t = t.tz_localize(None)
        elif table.loc[i, "FILE_FORMAT"] in allow_formats_document + allow_formats_html:
            t = table.loc[i, "TIME_MODIFIED"].floor("S")
        #TODO Use timezone?
        #TODO Use datetime?
        table.loc[i, "DATE_TIME"] = t

def get_pretable(pretable_file, cols):
    # Additional columns
    if pretable_file:
        pretable = read_table_from_csv(
            pretable_file
        )
        parse_datetime(pretable)
        cols_add = list(set(pretable.columns) - set(cols))
        pretable_file_name = pretable_file.name
    else:
        pretable = None
        cols_add = []
        pretable_file_name = None

    return pretable, pretable_file_name, cols_add

def merge_pretable(pretable, table):
    if pretable is not None:
        table.set_index("FILE_NAME", inplace=True)
        pretable.set_index("FILE_NAME", inplace=True)

        # Drop entries from pretable with no entry in table
        pretable = pretable[pretable.index.isin(table.index)]

        # TODO More potential columns to drop?
        if "PATH" in pretable.columns:
            pretable.drop(columns=["PATH"], inplace=True)

        table.loc[
            pretable.index,
            pretable.columns
        ] = pretable
        table.reset_index(inplace=True)
