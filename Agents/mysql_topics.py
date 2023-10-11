from DataOperations.Files import encode_data

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
                if len(config.table_name_hierachie) > 1:
                    config.table_name_hierachie.pop()
                    config.table_name = config.table_name_hierachie[-1]
                else:
                    # Nothing available, stay
                    pass
            else:
                # New table one level lower
                config.table_name_hierachie.append(request.form[key])
                config.table_name = request.form[key]

    df = pd.read_sql(config.table_name, con=config.db_connection)
    column_names = list(df.columns)
    n_columns = df.shape[1]
    n_rows = df.shape[0]
    dct = df.to_dict(orient="list")

    # Containing links to sub-tables?
    flag_table = None  # No subtables
    if ("NAME_TABLE" in column_names) & (
            (
                    "DOCUMENT_NAME" not in column_names
            ) | (
            "SUB_TOPIC" in column_names
    )
    ):
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

@mysql_topics.route('/content', methods=["GET","POST"])
def show_content():

    if request.method == 'POST':
        key = [k for k in request.form.keys()][0]
        document_name = request.form[key]
        df = pd.read_sql(config.table_name, con=config.db_connection)
        path = df.loc[df[key] == document_name, "PATH"].values[0]
        document_format = df.loc[df[key] == document_name, "DOCUMENT_FORMAT"].values[0]
        description = df.loc[df[key] == document_name, "DESCRIPTION"].values[0]
        # Convert data for html
        data = encode_data(path + document_name, 'base64')
        return render_template(
            '/mysql_topics/content.html',
            data=data,
            data_type=document_format.lower(),
            description=description
        )