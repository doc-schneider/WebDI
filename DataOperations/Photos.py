import pandas as pd
import datetime as dtm
from PIL import Image
from os import path

from DataOperations.Document import DocumentTable
from DataOperations.Utilities import get_files_info, add_thumbnail_to_filename


class PhotoFactory:

    @staticmethod
    def table_from_folder(path_photo, pretable=None):
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

        df = get_files_info(path_photo)
        # Filter for photo formats.
        df = df.loc[df['DOCUMENT_TYPE'].apply(lambda x: PhotoFactory.allowed_photo_formats(x))]

        for i in range(df.shape[0]):
            TIME_FROM.append(df['TIME_CREATED'].iloc[i])  
            TIME_TO.append((df['TIME_CREATED'].iloc[i] + dtm.timedelta(seconds=1)))   # Artificial time to avoid 0 interval.
            PATH.append(str(df['PATH'].iloc[i]))
            DOCUMENT_NAME.append(df['DOCUMENT_NAME'].iloc[i])
            DOCUMENT_TYPE.append(df['DOCUMENT_TYPE'].iloc[i])
            DESCRIPTION.append(None)
            PARENT_DESCRIPTION.append(None)
            CATEGORY.append(['photo'])
            PARENT_CATEGORY.append(None)
            EVENT.append(None)    # Folder name as a simple proxy?
            TAG.append(None)

            # DOCUMENT_NAME in pretable?
            # TODO: pretable = None
            ix = pretable.data.loc[pretable.data['DOCUMENT_NAME'] == DOCUMENT_NAME[-1]].index.values
            if ix.size != 0:
                ix = ix[0]
                DESCRIPTION[-1] = pretable.data['DESCRIPTION'].iloc[ix]
                PARENT_DESCRIPTION[-1] = pretable.data['PARENT_DESCRIPTION'].iloc[ix]
                PARENT_CATEGORY[-1] = pretable.data['PARENT_CATEGORY'].iloc[ix]
                EVENT[-1] = pretable.data['EVENT'].iloc[ix]
                TAG[-1] = pretable.data['TAG'].iloc[ix]
            PhotoFactory.make_thumbnail(PATH[-1], DOCUMENT_NAME[-1], DOCUMENT_TYPE[-1])

        return DocumentTable(
            pd.DataFrame(data={'TIME_FROM': TIME_FROM, 'TIME_TO': TIME_TO, 'PATH': PATH,
                               'DOCUMENT_NAME': DOCUMENT_NAME, 'DOCUMENT_TYPE': DOCUMENT_TYPE,
                               'DESCRIPTION': DESCRIPTION, 'PARENT_DESCRIPTION': PARENT_DESCRIPTION,
                               'CATEGORY': CATEGORY, 'PARENT_CATEGORY': PARENT_CATEGORY, 'EVENT': EVENT,
                               'TAG': TAG})
        )

    @staticmethod
    def allowed_photo_formats(input: str) -> bool:
        allowed_formats = ['jpg', 'jpeg']
        return input.lower() in allowed_formats

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
