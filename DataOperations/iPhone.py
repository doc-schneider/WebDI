import pandas as pd
import datetime as dtm
import csv
from pathlib import Path

from DataOperations import Data
import importlib
importlib.reload(Data)


class iPhoneFactory:

    @staticmethod
    def table_from_path(path_root, name, category=None, descriptions=None, events=None):
        # Export files of iExplorer:
        # - 'Chat with [name].txt': contains smileys
        # - 'Chat with [name].csv': contains name of photos (in 'Chat Attachments - [name]')
        #
        # Type: iphone_sms / sms (text with smileys)
        # Description: Content of SMS
        # Category: SMS sender 1/2 - sender 2/1
        # Event: Same as Category?
        # Path: To attachment

        TIME_FROM = list()
        TIME_TO = list()
        PATH = list()
        DOCUMENT_NAME = list()
        DOCUMENT_TYPE = list()
        DESCRIPTION = list()
        CATEGORY = list()
        EVENT = list()
        STATE = list()

        # txt file
        # - Every SMS begins with a date time entry [..]. But can span multiple lines.
        #file_txt = path_root + 'Chat with ' + name + '.txt'
        #with open(file_txt, encoding='utf-8') as f:
        #    lines_txt = [line.rstrip() for line in f]
        #f.close()
        #del lines_txt[:3] # Skip first 3 lines.
        # csv file
        file_csv = path_root + 'Chat with ' + name + '.csv'
        with open(file_csv, newline='', encoding='utf-8') as f:
            lines_csv = list(csv.reader(f))
        f.close()
        del lines_csv[:1]  # Skip first lines.

        for line in lines_csv:
            DOCUMENT_TYPE.append('iphone_sms')
            CATEGORY.append('SMS von ' + line[0])
            created = dtm.datetime.strptime(line[2], '%d.%m.%Y %H:%M:%S')
            TIME_FROM.append(created.strftime('%d.%m.%Y %H:%M:%S'))
            TIME_TO.append((created + dtm.timedelta(minutes=1)).strftime('%d.%m.%Y %H:%M:%S'))   # Artificial time to avoid 0 interval.
            DESCRIPTION.append(line[3])
            # line[3] = '<image>'
            if line[4]=='':
                PATH.append(None)
                DOCUMENT_NAME.append(None)
            else:
                pth = Path(line[4])
                DOCUMENT_NAME.append(pth.name)
                PATH.append(Path(path_root + '/Chat Attachments - ' + name))

            EVENT.append(None)

        df = pd.DataFrame(data={'TIME_FROM': TIME_FROM, 'TIME_TO': TIME_TO, 'PATH': PATH,
                                'DOCUMENT_NAME': DOCUMENT_NAME, 'DOCUMENT_TYPE': DOCUMENT_TYPE,
                                'DESCRIPTION': DESCRIPTION,
                                'CATEGORY': CATEGORY, 'EVENT': EVENT})
        return Data.DocumentTable(df)
