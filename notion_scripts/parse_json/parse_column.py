def parse_column(data, column):
    if column.column_type == "id":
        return data[column.title]

    if data["properties"].get(column.title) is not None:

        data = data["properties"][column.title][column.column_type]

        if column.column_type == "select":
            return data["name"]
        if column.column_type == "rich_text":
            if data:
                return data[0]['text']["content"]
            return None
        if column.column_type == "date":
            return data["start"]
        if column.column_type == "relation":
            return [i["id"] for i in data]
        if column.column_type == "title":
            return data[0]['plain_text']
        return data
    return None
