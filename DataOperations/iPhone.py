import pandas as pd
import datetime as dtm
import csv
#from pathlib import Path

from DataOperations.Utilities import add_mintimedelta


class iPhoneFactory:

    @staticmethod
    def table_from_path(path_root, name, category=None, descriptions=None, events=None):
        # Exported Messages from iExplorer:
        # - 'Chat with [name].csv':
        # - csv header: "Name","Address","Time","Message","Attachment","iMessage"
        # - Text line including emojis
        # - Another line with the same timestamp can have the link to an <image> or <attachement>
        # - Encoding: utf-8
        #
        # Table:
        # - TIME FROM / TO: Timestamp + min delta
        # - PATH / DOCUMENT_NAME: To attachment
        # - TYPE: Attachement type
        # - DESCRIPTION: Message text
        # - CATEGORY: iphone_sms / sms
        # - EVENT: SMS sender 1/2 - sender 2/1

        file_csv = path_root + 'Chat with ' + name + '.csv'

        df_iexplorer = pd.read_csv(file_csv)
        df_iexplorer.drop(columns=['iMessage'], inplace=True)
        df_iexplorer['TIME_FROM'] = pd.to_datetime(df_iexplorer['Time'])
        df_iexplorer.drop(columns=['Time'], inplace=True)

        # Messages with attachment
        df_attachment = df_iexplorer.loc[(df_iexplorer['Attachment'].notnull())].copy()
        df_iexplorer.drop(df_attachment.index, inplace=True)

        df = pd.DataFrame(data={'TIME_FROM': df_iexplorer['TIME_FROM'].tolist()})
        df['TIME_TO'] = add_mintimedelta(df_iexplorer['TIME_FROM'])

        df['DESCRIPTION'] = df_iexplorer['Message']

        df['CATEGORY'] = 'iphone_message'

        # TODO: Replace "Unknown" - occasionally occuring - name Chat name
        # TODO: Good category? Use TAG?
        df['EVENT'] = 'Message from ' + df_iexplorer['Name']

        # Find attachments belonging to a message
        df_attachment['TIME_FROM']

        'Backup Explorer/Media/Library/'  # SMS




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
