import pandas as pd
from PIL import Image
from os import path
import datetime as dtm
import base64
from io import BytesIO

from DataStructures.Document import DocumentTable
from DataOperations.Files import get_files_info


class PhotoFactory:
    # TODO: iPhone HEVC, MOV

    @staticmethod
    def table_from_folder(
            path_photo,
            pretable=None,
    ):

        # Returns TIME_CREATED, PATH, DOCUMENT_NAME, DOCUMENT_TYPE
        files_info = get_files_info(path_photo)

        # Minimal set of columns for photo table
        DATETIME = list()
        DESCRIPTION = list()

        # Optional columns
        if (pretable is not None):
            columns_add = list(set(pretable.data.columns) - {"DESCRIPTION"} - set(files_info.columns))
        table_add = {name: [] for name in columns_add}

        # Filter for photo formats.
        files_info = files_info.loc[
            files_info['DOCUMENT_TYPE'].apply(lambda x: PhotoFactory.allowed_photo_formats(x))
        ]
        files_info.reset_index(inplace=True, drop=True)

        for i in range(files_info.shape[0]):

            # Datetime created
            # TODO EXIF extractor only works for jpg (?)
            if files_info.loc[i, 'DOCUMENT_TYPE'].lower() in ['jpg', 'jpeg']:
                image = Image.open(files_info.loc[i, 'PATH'] + files_info.loc[i, 'DOCUMENT_NAME'])
                exifdata = image.getexif()
                DATETIME.append(
                    dtm.datetime.strptime(exifdata.get(36867), "%Y:%m:%d %H:%M:%S")
                )
            else:
                DATETIME.append(
                    files_info.loc[i, 'TIME_CREATED']
                )

            DESCRIPTION.append(None)

            if (pretable is not None):
                for col in columns_add:
                    table_add[col].append(None)
                ix = pretable.data['DOCUMENT_NAME'] == files_info.loc[i, 'DOCUMENT_NAME']
                if ix.any():
                    if "DESCRIPTION" in pretable.data.columns:
                        DESCRIPTION[-1] = pretable.data.loc[
                            ix,
                            'DESCRIPTION'
                        ].values[0]
                    for col in columns_add:
                        table_add[col][-1] = pretable.data.loc[
                            ix,
                            col
                        ].values[0]

        table = {
            'DATETIME': DATETIME,
            'PATH': files_info['PATH'].to_list(),
            'DOCUMENT_NAME': files_info['DOCUMENT_NAME'].to_list(),
            'DOCUMENT_TYPE': files_info['DOCUMENT_TYPE'].to_list(),
            'DESCRIPTION': DESCRIPTION
        }
        table.update(table_add)
        return DocumentTable(pd.DataFrame(data=table))

    @staticmethod
    def allowed_photo_formats(input: str) -> bool:
        allowed_formats = ['jpg', 'jpeg']   # 'mov'
        return input.lower() in allowed_formats

    # TODO Thumbnail in APP1 marker / exif (?). However, base64 (and open?)
    #  seems to take most time, thumbnail seems fast
    # TODO Encoding to DataOperations / File
    @staticmethod
    def load_thumbnail(file, encode_type):
        if (file is not None) and path.isfile(file):
            image = Image.open(file)
            image.thumbnail((512, 512))
            if encode_type == 'base64':
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                data = base64.b64encode(buffered.getvalue()).decode('ascii')
        else:
            data = None
        return data


    '''
    @staticmethod
    def table_thumbnails(table):
        # Make thumbnails form media documents references in table.
        # TODO Some / all jpg photos seem to have iphone previews in the same folder?
        # TODO Photos in the Parts / StickerCache section (PNG) are already small enough?
        # TODO Some files are missing because the iphone path was too long for copying
        # TODO Assume that list DOCUMENT_TYPE only contains a single element
        type_series = pd.Series(t[0] for t in table.data['DOCUMENT_TYPE'])
        # jpg, vcf, png, amr, mov, caf, gif, heic
        types = type_series.unique()
        # TODO jpg for the time being. PNG should only be for low size pictures (?)
        ix = type_series.isin(['jpg', 'JPG', 'jpeg'])
        pth = list(table.data['PATH'].loc[ix])
        nms = list(table.data['DOCUMENT_NAME'].loc[ix])
        tps = list(type_series.loc[ix])
        for p,n,t in zip(pth,nms,tps):
            if path.exists(p + '/' + n):   # File existing?
                PhotoFactory.make_thumbnail(p,n,t)

    @staticmethod
    def make_thumbnail(pathname, filename, documenttype):
        # TODO: Turning of "Hochkant"
        thmb_name = add_thumbnail_to_filename(filename, documenttype)
        thmb_filename = pathname + '/' + thmb_name
        name = pathname + '/' + filename
        im = Image.open(name)
        im.thumbnail((512, 512))  # Keeps aspect ratio of original image. Max dimension 512.
        im.save(thmb_filename, "JPEG")
    '''

