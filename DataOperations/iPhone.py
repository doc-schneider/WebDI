import pandas as pd
import datetime as dtm
import csv

from DataOperations.Utilities import add_mintimedelta, split_path_list, list_column
from DataOperations.Document import DocumentTable


class iPhoneFactory:

    @staticmethod
    def table_from_path(path_root, name, category=None, descriptions=None, events=None):
        # Exported Messages from iExplorer:
        # - 'Chat with [name].csv':
        # - csv header: "Name","Address","Time","Message","Attachment","iMessage" (yes/no)
        # - Text line including emojis
        # - Encoding: utf-8
        # - More lines with the same timestamp can have
        #  -- Links to <image> or <attachement>
        #  -- More text messages (possibly only a pathological case when several sms got stuck and then
        #  sent concurrently)
        #
        # Table:
        # - TIME FROM / TO: Timestamp + min delta
        # - PATH / DOCUMENT_NAME: To attachment
        # - DOCUMENT_TYPE: Attachement type
        # - DESCRIPTION: Message text
        # - DOCUMENT_GROUP: Links all rows with same timestamp. Timestamp as string(any better solution?)
        # - CATEGORY: iphone_sms / sms  (distinguish between iMessage and normal sms?)
        # - EVENT: SMS sender 1/2 - sender 2/1

        # TODO: Replace "Unknown" - occasionally occurring - name by Chat name

        file_csv = path_root + 'Chat with ' + name + '.csv'

        df_iexplorer = pd.read_csv(file_csv)
        df_iexplorer.drop(columns=['iMessage', 'Address'], inplace=True)
        df_iexplorer['TIME_FROM'] = pd.to_datetime(df_iexplorer['Time'], format='%d.%m.%Y %H:%M:%S')
        df_iexplorer.drop(columns=['Time'], inplace=True)
        df_iexplorer['TIME_TO'] = add_mintimedelta(df_iexplorer['TIME_FROM'])
        df_iexplorer['DOCUMENT_GROUP'] = df_iexplorer['TIME_FROM'].dt.strftime('%Y-%m-%d %H:%M:%S')

        df_iexplorer['CATEGORY'] = 'iphone_message'

        df_iexplorer.rename(columns={"Message": "DESCRIPTION"}, inplace=True)
        # Remove image/attachment marker
        df_iexplorer['DESCRIPTION'] = df_iexplorer['DESCRIPTION'].str.replace('<image>', '')
        df_iexplorer['DESCRIPTION'] = df_iexplorer['DESCRIPTION'].str.replace('<attachment>', '')

        df_iexplorer['EVENT'] = 'Message from ' + df_iexplorer['Name']
        df_iexplorer.drop(columns='Name', inplace=True)

        # Messages with attachment
        df_attachment = df_iexplorer.loc[(df_iexplorer['Attachment'].notnull())].copy()
        df_iexplorer.drop(columns=['Attachment'], inplace=True)
        # attachment: PATH / DOCUMENT_NAME / DOCUMENT_TYEP
        path, name, type = split_path_list(df_attachment['Attachment'])
        df_attachment.drop(columns=['Attachment'], inplace=True)
        # Remove everything before SMS and replace by new
        path = [p.replace('Backup Explorer/Media/Library/', path_root) for p in path]
        df_attachment['PATH'] = path
        df_attachment['DOCUMENT_NAME'] = name
        df_attachment['DOCUMENT_TYPE'] = type

        # Final merge
        df = df_iexplorer.merge(df_attachment, how='outer')

        # PATH can contain nans
        df.fillna('', inplace=True)

        # Convert to lists
        df = list_column(df, 'DOCUMENT_TYPE')
        df = list_column(df, 'CATEGORY')
        df = list_column(df, 'DESCRIPTION')

        return DocumentTable(df)
