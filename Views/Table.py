from Views.View_Factory import ViewFactory


class TableViewer():
    def __init__(self, datatable_initial):
        self.datatable = datatable_initial
        self.table_type = datatable_initial.table_type
        self.n_dim = datatable_initial.table.shape[0]

    def view(self):
        boxes = ViewFactory.view(self.datatable, load_media=False)

        boxes["N_DIM"] = self.n_dim

        return boxes
