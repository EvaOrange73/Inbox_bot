import json
from typing import Union, Dict

from utils.columns import Column


def equals_filter(data: Dict[Column, Union[str, bool]]):
    filters = []
    for pair in data.items():
        column = pair[0]
        text = pair[1]
        filters.append(
            {
                "property": column.title,
                column.column_type: {"equals": text}
            }
        )
    return json.dumps(
        {
            "filter": {
                "and": filters
            }
        }
    )
