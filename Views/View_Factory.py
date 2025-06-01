from pathlib import Path
import pandas as pd
import shutil
from urllib.parse import quote

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.Photo import PhotoFactory, allow_formats_image, allow_formats_video
import config


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
        if load_media:
            dct["IMAGE"] = []  # TODO type / value ?
            for i in range(datatable.table.shape[0]):
                file_format = datatable.table.loc[i, "FILE_FORMAT"]
                # Extract data
                if file_format in allow_formats_image:  # TODO in Operations/Photo
                    # Return image as base64 jpg
                    dct["IMAGE"].append(
                        PhotoFactory.convert_image(datatable.table.loc[i], file_format, config.environment_storage)
                    )
                elif file_format in allow_formats_video:
                    # TODO Can load as byte object in memory
                    if config.environment_storage == "LOCAL":
                        file_pth = Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"])
                        shutil.copyfile(
                            file_pth,
                            "assets/" + file_pth.name
                        )
                        dct["IMAGE"].append("/assets/" + file_pth.name)
                    elif config.environment_storage == "AZURE":
                        dct["IMAGE"].append(quote(datatable.table.loc[i, "AZURE_BLOB"], safe=""))
                else:
                    dct["IMAGE"].append(None)

            dct["IMAGE"] = pd.Series(dct["IMAGE"])

        return dct
