from utils.columns import InboxColumns


class UpdateDate:
    def __init__(self, date, column: InboxColumns, date_id="", name=""):
        self.id = date_id
        self.name = name
        self.date = date
        self.column = column
