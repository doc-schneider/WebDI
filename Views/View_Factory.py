from pathlib import Path

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.Photo import PhotoFactory


class ViewFactory:
    @staticmethod
    def view(datatable, view_mode=None):
        # Return text fields (but not the trivial file_name etc)
        cols_text = [c for c in datatable.table.columns if table_columns_names_types[c]["mysqltype"] == "text"]
        cols_text = [c for c in cols_text if not c in ["FILE_NAME", "PATH", "FILE_FORMAT"]]
        dct = datatable.table[cols_text].to_dict("series")

        # Source specifc
        if datatable.table_type.name == "PHOTO":
            dct["THUMBNAIL"] = []  # TODO Series?
            for i in range(datatable.table.shape[0]):
                dct["THUMBNAIL"].append(
                    PhotoFactory.convert_image(
                        Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"])
                    )
                )
        else:
            pass

        # View specifc
        if view_mode == "TIMELINE":
            dct["DATE_TIME"] = datatable.table["DATE_TIME"]
        else:
            pass

        return dct
