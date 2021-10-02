import pandas as pd
from PIL import Image
from os import path
import datetime as dtm
import base64
from io import BytesIO

from DataStructures.Document import DocumentTable
from DataOperations.Files import get_files_info
from DataOperations.Utilities import add_thumbnail_to_filename, \
    add_mintimedelta, list_column


class PhotoFactory:
    # TODO: iPhone HEVC

    @staticmethod
    def table_from_folder(
            path_photo,
            pretable=None,
            ignore_thumbnails=True,
            mode='standard'
    ):
        if mode == 'standard':
            DATETIME = list()
            DESCRIPTION = list()
        elif mode == 'complex':
            TIME_FROM = list()
            TIME_TO = list()
            PATH = list()
            DOCUMENT_NAME = list()
            DOCUMENT_TYPE = list()
            DESCRIPTION = list()
            PARENT_DESCRIPTION = list()
            CATEGORY = []
            PARENT_CATEGORY = []
            EVENT = list()
            TAG = list()
            # STATE = list()

        files_info = get_files_info(path_photo)

        # Filter for photo formats.
        files_info = files_info.loc[
            files_info['DOCUMENT_TYPE'].apply(lambda x: PhotoFactory.allowed_photo_formats(x))
        ]
        files_info.reset_index(inplace=True, drop=True)

        # Remove thumbnails
        if ignore_thumbnails:
            files_info = files_info.loc[
                files_info['DOCUMENT_NAME'].apply(lambda x: 'thumbnail' not in x)
            ]

        if mode == 'standard':
            for i in range(files_info.shape[0]):

                # Datetime created
                # TODO EXIF extractor only works for jpg (?)
                # TODO Mov
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

                if (pretable is not None) and \
                        (pretable.data['DOCUMENT_NAME'] == files_info.loc[i, 'DOCUMENT_NAME']).any():
                    DESCRIPTION.append(pretable.data.loc[
                        pretable.data['DOCUMENT_NAME'] == files_info.loc[i, 'DOCUMENT_NAME'],
                        'DESCRIPTION'
                    ].values[0])
                else:
                    DESCRIPTION.append(None)

            return DocumentTable(
                pd.DataFrame(data={
                    'DATETIME': DATETIME,
                    'PATH': files_info['PATH'],
                    'DOCUMENT_NAME': files_info['DOCUMENT_NAME'],
                    'DOCUMENT_TYPE': files_info['DOCUMENT_TYPE'],
                    'DESCRIPTION': DESCRIPTION
                }
                )
            )

        elif mode == 'complex':
            # Turn into list items
            files_info = list_column(files_info, 'DOCUMENT_TYPE')
            for i in range(df.shape[0]):
                TIME_FROM.append(df['TIME_CREATED'].iloc[i])
                TIME_TO.append(add_mintimedelta([df['TIME_CREATED'].iloc[i]])[0])   # Artificial time to avoid 0 interval.
                PATH.append(df['PATH'].iloc[i])
                DOCUMENT_NAME.append(df['DOCUMENT_NAME'].iloc[i])
                DOCUMENT_TYPE.append(df['DOCUMENT_TYPE'].iloc[i])
                DESCRIPTION.append([''])
                PARENT_DESCRIPTION.append([''])
                CATEGORY.append(['photo'])
                PARENT_CATEGORY.append([''])
                EVENT.append(None)    # Folder name as a simple proxy?
                TAG.append([''])
                # DOCUMENT_NAME in pretable?
                if pretable is not None:
                    ix = pretable.data.loc[pretable.data['DOCUMENT_NAME'] == DOCUMENT_NAME[-1]].index.values
                    if ix.size != 0:
                        ix = ix[0]
                        # TODO Pretable attributes beforehand
                        DESCRIPTION[-1] = pretable.data['DESCRIPTION'].iloc[ix]
                        PARENT_DESCRIPTION[-1] = pretable.data['PARENT_DESCRIPTION'].iloc[ix]
                        PARENT_CATEGORY[-1] = pretable.data['PARENT_CATEGORY'].iloc[ix]
                        EVENT[-1] = pretable.data['EVENT'].iloc[ix]
                        #TAG[-1] = pretable.data['TAG'].iloc[ix]
            return DocumentTable(
                pd.DataFrame(data={'TIME_FROM': TIME_FROM, 'TIME_TO': TIME_TO, 'PATH': PATH,
                                   'DOCUMENT_NAME': DOCUMENT_NAME, 'DOCUMENT_TYPE': DOCUMENT_TYPE,
                                   'DESCRIPTION': DESCRIPTION, 'PARENT_DESCRIPTION': PARENT_DESCRIPTION,
                                   'CATEGORY': CATEGORY, 'PARENT_CATEGORY': PARENT_CATEGORY, 'EVENT': EVENT,
                                   'TAG': TAG})
            )


    @staticmethod
    def allowed_photo_formats(input: str) -> bool:
        allowed_formats = ['jpg', 'jpeg', 'mov']
        return input.lower() in allowed_formats


    # TODO Thumbnail in APP1 marker / exif (?).
    #  However, base64 (and open?) seems to take most time, thumbnail seems fast
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

