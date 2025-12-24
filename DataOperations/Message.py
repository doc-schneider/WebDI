import os
import pandas as pd
from pathlib import Path

from DataStructures.Data import DataTable
from DataOperations.Files import get_files_info
from DataStructures.TableTypes import TableType, table_definitions


sender_receiver_default = "Stefan Schneider"

class MessageFactory:

    @staticmethod
    def table_from_folder(
            path_message_stream,
            message_collection,
            attachments_folder=None,
            format_stream="iMazing"
    ):
        # Create table from standard columns
        cols = list(table_definitions[TableType.MESSAGE]["Columns"].keys())
        message_table = pd.DataFrame(columns=cols)

        if format_stream == "iMazing":
            # This reads a csv file exported by iMazing for one "Chat-Sitzung". The communication between me and someone else.
            table_stream = pd.read_csv(path_message_stream, sep=",")  # comma separator # TODO Move to File
            message_table["MESSAGE_TYPE"] = table_stream["Service"]
            message_table["DATE_TIME"] = pd.to_datetime(table_stream["Datum der Nachricht"])
            message_table["SENDER"] = table_stream["Absendername"]
            ix = message_table["SENDER"].isnull()
            sender_receiver = message_table.loc[~ix, "SENDER"].unique()[0]
            message_table.loc[ix, "SENDER"] = sender_receiver_default
            message_table.loc[ix, "RECEIVER"] = sender_receiver
            message_table.loc[~ix, "RECEIVER"] = sender_receiver_default
            message_table["TEXT"] = table_stream["Text"]  # TODO There are occasional non-resolved symbol codes
            message_table.loc[message_table["TEXT"].isnull(), "TEXT"] = ""  # TODO Postprocessing by Data class

            # Attachments
            path_attachments = path_message_stream.parent / Path(attachments_folder)
            ats = get_files_info(path_attachments)
            message_table["ATTACHMENT"] = ""
            ix = ~table_stream["Anhang"].isnull()
            attachment_names = table_stream.loc[
                ix, "Anhang"
            ]
            # Match names in table with real file names
            # TODO Missing videos?
            attachment_real = list()
            for a_n in attachment_names:
                ix_at = ats["FILE_NAME"].str.contains(
                    str(Path(a_n).with_suffix(''))
                )
                if ix_at.any():
                    attachment_real.append(
                        ats.loc[ix_at, "PATH"].values[0] / ats.loc[ix_at, "FILE_NAME"].values[0]
                    )
                else:
                    attachment_real.append("")
            message_table.loc[ix, "ATTACHMENT"] = attachment_real  # TODO Not ideal. No separation into path and file
            message_table["MESSAGE_COLLECTION"] = message_collection

        message_table = DataTable(message_table, TableType.MESSAGE)
        message_table.replace_nan()
        message_table.format_path(cols=["ATTACHMENT"])
        return message_table

