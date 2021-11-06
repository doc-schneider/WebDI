from flask import render_template, request, Blueprint
from sqlalchemy import create_engine
import pandas as pd

from DataOperations.MySQL import read_dataframe
import config


## Blueprint
mysql = Blueprint('mysql', __name__)


@mysql.route('/databases', methods=["GET","POST"])
def show_databases():

    def render_databases():
        dct = {
            'databases': databases,
        }
        return dct

    query = "show databases"
    config.cursor.execute(query)
    databases = list()
    for database in config.cursor:
        databases.append(database[0])

    return render_template('/mysql/databases.html', **render_databases())


@mysql.route('/databasetables', methods=["GET","POST"])
def show_databasetables():

    def render_tables():
        dct = {
            'tables': tables,
        }
        return dct

    if request.method == 'POST' and (request.referrer.find("databases") != -1):
        config.database = request.form['database']
        query = "use " + config.database
        config.cursor.execute(query)

    query = "show tables"
    config.cursor.execute(query)
    tables = list()
    for table in config.cursor:
        tables.append(table[0])

    return render_template('/mysql/databasetables.html',  **render_tables())


@mysql.route('/table', methods=["GET","POST"])
def show_table():

    if request.method == 'POST':
        # TODO Engine should be ended when switching to another database
        # TODO No new engine if already exists
        db_connection_str = 'mysql+mysqlconnector://Stefan:Moppel3@localhost/' + config.database
        db_connection = create_engine(db_connection_str)
        config.connection = db_connection
        tbl = request.form['table']
        config.table = tbl

    df = read_dataframe(config.connection, config.table)

    return render_template('/mysql/table.html', tables=[df.to_html(classes='data', header="true")])

