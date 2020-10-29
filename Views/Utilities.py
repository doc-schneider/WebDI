import pandas as pd
import numpy as np
import base64

from DataOperations.Azure import AzureFactory


def timegrid(t_start, t_end, n_t):
    t_delta = (t_end - t_start)
    dt = t_delta / n_t
    df = pd.DataFrame(columns=['TIME_FROM', 'TIME_TO'])
    for i in range(n_t):
        df.loc[i] = [t_start + i * dt, t_start + (i + 1) * dt]
    return df


# The indexes of all documents in timegrid.
def find_documents(documenttable, tg):
    index_documents = list()
    for i in range(len(tg)):
        # All documents have non 0 timedelta TIME_TO - TIME_FROM. So rightmost open interval doesn't exclude any document
        timeinterval = pd.Interval(tg['TIME_FROM'].iloc[i],
                                   tg['TIME_TO'].iloc[i], closed='left')
        index_documents.append(documenttable.find_in_timeinterval(timeinterval))
    return index_documents


# Which document to show in each time cell. Default: first.
# TODO: Shouldn't index_show be a relative index within a box?
def show_documents(index_documents, which=0):
    index_show = list()
    for i in range(len(index_documents)):
        if not index_documents[i]:
            index_show.append(None)
        else:
            index_show.append(index_documents[i][which])
    return index_show


def view_data(location_document, encode_type, document_pathtype):
    if encode_type == 'html_path':
        # data = path to html source
        data = location_document + '.html'
    elif encode_type == 'base64':
        if document_pathtype == 'AZURE':
            downloaded_blob = AzureFactory.download_blob_single(location_document[0],
                                                                location_document[1])
            data = base64.b64encode(downloaded_blob.readall()).decode('ascii')
        else:
            if location_document is not None:
                with open(location_document, "rb") as data_file:
                    data = base64.b64encode(data_file.read()).decode('ascii')
            else:
                data = None

    return data


# All events  referenced in documenttable.
def find_events(eventtable, documenttable):
    events = np.unique(documenttable.data['EVENT'].values).tolist()
    df = eventtable.data[eventtable.data['EVENT_NAME'].isin(events)].copy()
    df['TIME_FROM'] = df['EVENT_TIME_FROM']
    df['TIME_TO'] = df['EVENT_TIME_TO']
    return df


def graphics_event_label():
    # Position of event label (left edge)
    pass


# Calculates the svg graphics numbers for depicting intervals timeline
def graphics_markers_time(table, index_documents, time_interval):
    rect_width_min = 0.5  # Percentage
    # Tuples for left corner and width of rectangles
    lst_graphics = list()
    int_all = pd.Interval(time_interval[0], time_interval[1], closed='both')
    for i in range(len(index_documents)):
        for ix in index_documents[i]:
            # Coordinates as percentages
            if not isinstance(table['TIME_FROM'].iloc[ix], list):
                rect_left = 100. * (pd.Interval(time_interval[0], table['TIME_FROM'].iloc[ix],
                                        closed='both').length / int_all.length)
                rect_width = 100. * (pd.Interval(table['TIME_FROM'].iloc[ix], table['TIME_TO'].iloc[ix],
                                         closed='both').length / int_all.length)
            else:
                # TODO event: List, Can be beyond interval
                rect_left = 100. * (pd.Interval(time_interval[0],
                                               max(time_interval[0], table['TIME_FROM'].iloc[ix][0]),
                                               closed='both').length / int_all.length)
                rect_width = 100. * (pd.Interval(table['TIME_FROM'].iloc[ix][0],
                                                min(time_interval[1], table['TIME_TO'].iloc[ix][0]),
                                                closed='both').length / int_all.length)
            rect_mid = rect_left + 0.5*rect_width
            # Ensure min width. But keep inside [0,1]
            rect_left_new = rect_mid - np.max((0.5*rect_width_min, 0.5*rect_width))
            rect_right_new = rect_mid + np.max((0.5*rect_width_min, 0.5*rect_width))
            if rect_left_new < 0.:
                rect_left_new = 0.
                rect_right_new = rect_width_min
            elif rect_right_new > 100.:
                rect_left_new = 100. - rect_width_min
                rect_right_new = 100.
            rect_width_new = rect_right_new - rect_left_new
            lst_graphics.append((rect_left_new, rect_width_new))
    return lst_graphics
