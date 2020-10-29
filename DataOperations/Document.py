from DataOperations.Data import DataTable


class DocumentTable(DataTable):

    def __init__(self, table):
        super().__init__(table)

    def find_in_timeinterval(self, timeinterval):
        # Returns the index of all documents whose time_interval overlaps a requested time interval
        ix = list()
        for j in range(self.length):
            if timeinterval.overlaps(self.data['TIME_INTERVAL'].iloc[j]):
                ix.append(j)
        return ix