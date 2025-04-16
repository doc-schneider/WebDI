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
        if load_media:
            dct["IMAGE"] = []  # TODO type / value ?
            for i in range(datatable.table.shape[0]):

                if datatable.table_type.name == "PHOTO":
                    file_format = datatable.table.loc[i, "FILE_FORMAT"]
                    file_pth = Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"])
                elif datatable.table_type.name == "MESSAGE":
                    if datatable.table.loc[i, "ATTACHMENT"]:
                        #TODO Attachment processing into Viewer and File
                        file_pth = Path(datatable.table.loc[i, "ATTACHMENT"])
                        file_format = file_pth.suffix.lstrip(".").upper()
                    else:
                        file_format = None
                else:
                    print("ERROR")

                # Extract data
                if file_format in allow_formats_image:
                    # Return image as base64 jpg
                    dct["IMAGE"].append(
                        PhotoFactory.convert_image(file_pth, file_format)
                    )
                elif file_format in allow_formats_video:
                    # TODO Really necessary? Can change access rights instead?
                    # TODO Can load as byte object in memory?
                    shutil.copyfile(
                        file_pth,
                        "assets/" + file_pth.name
                    )
                    dct["IMAGE"].append("/assets/" + file_pth.name)
                else:
                    dct["IMAGE"].append(None)

            dct["IMAGE"] = pd.Series(dct["IMAGE"])

        return dct
