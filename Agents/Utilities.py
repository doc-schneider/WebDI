from DataStructures.Data import DataTableFactory
from DataStructures.Document import DocumentTable
from DataStructures.Event import EventTable

# Get and compile correct path and name parts
# Route to readers
def get_documenttable(environment, document_pathtype, table_path_0, table_path_1, table_type='document'):
    # TODO Generalize over table types
    # Get documents and events
    if document_pathtype == 'PATH':
        path_root = table_path_0
        # Get document table
        path_master = path_root + table_path_1
        if table_type=='document':
            return DocumentTable(DataTableFactory.importFromCsv(path_master))
        elif table_type=='event':
            return EventTable(DataTableFactory.importFromCsv(path_master))
    elif document_pathtype == 'AZURE':
        container_name = table_path_0
        table_name_azure = table_path_1
        if table_type == 'document':
            return DocumentTable(DataTableFactory.importFromAzure(container_name, table_name_azure, environment))
        elif table_type == 'event':
            return EventTable(DataTableFactory.importFromAzure(container_name, table_name_azure, environment))