import pandas as pd
import os

from DataStructures.Data import DocumentTable


class CD(DocumentTable):
    def __init__(self, table, cover=None):
        super().__init__(table)
        self.cover = cover   # Filename of cover.


class MusicFactory:

    @staticmethod
    def cd_from_path(path_root, pretable=None, leaveout_list=None):
        TIME_FROM = list()
        TIME_TO = list()
        PATH = list()
        DOCUMENT_NAME = list()
        DOCUMENT_TYPE = list()
        DESCRIPTION = list()
        PARENT_DESCRIPTION = list()
        CATEGORY = list()
        PARENT_CATEGORY = list()
        EVENT = list()
        STATE = list()

        # Pre-table needs to have the same order of items as the files in the directory
        # TODO Make flexible matching
        pretbl = pretable.data
        npretbl = pretbl.shape[0]

        files = os.listdir(path_root)

        for f in leaveout_list:
            if f in files:
                files.remove(f)

        nfiles = len(files)
        for i in range(nfiles):
            # TODO: Need the original creation time in pre-table
            #(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = \
            #    os.stat(path_root + files[i])
            #time.ctime(mtime)  # last modified
            #time.ctime(ctime)   # created
            TIME_FROM.append(None)       # NaT?
            TIME_TO.append(None)
            PATH.append(path_root)
            fname, ftype = os.path.splitext(files[i])
            DOCUMENT_NAME.append(fname + ftype)
            DOCUMENT_TYPE.append(ftype[1:])   # Remove .
            DESCRIPTION.append(None)
            PARENT_DESCRIPTION.append(None)
            CATEGORY.append(None)
            PARENT_CATEGORY.append(None)
            EVENT.append(None)

            # Supplement or overwrite with pre-table
            if i<npretbl:
                DESCRIPTION[-1] = pretbl['DESCRIPTION'].iloc[i]
                PARENT_DESCRIPTION[-1] = pretbl['PARENT_DESCRIPTION'].iloc[i]
                CATEGORY[-1] = pretbl['CATEGORY'].iloc[i]
                PARENT_CATEGORY[-1] = pretbl['PARENT_CATEGORY'].iloc[i]

        df = pd.DataFrame(data={'TIME_FROM': TIME_FROM, 'TIME_TO': TIME_TO, 'PATH': PATH,
                                'DOCUMENT_NAME': DOCUMENT_NAME, 'DOCUMENT_TYPE': DOCUMENT_TYPE,
                                'DESCRIPTION': DESCRIPTION, 'PARENT_DESCRIPTION': PARENT_DESCRIPTION,
                                'CATEGORY': CATEGORY, 'PARENT_CATEGORY': PARENT_CATEGORY,
                                'EVENT': EVENT})

        ix = DESCRIPTION.index(['Cover'])
        cover = path_root + DOCUMENT_NAME[ix] + '.' + DOCUMENT_TYPE[ix]

        return CD(df, cover)
