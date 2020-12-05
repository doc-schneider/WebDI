from flask import render_template, request, Blueprint, session

from Views.Play import PlayViewer
import config


## Blueprint
play = Blueprint('play', __name__)

@play.route('/audio', methods=["GET","POST"])
def show_list_single():

    def render_play_audio():
        return {'usr_src': config.playview.data_for_view()}

    if request.method == 'POST':  # GET is only page refresh
        for i in request.form:
            i = int(i)
            config.playview = PlayViewer()
            config.playview.init_play(config.documenttable, config.document_pathtype,
                                      config.environment, session.get('index_single', None)[i])

    return render_template('/play/audio.html', **render_play_audio())
