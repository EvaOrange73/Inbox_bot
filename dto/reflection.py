class Reflection:
    def __init__(self, reflection_id, name, reflection_type, date, productivity, hangouts, is_processed):
        self.is_processed = is_processed
        self.hangouts = hangouts
        self.productivity = productivity
        self.date = date
        self.type = reflection_type
        self.name = name
        self.id = reflection_id
