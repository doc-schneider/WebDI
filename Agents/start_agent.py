from flask import render_template, request, Blueprint

import config
from Agents.Utilities import get_documenttable
from Views.Start import StartViewer


## Blueprint
start = Blueprint('start', __name__)

@start.route('/', methods=["GET","POST"])
def show_start():

    def render_start():
        return {
            'photo': config.startview.data_for_view()[0],
            'first_name': config.startview.first_name,
            'family_name': config.startview.family_name,
            'description': config.startview.description[0],
            'n_views': len(config.startview.document_table),
            'document_table': config.startview.document_table,
            'document_type': config.startview.document_type,
            'view_type': config.startview.view_type
        }

    if request.method == 'GET':
        
        # Initial
        config.starttable = get_documenttable(config.environment, config.document_pathtype,
                                                  config.path, config.starttable_name)
        # StartViewer
        config.startview = StartViewer(config.starttable, config.document_pathtype, config.environment)

        #  DocumentTable
        # - Only first table of list for the time being
        view_type = config.startview.view_type[0]
        config.documenttable = get_documenttable(config.environment, config.document_pathtype,
                                                 config.startview.document_azure_container + '/' +
                                                 config.startview.document_azure_blob,
                                                 config.startview.document_table[0])
        if view_type == 'timeline':
            config.documenttable.timesort()
            config.documenttable.add_timeinterval()

        # EventTable
        event_table_name = config.startview.event_table
        if event_table_name:
            config.eventtable = get_documenttable(config.environment, config.document_pathtype,
                                                  config.path,
                                                  event_table_name, table_type='event')

    return render_template('/start.html', **render_start())