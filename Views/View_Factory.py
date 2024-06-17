from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.Photo import PhotoFactory


class ViewFactory:
    @staticmethod
    def view(datatable, view_mode=None):
        # TODO Don't need these fields since they are already config.table
        # Return text fields (but not the trivial file_name etc)
        cols_text = [c for c in datatable.table.columns if table_columns_names_types[c]["mysqltype"] == "text"]
        cols_text = [c for c in cols_text if not c in ["FILE_NAME", "PATH", "FILE_FORMAT"]]
        dct = datatable.table[cols_text].to_dict("series")

        # Source specifc
        if datatable.table_type.name == "PHOTO":
            dct["IMAGE"] = []
            for i in range(datatable.table.shape[0]):
                dct["IMAGE"].append(
                    PhotoFactory.convert_image(
                        Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"])
                    )
                )
            dct["IMAGE"] = pd.Series(dct["IMAGE"])
        else:
            pass

        # View specifc
        if view_mode == "TIMELINE":
            dct["DATE_TIME"] = datatable.table["DATE_TIME"]
        elif view_mode == "ALBUM":
            dct["DATE_TIME"] = datatable.table["DATE_TIME"]
        else:
            pass

        return dct
