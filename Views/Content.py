from Views.View_Factory import ViewFactory


class ContentViewer():
    def __init__(self, table_row):
        self.datatable = table_row
        self.table_type = table_row.table_type
        self.update(table_row)

    def update(self, datatable):
        pass

    def view(self):
        box = ViewFactory.view(self.datatable)
        box["date_time"] = self.datatable.table["DATE_TIME"]
        return box
