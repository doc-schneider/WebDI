

class PortalViewer():
    def __init__(self, portaltable):
        self.n_rows = portaltable.shape[0]
        self.n_keys = portaltable.shape[1]
        self.keys = list(portaltable.columns.values)

    def view(self, portaltable):
        # TODO Convert None to empty str
        dct = {'values': portaltable.values}
        dct['n_rows'] = self.n_rows
        dct['n_keys'] = self.n_keys
        dct['keys'] = self.keys
        return dct

