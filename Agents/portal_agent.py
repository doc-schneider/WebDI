from flask import render_template, request, Blueprint

import config
from Views.Portal import PortalViewer
from DataOperations.MySQL import (
    read_specific_dataframe,
)


## Blueprint
portal = Blueprint('portal', __name__)

@portal.route('/portal', methods=["GET","POST"])
def show_portal():

    def render_portal():
        return config.PortalView.view(config.portaltable)

    def init_PortalView(portaltable):
        return PortalViewer(portaltable)

    if request.method == 'GET':
        if not hasattr(config, 'PortalView'):
            config.PortalView = PortalViewer(config.portaltable)

        return render_template('/portal/portal.html', **render_portal())

    elif request.method == 'POST':
        row = int(request.form['portal'])
        config.portaltable = read_specific_dataframe(
            config.db_connection,
            config.portaltable.loc[row, "SUB_PORTAL"],
            "portal")
        config.PortalView = PortalViewer(config.portaltable)

        return render_template('/portal/portal.html', **render_portal())

