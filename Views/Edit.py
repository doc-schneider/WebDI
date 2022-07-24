import pandas as pd

from DataOperations.MySQL import alter_record


class MetainformationEditor:
    def __init__(
            self,
            documenttable,
            index_show,
            document_category,
            db_connection
    ):
        self.document_category = document_category
        self.db_connection = db_connection
        self.index_show = index_show
        self.read_document_info(documenttable)

    def read_document_info(self, documenttable):
        self.info_dct = documenttable.data.loc[self.index_show, :].to_dict()
        # Only str entries (for the time being)
        #self.info_dct = {key: value for key, value in self.info_dct.items() if isinstance(value, str)}
        self.table_name = self.info_dct["TABLE_NAME"]
        self.document_name = self.info_dct["DOCUMENT_NAME"]

    def edit_table(self, request_form):
        # TODO Change info_dict as to show new information in website form
        for key, value in self.info_dct.items():
            if self.info_dct[key] != request_form[key]:
                # Potentially only type different. request form returns only str
                if isinstance(self.info_dct[key], pd.Timestamp):
                    if pd.Timestamp(request_form[key]) != self.info_dct[key]:
                        pass
                elif (self.info_dct[key] is None) and (request_form[key] != "None"):  # Changed content from None to str
                    alter_record(
                        self.db_connection,
                        self.table_name,
                        self.document_category,
                        (key, request_form[key]),
                        ("DOCUMENT_NAME", self.info_dct["DOCUMENT_NAME"])
                    )  # DocumentName is the record identifier
                elif isinstance(self.info_dct[key], str):
                    # TODO Merge with above case
                    alter_record(
                        self.db_connection,
                        self.table_name,
                        self.document_category,
                        (key, request_form[key]),
                        ("DOCUMENT_NAME", self.info_dct["DOCUMENT_NAME"])
                    )
                # TODO EventId nan?


