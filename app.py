import pandas as pd
import dash
from dash import Dash, html, dcc
from sqlalchemy import create_engine, MetaData

import config


# Settings
config.environment = "local"   # "azure"

flag = False
if flag:
    # MySQL
    db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
    db_engine = create_engine(db_connection_str)
    db_conn = db_engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=db_engine)
    config.mysql = {
        "engine": db_engine,
        "conn": db_conn,
        "metadata": metadata
    }

    table = metadata.tables["stefan_logbook"]
    query = table.select()
    query_result = db_conn.execute(query)
    table_df = pd.DataFrame(query_result.fetchall())

dash_app = Dash(__name__, use_pages=True)
app = dash_app.server

dash_app.layout = html.Div([
    html.H1('Stefans Welt'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    dash_app.run(debug=True)
