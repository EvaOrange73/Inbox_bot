class Day:
    def __init__(self, day_id, date, contexts, hangouts, context_names):
        self.context_names = context_names
        self.hangouts = hangouts
        self.contexts = contexts
        self.date = date
        self.id = day_id
        self.hangout_names = [context_names[i] for i in range(len(context_names)) if hangouts[i]]
