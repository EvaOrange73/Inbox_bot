import json
from typing import Dict

from notion_scripts.form_json.utils import paragraph
from utils.columns import Column


def form_json(data: Dict[Column, str], parent=None, children=None):
    new_json = {}
    if parent is not None:
        new_json["parent"] = {"database_id": parent}

    new_json["properties"] = {}

    for pair in data.items():
        column = pair[0]
        text = pair[1]

        if column.column_type == "title":
            new_json["properties"][column.title] = {
                column.column_type: [{
                    "text": {"content": text}
                }]
            }
        elif column.column_type == "date":
            new_json["properties"][column.title] = {column.column_type: {"start": text}}
        elif column.column_type == "select":
            new_json["properties"][column.title] = {column.column_type: {"name": text}}
        elif column.column_type == "rich_text":
            new_json["properties"][column.title] = {column.column_type: [
                {
                    "type": "text",
                    "text": {
                        "content": text
                    }
                }
            ]}

        elif column.column_type == "relation":
            if type(text) == list:
                new_json["properties"][column.title] = {column.column_type: [{'id': item} for item in text]}
            else:
                new_json["properties"][column.title] = {column.column_type: [
                    {
                        'id': text
                    }
                ]}
        else:
            new_json["properties"][column.title] = {column.column_type: text}

    if children is not None:
        if type(children) == list:
            new_json["children"] = children
        elif type(children) == str:
            new_json["children"] = [paragraph(children)]

    # print(new_json)
    return json.dumps(new_json)
