from pathlib import Path

import pandas
import pandas as pd
from urllib.parse import quote
from dash import html, dcc

from DataStructures.TableTypes import table_columns_names_types, table_definitions
from DataOperations.Photo import PhotoFactory, allow_formats_image, allow_formats_video
from DataOperations.Azure import AzureFactory
import config  # TODO Not in this this module


# TODO  Work directly with copy of config.table?
class ViewFactory:

    # TODO into Data?
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

        # Source specific
        if "IMAGE" not in dct:
            dct["IMAGE"] = []  # TODO type / value ?
            for i in range(datatable.table.shape[0]):
                file_format = datatable.table.loc[i, "FILE_FORMAT"]
                # Extract data
                if load_media and file_format in allow_formats_image:  # TODO in Operations/Photo
                    # Return image as base64 jpg
                    dct["IMAGE"].append(
                        PhotoFactory.convert_image(datatable.table.loc[i], file_format, config.environment_storage, config.environment_app)
                    )
                elif load_media and file_format in allow_formats_video:
                    # TODO Can load as byte object in memory
                    if config.environment_storage == "LOCAL":
                        file_pth = Path(datatable.table.loc[i, "PATH"], datatable.table.loc[i, "FILE_NAME"])
                        dct["IMAGE"].append(quote(str(file_pth), safe=""))
                    elif config.environment_storage == "AZURE":
                        config.AZURE_CONTAINER = datatable.table.loc[i, "AZURE_CONTAINER"]
                        dct["IMAGE"].append(datatable.table.loc[i, "AZURE_BLOB"])
                else:
                    dct["IMAGE"].append(None)
            dct["IMAGE"] = pd.Series(dct["IMAGE"])

        boxes = {}
        boxes["IMAGE"] = dct["IMAGE"]
        boxes["FILE_FORMAT"] = dct["FILE_FORMAT"]

        # Convert to format for viewing boxes
        # TODO Distinguish Timeline and other viewing formats?
        if datatable.table_type.name == "MESSAGE":
            boxes['DATE_TIME'] = dct['DATE_TIME']
            boxes["ID"] = dct["ID_MESSAGE"]
            boxes['TEXT'] = dct['TEXT']
            boxes['TEXT_ADDITIONAL'] = {}
            boxes['TEXT_ADDITIONAL'][0] = ["Von: " + s if s else None for s in dct["SENDER"]]
            boxes['TEXT_ADDITIONAL'][1] = ["An: " + s if s else None for s in dct["RECEIVER"]]
        elif datatable.table_type.name == "NOTE":
            boxes['DATE_TIME'] = dct['DATE_TIME']
            boxes["ID"] = dct["ID_NOTE"]
            boxes['TEXT'] = dct['TITLE']
            if "TEXT" in dct.keys():  # TODO Directly into MARKDOWN
                boxes['MARKDOWN'] = dct["TEXT"]
            # TODO As title for page: Notebook, Notebook Collection
        elif datatable.table_type.name == "PHOTO":
            # Album View
            boxes['FILE_NAME'] = dct['FILE_NAME']
            boxes['DATE_TIME'] = dct['DATE_TIME']
            boxes['TEXT'] = dct["DESCRIPTION"]
            boxes["CHAPTER"] = dct["CHAPTER"]
        elif datatable.table_type.name == "PHOTO_PAGE":
            # Album View
            boxes['FILE_NAME'] = dct['FILE_NAME']
            boxes['PAGE_NUMBER'] = dct['PAGE_NUMBER']
            boxes['TEXT'] = dct["DESCRIPTION"]
            boxes["CHAPTER"] = dct["CHAPTER"]
        elif datatable.table_type.name == "ALBUM":
            boxes['DATE_TIME'] = dct['DATE_FROM']
            boxes["ID"] = dct["ID_ALBUM"]
            boxes['TEXT'] = dct['PHOTO_ALBUM']
            boxes['TEXT_ADDITIONAL'] = {}
            boxes['TEXT_ADDITIONAL'][0] = dct["DESCRIPTION"]
        elif datatable.table_type.name == "FILM":
            boxes['TEXT'] = dct['TITLE']["value"]
            boxes['TEXT_ADDITIONAL'] = {}
            boxes['TEXT_ADDITIONAL'][0] = dct["DESCRIPTION"]
            # TODO More,
        elif datatable.table_type.name == "FILM_CONTENT":
            pass
            # TODO Anything here?
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
                if config.environment_storage == "LOCAL":
                    return [
                        html.Video(
                            src=f"/video?name={content_display}",
                            controls=True,
                            style={"max-width": "100%", "max-height": "90vh", "height": "auto"}
                        )
                    ]
                elif config.environment_storage == "AZURE":
                    container = config.AZURE_CONTAINER
                    blob = content_display
                    sas = AzureFactory.create_blob_sas(container, blob, config.environment_app)
                    container = quote(container, safe="")
                    blob = quote(blob, safe="")
                    # video_url = f"/video?container={container}&blob={blob}"
                    video_url = f"https://docschneiderstorage.blob.core.windows.net/{container}/{blob}?{sas}"
                    return [
                        html.Video(
                            src=video_url,
                            controls=True,
                            preload="metadata",
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
                return [
                    html.Div(dcc.Markdown(boxes_dct[item][i]))
                ]
            elif item == "DATE_TIME":
                return [
                    html.Div(boxes_dct[item].dt.strftime('%Y-%m-%d %X').fillna('')[i])
                ]
            elif item in ["PAGE_NUMBER"]:
                # TODO Merge with below?
                return [
                    html.Div(boxes_dct[item][i])
                ]
            else:
                # TODO What is this doing?
                return [
                    html.Div(txt_add[i]) for _, txt_add in boxes_dct[item].items()
                ]
        else:
            return []
