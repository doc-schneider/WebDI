from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.Photo import PhotoFactory


class ViewFactory:
    @staticmethod
    def view(datatable, view_mode=None):
        # TODO
        #  - Work directly with config.table? No dict, removal?

        # Return fields (but not the trivial file_name etc)
        cols = [c for c in datatable.table.columns if not c in ["FILE_NAME", "PATH", "FILE_FORMAT"]]
        dct = datatable.table[cols].to_dict("series")

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
        elif view_mode == "COLLECTION":
            dct["DATE_FROM"] = datatable.table["DATE_FROM"]
            dct["DATE_TO"] = datatable.table["DATE_TO"]
        else:
            pass

        return dct
