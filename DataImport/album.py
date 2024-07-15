import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.DataFactory import DataFactory
from DataOperations.MySQL import table_fetch


# Extract album data from a new photo dataframe
album = photo_table.table["PHOTO_ALBUM"].unique()[0]
d_t = photo_table.table["DATE_TIME"]
date_from = d_t.min()
date_to = d_t.max()
cols = list(table_definitions[TableType.ALBUM]["Columns"].keys())
album_table = pd.DataFrame(
    index=[0],
    data={
        cols[0]: album,
        cols[1]: date_from,
        cols[2]: date_to,
        cols[3]: ""
    }
)

#
album_table = table_fetch(metadata, db_conn, "albums")
id_dict = pd.Series(album_table["ID_ALBUM"].values, index=album_table["PHOTO_ALBUM"]).to_dict()

#
photo_table = DataFactory.fetch_table(TableType.PHOTO, "photos")
albums = photo_table.table["PHOTO_ALBUM"].unique()
date_from = []
date_to = []
for a in albums:
    d_t = photo_table.table.loc[photo_table.table["PHOTO_ALBUM"] == a, "DATE_TIME"]
    date_from.append(d_t.min())
    date_to.append(d_t.max())
cols = list(table_definitions[TableType.ALBUM]["Columns"].keys())
album_table = pd.DataFrame(
    data={
        cols[0]: albums,
        cols[1]: date_from,
        cols[2]: date_to,
        cols[3]: ""
    }
)





