import pandas as pd
import dash
from dash import Dash, html, dcc
from sqlalchemy import create_engine, MetaData

from DataOperations import MySQL
from DataStructures.Data import DataTable
import config


# Settings
config.environment = "local"   # "azure"

if config.environment == "local":
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
    # Table
    config.table = {"mysql_name": "stefan_logbook", "mysql_table": None, "datatable": None}
    config.table["mysql_table"] = metadata.tables[config.table["mysql_name"]]
    config.table["datatable"] = DataTable(MySQL.table_fetch(config.mysql["conn"], config.table["mysql_table"]))

# View type
config.view_type = "timeline"
if config.view_type == "timeline":
    # This dict stores information about the timeline as created by the timeline module in pages
    config.timeline = {"n_boxes": 0}

dash_app = Dash(__name__, use_pages=True)
app = dash_app.server

dash_app.layout = html.Div([
    html.H1('Stefans Welt'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
    dcc.Store(storage_type="session", id='store')
])

if __name__ == '__main__':
    dash_app.run(debug=True)
