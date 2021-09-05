from utils.columns import InboxColumns


class UpdateDate:
    def __init__(self, name, date, column: InboxColumns):
        self.name = name
        self.date = date
        self.column = column
