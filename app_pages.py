import dash
from dash import Dash, html, dcc
from sqlalchemy import create_engine, MetaData
import mysql.connector

from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
import config


# MySQL
db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
db_engine = create_engine(db_connection_str)
db_conn = db_engine.connect()
metadata = MetaData()
metadata.reflect(bind=db_engine)
config.mysql = {
    "engine": db_engine,
    "conn": db_conn,
    "metadata": metadata,
}
# Simple connector
db_connector = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Moppel3!",
    database="lives",
)
db_cursor = db_connector.cursor()
config.mysql["connector"] = db_connector
config.mysql["cursor"] = db_cursor

# Tables
config.table = {
    TableType.ALBUM: {
        "mysql_name": "albums",
        "mysql_table": None,
        "data_table": None
    },
    TableType.PHOTO: {
        "mysql_name": "photos",
        "mysql_table": None,
        "data_table": None
    },
    TableType.NOTE: {
        "mysql_name": "notes",
        "mysql_table": None,
        "data_table": None
    },
    TableType.NOTEBOOK: {
        "mysql_name": "notebooks",
        "mysql_table": None,
        "data_table": None
    },
    TableType.DOCUMENT: {
        "mysql_name": "documents",
        "mysql_table": None,
        "data_table": None
    },
    TableType.DOCUMENT_COLLECTION: {
        "mysql_name": "document_collections",
        "mysql_table": None,
        "data_table": None
    },
    TableType.TAG: {
        "mysql_name": "tags",
        "mysql_table": None,
        "data_table": None
    },
    TableType.EVENT: {
        "mysql_name": "events",
        "mysql_table": None,
        "data_table": None
    },
}
for key in config.table.keys():
    config.table[key]["data_table"] = DataTable.fetch_table(
        key,
        config.table[key]["mysql_name"]
    )
config.collection_types = [TableType.ALBUM, TableType.NOTE, TableType.NOTEBOOK]  #TODO What was that for?

dash_app = Dash(__name__, use_pages=True)

dash_app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dcc.Store(id='store', storage_type='session', data={"album": {"ID_ALBUM": 14}, "album_view": {"IX_PHOTO": [None]}}),
    dash.page_container,
])

if __name__ == '__main__':
    dash_app.run(host='192.168.0.225', port=5000, debug=False)  #  (host='192.168.0.225', port=5000, debug=True)



