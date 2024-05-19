

class ViewFactory:
    @staticmethod
    def view(datatable):
        dct = {
            "title_boxes": datatable.table["TITLE"],
            "description_boxes": datatable.table["DESCRIPTION"],
        }
        return dct
