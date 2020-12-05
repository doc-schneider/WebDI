from flask import render_template, request, Blueprint, session

from Views.List import ListAllViewer, ListSingleViewer
import config


## Blueprint
listen = Blueprint('listen', __name__)

@listen.route('/all', methods=["GET","POST"])
def show_list():

    def render_list():
        return {'n_boxes': config.listview.n_boxes,
                'usr_src': config.listview.data_for_view(),
                'usr_txt': config.listview.description_document,
                }

    def init_listview():
        # Initialize at first call
        if not hasattr(config, 'listview'):
            config.listview = ListAllViewer()
            config.listview.init_cd_list(config.documenttable, config.document_pathtype,
                                         config.environment, config.use_thumbnail)

    init_listview()
    # Store index_show in session
    session['index_all'] = [int(ix) for ix in config.listview.index_show]

    return render_template('/listen/all.html', **render_list())


@listen.route('/single', methods=["GET","POST"])
def show_list_single():

    def render_list_single():
        return {'n_boxes': config.listsingleview.n_boxes,
                'usr_src': config.listsingleview.data_for_view(),
                'usr_txt': config.listsingleview.description_document,
                }

    if request.method == 'POST':  # GET is only page refresh
        for i in request.form:
            i = int(i)
            config.listsingleview = ListSingleViewer()
            config.listsingleview.init_cd_list(config.documenttable, config.document_pathtype,
                                               config.environment, session.get('index_all', None)[i])
            session['index_single'] = [int(ix) for ix in config.listsingleview.index_documents]

    return render_template('/listen/single.html', **render_list_single())
