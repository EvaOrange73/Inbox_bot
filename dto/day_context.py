from typing import List

from dto.context import Context


class DayContext:
    def __init__(self, list_of_context: List[Context], date):

        other_contexts = []
        date_contexts = []

        for context in list_of_context:
            if context.get_day_quantity(date) > 0:
                date_contexts.append(context)
            else:
                other_contexts.append(context)

        self.other = other_contexts
        self.default_order = date_contexts
        self.right_order = []
