def parse_column(data, column):
    if data.get(column.title) is not None:
        if column.column_type == "checkbox":
            return data[column.title]["checkbox"]
        elif column.column_type == "select":
            return data[column.title]["select"]["name"]
        elif column.column_type == "rich_text":
            return data[column.title]["rich_text"][0]['text']["content"]
        elif column.column_type == "date":
            return data[column.title]["date"]["start"]
        elif column.column_type == "relation":
            return [i["id"] for i in data[column.title]["relation"]]
        elif column.column_type == "title":
            return data[column.title]["title"][0]['plain_text']
    else:
        return None
