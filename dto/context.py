class Context:
    def __init__(self, text, id, is_planned, start="", end="", all_tasks=None, habits=None):
        self.is_planned = is_planned
        if habits is None:
            habits = []
        if all_tasks is None:
            all_tasks = []
        self.text = text
        self.id = id
        self.start = start
        self.end = end
        self.all_tasks = all_tasks
        self.quantity = len(all_tasks)
        self.habits = habits

    def get_day_tasks(self, date):
        return [task for task in self.all_tasks if task.date == date.isoformat()]

    def get_day_quantity(self, date):
        return len(self.get_day_tasks(date))
