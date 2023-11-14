from flask import Flask, render_template, request, session

from DataStructures.Data import DataTableFactory
from Views.List import ListViewer
from ListView.Single import ListSingleViewer


## Get documents and events
#path_root = '//192.168.178.53/Stefan/DigitalImmortality/Document and Event Tables/'
#
# Get document table
#path_master = path_root + 'Dokumentliste_Cembalomusik Papa_cd.csv'
#documenttable = DataTableFactory.importFromCsv(path_master)
#
## Make ListView object
#listview = ListViewer()
# List of CD type
#listview.init_cd_list(documenttable)

def get_documenttable():
    # Get documents and events
    path_root = '//192.168.178.53/Stefan/DigitalImmortality/Document and Event Tables/'
    # Get document table
    path_master = path_root + 'Dokumentliste_Cembalomusik Papa_cd.csv'
    return DataTableFactory.importFromCsv(path_master)

## Flask
app = Flask(__name__)

# Secret key is needed for session
app.secret_key = 'geheim'

@app.route('/listen/all', methods=["GET","POST"])
def show_list():
    def render_list():
        return {'n_boxes': listview.n_boxes,
                'usr_src': listview.data_for_view(),
                'usr_txt': listview.description_document,
                }
    documenttable = get_documenttable()
    # Make ListView object
    listview = ListViewer()
    # List of CD type
    listview.init_cd_list(documenttable)
    # Store index_show in session
    session['index_show'] = [int(ix) for ix in listview.index_show]
    return render_template('/listen/all.html', **render_list())

@app.route('/listen/single', methods=["GET","POST"])
def show_list_single():
    def render_list_single():
        return {'n_boxes': listsingleview.n_boxes,
                'usr_src': listsingleview.data_for_view(),
                'usr_txt': listsingleview.description_document,
                }
    documenttable = get_documenttable()
    for i in request.form:
        i = int(i)
        listsingleview = ListSingleViewer()
        listsingleview.init_cd(documenttable, session.get('index_show',None)[i])
    return render_template('/listen/single.html', **render_list_single())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82)

