def parse_column(data, column):
    if column.column_type == "id":
        return data[column.title]
    else:
        if data["properties"].get(column.title) is not None:

            data = data["properties"][column.title][column.column_type]

            if column.column_type == "select":
                return data["name"]
            elif column.column_type == "rich_text":
                return data[0]['text']["content"]
            elif column.column_type == "date":
                return data["start"]
            elif column.column_type == "relation":
                return [i["id"] for i in data]
            elif column.column_type == "title":
                return data[0]['plain_text']
            else:
                return data
        else:
            return None
