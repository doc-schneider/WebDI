from pathlib import Path
import pandas as pd
import shutil

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.Photo import PhotoFactory, allow_formats_image, allow_formats_video


class ViewFactory:
    @staticmethod
    def view(datatable, load_media=True):
        # TODO  Work directly with copy of config.table?
        dct = datatable.table[datatable.table.columns].to_dict("series")
        # Enrich by type information
        for k in dct.keys():
            if k[:2] == "ID":  # MySQl key
                dct[k] = {
                    "mysqltype": "integer",
                    "value": dct[k]
                }
            else:
                dct[k] = {
                    "mysqltype": table_columns_names_types[k]["mysqltype"],
                    "value": dct[k]
                }
        # Source specifc
        #TODO value:type
        if datatable.table_type.name == "PHOTO" and load_media:
            dct["IMAGE"] = []  # TODO type / value ?
            for i in range(datatable.table.shape[0]):
                if datatable.table.loc[i, "FILE_FORMAT"] in allow_formats_image:
                    # Return image as base64 jpg
                    dct["IMAGE"].append(
                        PhotoFactory.convert_image(
                            Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"]),
                            datatable.table.loc[i, "FILE_FORMAT"]
                        )
                    )
                elif datatable.table.loc[i, "FILE_FORMAT"] in allow_formats_video:
                    # TODO Really necessary? Can change access rights instead?
                    shutil.copyfile(
                        Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"]),
                        "assets/" + datatable.table.loc[i, "FILE_NAME"]
                    )
                    dct["IMAGE"].append("/assets/" + datatable.table.loc[i, "FILE_NAME"])
            dct["IMAGE"] = pd.Series(dct["IMAGE"])
        else:
            pass

        return dct
