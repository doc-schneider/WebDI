import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener
from pathlib import Path
import datetime as dtm
import base64
from io import BytesIO

from DataOperations.Files import get_files_info, read_table_from_csv
from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable

register_heif_opener()

# TODO:
#  - MOV, ..
#  - Case insensitive
allow_formats = [".HEIC", ".JPG"]

class PhotoFactory:

    @staticmethod
    def table_from_folder(
            path_photo,
            album_name,
            chapters=None,
            pretable_file=None
    ):
        # Create table from standard columns
        cols = list(table_definitions[TableType.PHOTO]["Columns"].keys())

        # Get pretable
        # - Assumed that additional columns are valid
        if pretable_file:
            pretable = read_table_from_csv(pretable_file)
            cols_add = list(set(pretable.columns) - set(cols))
            cols = cols + cols_add

        table = pd.DataFrame(
            columns=cols
        )

        for i in range(len(path_photo)):
            table_part = pd.DataFrame(
                columns=cols
            )

            table_files = get_files_info(
                path_photo[i],
                [],
                allow_formats,
                [pretable_file.name],
            )
            table_files.drop(columns=set(table_files.columns) - set(cols), inplace=True)
            table_part = pd.concat([table_part, table_files], axis=0, ignore_index=True)

            table_part["CHAPTER"] = chapters[i]

            table = pd.concat([table, table_part], axis=0, ignore_index=True)

        # Get creation time form meta data (exif)
        for i in range(table.shape[0]):
            exif_dct = PhotoFactory.get_exif_data(Path(table.loc[i, "PATH"], table.loc[i, "FILE_NAME"]))
            table.loc[i, "DATE_TIME"] = dtm.datetime.strptime(exif_dct["DateTime"], "%Y:%m:%d %H:%M:%S")

        table["PHOTO_ALBUM"] = album_name

        if pretable_file:
            table.set_index("FILE_NAME", inplace=True)
            pretable.set_index("FILE_NAME", inplace=True)

            # TODO More potential columns to drop?
            if "PATH" in pretable.columns:
                pretable.drop(columns=["PATH"], inplace=True)

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
    def get_exif_data(file_location):
        image = Image.open(file_location)
        exif_data = image.getexif()
        return {TAGS.get(tag, tag): value for tag, value in exif_data.items()}

    @staticmethod
    def convert_image(file_location):
        # Conversion to jpeg and base64
        image = Image.open(file_location)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('ascii')

        # image.thumbnail((512, 512))
