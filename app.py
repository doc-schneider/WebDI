import dash
from dash import Dash, html, dcc
from sqlalchemy import create_engine, MetaData

from DataStructures.DataFactory import DataFactory
from DataStructures.TableTypes import TableType
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
    config.table = {
        "table_type": TableType.PHOTO,
        "mysql_name": "photos",
        "mysql_table": None,
        "data_table": None
    }
    config.table["data_table"] = DataFactory.fetch_table(
        config.table["table_type"],
        config.table["mysql_name"]
    )

# View type
config.view_type = "album"  # "timeline"
if config.view_type == "timeline":
    pass

dash_app = Dash(__name__, use_pages=True)
app = dash_app.server

dash_app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
    dcc.Store(storage_type="session", id='store')
])

if __name__ == '__main__':
    dash_app.run(debug=True)  # (host='192.168.0.225', port=5000, debug=True)
