from utils.columns import InboxColumns


class UpdateDate:
    def __init__(self, date, column: InboxColumns):
        self.date = date
        self.column = column
