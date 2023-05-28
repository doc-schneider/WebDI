from flask import render_template, request, Blueprint
import pandas as pd

import config


## Blueprint
mysql_topics = Blueprint('mysql_topics', __name__)

@mysql_topics.route('/table', methods=["GET","POST"])
def show_table():

    if request.method == 'POST':
        # TODO THere is onyl a singel key. Value instead?
        for key in request.form.keys():
            if key == "None":
                # Nothing available, stay
                pass
            elif key == "back":
                config.table = config.table_previous
                # TODO Table hierarchy
            else:
                # New table
                config.table_previous = config.table
                config.table = key

    df = pd.read_sql(config.table, con=config.db_connection)
    column_names = list(df.columns)
    n_columns = df.shape[1]
    n_rows = df.shape[0]
    dct = df.to_dict(orient="list")

    # Containing links to sub-tables?
    flag_table = None  # No subtables
    # TODO Make all NAME_TABLE
    if "TABLE" in column_names:
        flag_table = "TABLE"
    elif "TABLE_NAME" in column_names:
        flag_table = "TABLE_NAME"
    elif "NAME_TABLE" in column_names:
        flag_table = "NAME_TABLE"

    if flag_table is not None:
        column_clickable = flag_table
        config.table_type = "meta"
    else:
        # Lowest level table with documents
        column_clickable = "DOCUMENT_NAME"
        config.table_type = "basic"

    return render_template('/mysql_topics/table.html',
                           table=dct,
                           columns=column_names,
                           n_columns=n_columns,
                           n_rows=n_rows,
                           column_clickable=column_clickable,
                           table_type=config.table_type
                           )
