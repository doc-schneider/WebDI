from pathlib import Path
import pandas as pd
from urllib.parse import quote
from dash import html, dcc

from DataStructures.TableTypes import table_columns_names_types, table_definitions
from DataOperations.Photo import PhotoFactory, allow_formats_image, allow_formats_video
import config  # TODO Not in this this module


# TODO  Work directly with copy of config.table?
class ViewFactory:

    # Filter table for specification of a parent id if specified in session
    @staticmethod
    def filter_table(datatable, session):
        table_type = datatable.table_type
        if "ParentTableType" in table_definitions[table_type]:
            parent_table_type = table_definitions[table_type]["ParentTableType"]
            datatable = datatable.filter(session[parent_table_type.name])
        return datatable

    @staticmethod
    def view(datatable, load_media=True):
        # Adding FILE information if not present
        if datatable.table_type.name in ["MESSAGE", "ALBUM"]:
            datatable.table["FILE_NAME"] = None
            datatable.table["PATH"] = None
            datatable.table["FILE_FORMAT"] = None

        # TODO Could be done at start when loading the table
        if datatable.table_type.name in ["MESSAGE"]:
            resolve_attachment = True
        else:
            resolve_attachment = False

        if resolve_attachment:
            for i in range(len(datatable.table)):
                if datatable.table.loc[i, "ATTACHMENT"]:  # Not empty?
                    # TODO Merge with similar procedure in Files.py?
                    file_pth = Path(datatable.table.loc[i, "ATTACHMENT"])
                    datatable.table.loc[i, "FILE_NAME"] = file_pth.name
                    datatable.table.loc[i, "PATH"] = file_pth.parent
                    datatable.table.loc[i, "FILE_FORMAT"] = file_pth.suffix[1:].upper()

        dct = datatable.table[datatable.table.columns].to_dict("series")

        # Enrich by type information
        # TODO No longer needed
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
        dct["IMAGE"] = []  # TODO type / value ?
        for i in range(datatable.table.shape[0]):
            file_format = datatable.table.loc[i, "FILE_FORMAT"]
            # Extract data
            if load_media and file_format in allow_formats_image:  # TODO in Operations/Photo
                # Return image as base64 jpg
                dct["IMAGE"].append(
                    PhotoFactory.convert_image(datatable.table.loc[i], file_format, config.environment_storage)
                )
            elif load_media and file_format in allow_formats_video:
                # TODO Can load as byte object in memory
                if config.environment_storage == "LOCAL":
                    file_pth = Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"])
                    dct["IMAGE"].append(quote(str(file_pth), safe=""))
                elif config.environment_storage == "AZURE":
                    dct["IMAGE"].append(quote(datatable.table.loc[i, "AZURE_BLOB"], safe=""))
            else:
                dct["IMAGE"].append(None)
        dct["IMAGE"] = pd.Series(dct["IMAGE"])

        boxes = {}
        boxes["IMAGE"] = dct["IMAGE"]
        boxes["FILE_FORMAT"] = dct["FILE_FORMAT"]["value"]

        # Convert to format for viewing boxes
        # TODO Distinguish Timeline and other viewing formats
        if datatable.table_type.name == "MESSAGE":
            boxes['DATE_TIME'] = dct['DATE_TIME']["value"]
            boxes["ID"] = dct["ID_MESSAGE"]["value"]
            boxes['TEXT'] = dct['TEXT']["value"]
            boxes['TEXT_ADDITIONAL'] = {}
            boxes['TEXT_ADDITIONAL'][0] = ["Von: " + s if s else None for s in dct["SENDER"]["value"]]
            boxes['TEXT_ADDITIONAL'][1] = ["An: " + s if s else None for s in dct["RECEIVER"]["value"]]
        elif datatable.table_type.name == "NOTE":
            boxes['DATE_TIME'] = dct['DATE_TIME']["value"]
            boxes["ID"] = dct["ID_NOTE"]["value"]
            boxes['TEXT'] = dct['TITLE']["value"]
            if "TEXT" in dct.keys():
                boxes['MARKDOWN'] = dct["TEXT"]["value"]
            # TODO As title for page: Notebook, Notebook Collection
        elif datatable.table_type.name == "PHOTO":
            # Album View
            boxes['FILE_NAME'] = dct['FILE_NAME']["value"]
            boxes['DATE_TIME'] = dct['DATE_TIME']["value"]
            boxes['TEXT'] = dct["DESCRIPTION"]["value"]
            boxes["CHAPTER"] = dct["CHAPTER"]["value"]
        elif datatable.table_type.name == "ALBUM":
            boxes['DATE_TIME'] = dct['DATE_FROM']["value"]
            boxes["ID"] = dct["ID_ALBUM"]["value"]
            boxes['TEXT'] = dct['PHOTO_ALBUM']["value"]
            boxes['TEXT_ADDITIONAL'] = {}
            boxes['TEXT_ADDITIONAL'][0] = dct["DESCRIPTION"]["value"]

        return boxes

    @staticmethod
    def media_type_box(media_type, content_display):
        if content_display:
            if media_type in allow_formats_image:
                return [
                    html.Img(
                        src="data:image/jpeg;base64," + content_display,
                        style={"max-width": "100%", "max-height": "90vh", "height": "auto"}
                    )
                ]
            elif media_type in allow_formats_video:
                return [
                    html.Video(
                        src=f"/video?name={content_display}",
                        controls=True,
                        style={"max-width": "100%", "max-height": "90vh", "height": "auto"}
                    )
            ]
        else:
            return [
                html.Div()
            ]

    # Additional Text items
    @staticmethod
    def additional_items(boxes_dct, i, item):
        if item in boxes_dct.keys():
            if item == "MARKDOWN":
                return [html.Div(dcc.Markdown(boxes_dct[item][i]))]
            else:
                return [
                    html.Div(txt_add[i]) for _, txt_add in boxes_dct[item].items()
                ]
        else:
            return []
