import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener
from pymediainfo import MediaInfo
from pathlib import Path
import base64
from io import BytesIO

from DataOperations.Files import get_files_info, read_table_from_csv
from DataStructures.TableTypes import TableType, table_definitions, table_columns_names_types
from DataStructures.Data import DataTable

register_heif_opener()

allow_formats_image_JPEG = ["JPG", "JPEG", "PNG"]
allow_formats_image_HEVC = ["HEIC"]
allow_formats_image = allow_formats_image_JPEG + allow_formats_image_HEVC
allow_formats_video = ["MOV", "MP4"]

# Mapping for image orientation correction
# -90: Rotate the image by 90 degrees clockwise
# ...
# TODO What is wrong information? key or value?
rotation_mapping = {
    1: 0,
    3: 180,
    6: -90,
    8: 90
}

date_format_German = '%d.%m.%Y %H:%M:%S'

class PhotoFactory:

    @staticmethod
    def table_from_folder(
            path_photo,
            album_name,
            chapters,
            timezone_default="CET",
            pretable_file=None
    ):
        # Create table from standard columns
        cols = list(table_definitions[TableType.PHOTO]["Columns"].keys())

        # Get pretable
        # - Additional columns
        # - Replacement columns
        # - Replacement rows
        if pretable_file:
            pretable = read_table_from_csv(
                pretable_file
            )
            PhotoFactory.parse_datetime(pretable)
            if "DATE_TIME" in pretable.columns:
                # Take datetime info from pretable (i.e. for photos without exif data)
                pretable_datetime = pretable.loc[
                    pretable["DATE_TIME"].notna(),
                    ["FILE_NAME", "DATE_TIME"]
                ]
            else:
                pretable_datetime = None
            cols_add = list(set(pretable.columns) - set(cols))
            pretable_file_name = pretable_file.name
        else:
            cols_add = []
            pretable_file_name = None
            pretable_datetime = None

        table = pd.DataFrame(
            columns=cols
        )

        for i in range(len(path_photo)):
            table_part = pd.DataFrame(
                columns=cols + cols_add
            )

            table_files = get_files_info(
                path_photo[i],
                [],
                allow_formats_image + allow_formats_video,
                [pretable_file_name],
            )
            table_files.drop(columns=set(table_files.columns) - set(cols), inplace=True)
            table_part = pd.concat([table_part, table_files], axis=0, ignore_index=True)

            table_part["CHAPTER"] = chapters[i]

            table = pd.concat([table, table_part], axis=0, ignore_index=True)

        # Get meta data (exif)
        # - Recording time
        # TODO Process exif data in function
        for i in range(table.shape[0]):
            file_name = table.loc[i, "FILE_NAME"]
            if (pretable_datetime is not None) and (file_name in pretable_datetime["FILE_NAME"].values):
                t = pretable_datetime.loc[pretable_datetime["FILE_NAME"] == file_name, "DATE_TIME"].values[0]
            elif table.loc[i, "FILE_FORMAT"] in allow_formats_image:
                exif_dct, exif_gps = PhotoFactory.get_exif_data(
                    Path(table.loc[i, "PATH"], table.loc[i, "FILE_NAME"]),
                    table.loc[i, "FILE_FORMAT"]
                )
                # Extracting local time when image was taken
                t_key = next(iter(set(exif_dct.keys()) & set(["DateTime", "DateTimeOriginal"])))
                t = pd.to_datetime(exif_dct[t_key], format="%Y:%m:%d %H:%M:%S")
                if not exif_gps:
                    # Eg, non Apple camera. Assuming that no GPS info means camera always records CET time
                    t = t.tz_localize("CET")
                    t = t.tz_convert(timezone_default)
                    t = t.tz_localize(None)
            elif table.loc[i, "FILE_FORMAT"] in allow_formats_video:
                exif_dct = PhotoFactory.get_meta_data(Path(table.loc[i, "PATH"], table.loc[i, "FILE_NAME"]))
                if "comapplequicktimemake" in exif_dct.keys():  # Apple MOV
                    t = pd.Timestamp(exif_dct["comapplequicktimecreationdate"])  ## includes local tz
                    t = t.tz_localize(None)
                elif "recorded_date" in exif_dct.keys():  # Apple MP4
                    t = pd.Timestamp(exif_dct["recorded_date"])
                    t = t.tz_localize(None)
            table.loc[i, "DATE_TIME"] = t

        table["PHOTO_ALBUM"] = album_name

        table.set_index("FILE_NAME", inplace=True)
        if pretable_file:
            pretable.set_index("FILE_NAME", inplace=True)
            # Drop entries from pretable with no entry in table
            pretable = pretable[pretable.index.isin(table.index)]
            # Pretable columns to drop
            cols_drop = ["PATH", "DATE_TIME"]
            for c in list(set(cols_drop) & set(pretable.columns)):
                pretable.drop(columns=c, inplace=True)
            table.loc[
                pretable.index,
                pretable.columns
            ] = pretable
        table.reset_index(inplace=True)

        photo_table = DataTable(table, TableType.PHOTO)

        photo_table.replace_nan()
        photo_table.format_path()
        photo_table.format_documentgroup()

        return photo_table

    @staticmethod
    def parse_datetime(df):
        cols = [k for k, v in table_columns_names_types.items() if v["mysqltype"]=="datetime" and k in df.columns]
        for c in cols:
            df[c] = pd.to_datetime(df[c], format=date_format_German)

    @staticmethod
    def get_exif_data(file_location, file_format):
        image = Image.open(file_location)
        # TODO Unify
        if file_format in allow_formats_image_JPEG:
            exif_data = image._getexif()
        elif file_format in allow_formats_image_HEVC:
            exif_data = image.getexif()
        exif_dct = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}

        exif_gps = {}
        if file_format in allow_formats_image_JPEG:
            gps_info = exif_dct.get('GPSInfo', {})
            for key in gps_info.keys():
                decoded = GPSTAGS.get(key, key)
                exif_gps[decoded] = gps_info[key]
        elif file_format in allow_formats_image_HEVC:
            exif_gps = exif_dct.get('GPSInfo', {})
            # TODO This is only an offset number

        return exif_dct, exif_gps

    @staticmethod
    def get_meta_data(file_location):
        media_info = MediaInfo.parse(file_location)
        return media_info.general_tracks[0].to_data()

    @staticmethod
    def convert_image(file_location, file_format, correct_orientation=True):
        # Conversion to jpeg and base64
        image = Image.open(file_location)

        if correct_orientation:
            # Prevent rotated display on web page
            exif_dct, _ = PhotoFactory.get_exif_data(file_location, file_format)
            if "Orientation" in exif_dct.keys():
                # 1 - Normal (no rotation)
                # 2 - Flipped horizontally
                # 3 - Rotated 180 degrees
                # 4 - Flipped vertically
                # 5 - Transposed (flipped horizontally and rotated 270 degrees clockwise)
                # 6 - Rotated 90 degrees clockwise
                # 7 - Transverse (flipped horizontally and rotated 90 degrees clockwise)
                # 8 - Rotated 270 degrees clockwise
                image_orientation = exif_dct["Orientation"]
                image = image.rotate(rotation_mapping[image_orientation], expand=True)

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('ascii')

