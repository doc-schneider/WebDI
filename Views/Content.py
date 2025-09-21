from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory


class ContentViewer():
    def __init__(self, datatable, id_row):
        self.datatable = datatable
        self.datatable_show = None
        self.table_type = datatable.table_type
        self.id = id_row
        self.update()

    def update(self):
        primary_key = table_definitions[self.table_type]["PrimaryKey"]
        self.datatable_show = DataTable(
            self.datatable.table.loc[
            self.datatable.table[primary_key] == self.id, :
            ].reset_index(drop=True),
            self.table_type
        )

    def view(self):
        # if self.table_type.name in ["MESSAGE"]:
        #     resolve_attachment = True
        # else:
        #     resolve_attachment = False
        boxes = ViewFactory.view(self.datatable_show)
        # boxes = {}
        # boxes["IMAGE"] = dct["IMAGE"]
        # boxes["FILE_FORMAT"] = dct["FILE_FORMAT"]["value"]
        # if self.table_type.name == "PHOTO":
        #     boxes['DATE_TIME'] = dct['DATE_TIME']["value"]
        #     boxes['TEXT'] = dct["DESCRIPTION"]["value"]
        # elif self.table_type.name == "MESSAGE":
        #     boxes['DATE_TIME'] = dct['DATE_TIME']["value"]
        #     boxes['TEXT'] = dct['TEXT']["value"]
        #     boxes['TEXT_ADDITIONAL'] = {}
        #     boxes['TEXT_ADDITIONAL'][0] = ["Von: " + s if s else None for s in dct["SENDER"]["value"]]
        #     boxes['TEXT_ADDITIONAL'][1] = ["An: " + s if s else None for s in dct["RECEIVER"]["value"]]
        return boxes
