from flask import render_template, request, Blueprint

import config
from Views.Edit import MetainformationEditor


## Blueprint
edit = Blueprint('edit', __name__)

@edit.route('/metadocument', methods=["GET","POST"])
def edit_meta_document():

    def render_metadocument():
        return {"info_dct": config.Editor.info_dct}

    if request.method == 'POST':   # GET is only page refresh
        keys = list(request.form.keys())
        # First call of page.
        if keys[0] == 'edit':
            config.Editor = MetainformationEditor(
                config.SingleView.documenttable,
                config.SingleView.BoxSeries[0].index_show,
                config.document_category,
                config.db_connection
            )
        else:  # Submit input
            config.Editor.edit_table(request.form)

    return render_template('/edit/metadocument.html', **render_metadocument())