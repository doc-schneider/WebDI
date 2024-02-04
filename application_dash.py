import dash
from dash import Dash, html, dcc
from sqlalchemy import create_engine, MetaData

from DataOperations import TableOperations
from DataStructures.TableTypes import TableType
import config


config.person = "stefan"
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
# View Table: Start with Topic / highest level
#config.table_view = TableOperations.init_table(TableType["TOPIC"], config.person)

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])
if __name__ == '__main__':
    app.run(debug=True)
